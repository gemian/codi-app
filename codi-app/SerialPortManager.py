import serial
import struct
import threading
import codi_st32_generated_functions as st32Cmd

isRunning = True
socket = None
thread = None
lock = threading.Lock()

def init():
    global socket
    global thread
    try:
        socket = serial.Serial('/dev/ttyS1', baudrate=115200)
        socket.timeout = 0.1

        thread = threading.Thread(target=readFromSerial)
        thread.start()
    except Exception as e:
        print(e)

def stop():
    global isRunning
    global socket

    isRunning = False
    try:
        socket.cancel_read()
    except:
        socket.close()

def readFromSerial():
    global socket
    global isRunning

    msgHeader = bytes.fromhex('58 21 58 21')
    print('Listening...')
    while isRunning:
        header = socket.read_until(msgHeader, size=300)
        # print('Found header', header)

        # Read Size
        if len(header) >= 4:
            msgSize = struct.unpack('>I', socket.read(4))[0]
            # print('Found message size', msgSize)
            if msgSize <= 300:
                msg = socket.read(msgSize-8)
                st32Cmd.readMessage(msg)
            else:
                if isRunning:
                    print('Message length wrong, ignoring msg')

def sendCommand(cmd):
    global socket
    global lock

    try:
        lock.acquire()
        socket.write(cmd)
        lock.release()
    except Exception as e:
        print(e)
