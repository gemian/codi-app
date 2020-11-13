
from pydbus import SystemBus, SessionBus
from gi.repository import GLib
import PropertyManager
import LEDManager
import codi_mtk_generated_functions as mtkCmd


def addressbookChanged(par1, par2, par3, par4, par5):
    print('AddressBook Changed')
    mtkCmd.MTKDataChangeAlert(1, 0)
    mtkCmd.MTKDataChangeAlert(0, 0)

def init(startMainLoop=True):
    global bus
    global session
    global ril0
    global ril1
    global power
    global network

    bus = SystemBus()
    # bus.subscribe(signal_fired=print)
    power = bus.get('.UPower')
    power.onPropertiesChanged = PropertyManager.propertiesChanged
    power = bus.get('.UPower', '/org/freedesktop/UPower/devices/battery_battery')
    power.onPropertiesChanged = PropertyManager.propertiesChanged
    LEDManager.ledsCharging(power.State == 1)

    ril0 = bus.get('org.ofono', '/ril_0')
    ril0.onCallAdded = PropertyManager.callStatusChanged
    ril0.onCallRemoved = PropertyManager.callStatusChanged
    ril1 = bus.get('org.ofono', '/ril_1')
    ril1.onCallAdded = PropertyManager.callStatusChanged
    ril1.onCallRemoved = PropertyManager.callStatusChanged

    network = bus.get('org.freedesktop.NetworkManager')
    network.onPropertiesChanged = PropertyManager.networkPropertiesChanged
    mtkCmd.WiFiStatusInfo(int(network.WirelessEnabled), 100)

    PropertyManager.init()

    session = SessionBus()
    session.subscribe(object='/com/canonical/pim/AddressBook', signal_fired=addressbookChanged)

    # help(ril0)
    # ril0['org.ofono.CallVolume'].onPropertyChanged = propertyChanged

    # ril0['org.ofono.VoiceCallManager'].onPropertyChanged = propertyChanged
    # print(dir(ril0['org.ofono.VoiceCallManager']))
    # notifications = session.get('org.kde.kglobalaccel', '/component/kmix')
    # notifications.onglobalShortcutPressed = volumeChanged

    if startMainLoop:
        loop = GLib.MainLoop()
        loop.run()
