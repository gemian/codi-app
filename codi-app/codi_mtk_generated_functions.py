import struct
import SerialPortManager

def writeUint8(p):
    return struct.pack(">B", p)

def writeUint16(p):
    return struct.pack(">H", p)

def writeUint32(p):
    return struct.pack(">I", p)

def writeInt8(p):
    return struct.pack(">b", p)

def writeInt16(p):
    return struct.pack(">h", p)

def writeInt32(p):
    return struct.pack(">i", p)

def writeString(s):
    return writeUint32(len(s)) + s.encode()

def writeUTF8String(s):
    return writeString(s)

def writeBlob(b):
    return writeString(b)

def sendMessage(commandId, args=[]):
    msgHeader = bytes.fromhex('58 21 58 21')
    cmdId = writeUint32(commandId)
    cmdSessionId = bytes.fromhex('00 00 00 01')
    msgLength = len(msgHeader) + 4 + len(cmdId) + len(cmdSessionId)
    for i in args:
        msgLength += len(i)

    cmd = msgHeader + writeUint32(msgLength) + cmdId + cmdSessionId
    for i in args:
        cmd += i
    SerialPortManager.sendCommand(list(cmd))

CMD_MTK_GET_PROTOCOL_VERSION = 0
CMD_MTK_GET_CODI_FLASH_VERSION = 1
CMD_ST32_INFO_CODI_FLASH_VERSION = 2
CMD_ST32_INFO_PROTOCOL_VERSION = 3
CMD_ST32_SET_BINARY = 4
CMD_ST32_SET_S8 = 5
CMD_ST32_RESTART = 6
CMD_ST32_GET_DATETIME = 7
CMD_MTK_INFO_DATETIME = 8
CMD_ST32_SET_LOCATION_STATUS = 9
CMD_ST32_GET_LOCATION_STATUS = 10
CMD_MTK_INFO_LOCATION_STATUS = 11
CMD_ST32_SET_TORCH_STATUS = 12
CMD_ST32_GET_TORCH_STATUS = 13
CMD_MTK_INFO_TORCH_STATUS = 14
CMD_ST32_GET_COVER_STATUS = 15
CMD_MTK_INFO_COVER_STATUS = 16
CMD_ST32_SET_WIFI_STATUS = 17
CMD_ST32_GET_WIFI_STATUS = 18
CMD_MTK_INFO_WIFI_STATUS = 19
CMD_ST32_SET_BT_STATUS = 20
CMD_ST32_GET_BT_STATUS = 21
CMD_MTK_INFO_BT_STATUS = 22
CMD_ST32_SET_BATTERY_SAVER_STATUS = 23
CMD_ST32_GET_BATTERY_SAVER_STATUS = 24
CMD_MTK_INFO_BATTERY_SAVER_STATUS = 25
CMD_ST32_SET_FLIGHT_MODE_STATUS = 26
CMD_ST32_GET_FLIGHT_MODE_STATUS = 27
CMD_MTK_INFO_FLIGHT_MODE_STATUS = 28
CMD_ST32_SET_HOTSPOT_STATUS = 29
CMD_ST32_GET_HOTSPOT_STATUS = 30
CMD_MTK_INFO_HOTSPOT_STATUS = 31
CMD_ST32_SET_MOBILE_DATA_STATUS = 32
CMD_ST32_GET_MOBILE_DATA_STATUS = 33
CMD_MTK_INFO_MOBILE_DATA_STATUS = 34
CMD_ST32_SET_DND_STATUS = 35
CMD_ST32_GET_DND_STATUS = 36
CMD_MTK_INFO_DND_STATUS = 37
CMD_ST32_SET_VOLUME_LEVEL = 38
CMD_ST32_GET_VOLUME_LEVEL = 39
CMD_MTK_INFO_VOLUME_LEVEL = 40
CMD_ST32_GET_BATTERY_LEVEL = 41
CMD_MTK_INFO_BATTERY_LEVEL = 42
CMD_ST32_INFO_CODI_STATUS = 43
CMD_MTK_SET_CODI_STATUS = 121
CMD_ST32_SET_LOCK = 45
CMD_ST32_GET_LOCK_STATUS = 46
CMD_MTK_INFO_LOCK_STATUS = 47
CMD_ST32_DISMISS_CALL_SMS = 48
CMD_ST32_ACTION_UNLOCK = 49
CMD_ST32_INFO_ST_CHARGING = 50
CMD_ST32_PLAY_DTMF = 51
CMD_ST32_SEND_DTMF = 52
CMD_ST32_ACTION_CALL = 53
CMD_ST32_SEND_TELE_CODE = 54
CMD_ST32_SET_CALL_MUTE_STATUS = 55
CMD_ST32_GET_CALL_MUTE_STATUS = 56
CMD_MTK_INFO_CALL_MUTE_STATUS = 57
CMD_ST32_SET_CALL_OUTPUT = 58
CMD_ST32_GET_CALL_OUTPUT = 59
CMD_MTK_INFO_CALL_OUTPUT = 60
CMD_ST32_GET_CALL_OUTPUT_OPTIONS = 61
CMD_MTK_INFO_CALL_OUTPUT_OPTIONS = 62
CMD_ST32_ACTION_CAMERA = 63
CMD_ST32_GET_CAMERA_FRAME = 64
CMD_ST32_SET_CAMERA_SETTINGS = 65
CMD_ST32_CAMERA_CAPTURE_IMAGE = 66
CMD_ST32_ACTION_VIDEO = 67
CMD_ST32_GET_VIDEO_FRAME = 68
CMD_ST32_SET_VIDEO_SETTINGS = 69
CMD_ST32_VIDEO_CAPTURE_IMAGE = 70
CMD_MTK_INFO_CAMERA_STATUS = 71
CMD_MTK_INFO_CAMERA_SETTINGS = 72
CMD_MTK_INFO_VIDEO_STATUS = 73
CMD_MTK_INFO_VIDEO_SETTINGS = 74
CMD_MTK_INFO_COVER_LIGHT_SENSOR = 75
CMD_ST32_GET_COVER_LIGHT_SENSOR = 76
CMD_MTK_LOAD_LANGUAGE_RESOURCE = 77
CMD_MTK_GET_CURRENT_LANGUAGE = 78
CMD_ST32_INFO_CURRENT_LANGUAGE = 79
CMD_MTK_SET_CURRENT_LANGUAGE = 80
CMD_MTK_SHOW_MEDIA = 81
CMD_MTK_STOP_MEDIA = 82
CMD_MTK_LOAD_MEDIA = 83
CMD_MTK_UNLOAD_MEDIA = 84
CMD_MTK_HAS_MEDIA = 85
CMD_ST32_INFO_MEDIA_RESOURCE = 86
CMD_ST32_INFO_MEDIA_ACTIVITY = 87
CMD_MTK_SHOW_ALERT = 88
CMD_ST32_INFO_ALERT = 89
CMD_MTK_STOP_ALERT = 90
CMD_MTK_ORIENTATION_INFO = 91
CMD_ST32_GET_ORIENTATION = 92
CMD_MTK_ACTION_CODI_HOME = 93
CMD_MTK_INFO_NEXT_ALARM = 94
CMD_MTK_SHOW_BATTERY_LEVEL = 95
CMD_ST32_GET_CALL_HISTORY = 96
CMD_ST32_GET_CONTACTS = 97
CMD_MTK_CONTACT_INFO = 98
CMD_MTK_CALL_HISTORY_INFO = 99
CMD_MTK_NOTIFICATION_INFO = 100
CMD_MTK_PLAYER_INFO = 101
CMD_ST32_ACTION_PLAYER = 102
CMD_MTK_CALL_INFO = 103
CMD_ST32_ACTION_NOTIFICATION = 104
CMD_ST32_GET_LEDISON_PATTERN = 105
CMD_MTK_LEDISON_MODE_INFO = 106
CMD_ST32_GET_LEDISON_MODE = 107
CMD_MTK_LEDISON_PATTERN_INFO = 108
CMD_ST32_GET_CONTACT_ICON = 109
CMD_MTK_CONTACT_ICON_INFO = 110
CMD_MTK_MODEM_SIGNAL_INFO = 111
CMD_MTK_WEATHER_INFO = 112
CMD_MTK_EXTRA_COMMAND = 113
CMD_ST32_GET_MODEM_SIGNAL_INFO = 114
CMD_ST32_GET_DATE_TIME_FORMAT = 115
CMD_MTK_DATE_TIME_FORMAT_INFO = 116
CMD_ST32_GET_ALBUM_ART = 117
CMD_MTK_ALBUM_ART_INFO = 118
CMD_MTK_CAMERA_FRAME_IMG = 119
CMD_MTK_KEY_PRESS_INFO = 120
CMD_ST32_ACTION_VOICE_RECODER = 122
CMD_ST32_SET_VOICE_RECORDER_SETTINGS = 123
CMD_MTK_INFO_VOICE_RECODER_SETTINGS = 124
CMD_MTK_INFO_VOICE_RECORDER_STATUS = 125
CMD_MTK_DATA_CHANGE_ALERT = 126
CMD_ST32_DATA_CHANGE_ALERT = 127
CMD_AEON_MTK_SET_ST32_RESET = 140
CMD_GET_ST32_SW_VERSION = 141
CMD_SYNC_USB_STATUS = 142
CMD_SYNC_SYS_SLEEP_STATUS = 143
CMD_SYNC_RIGHT_USB_OTG_STATUS = 144
CMD_ST_ENTRY_DEEP_SLEEP_STATUS = 145

