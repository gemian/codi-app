import struct
import logging
import CodiFunctions as cf

def readUint8(p):
    return struct.unpack(">B", p[:1])[0], p[1:]

def readUint16(p):
    return struct.unpack(">H", p[:2])[0], p[2:]

def readUint32(p):
    return struct.unpack(">I", p[:4])[0], p[4:]

def readInt8(p):
    return struct.unpack(">b", p[:1])[0], p[1:]

def readInt16(p):
    return struct.unpack(">h", p[:2])[0], p[2:]

def readInt32(p):
    return struct.unpack(">i", p[:4])[0], p[4:]

def readString(p):
    s, np = readUint32(p)
    if len(np) >= s:
        return np[:s], np[s:]
    else:
        log.error('Error reading string %r%r%r', s, '>', len(np))
        return '', p

def readUTF8String(p):
    return readString(p)

def readBlob(p):
    return readString(p)

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

log = logging.getLogger('codi')

def readMessage(msg):
    cmdId, msg = readUint32(msg)
    # log.info("Got cmdId %r", cmdId)
    sessionId, msg = readUint32(msg)
    # log.info("Got sessionId %r", sessionId)
    handled = False
    if cmdId == CMD_ST32_INFO_CODI_FLASH_VERSION:
        handled = True
        log.info("<- CoDiFlashVersionInfo")
        try:
            version, msg = readString(msg)
            log.info("version = %r", version)
            cf.CoDiFlashVersionInfo(version)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_INFO_PROTOCOL_VERSION:
        handled = True
        log.info("<- ProtocolVersionInfo")
        try:
            majorVer, msg = readUint8(msg)
            minVer, msg = readUint8(msg)
            log.info("majorVer = %r", majorVer)
            log.info("minVer = %r", minVer)
            cf.ProtocolVersionInfo(majorVer, minVer)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_SET_BINARY:
        handled = True
        log.info("<- SetBinary")
        try:
            data, msg = readBlob(msg)
            log.info("data = %r", data)
            cf.SetBinary(data)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_SET_S8:
        handled = True
        log.info("<- SetSigned8")
        try:
            num, msg = readInt8(msg)
            log.info("num = %r", num)
            cf.SetSigned8(num)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_RESTART:
        handled = True
        log.info("<- Restart")
        try:
            restartmode, msg = readUint32(msg)
            log.info("restartmode = %r", restartmode)
            cf.Restart(restartmode)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_DATETIME:
        handled = True
        log.info("<- GetDateTime")
        try:
            cf.GetDateTime()
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_SET_LOCATION_STATUS:
        handled = True
        log.info("<- SetLocationStatus")
        try:
            status, msg = readUint16(msg)
            log.info("status = %r", status)
            cf.SetLocationStatus(status)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_LOCATION_STATUS:
        handled = True
        log.info("<- GetLocationStatus")
        try:
            cf.GetLocationStatus()
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_SET_TORCH_STATUS:
        handled = True
        log.info("<- SetTorchStatus")
        try:
            status, msg = readUint16(msg)
            log.info("status = %r", status)
            cf.SetTorchStatus(status)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_TORCH_STATUS:
        handled = True
        log.info("<- GetTorchStatus")
        try:
            cf.GetTorchStatus()
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_COVER_STATUS:
        handled = True
        log.info("<- GetCoverStatus")
        try:
            cf.GetCoverStatus()
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_SET_WIFI_STATUS:
        handled = True
        log.info("<- SetWiFiStatus")
        try:
            status, msg = readUint16(msg)
            log.info("status = %r", status)
            cf.SetWiFiStatus(status)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_WIFI_STATUS:
        handled = True
        log.info("<- GetWiFiStatus")
        try:
            cf.GetWiFiStatus()
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_SET_BT_STATUS:
        handled = True
        log.info("<- SetBTStatus")
        try:
            status, msg = readUint16(msg)
            log.info("status = %r", status)
            cf.SetBTStatus(status)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_BT_STATUS:
        handled = True
        log.info("<- GetBTStatus")
        try:
            cf.GetBTStatus()
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_SET_BATTERY_SAVER_STATUS:
        handled = True
        log.info("<- SetBatterySaverStatus")
        try:
            status, msg = readUint16(msg)
            log.info("status = %r", status)
            cf.SetBatterySaverStatus(status)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_BATTERY_SAVER_STATUS:
        handled = True
        log.info("<- GetBatterySaverStatus")
        try:
            cf.GetBatterySaverStatus()
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_SET_FLIGHT_MODE_STATUS:
        handled = True
        log.info("<- SetFlightModeStatus")
        try:
            status, msg = readUint16(msg)
            log.info("status = %r", status)
            cf.SetFlightModeStatus(status)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_FLIGHT_MODE_STATUS:
        handled = True
        log.info("<- GetFlightModeStatus")
        try:
            cf.GetFlightModeStatus()
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_SET_HOTSPOT_STATUS:
        handled = True
        log.info("<- SetHotspotStatus")
        try:
            status, msg = readUint16(msg)
            log.info("status = %r", status)
            cf.SetHotspotStatus(status)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_HOTSPOT_STATUS:
        handled = True
        log.info("<- GetHotspotStatus")
        try:
            cf.GetHotspotStatus()
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_SET_MOBILE_DATA_STATUS:
        handled = True
        log.info("<- SetMobileDataStatus")
        try:
            status, msg = readUint16(msg)
            log.info("status = %r", status)
            cf.SetMobileDataStatus(status)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_MOBILE_DATA_STATUS:
        handled = True
        log.info("<- GetMobileDataStatus")
        try:
            cf.GetMobileDataStatus()
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_SET_DND_STATUS:
        handled = True
        log.info("<- SetDoNotDisturbStatus")
        try:
            status, msg = readUint16(msg)
            log.info("status = %r", status)
            cf.SetDoNotDisturbStatus(status)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_DND_STATUS:
        handled = True
        log.info("<- GetDoNotDisturbStatus")
        try:
            cf.GetDoNotDisturbStatus()
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_SET_VOLUME_LEVEL:
        handled = True
        log.info("<- SetVolumeLevel")
        try:
            status, msg = readUint16(msg)
            stream, msg = readUint16(msg)
            log.info("status = %r", status)
            log.info("stream = %r", stream)
            cf.SetVolumeLevel(status, stream)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_VOLUME_LEVEL:
        handled = True
        log.info("<- GetVolumeLevel")
        try:
            stream, msg = readUint16(msg)
            log.info("stream = %r", stream)
            cf.GetVolumeLevel(stream)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_BATTERY_LEVEL:
        handled = True
        log.info("<- GetBatteryLevel")
        try:
            cf.GetBatteryLevel()
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_INFO_CODI_STATUS:
        handled = True
        log.info("<- CoDiStatusInfo")
        try:
            mode, msg = readUint32(msg)
            screen, msg = readUint32(msg)
            data1, msg = readUint32(msg)
            log.info("mode = %r", mode)
            log.info("screen = %r", screen)
            log.info("data1 = %r", data1)
            cf.CoDiStatusInfo(mode, screen, data1)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_SET_LOCK:
        handled = True
        log.info("<- SetLock")
        try:
            status, msg = readUint16(msg)
            log.info("status = %r", status)
            cf.SetLock(status)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_LOCK_STATUS:
        handled = True
        log.info("<- GetLockStatus")
        try:
            cf.GetLockStatus()
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_DISMISS_CALL_SMS:
        handled = True
        log.info("<- DismissCallSMS")
        try:
            sim, msg = readUint32(msg)
            line, msg = readUint32(msg)
            msisdn, msg = readString(msg)
            text, msg = readUTF8String(msg)
            log.info("sim = %r", sim)
            log.info("line = %r", line)
            log.info("msisdn = %r", msisdn)
            log.info("text = %r", text)
            cf.DismissCallSMS(sim, line, msisdn, text)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_ACTION_UNLOCK:
        handled = True
        log.info("<- ActionUnlock")
        try:
            method, msg = readUint32(msg)
            strdata, msg = readString(msg)
            log.info("method = %r", method)
            log.info("strdata = %r", strdata)
            cf.ActionUnlock(method, strdata)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_INFO_ST_CHARGING:
        handled = True
        log.info("<- STChargingInfo")
        try:
            status, msg = readUint32(msg)
            measurement, msg = readUint32(msg)
            log.info("status = %r", status)
            log.info("measurement = %r", measurement)
            cf.STChargingInfo(status, measurement)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_PLAY_DTMF:
        handled = True
        log.info("<- PlayDTMF")
        try:
            ascii_num, msg = readUint8(msg)
            log.info("ascii_num = %r", ascii_num)
            cf.PlayDTMF(ascii_num)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_SEND_DTMF:
        handled = True
        log.info("<- SendDTMF")
        try:
            sim, msg = readUint32(msg)
            line, msg = readUint32(msg)
            asciinum, msg = readUint8(msg)
            playit, msg = readUint8(msg)
            log.info("sim = %r", sim)
            log.info("line = %r", line)
            log.info("asciinum = %r", asciinum)
            log.info("playit = %r", playit)
            cf.SendDTMF(sim, line, asciinum, playit)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_ACTION_CALL:
        handled = True
        log.info("<- ActionCall")
        try:
            action, msg = readUint32(msg)
            sim, msg = readUint32(msg)
            line, msg = readUint32(msg)
            numtype, msg = readUint32(msg)
            msisdn, msg = readString(msg)
            contact, msg = readUTF8String(msg)
            contact_id, msg = readString(msg)
            log.info("action = %r", action)
            log.info("sim = %r", sim)
            log.info("line = %r", line)
            log.info("numtype = %r", numtype)
            log.info("msisdn = %r", msisdn)
            log.info("contact = %r", contact)
            log.info("contact_id = %r", contact_id)
            cf.ActionCall(action, sim, line, numtype, msisdn, contact, contact_id)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_SEND_TELE_CODE:
        handled = True
        log.info("<- SendTeleCode")
        try:
            sim, msg = readUint32(msg)
            line, msg = readUint32(msg)
            telecode, msg = readString(msg)
            log.info("sim = %r", sim)
            log.info("line = %r", line)
            log.info("telecode = %r", telecode)
            cf.SendTeleCode(sim, line, telecode)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_SET_CALL_MUTE_STATUS:
        handled = True
        log.info("<- SetCallMuteStatus")
        try:
            status, msg = readUint32(msg)
            log.info("status = %r", status)
            cf.SetCallMuteStatus(status)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_CALL_MUTE_STATUS:
        handled = True
        log.info("<- GetCallMuteStatus")
        try:
            cf.GetCallMuteStatus()
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_SET_CALL_OUTPUT:
        handled = True
        log.info("<- SetCallOutput")
        try:
            status, msg = readUint32(msg)
            log.info("status = %r", status)
            cf.SetCallOutput(status)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_CALL_OUTPUT:
        handled = True
        log.info("<- GetCallOutput")
        try:
            cf.GetCallOutput()
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_CALL_OUTPUT_OPTIONS:
        handled = True
        log.info("<- GetCallOutputOptions")
        try:
            cf.GetCallOutputOptions()
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_ACTION_CAMERA:
        handled = True
        log.info("<- ActionCamera")
        try:
            action, msg = readUint32(msg)
            log.info("action = %r", action)
            cf.ActionCamera(action)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_CAMERA_FRAME:
        handled = True
        log.info("<- GetCameraFrame")
        try:
            cf.GetCameraFrame()
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_SET_CAMERA_SETTINGS:
        handled = True
        log.info("<- SetCameraSettings")
        try:
            parameter, msg = readUint32(msg)
            value, msg = readUint32(msg)
            log.info("parameter = %r", parameter)
            log.info("value = %r", value)
            cf.SetCameraSettings(parameter, value)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_CAMERA_CAPTURE_IMAGE:
        handled = True
        log.info("<- CameraCaptureImage")
        try:
            cf.CameraCaptureImage()
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_ACTION_VIDEO:
        handled = True
        log.info("<- ActionVideo")
        try:
            action, msg = readUint32(msg)
            log.info("action = %r", action)
            cf.ActionVideo(action)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_VIDEO_FRAME:
        handled = True
        log.info("<- GetVideoFrame")
        try:
            cf.GetVideoFrame()
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_SET_VIDEO_SETTINGS:
        handled = True
        log.info("<- SetVideoSettings")
        try:
            parameter, msg = readUint32(msg)
            value, msg = readUint32(msg)
            log.info("parameter = %r", parameter)
            log.info("value = %r", value)
            cf.SetVideoSettings(parameter, value)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_VIDEO_CAPTURE_IMAGE:
        handled = True
        log.info("<- VideoCaptureImage")
        try:
            cf.VideoCaptureImage()
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_COVER_LIGHT_SENSOR:
        handled = True
        log.info("<- GetCoverLightSensor")
        try:
            cf.GetCoverLightSensor()
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_INFO_CURRENT_LANGUAGE:
        handled = True
        log.info("<- CurrentLanguageInfo")
        try:
            langid, msg = readString(msg)
            hasallresources, msg = readUint32(msg)
            data1, msg = readUint32(msg)
            log.info("langid = %r", langid)
            log.info("hasallresources = %r", hasallresources)
            log.info("data1 = %r", data1)
            cf.CurrentLanguageInfo(langid, hasallresources, data1)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_INFO_MEDIA_RESOURCE:
        handled = True
        log.info("<- MediaResourceInfo")
        try:
            typestr, msg = readString(msg)
            resname, msg = readString(msg)
            length, msg = readUint32(msg)
            status, msg = readUint32(msg)
            log.info("typestr = %r", typestr)
            log.info("resname = %r", resname)
            log.info("length = %r", length)
            log.info("status = %r", status)
            cf.MediaResourceInfo(typestr, resname, length, status)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_INFO_MEDIA_ACTIVITY:
        handled = True
        log.info("<- MediaActivityInfo")
        try:
            typestr, msg = readString(msg)
            resname, msg = readString(msg)
            status, msg = readUint32(msg)
            log.info("typestr = %r", typestr)
            log.info("resname = %r", resname)
            log.info("status = %r", status)
            cf.MediaActivityInfo(typestr, resname, status)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_INFO_ALERT:
        handled = True
        log.info("<- AlertInfo")
        try:
            status, msg = readUint32(msg)
            response, msg = readUint32(msg)
            responsestr, msg = readUTF8String(msg)
            log.info("status = %r", status)
            log.info("response = %r", response)
            log.info("responsestr = %r", responsestr)
            cf.AlertInfo(status, response, responsestr)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_ORIENTATION:
        handled = True
        log.info("<- GetOrientation")
        try:
            cf.GetOrientation()
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_CALL_HISTORY:
        handled = True
        log.info("<- GetCallHistory")
        try:
            index, msg = readUint32(msg)
            log.info("index = %r", index)
            cf.GetCallHistory(index)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_CONTACTS:
        handled = True
        log.info("<- GetContacts")
        try:
            index, msg = readUint32(msg)
            log.info("index = %r", index)
            cf.GetContacts(index)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_ACTION_PLAYER:
        handled = True
        log.info("<- ActionPlayer")
        try:
            action, msg = readUint32(msg)
            log.info("action = %r", action)
            cf.ActionPlayer(action)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_ACTION_NOTIFICATION:
        handled = True
        log.info("<- ActionNotification")
        try:
            notid, msg = readUint32(msg)
            action, msg = readUint32(msg)
            pos, msg = readUint32(msg)
            log.info("notid = %r", notid)
            log.info("action = %r", action)
            log.info("pos = %r", pos)
            cf.ActionNotification(notid, action, pos)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_LEDISON_PATTERN:
        handled = True
        log.info("<- GetLEDisonPattern")
        try:
            contactid, msg = readString(msg)
            contactname, msg = readUTF8String(msg)
            msisdn, msg = readString(msg)
            log.info("contactid = %r", contactid)
            log.info("contactname = %r", contactname)
            log.info("msisdn = %r", msisdn)
            cf.GetLEDisonPattern(contactid, contactname, msisdn)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_LEDISON_MODE:
        handled = True
        log.info("<- GetLEDisonMode")
        try:
            cf.GetLEDisonMode()
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_CONTACT_ICON:
        handled = True
        log.info("<- GetContactIcon")
        try:
            contactid, msg = readString(msg)
            contactname, msg = readUTF8String(msg)
            msisdn, msg = readString(msg)
            log.info("contactid = %r", contactid)
            log.info("contactname = %r", contactname)
            log.info("msisdn = %r", msisdn)
            cf.GetContactIcon(contactid, contactname, msisdn)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_MODEM_SIGNAL_INFO:
        handled = True
        log.info("<- GetModemSignalInfo")
        try:
            cf.GetModemSignalInfo()
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_DATE_TIME_FORMAT:
        handled = True
        log.info("<- GetDateTimeFormat")
        try:
            cf.GetDateTimeFormat()
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_GET_ALBUM_ART:
        handled = True
        log.info("<- GetAlbumArt")
        try:
            mediasessionformat, msg = readBlob(msg)
            log.info("mediasessionformat =", mediasessionformat)
            cf.GetAlbumArt(mediasessionformat)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_ACTION_VOICE_RECODER:
        handled = True
        log.info("<- ActionVoiceRecorder")
        try:
            action, msg = readUint32(msg)
            log.info("action = %r", action)
            cf.ActionVoiceRecorder(action)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_SET_VOICE_RECORDER_SETTINGS:
        handled = True
        log.info("<- SetVoiceRecorderSettings")
        try:
            parameter, msg = readUint32(msg)
            value, msg = readUint32(msg)
            log.info("parameter = %r", parameter)
            log.info("value = %r", value)
            cf.SetVoiceRecorderSettings(parameter, value)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_ST32_DATA_CHANGE_ALERT:
        handled = True
        log.info("<- STDataChangeAlert")
        try:
            type, msg = readUint32(msg)
            data1, msg = readUint32(msg)
            log.info("type = %r", type)
            log.info("data1 = %r", data1)
            cf.STDataChangeAlert(type, data1)
        except Exception as e:
            log.error(e)

    if cmdId == CMD_SYNC_SYS_SLEEP_STATUS:
        handled = True
        log.info("<- CoDiOFF")
        try:
            par1, msg = readUint8(msg)
            log.info("par1 = %r", par1)
            par2, msg = readUint8(msg)
            log.info("par2 = %r", par2)
            cf.CoDiOFF(par1, par2)
        except Exception as e:
            log.error(e)

    if cmdId == 147:
        handled = True
        log.info("<- MouseInfo")
        try:
            mode, msg = readUint8(msg)
            log.info("mode = %r", mode)
            x_coord, msg = readInt16(msg)
            log.info("x_coord = %r", x_coord)
            y_coord, msg = readInt16(msg)
            log.info("y_coord = %r", y_coord)
            cf.MouseInfo(mode, x_coord, y_coord)
        except Exception as e:
            log.error(e)

    if cmdId == 148:
        handled = True
        log.info("<- MouseInfo2")
        try:
            pressState, msg = readUint8(msg)
            log.info("pressState = %r", pressState)
            previousState, msg = readUint8(msg)
            log.info("previousSatate = %r", previousState)
            x_coord, msg = readUint16(msg)
            log.info("x_coord = %r", x_coord)
            y_coord, msg = readUint16(msg)
            log.info("y_coord = %r", y_coord)
            cf.MouseInfo2(pressState, previousState, x_coord, y_coord)
        except Exception as e:
            log.error(e)

    if not handled:
        log.info("<- Unrecognised command %r", cmdId)