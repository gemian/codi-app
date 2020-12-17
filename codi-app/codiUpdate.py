#!/usr/bin/env python3
import logging
import os
import time
import struct
import urllib.request
import optparse
from distutils.version import LooseVersion
from xmodem import YMODEM
import codi_st32_generated_functions as st32Cmd
import SerialPortManager
import lock_file

ospi_url = None
resources_url = None

def writeUint8(p):
    return struct.pack(">B", p)


def writeUint32(p):
    return struct.pack(">I", p)


def writeString(s):
    return writeUint32(len(s)) + s.encode()


def sendMessage(commandId, args=None, sessionId='00 00 00 01'):
    if args is None:
        args = []
    msgHeader = bytes.fromhex('58 21 58 21')
    cmdId = writeUint32(commandId)
    cmdSessionId = bytes.fromhex(sessionId)
    # cmdSessionId = bytes.fromhex('00 00 00 01')
    msgLength = len(msgHeader) + 4 + len(cmdId) + len(cmdSessionId)
    for i in args:
        msgLength += len(i)

    cmd = msgHeader + writeUint32(msgLength) + cmdId + cmdSessionId
    for i in args:
        cmd += i
    SerialPortManager.sendCommand(list(cmd))


def check_new_fota_versions_available():
    global ospi_url
    global resources_url

    time.sleep(1)  # Wait for listening thread to get started
    sendMessage(st32Cmd.CMD_MTK_GET_CODI_FLASH_VERSION)
    sendMessage(st32Cmd.CMD_MTK_GET_PROTOCOL_VERSION)
    # download available versions - http://fota.planetcom.co.uk/stm32flash/cosmo_stm32_firmware_versions.txt
    base_url = None
    newest_version = None
    for line in urllib.request.urlopen("http://fota.planetcom.co.uk/stm32flash/cosmo_stm32_firmware_versions.txt"):
        firmware_line = line.decode('utf-8')
        firmware_parts = firmware_line.split(':')
        if len(firmware_parts) >= 3 and firmware_parts[0] == 'L':
            base_url = firmware_parts[1] + ':' + firmware_parts[2].strip()
        if len(firmware_parts) >= 8 and firmware_parts[0] == 'F':
            version = firmware_parts[1].replace(',', '.').replace('V', '')
            if newest_version == None or LooseVersion(version) > LooseVersion(newest_version):
                newest_version = version
                ospi_url = base_url+'/'+firmware_parts[2]
                ospi_size = firmware_parts[3]
                ospi_checksum = firmware_parts[4]
                resources_url = base_url+'/'+firmware_parts[5]
                resources_size = firmware_parts[6]
                resources_checksum = firmware_parts[7]

    time.sleep(2)  # Wait for CODI to reply
    print("CODI versions:", st32Cmd.get_codi_version(), st32Cmd.get_resources_version(), st32Cmd.get_protocol_major(),
          st32Cmd.get_protocol_minor())
    print("NewestVersion:", newest_version)
    # print("BaseUrl:",base_url)
    # print("OspiUrl:",base_url+'/'+ospi_url)
    # print("ResourcesUrl:",base_url+'/'+resources_url)

    if st32Cmd.get_codi_version() is not None and st32Cmd.get_resources_version() is not None:
        print(LooseVersion(newest_version) > LooseVersion(st32Cmd.get_codi_version().replace('V', '')),
              LooseVersion(newest_version) > LooseVersion(st32Cmd.get_resources_version().replace('R', '')))
        return LooseVersion(newest_version) > LooseVersion(st32Cmd.get_codi_version().replace('V', '')) or \
               LooseVersion(newest_version) > LooseVersion(st32Cmd.get_resources_version().replace('R', ''))
    else:
        return False


def stm32_hardware_reset():
    print("Reset STM32 1")
    with open('/proc/AEON_RESET_STM32', 'w') as f:
        f.write("1")
    time.sleep(1)
    print("Reset STM32 0")
    with open('/proc/AEON_RESET_STM32', 'w') as f:
        f.write("0")
    time.sleep(4)


def stm32_into_download_mode(prepare="0"):
    print("STM32_DL_FW", prepare)
    with open('/proc/AEON_STM32_DL_FW', 'w') as f:
        f.write(prepare)


ser = None

def print_progress_bar (iteration, error_count, total):
    errors = "E:" + str(error_count)
    length = int(os.popen('stty size', 'r').read().split()[1]) - len(errors) - 11
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    print(f'\r |{bar}| {percent}% {errors}', end = "\r")

def callback(total_packets, success_count, error_count, total):
    print_progress_bar(total_packets, error_count, total)


def send_file(file):
    global ser

    time.sleep(1)  # Wait for listening thread to get started
    print("Switch to upload")
    SerialPortManager.switchToUploadMode()
    time.sleep(1)
    stm32_into_download_mode("1")
    time.sleep(4)
    print("Sending 140 '0d oa' session 5 - requesting reset")
    sendMessage(140, [writeUint8(0x0d), writeUint8(0x0a)], '00 00 00 05')
    time.sleep(2)
    stm32_hardware_reset()
    stm32_into_download_mode()
    print("Send Command 1")
    SerialPortManager.sendCommand(writeString("1"))
    time.sleep(1)

    ser = SerialPortManager.getSocket()

    modem = YMODEM(ser)

    print("Sending", file)
    try:
        print("\r\nSend completed:", modem.send(file, callback=callback))
    except Exception as e:
        print("Exception", e)
    SerialPortManager.switchToCmdMode()
    print("Finished")


parser = optparse.OptionParser(usage='%prog [filename]')
parser.add_option("-d", "--debug",
                  action="store_true", dest="debug",
                  help="output debug logging to ymodem.log")

options, args = parser.parse_args()

if options.debug:
    logging.basicConfig(filename='/tmp/codiUpdate.log', level=logging.DEBUG)

lock = "/tmp/.codi.lock"
killed = lock_file.check_and_kill(lock)
lock_file.lock(lock)

SerialPortManager.init()
if len(args) > 0:
    send_file(args[0])

if check_new_fota_versions_available():
    print("")
    print("Newer version available")
    print("Please flash resources first")
    print("R:",resources_url)
    print("M:",ospi_url)

elif st32Cmd.get_codi_version() is not None:
    print("Your all up to date - no new firmware")
else:
    print("CODI Error getting existing version")
SerialPortManager.stop()

#if killed:
#    print("Restarting codi server")
#    os.system("/usr/lib/codi/codiServer.py & disown")