def GetFlashVersion():
    print("-> GetFlashVersion")
    sendMessage(CMD_MTK_GET_CODI_FLASH_VERSION)

def DateTimeInfo(day, month, year, hour, minute, second, tz):
    print("-> DateTimeInfo")
    sendMessage(CMD_MTK_INFO_DATETIME, [writeUint32(day), writeUint32(month), writeUint32(year), writeUint32(hour), writeUint32(minute), writeUint32(second), writeUint32(tz)])

def LocationStatusInfo(status):
    print("-> LocationStatusInfo")
    sendMessage(CMD_MTK_INFO_LOCATION_STATUS, [writeUint16(status)])

def TorchStatusInfo(status):
    print("-> TorchStatusInfo")
    sendMessage(CMD_MTK_INFO_TORCH_STATUS, [writeUint16(status)])

def CoverStatusInfo(status):
    print("-> CoverStatusInfo")
    sendMessage(CMD_MTK_INFO_COVER_STATUS, [writeUint16(status)])

def WiFiStatusInfo(status, signalval):
    print("-> WiFiStatusInfo")
    sendMessage(CMD_MTK_INFO_WIFI_STATUS, [writeUint16(status), writeUint32(signalval)])

def BTStatusInfo(status):
    print("-> BTStatusInfo")
    sendMessage(CMD_MTK_INFO_BT_STATUS, [writeUint16(status)])

