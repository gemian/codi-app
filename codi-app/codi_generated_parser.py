import argparse

parser = argparse.ArgumentParser(description="Codi Utility for Linux.")
subparsers = parser.add_subparsers(help="sub-command help", dest="command")
cmd0 = subparsers.add_parser("GetFlashVersion", help="GetFlashVersion")

cmd1 = subparsers.add_parser("DateTimeInfo", help="DateTimeInfo day month year hour minute second tz")
cmd1.add_argument("day", type=int)
cmd1.add_argument("month", type=int)
cmd1.add_argument("year", type=int)
cmd1.add_argument("hour", type=int)
cmd1.add_argument("minute", type=int)
cmd1.add_argument("second", type=int)
cmd1.add_argument("tz", type=int)

cmd2 = subparsers.add_parser("LocationStatusInfo", help="LocationStatusInfo status")
cmd2.add_argument("status", type=int)

cmd3 = subparsers.add_parser("TorchStatusInfo", help="TorchStatusInfo status")
cmd3.add_argument("status", type=int)

cmd4 = subparsers.add_parser("CoverStatusInfo", help="CoverStatusInfo status")
cmd4.add_argument("status", type=int)

cmd5 = subparsers.add_parser("WiFiStatusInfo", help="WiFiStatusInfo status signalval")
cmd5.add_argument("status", type=int)
cmd5.add_argument("signalval", type=int)

cmd6 = subparsers.add_parser("BTStatusInfo", help="BTStatusInfo status")
cmd6.add_argument("status", type=int)

cmd7 = subparsers.add_parser("BatterySaverStatusInfo", help="BatterySaverStatusInfo status")
cmd7.add_argument("status", type=int)

cmd8 = subparsers.add_parser("FlightModeStatusInfo", help="FlightModeStatusInfo status")
cmd8.add_argument("status", type=int)

cmd9 = subparsers.add_parser("HotspotStatusInfo", help="HotspotStatusInfo status")
cmd9.add_argument("status", type=int)

cmd10 = subparsers.add_parser("MobileDataStatusInfo", help="MobileDataStatusInfo status")
cmd10.add_argument("status", type=int)

cmd11 = subparsers.add_parser("DoNotDisturbStatusInfo", help="DoNotDisturbStatusInfo status")
cmd11.add_argument("status", type=int)

cmd12 = subparsers.add_parser("VolumeLevelInfo", help="VolumeLevelInfo status stream")
cmd12.add_argument("status", type=int)
cmd12.add_argument("stream", type=int)

cmd13 = subparsers.add_parser("BatteryLevelInfo", help="BatteryLevelInfo status")
cmd13.add_argument("status", type=int)

cmd14 = subparsers.add_parser("SetCoDiStatus", help="SetCoDiStatus mode screen data1")
cmd14.add_argument("mode", type=int)
cmd14.add_argument("screen", type=int)
cmd14.add_argument("data1", type=int)

cmd15 = subparsers.add_parser("LockStatusInfo", help="LockStatusInfo locked method strdata")
cmd15.add_argument("locked", type=int)
cmd15.add_argument("method", type=int)
cmd15.add_argument("strdata", type=str)

cmd16 = subparsers.add_parser("CallMuteStatusInfo", help="CallMuteStatusInfo status")
cmd16.add_argument("status", type=int)

cmd17 = subparsers.add_parser("CallOutputInfo", help="CallOutputInfo output")
cmd17.add_argument("output", type=int)

cmd18 = subparsers.add_parser("CallOutputOptionsInfo", help="CallOutputOptionsInfo output_options")
cmd18.add_argument("output_options", type=int)

cmd19 = subparsers.add_parser("CameraStatusInfo", help="CameraStatusInfo status")
cmd19.add_argument("status", type=int)

cmd20 = subparsers.add_parser("CameraSettingsInfo", help="CameraSettingsInfo parameter value")
cmd20.add_argument("parameter", type=int)
cmd20.add_argument("value", type=int)

cmd21 = subparsers.add_parser("VideoStatusInfo", help="VideoStatusInfo status")
cmd21.add_argument("status", type=int)

cmd22 = subparsers.add_parser("VideoSettingsInfo", help="VideoSettingsInfo parameter value")
cmd22.add_argument("parameter", type=int)
cmd22.add_argument("value", type=int)

cmd23 = subparsers.add_parser("CoverLightSensorInfo", help="CoverLightSensorInfo value")
cmd23.add_argument("value", type=int)

cmd24 = subparsers.add_parser("LoadLanguageResource", help="LoadLanguageResource langid resname resdata forcereload")
cmd24.add_argument("langid", type=str)
cmd24.add_argument("resname", type=str)
cmd24.add_argument("resdata", type=bytes)
cmd24.add_argument("forcereload", type=int)

