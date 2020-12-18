import logging
import DBusServer
import CodiStatus
import codi_mtk_generated_functions as mtkCmd
import CodiFunctions as cf
import LEDManager
import subprocess
import Addressbook

log = logging.getLogger('codi')

def init():
    global CallInfo
    global DeviceInfo
    CallInfo = CodiStatus.CallInfo
    DeviceInfo = CodiStatus.DeviceInfo


def volumeButtonPressed(sender, name, value):
    log.info('<= %r %r %r', sender, name, value)

    if name == 'decrease_volume':
        if CallInfo.state == 'incoming':
            try:
                CallInfo.currentCall.Answer()
            except Exception as e:
                log.error(e)
        else:
            mtkCmd.KeyPressInfo(25, value, 0)
    if name == 'increase_volume':
        if CallInfo.state in ('alerting', 'incoming', 'active', 'dialing'):
            try:
                CallInfo.currentCall.Hangup()
            except Exception as e:
                log.error(e)
        else:
            mtkCmd.KeyPressInfo(24, value, 0)

def propertiesChanged(sender, property, data):
    log.info('<= %r %r %r', sender, property, data)
    if 'LidIsClosed' in property.keys():
        value = property['LidIsClosed']
        DeviceInfo.lidClosed = value

        if CallInfo.state == 'disconnected':
            if value:
                mtkCmd.SetCoDiStatus(1, 0, 1)
                LEDManager.ledsBlue()
                mtkCmd.SetMouse(0, 1)
            else:
                mtkCmd.SetCoDiStatus(1, 7, 1)
                LEDManager.ledsOff()
                mtkCmd.SetMouse(1, 1)
    if 'Energy' in property and 'EnergyFull' in property:
        energy = property['Energy']
        eFull = property['EnergyFull']
        DeviceInfo.batteryLevel = int(energy * 100 / eFull)
        cf.GetBatteryLevel()
        LEDManager.ledsCharging(DBusServer.power.State == 1)

def networkPropertiesChanged(properties):
    log.info('<= %r', properties)
    mtkCmd.WiFiStatusInfo(int(DBusServer.network.WirelessEnabled), 100)

def propertyChanged(property, value):
    log.info('<=', property, value)
    # TODO: This does NOT work for some reason!
    if property == 'Muted':
        mtkCmd.CallMuteStatusInfo(1)
    if property == 'State':
        CallInfo.state = value
        if value == 'active':
            mtkCmd.CallInfo(CallInfo.modemId, 2, '0', CallInfo.contactName, CallInfo.msisdn, 0)
        if value == 'disconnected':
            mtkCmd.CallInfo(CallInfo.modemId, 0, '0', CallInfo.contactName, CallInfo.msisdn, 0)
            mtkCmd.MTKDataChangeAlert(1, 0)
            if DeviceInfo.lidClosed:
                LEDManager.ledsBlue()
            else:
                LEDManager.ledsOff()
            cf.SetCallOutput(0)


def callStatusChanged(sender, data=None):
    log.info('<=', sender, data)
    if data:
        CallInfo.currentCall = DBusServer.bus.get('org.ofono', sender)
        CallInfo.currentCall.onPropertyChanged = propertyChanged
        CallInfo.state = data['State']
        if data['State'] in ['incoming', 'dialing']:
            CallInfo.modemId = 0
            if '/ril_1' in sender:
                CallInfo.modemId = 1
            CallInfo.contactName = data['Name']
            CallInfo.msisdn = data['LineIdentification']
            if CallInfo.contactName == '':
                CallInfo.contactName = Addressbook.contactNameForNumber(CallInfo.msisdn)
            LEDManager.ledsIncomingCall()
            if data['State'] == 'incoming':
                mtkCmd.CallInfo(CallInfo.modemId, 1, '0', CallInfo.contactName, CallInfo.msisdn, 0)
            else:
                mtkCmd.CallInfo(CallInfo.modemId, 13, '0', CallInfo.contactName, CallInfo.msisdn, 0)