def BatterySaverStatusInfo(status):
    print("-> BatterySaverStatusInfo")
    sendMessage(CMD_MTK_INFO_BATTERY_SAVER_STATUS, [writeUint16(status)])

def FlightModeStatusInfo(status):
    print("-> FlightModeStatusInfo")
    sendMessage(CMD_MTK_INFO_FLIGHT_MODE_STATUS, [writeUint16(status)])

def HotspotStatusInfo(status):
    print("-> HotspotStatusInfo")
    sendMessage(CMD_MTK_INFO_HOTSPOT_STATUS, [writeUint16(status)])

def MobileDataStatusInfo(status):
    print("-> MobileDataStatusInfo")
    sendMessage(CMD_MTK_INFO_MOBILE_DATA_STATUS, [writeUint16(status)])

def DoNotDisturbStatusInfo(status):
    print("-> DoNotDisturbStatusInfo")
    sendMessage(CMD_MTK_INFO_DND_STATUS, [writeUint16(status)])

def VolumeLevelInfo(status, stream):
    print("-> VolumeLevelInfo")
    sendMessage(CMD_MTK_INFO_VOLUME_LEVEL, [writeUint16(status), writeUint16(stream)])

def BatteryLevelInfo(status):
    print("-> BatteryLevelInfo")
    sendMessage(CMD_MTK_INFO_BATTERY_LEVEL, [writeUint16(status)])

