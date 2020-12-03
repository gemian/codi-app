from datetime import datetime
import time
import os
import DBusServer
from gi.repository import GLib
import CodiStatus
import Addressbook
import codi_mtk_generated_functions as mtkCmd
import LEDManager
import sqlite3

tapHistory = False

def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    # print(type(offset))
    return utc_datetime + offset

# ST32 calls these functions

def GetBatteryLevel():
    mtkCmd.BatteryLevelInfo(CodiStatus.DeviceInfo.batteryLevel)

def GetDoNotDisturbStatus():
    mtkCmd.DoNotDisturbStatusInfo(0)

def GetBTStatus():
    mtkCmd.BTStatusInfo(0)

def GetWiFiStatus():
    mtkCmd.WiFiStatusInfo(1, 100)

def GetLockStatus():
    # UNLOCKED        0
    # LOCK_PASSWORD   4
    mtkCmd.LockStatusInfo(0, 4, '')

def GetLocationStatus():
    mtkCmd.LocationStatusInfo(0)

def GetFlightModeStatus():
    mtkCmd.FlightModeStatusInfo(0)

def GetHotspotStatus():
    mtkCmd.HotspotStatusInfo(0)

def GetVolumeLevel():
    mtkCmd.VolumeLevelInfo(50)

def GetBatterySaverStatus():
    mtkCmd.BatterySaverStatusInfo(0)

def GetMobileDataStatus():
    mtkCmd.MobileDataStatusInfo(1)

def GetModemSignalInfo():
    # sim1, sim2, sim2type
    mtkCmd.ModemSignalInfo(100, 0, 0)

# def SetLock(status):
#     LEDManager.ledsBlue()

def GetDateTime():
    now = datetime.now()
    mtkCmd.DateTimeInfo(int(now.strftime('%d')),
    int(now.strftime('%m'))-1,
        int(now.strftime('%Y')),
        int(now.strftime('%H')),
        int(now.strftime('%M')),
        int(now.strftime('%S')),
        0)

def ActionCall(action, sim, line, numtype, msisdn, contact, contact_id):
    try:
        msisdn = str(msisdn, 'utf-8')
        if action == 0:
            ril = DBusServer.ril0
            if sim == 2:
                ril = DBusServer.ril1
            ril.Dial(msisdn, '')
            conn = sqlite3.connect('/home/cosmo/.local/share/history-service/history.sqlite')
            try:
                c = conn.cursor()
                statement = 'insert into voice_events values ("ofono/ofono/ril_0", "' + msisdn + \
                        '", "' + msisdn + datetime.now().strftime(':%a %b %d %H:%M:%S %Y') + \
                        '", "self", "' + \
                        datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z') + \
                        '", 0, 4, 0, "' + msisdn + '")'
                # print(statement)
                c.execute(statement)
                conn.commit()
                c.close()
                conn.close()
            except Exception as e:
                print('Exception:', e)
        if action == 14:
            # print(dir(DBusServer.ril0['org.ofono.VoiceCallManager']))
            DBusServer.ril0['org.ofono.VoiceCallManager'].SwapCalls()

            # print(dir(CodiStatus.CallInfo.currentCall))
    except Exception as e:
        print(e)



def SetCallMuteStatus(status):
    try:
        DBusServer.ril0['org.ofono.CallVolume'].SetProperty('Muted', GLib.Variant(value=status, format_string='b'))
    except Exception as e:
        print(e)


def SendDTMF(sim, line, asciinum, palyit):
    try:
        if asciinum > 48:
            asciinum -= 48
        # zeroAscii = ord('0')
        # DBusServer.ril0['org.ofono.VoiceCallManager'].SendTones('1*2')

        if asciinum < 10:
            DBusServer.ril0['org.ofono.VoiceCallManager'].SendTones(str(asciinum))
        elif asciinum == 42:
            DBusServer.ril0['org.ofono.VoiceCallManager'].SendTones('*')
        elif asciinum == 35:
            DBusServer.ril0['org.ofono.VoiceCallManager'].SendTones('#')
    except Exception as e:
        print(e)

def SetCallOutput(status):
    try:
        if status == 0:
            os.system('pactl set-sink-port 1 "output-earpiece"')
        elif status == 1:
            os.system('pactl set-sink-port 1 "output-speaker"')
    except Exception as e:
        print(e)

