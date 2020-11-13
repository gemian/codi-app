
class CallInfoClass:
    modemId = 0
    contactName = ''
    msisdn = ''
    currentCall = None
    state = 'disconnected'

class DeviceInfoClass:
    batteryLevel = 0
    lidClosed = True

def init():
    global DeviceInfo
    global CallInfo
    global Contacts

    CallInfo = CallInfoClass()
    DeviceInfo = DeviceInfoClass()
    Contacts = []

    try:
        with open('/proc/battery_status') as f:
            DeviceInfo.batteryLevel = int(f.read().split(',')[1])
    except Exception as e:
        print(e)