def SetCoDiStatus(mode, screen, data1):
    print("-> SetCoDiStatus")
    sendMessage(CMD_MTK_SET_CODI_STATUS, [writeUint32(mode), writeUint32(screen), writeUint32(data1)])

def LockStatusInfo(locked, method, strdata):
    print("-> LockStatusInfo")
    sendMessage(CMD_MTK_INFO_LOCK_STATUS, [writeUint16(locked), writeUint32(method), writeString(strdata)])

def CallMuteStatusInfo(status):
    print("-> CallMuteStatusInfo")
    sendMessage(CMD_MTK_INFO_CALL_MUTE_STATUS, [writeUint32(status)])

def CallOutputInfo(output):
    print("-> CallOutputInfo")
    sendMessage(CMD_MTK_INFO_CALL_OUTPUT, [writeUint32(output)])

def CallOutputOptionsInfo(output_options):
    print("-> CallOutputOptionsInfo")
    sendMessage(CMD_MTK_INFO_CALL_OUTPUT_OPTIONS, [writeUint32(output_options)])

def CameraStatusInfo(status):
    print("-> CameraStatusInfo")
    sendMessage(CMD_MTK_INFO_CAMERA_STATUS, [writeUint32(status)])

def CameraSettingsInfo(parameter, value):
    print("-> CameraSettingsInfo")
    sendMessage(CMD_MTK_INFO_CAMERA_SETTINGS, [writeUint32(parameter), writeUint32(value)])

def VideoStatusInfo(status):
    print("-> VideoStatusInfo")
    sendMessage(CMD_MTK_INFO_VIDEO_STATUS, [writeUint32(status)])

def VideoSettingsInfo(parameter, value):
    print("-> VideoSettingsInfo")
    sendMessage(CMD_MTK_INFO_VIDEO_SETTINGS, [writeUint32(parameter), writeUint32(value)])

def CoverLightSensorInfo(value):
    print("-> CoverLightSensorInfo")
    sendMessage(CMD_MTK_INFO_COVER_LIGHT_SENSOR, [writeUint32(value)])

def LoadLanguageResource(langid, resname, resdata, forcereload):
    print("-> LoadLanguageResource")
    sendMessage(CMD_MTK_LOAD_LANGUAGE_RESOURCE, [writeString(langid), writeString(resname), writeBlob(resdata), writeUint32(forcereload)])

def GetCurrentLanguage():
    print("-> GetCurrentLanguage")
    sendMessage(CMD_MTK_GET_CURRENT_LANGUAGE)

def SetCurrentLanguage(langid):
    print("-> SetCurrentLanguage")
    sendMessage(CMD_MTK_SET_CURRENT_LANGUAGE, [writeString(langid)])

def ShowMedia(typestr, resname, seconds, speed, aftermode):
    print("-> ShowMedia")
    sendMessage(CMD_MTK_SHOW_MEDIA, [writeString(typestr), writeString(resname), writeUint32(seconds), writeUint32(speed), writeUint32(aftermode)])

def StopMedia(typestr, resname, aftermode):
    print("-> StopMedia")
    sendMessage(CMD_MTK_STOP_MEDIA, [writeString(typestr), writeString(resname), writeUint32(aftermode)])

