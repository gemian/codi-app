import serial
import struct
import threading
import time
import logging
import codi_st32_generated_functions as st32Cmd

log = logging.getLogger('codi')
isRunning = True
socket = None
thread = None
lock = threading.Lock()

def init():
    global socket
    global thread
    try:
        socket = serial.Serial('/dev/ttyS1', baudrate=115200)

        thread = threading.Thread(target=readFromSerial)
        thread.start()
    except Exception as e:
        log.error(e)

def stop():
    global isRunning
    global socket
    global thread

    isRunning = False
    socket.cancel_read()
    time.sleep(0.1)
    socket.close()
    thread.join(4)


def get_socket():
    global socket
    global isRunning
    global thread
    global inUpload

    isRunning = False
    inUpload = False
    if socket is not None:
        socket.cancel_read()
    if thread is not None:
        thread.join(4)
    return socket


def readFromSerial():
    global socket
    global isRunning

    msgHeader = bytes.fromhex('58 21 58 21')
    log.info('[115200]Listening...')
    while isRunning:
        header = socket.read_until(msgHeader, size=300)
        # print('[115200]Found header', header)

        # Read Size
        if len(header) >= 4 and isRunning and header[0:4] == msgHeader:
            msgSize = struct.unpack('>I', socket.read(4))[0]
            # print('[115200]Found message size', msgSize)
            if msgSize <= 300 and isRunning:
                msg = socket.read(msgSize-8)
                st32Cmd.readMessage(msg)
            else:
                if isRunning:
                    log.error('[115200]Message length wrong, ignoring msg')


def sendCommand(cmd):
    global socket
    global lock

    try:
        lock.acquire()
        socket.write(cmd)
        lock.release()
    except Exception as e:
        log.error(e)


def uploadReadFromSerial():
    global socket
    global isRunning

    log.info('[230400]Listening...')
    while isRunning:
        uploadResponse = socket.read()
        if socket.in_waiting > 0:
            uploadResponse += socket.read(socket.in_waiting)
        log.debug('[230400]Response %r', uploadResponse)


def switchToUploadMode():
    global socket
    global lock
    global thread
    global isRunning

    try:
        isRunning = False
        if socket is not None:
            socket.cancel_read()
            time.sleep(1)
            socket.close()
        if thread is not None:
            thread.join(4)

        socket = serial.Serial('/dev/ttyS1', baudrate=230400, timeout=4)
        thread = threading.Thread(target=uploadReadFromSerial)
        isRunning = True
        thread.start()
    except Exception as e:
        log.error(e)


def switchToCmdMode():
    global socket
    global lock
    global thread
    global isRunning

    try:
        isRunning = False
        if socket is not None:
            socket.cancel_read()
            time.sleep(1)
            socket.close()
        if thread is not None:
            thread.join(4)

        socket = serial.Serial('/dev/ttyS1', baudrate=115200)
        thread = threading.Thread(target=readFromSerial)
        isRunning = True
        thread.start()
    except Exception as e:
        log.error(e)

