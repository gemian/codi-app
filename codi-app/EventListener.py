import evdev
from evdev import InputDevice, categorize, ecodes, UInput
import threading
import DBusServer
import PropertyManager

dev = None
mouse = None

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
    global mouse

    cap = { ecodes.EV_KEY: [272, 273, 274],
           ecodes.EV_REL: [0, 1, 8],
           4: [4],
           ecodes.EV_ABS: [ecodes.ABS_X, ecodes.ABS_Y] }
    mouse = UInput(cap)

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


def mouseRelative(x, y):
    global mouse

    mouse.write(ecodes.EV_REL, ecodes.REL_X, x)
    mouse.write(ecodes.EV_REL, ecodes.REL_Y, y)
    mouse.syn()

def mouseGlobal(x, y):
    global mouse

    print('cap', ecodes.EV_ABS, ecodes.ABS_X, ecodes.ABS_Y)
    mouse.write(ecodes.EV_ABS, ecodes.ABS_X, x)
    mouse.write(ecodes.EV_ABS, ecodes.ABS_Y, y)
    mouse.syn()

def mouseClick():
    global mouse

    mouse.write(ecodes.EV_KEY, ecodes.BTN_MOUSE, 1)
    mouse.write(ecodes.EV_KEY, ecodes.BTN_MOUSE, 0)
    mouse.syn()