cmd25 = subparsers.add_parser("GetCurrentLanguage", help="GetCurrentLanguage")

cmd26 = subparsers.add_parser("SetCurrentLanguage", help="SetCurrentLanguage langid")
cmd26.add_argument("langid", type=str)

cmd27 = subparsers.add_parser("ShowMedia", help="ShowMedia typestr resname seconds speed aftermode")
cmd27.add_argument("typestr", type=str)
cmd27.add_argument("resname", type=str)
cmd27.add_argument("seconds", type=int)
cmd27.add_argument("speed", type=int)
cmd27.add_argument("aftermode", type=int)

cmd28 = subparsers.add_parser("StopMedia", help="StopMedia typestr resname aftermode")
cmd28.add_argument("typestr", type=str)
cmd28.add_argument("resname", type=str)
cmd28.add_argument("aftermode", type=int)

cmd29 = subparsers.add_parser("LoadMedia", help="LoadMedia typestr resname resdata loadmode")
cmd29.add_argument("typestr", type=str)
cmd29.add_argument("resname", type=str)
cmd29.add_argument("resdata", type=bytes)
cmd29.add_argument("loadmode", type=int)

cmd30 = subparsers.add_parser("UnloadMedia", help="UnloadMedia typestr resname")
cmd30.add_argument("typestr", type=str)
cmd30.add_argument("resname", type=str)

cmd31 = subparsers.add_parser("HasMedia", help="HasMedia typestr resname")
cmd31.add_argument("typestr", type=str)
cmd31.add_argument("resname", type=str)

cmd32 = subparsers.add_parser("ShowAlert", help="ShowAlert alertmode alertype alerticondata typestr resname seconds speed aftermode option1 option2")
cmd32.add_argument("alertmode", type=int)
cmd32.add_argument("alertype", type=int)
cmd32.add_argument("alerticondata", type=bytes)
cmd32.add_argument("typestr", type=str)
cmd32.add_argument("resname", type=str)
cmd32.add_argument("seconds", type=int)
cmd32.add_argument("speed", type=int)
cmd32.add_argument("aftermode", type=int)
cmd32.add_argument("option1", type=str)
cmd32.add_argument("option2", type=str)

cmd33 = subparsers.add_parser("StopAlert", help="StopAlert aftermode")
cmd33.add_argument("aftermode", type=int)

cmd34 = subparsers.add_parser("OrientationInfo", help="OrientationInfo value")
cmd34.add_argument("value", type=int)

cmd35 = subparsers.add_parser("ActionCoDiHome", help="ActionCoDiHome screenoff")
cmd35.add_argument("screenoff", type=int)

cmd36 = subparsers.add_parser("NextAlarmInfo", help="NextAlarmInfo appid daystring timestr")
cmd36.add_argument("appid", type=int)
cmd36.add_argument("daystring", type=str)
cmd36.add_argument("timestr", type=str)

cmd37 = subparsers.add_parser("ShowBatteryLevel", help="ShowBatteryLevel percentage showforseconds")
cmd37.add_argument("percentage", type=int)
cmd37.add_argument("showforseconds", type=int)

cmd38 = subparsers.add_parser("ContactInfo", help="ContactInfo contactid totalcontacts batchsize contactname msisdn")
cmd38.add_argument("contactid", type=str)
cmd38.add_argument("totalcontacts", type=int)
cmd38.add_argument("batchsize", type=int)
cmd38.add_argument("contactname", type=str)
cmd38.add_argument("msisdn", type=str)

cmd39 = subparsers.add_parser("CallHistoryInfo", help="CallHistoryInfo cdrid totalcdr batchsize contactname msisdn day month year hour minute second tz state")
cmd39.add_argument("cdrid", type=int)
cmd39.add_argument("totalcdr", type=int)
cmd39.add_argument("batchsize", type=int)
cmd39.add_argument("contactname", type=str)
cmd39.add_argument("msisdn", type=str)
cmd39.add_argument("day", type=int)
cmd39.add_argument("month", type=int)
cmd39.add_argument("year", type=int)
cmd39.add_argument("hour", type=int)
cmd39.add_argument("minute", type=int)
cmd39.add_argument("second", type=int)
cmd39.add_argument("tz", type=int)
cmd39.add_argument("state", type=int)

