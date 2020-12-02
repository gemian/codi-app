import evdev
from evdev import InputDevice, categorize, ecodes
import threading
import DBusServer
import PropertyManager

dev = None

def readEvent():
    global dev
    for event in dev.read_loop():
        # print(event)
        if event.code == 115:
            PropertyManager.volumeButtonPressed('EventListener', 'increase_volume', event.value)
        if event.code == 114:
            PropertyManager.volumeButtonPressed('EventListener', 'decrease_volume', event.value)


def init():
    global dev

    for path in evdev.list_devices():
        try:
            device = evdev.InputDevice(path)
            if device.name == 'mtk-kpd':
                print('Device', device.name, 'found.')
                dev = device
                thread = threading.Thread(target=readEvent)
                thread.start()
                return
        except:
            pass