def LoadMedia(typestr, resname, resdata, loadmode):
    print("-> LoadMedia")
    sendMessage(CMD_MTK_LOAD_MEDIA, [writeString(typestr), writeString(resname), writeBlob(resdata), writeUint32(loadmode)])

def UnloadMedia(typestr, resname):
    print("-> UnloadMedia")
    sendMessage(CMD_MTK_UNLOAD_MEDIA, [writeString(typestr), writeString(resname)])

def HasMedia(typestr, resname):
    print("-> HasMedia")
    sendMessage(CMD_MTK_HAS_MEDIA, [writeString(typestr), writeString(resname)])

def ShowAlert(alertmode, alertype, alerticondata, typestr, resname, seconds, speed, aftermode, option1, option2):
    print("-> ShowAlert")
    sendMessage(CMD_MTK_SHOW_ALERT, [writeUint32(alertmode), writeUint32(alertype), writeBlob(alerticondata), writeString(typestr), writeString(resname), writeUint32(seconds), writeUint32(speed), writeUint32(aftermode), writeUTF8String(option1), writeUTF8String(option2)])

def StopAlert(aftermode):
    print("-> StopAlert")
    sendMessage(CMD_MTK_STOP_ALERT, [writeUint32(aftermode)])

def OrientationInfo(value):
    print("-> OrientationInfo")
    sendMessage(CMD_MTK_ORIENTATION_INFO, [writeUint32(value)])

def ActionCoDiHome(screenoff):
    print("-> ActionCoDiHome")
    sendMessage(CMD_MTK_ACTION_CODI_HOME, [writeUint32(screenoff)])

def NextAlarmInfo(appid, daystring, timestr):
    print("-> NextAlarmInfo")
    sendMessage(CMD_MTK_INFO_NEXT_ALARM, [writeUint32(appid), writeString(daystring), writeString(timestr)])

def ShowBatteryLevel(percentage, showforseconds):
    print("-> ShowBatteryLevel")
    sendMessage(CMD_MTK_SHOW_BATTERY_LEVEL, [writeUint32(percentage), writeUint32(showforseconds)])

def ContactInfo(contactid, totalcontacts, batchsize, contactname, msisdn):
    print("-> ContactInfo")
    sendMessage(CMD_MTK_CONTACT_INFO, [writeString(contactid), writeUint32(totalcontacts), writeUint32(batchsize), writeUTF8String(contactname), writeString(msisdn)])

def CallHistoryInfo(cdrid, totalcdr, batchsize, contactname, msisdn, day, month, year, hour, minute, second, tz, state):
    print("-> CallHistoryInfo")
    sendMessage(CMD_MTK_CALL_HISTORY_INFO, [writeUint32(cdrid), writeUint32(totalcdr), writeUint32(batchsize), writeUTF8String(contactname), writeString(msisdn), writeUint32(day), writeUint32(month), writeUint32(year), writeUint32(hour), writeUint32(minute), writeUint32(second), writeUint32(tz), writeUint32(state)])

def NotificationInfo(notid, action, appname, shortinfo, longinfo, day, month, year, hour, minute, second, tz, replyactions, replyaction1, replyaction2, replyaction3):
    print("-> NotificationInfo")
    sendMessage(CMD_MTK_NOTIFICATION_INFO, [writeUint32(notid), writeUint32(action), writeUTF8String(appname), writeUTF8String(shortinfo), writeUTF8String(longinfo), writeUint32(day), writeUint32(month), writeUint32(year), writeUint32(hour), writeUint32(minute), writeUint32(second), writeUint32(tz), writeUint32(replyactions), writeUTF8String(replyaction1), writeUTF8String(replyaction2), writeUTF8String(replyaction3)])

