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
import CodiFunctions as cf

log = logging.getLogger('codiUpdate')

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
    # download available versions - https://fota.planetcom.co.uk/stm32flash/cosmo_stm32_firmware_versions.txt
    newest_version = None
    try:
        for line in urllib.request.urlopen("https://fota.planetcom.co.uk/stm32flash/cosmo_stm32_firmware_versions.txt"):
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
    except Exception as e:
        log.error(e)

    time.sleep(2)  # Wait for CODI to reply
    print("Current CODI versions:", cf.get_codi_version(), cf.get_resources_version(), cf.get_protocol_major(),
          cf.get_protocol_minor())
    print("Newest Server Version:", newest_version)

    if cf.get_codi_version() is not None and cf.get_resources_version() is not None:
        return LooseVersion(newest_version) > LooseVersion(cf.get_codi_version().replace('V', '')) or \
               LooseVersion(newest_version) > LooseVersion(cf.get_resources_version().replace('R', ''))
    else:
        return False


def stm32_hardware_reset():
    print("Resetting CoDi")
    with open('/proc/AEON_RESET_STM32', 'w') as f:
        f.write("1")
    time.sleep(1)
    with open('/proc/AEON_RESET_STM32', 'w') as f:
        f.write("0")
    time.sleep(4)
    print("Reset complete")


def stm32_into_download_mode(prepare):
    print("Into download mode, prepare:", prepare)
    with open('/proc/AEON_STM32_DL_FW', 'w') as f:
        if prepare:
            f.write("1")
        else:
            f.write("0")

ser = None

def print_progress_bar (iteration, error_count, total):
    errors = "E:" + str(error_count)
    length = int(os.popen('stty size', 'r').read().split()[1]) - len(errors) - 11
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    print(f'\r |{bar}| {percent}% {errors}', end = "\r")

def callback(total_packets, success_count, error_count, total):
    print_progress_bar(total_packets, error_count, total)


def send_file(file, slow_mode):
    global ser

    time.sleep(1)  # Wait for listening thread to get started
    print("Switch to upload")
    SerialPortManager.switchToUploadMode()
    time.sleep(1)
    stm32_into_download_mode(True)
    time.sleep(4)
    log.info("Sending 140 '0d oa' session 5 - requesting reset")
    sendMessage(140, [writeUint8(0x0d), writeUint8(0x0a)], '00 00 00 05')
    time.sleep(2)
    stm32_hardware_reset()
    stm32_into_download_mode(False)
    print("Send Command 1")
    SerialPortManager.sendCommand(writeString("1"))
    time.sleep(2)

    ser = SerialPortManager.get_socket()

    modem = YMODEM(ser)

    print("Sending:", file)
    print("Expect a few errors at 0% as the CoDi is erasing the flash, ~3 fw, ~15 res")
    file_sent = False
    try:
        file_sent = modem.send(file, slow_mode, callback=callback)
        print("\r\nSend completed:", file_sent)
    except Exception as e:
        log.error(e)
    SerialPortManager.switchToCmdMode()
    print("Finished")
    return file_sent


parser = optparse.OptionParser(usage='%prog [filename]')
parser.add_option("-d", "--debug",
                  action="store_true", dest="debug",
                  help="output debug logging to ymodem.log")
parser.add_option("-s", "--slow",
                  action="store_true", dest="slow_mode",
                  help="use slow mode for serial communications, this can help with stuck flashing")

options, args = parser.parse_args()

if options.debug:
    logging.basicConfig(filename='/tmp/codiUpdate.log', level=logging.DEBUG)

lock = "/tmp/.codi.lock"
killed = lock_file.check_and_kill(lock)
lock_file.lock(lock)

SerialPortManager.init()
fileSent = False
if len(args) > 0:
    fileSent = send_file(args[0], options.slow_mode)
else:
    print("")
    versionAvailable = check_new_fota_versions_available()
    if versionAvailable:
        print("Newer version available, please download and flash as desired, suggest resources first")
        print("R:",resources_url)
        print("F:",ospi_url)
    else:
        if cf.get_codi_version() is None:
            print("CODI Error getting existing version, a reset might help or a reflash may be needed")
            if ospi_url is not None:
                print("Server versions available")
                print("R:",resources_url)
                print("F:",ospi_url)
        else:
            print("Your all up to date - no new firmware")
            print("Note firmware version numbers are early in the binary so a partial flash may still show as up to date")

SerialPortManager.stop()

if killed:
    print("")
    print("Please logout & in again to restart the CoDi server once you've done all needed flashing")
#    print("Restarting codi server")
#    os.system("/usr/lib/codi/codiServer.py & disown")