cmd40 = subparsers.add_parser("NotificationInfo", help="NotificationInfo notid action appname shortinfo longinfo day month year hour minute second tz replyactions replyaction1 replyaction2 replyaction3")
cmd40.add_argument("notid", type=int)
cmd40.add_argument("action", type=int)
cmd40.add_argument("appname", type=str)
cmd40.add_argument("shortinfo", type=str)
cmd40.add_argument("longinfo", type=str)
cmd40.add_argument("day", type=int)
cmd40.add_argument("month", type=int)
cmd40.add_argument("year", type=int)
cmd40.add_argument("hour", type=int)
cmd40.add_argument("minute", type=int)
cmd40.add_argument("second", type=int)
cmd40.add_argument("tz", type=int)
cmd40.add_argument("replyactions", type=int)
cmd40.add_argument("replyaction1", type=str)
cmd40.add_argument("replyaction2", type=str)
cmd40.add_argument("replyaction3", type=str)

cmd41 = subparsers.add_parser("PlayerInfo", help="PlayerInfo appname artist album track offset length state imageadr")
cmd41.add_argument("appname", type=str)
cmd41.add_argument("artist", type=str)
cmd41.add_argument("album", type=str)
cmd41.add_argument("track", type=str)
cmd41.add_argument("offset", type=int)
cmd41.add_argument("length", type=int)
cmd41.add_argument("state", type=int)
cmd41.add_argument("imageadr", type=bytes)

cmd42 = subparsers.add_parser("CallInfo", help="CallInfo modem action contactid contactname msisdn hasicon")
cmd42.add_argument("modem", type=int)
cmd42.add_argument("action", type=int)
cmd42.add_argument("contactid", type=str)
cmd42.add_argument("contactname", type=str)
cmd42.add_argument("msisdn", type=str)
cmd42.add_argument("hasicon", type=int)

cmd43 = subparsers.add_parser("LEDisonModeInfo", help="LEDisonModeInfo value")
cmd43.add_argument("value", type=int)

cmd44 = subparsers.add_parser("LEDisonPatternInfo", help="LEDisonPatternInfo animid animname animationdata")
cmd44.add_argument("animid", type=int)
cmd44.add_argument("animname", type=str)
cmd44.add_argument("animationdata", type=bytes)

cmd45 = subparsers.add_parser("ContactIconInfo", help="ContactIconInfo contactid contactname msisdn icondata")
cmd45.add_argument("contactid", type=str)
cmd45.add_argument("contactname", type=str)
cmd45.add_argument("msisdn", type=str)
cmd45.add_argument("icondata", type=bytes)

cmd46 = subparsers.add_parser("ModemSignalInfo", help="ModemSignalInfo sim1 sim2 sim2type")
cmd46.add_argument("sim1", type=int)
cmd46.add_argument("sim2", type=int)
cmd46.add_argument("sim2type", type=int)

cmd47 = subparsers.add_parser("WeatherInfo", help="WeatherInfo weatherstate temp scale additionaltext")
cmd47.add_argument("weatherstate", type=int)
cmd47.add_argument("temp", type=int)
cmd47.add_argument("scale", type=str)
cmd47.add_argument("additionaltext", type=str)

cmd48 = subparsers.add_parser("ExtraCommand", help="ExtraCommand data1 data2 str1 str2")
cmd48.add_argument("data1", type=int)
cmd48.add_argument("data2", type=int)
cmd48.add_argument("str1", type=str)
cmd48.add_argument("str2", type=str)

cmd49 = subparsers.add_parser("DateTimeFormat", help="DateTimeFormat dateformat timeformat")
cmd49.add_argument("dateformat", type=str)
cmd49.add_argument("timeformat", type=int)

cmd50 = subparsers.add_parser("AlbumArtInfo", help="AlbumArtInfo albumartpng")
cmd50.add_argument("albumartpng", type=bytes)

cmd51 = subparsers.add_parser("CameraFrameImage", help="CameraFrameImage width height png")
cmd51.add_argument("width", type=int)
cmd51.add_argument("height", type=int)
cmd51.add_argument("png", type=bytes)

cmd52 = subparsers.add_parser("KeyPressInfo", help="KeyPressInfo keycode mode modifiers")
cmd52.add_argument("keycode", type=int)
cmd52.add_argument("mode", type=int)
cmd52.add_argument("modifiers", type=int)

cmd53 = subparsers.add_parser("VoiceRecorderSettingsInfo", help="VoiceRecorderSettingsInfo parameter value")
cmd53.add_argument("parameter", type=int)
cmd53.add_argument("value", type=int)

cmd54 = subparsers.add_parser("VoiceRecorderStatusInfo", help="VoiceRecorderStatusInfo status")
cmd54.add_argument("status", type=int)

cmd55 = subparsers.add_parser("MTKDataChangeAlert", help="MTKDataChangeAlert type data1")
cmd55.add_argument("type", type=int)
cmd55.add_argument("data1", type=int)


dbusCmd = subparsers.add_parser("dbus", help="DBUS command")
dbusCmd.add_argument("cmd", type=str)

args = vars(parser.parse_args())