def Restart(restartMode):
    try:
        if restartMode == 0:
            mtkCmd.SetMouse(0, 1)
            LEDManager.ledsOff()
            CodiStatus.DeviceInfo.lidClosed = False
            mtkCmd.SetCoDiStatus(3, 3, 3)
            os.system('qdbus org.kde.ksmserver /KSMServer org.kde.KSMServerInterface.logout 0 2 -1')
        if restartMode == 1:
            mtkCmd.SetMouse(0, 1)
            CodiStatus.DeviceInfo.lidClosed = False
            LEDManager.ledsOff()
            mtkCmd.SetCoDiStatus(3, 3, 3)
            os.system('qdbus org.kde.ksmserver /KSMServer org.kde.KSMServerInterface.logout 0 1 -1')
    except Exception as e:
        print(e)

# def SetVolumeLevel(status, stream):
# 	# Not working
#     os.system('pactl set-sink-volume sink.primary')

def CoDiOFF(par1, par2):
    if CodiStatus.CallInfo.state == 'disconnected':
        if CodiStatus.DeviceInfo.lidClosed:
            if par2 == 0:
                LEDManager.ledsBlue()
            else:
                LEDManager.ledsOff()

def GetCallHistory(index):
    batchSize = 10
    conn = sqlite3.connect('/home/cosmo/.local/share/history-service/history.sqlite')
    try:
        c = conn.cursor()
        totalCdr = c.execute('select count(*) from voice_events').fetchall()[0][0]
    except Exception as e:
        print('Exception:', e)
        totalCdr = 0

    try:
        c = conn.cursor()
        history = c.execute('select * from voice_events order by timestamp desc limit ' + str(batchSize) + ' offset ' + str(index)).fetchall()
        for i in range(len(history)):
            tod = history[i][4]
            state = 1
            if history[i][7] == 1:
                state = 0
            if history[i][3] == 'self':
                state = 2
            try:
                dt = datetime.strptime(history[i][4][0:19], '%Y-%m-%dT%H:%M:%S')
                dt = datetime_from_utc_to_local(dt)
                # print(history[i])
                # print(i, totalCdr, batchSize, history[i][1], history[i][1], dt.day, dt.month, dt.year, dt.hour, dt.minute, dt.second, 0, state)
                mtkCmd.CallHistoryInfo(i, totalCdr, batchSize, Addressbook.contactNameForNumber(history[i][1]), history[i][1], dt.day, dt.month, dt.year, dt.hour, dt.minute, dt.second, 0, state)
            except Exception as e:
                print('Exception:', e)
    except Exception as e:
        print('Exception:', e)

    c.close()
    conn.close()

def GetContacts(index):
    Addressbook.refreshContacts()
    batch = 10
    if index == 100000:
        mtkCmd.ContactInfo('0', 0, 100000, '', '')
        return

    if len(CodiStatus.Contacts) < index:
        mtkCmd.ContactInfo('0', 0, batch, '', '')
        return

    for c in CodiStatus.Contacts[index:index+batch]:
        mtkCmd.ContactInfo(c[0], len(CodiStatus.Contacts), batch, c[1], c[2])

tapHistory = False

def MouseInfo(mode, x_coord, y_coord):
    global tapHistory

    if tapHistory and mode == 2:
            os.system('xdotool click 1')
            tapHistory = False
            return

    if mode == 3:
        tapHistory = True
    else:
        tapHistory = False

    # if mode == 4:
    #     os.system('xdotool click 1')
    #     return

    if x_coord < -200 or x_coord > 200 or y_coord < -200 or y_coord > 200:
        print('Discarding...')
        return

    mx = 0
    my = 0

    if abs(x_coord) > 25:
        mx = 1
    if abs(y_coord) > 25:
        my = 1

    if abs(x_coord) < 25 and my == 0:
        x_coord /= 2
    else:
        x_coord *= 2
    if abs(y_coord) < 25 and mx == 0:
        y_coord /= 2
    else:
        y_coord *= 2

    x = str(-y_coord).replace('-', '\\-')
    y = str(-x_coord).replace('-', '\\-')


    if mode == 0:
        os.system('xdotool mousemove -- ' + x + ' ' + y)
    else:
        os.system('xdotool mousemove_relative -- ' + x + ' ' + y)