def PlayerInfo(appname, artist, album, track, offset, length, state, imageadr):
    print("-> PlayerInfo")
    sendMessage(CMD_MTK_PLAYER_INFO, [writeUTF8String(appname), writeUTF8String(artist), writeUTF8String(album), writeUTF8String(track), writeUint32(offset), writeUint32(length), writeUint32(state), writeBlob(imageadr)])

def CallInfo(modem, action, contactid, contactname, msisdn, hasicon):
    print("-> CallInfo")
    sendMessage(CMD_MTK_CALL_INFO, [writeUint32(modem), writeUint32(action), writeString(contactid), writeUTF8String(contactname), writeString(msisdn), writeUint32(hasicon)])

def LEDisonModeInfo(value):
    print("-> LEDisonModeInfo")
    sendMessage(CMD_MTK_LEDISON_MODE_INFO, [writeUint32(value)])

def LEDisonPatternInfo(animid, animname, animationdata):
    print("-> LEDisonPatternInfo")
    sendMessage(CMD_MTK_LEDISON_PATTERN_INFO, [writeUint32(animid), writeUTF8String(animname), writeBlob(animationdata)])

def ContactIconInfo(contactid, contactname, msisdn, icondata):
    print("-> ContactIconInfo")
    sendMessage(CMD_MTK_CONTACT_ICON_INFO, [writeString(contactid), writeUTF8String(contactname), writeString(msisdn), writeBlob(icondata)])

def ModemSignalInfo(sim1, sim2, sim2type):
    print("-> ModemSignalInfo")
    sendMessage(CMD_MTK_MODEM_SIGNAL_INFO, [writeUint32(sim1), writeUint32(sim2), writeUint32(sim2type)])

def WeatherInfo(weatherstate, temp, scale, additionaltext):
    print("-> WeatherInfo")
    sendMessage(CMD_MTK_WEATHER_INFO, [writeUint32(weatherstate), writeUint32(temp), writeString(scale), writeString(additionaltext)])

def ExtraCommand(data1, data2, str1, str2):
    print("-> ExtraCommand")
    sendMessage(CMD_MTK_EXTRA_COMMAND, [writeUint32(data1), writeUint32(data2), writeString(str1), writeString(str2)])

def DateTimeFormat(dateformat, timeformat):
    print("-> DateTimeFormat")
    sendMessage(CMD_MTK_DATE_TIME_FORMAT_INFO, [writeString(dateformat), writeUint32(timeformat)])

def AlbumArtInfo(albumartpng):
    print("-> AlbumArtInfo")
    sendMessage(CMD_MTK_ALBUM_ART_INFO, [writeBlob(albumartpng)])

def CameraFrameImage(width, height, png):
    print("-> CameraFrameImage")
    sendMessage(CMD_MTK_CAMERA_FRAME_IMG, [writeUint16(width), writeUint16(height), writeBlob(png)])

def KeyPressInfo(keycode, mode, modifiers):
    print("-> KeyPressInfo")
    sendMessage(CMD_MTK_KEY_PRESS_INFO, [writeUint16(keycode), writeUint16(mode), writeUint16(modifiers)])

def VoiceRecorderSettingsInfo(parameter, value):
    print("-> VoiceRecorderSettingsInfo")
    sendMessage(CMD_MTK_INFO_VOICE_RECODER_SETTINGS, [writeUint32(parameter), writeUint32(value)])

def VoiceRecorderStatusInfo(status):
    print("-> VoiceRecorderStatusInfo")
    sendMessage(CMD_MTK_INFO_VOICE_RECORDER_STATUS, [writeUint32(status)])

def MTKDataChangeAlert(type, data1):
    print("-> MTKDataChangeAlert")
    sendMessage(CMD_MTK_DATA_CHANGE_ALERT, [writeUint32(type), writeUint32(data1)])

def SetMouse(onOff, absoluteOrRelative):
    print("-> SetMouse")
    sendMessage(146, [writeUint8(onOff), writeUint8(absoluteOrRelative)])
