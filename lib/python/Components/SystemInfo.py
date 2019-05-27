from enigma import eDVBResourceManager, Misc_Options
from Tools.Directories import fileExists, fileCheck, pathExists, resolveFilename, SCOPE_SKIN
from Tools.HardwareInfo import HardwareInfo
from boxbranding import getBoxType, getMachineBuild

SystemInfo = {}

def getNumVideoDecoders():
	number_of_video_decoders = 0
	while fileExists("/dev/dvb/adapter0/video%d" % (number_of_video_decoders), 'f'):
		number_of_video_decoders += 1
	return number_of_video_decoders

def countFrontpanelLEDs():
	number_of_leds = fileExists("/proc/stb/fp/led_set_pattern") and 1 or 0
	while fileExists("/proc/stb/fp/led%d_pattern" % number_of_leds):
		number_of_leds += 1
	return number_of_leds

def getHasTuners():
	if fileExists("/proc/bus/nim_sockets"):
		nimfile = open("/proc/bus/nim_sockets")
		data = nimfile.read().strip()
		nimfile.close()
		return len(data) > 0
	return False

SystemInfo["NumVideoDecoders"] = getNumVideoDecoders()
SystemInfo["PIPAvailable"] = SystemInfo["NumVideoDecoders"] > 1
SystemInfo["CanMeasureFrontendInputPower"] = eDVBResourceManager.getInstance().canMeasureFrontendInputPower()
SystemInfo["12V_Output"] = Misc_Options.getInstance().detected_12V_output()
SystemInfo["ZapMode"] = fileCheck("/proc/stb/video/zapmode") or fileCheck("/proc/stb/video/zapping_mode")
SystemInfo["NumFrontpanelLEDs"] = countFrontpanelLEDs()
SystemInfo["FrontpanelDisplay"] = fileExists("/dev/dbox/oled0") or fileExists("/dev/dbox/lcd0")
SystemInfo["LCDsymbol_circle_recording"] = fileCheck("/proc/stb/lcd/symbol_circle") or getBoxType() in ("hd51", "vs1500") and fileCheck("/proc/stb/lcd/symbol_recording")
SystemInfo["LCDsymbol_timeshift"] = fileCheck("/proc/stb/lcd/symbol_timeshift")
SystemInfo["LCDshow_symbols"] = (getBoxType().startswith("et9") or getBoxType() in  ("hd51", "vs1500")) and fileCheck("/proc/stb/lcd/show_symbols")
SystemInfo["LCDsymbol_hdd"] = getBoxType() in ("hd51", "vs1500") and fileCheck("/proc/stb/lcd/symbol_hdd")
SystemInfo["FrontpanelDisplayGrayscale"] = fileExists("/dev/dbox/oled0")
SystemInfo["LcdDisplay"] = fileExists("/dev/dbox/lcd0")
SystemInfo["DeepstandbySupport"] = getBoxType() != "dm800"
SystemInfo["OledDisplay"] = fileExists(resolveFilename(SCOPE_SKIN, 'lcd_skin/skin_lcd_default.xml'))
SystemInfo["GraphicLCD"] = getBoxType() in ('quadbox2400')
SystemInfo["GBWOL"] = fileExists("/usr/bin/gigablue_wol")
SystemInfo["Fan"] = fileCheck("/proc/stb/fp/fan")
SystemInfo["FanPWM"] = SystemInfo["Fan"] and fileCheck("/proc/stb/fp/fan_pwm")
SystemInfo["StandbyLED"] = fileCheck("/proc/stb/power/standbyled")
SystemInfo["HasExternalPIP"] = getMachineBuild() not in ('et9x00', 'et6x00', 'et5x00') and fileCheck("/proc/stb/vmpeg/1/external")
SystemInfo["PowerOffDisplay"] = getBoxType() not in ('formuler1') and fileCheck("/proc/stb/power/vfd") or fileCheck("/proc/stb/lcd/vfd")
SystemInfo["VideoDestinationConfigurable"] = fileExists("/proc/stb/vmpeg/0/dst_left")
SystemInfo["hasPIPVisibleProc"] = fileCheck("/proc/stb/vmpeg/1/visible")
SystemInfo["hasTuners"] = getHasTuners() or fileCheck("/usr/lib/enigma2/python/Plugins/SystemPlugins/SatipClient/plugin.pyo")
SystemInfo["hasGBIpboxClient"] = fileCheck("/usr/lib/enigma2/python/Plugins/Extensions/GBIpboxClient/plugin.pyo")

#if getBoxType() in ('gbquadplus'):
#	SystemInfo["WakeOnLAN"] = False
#else:
SystemInfo["WakeOnLAN"] = fileCheck("/proc/stb/fp/wol")

SystemInfo["VFD_scroll_repeats"] = fileCheck("/proc/stb/lcd/scroll_repeats")
SystemInfo["VFD_scroll_delay"] = fileCheck("/proc/stb/lcd/scroll_delay")
SystemInfo["VFD_initial_scroll_delay"] = fileCheck("/proc/stb/lcd/initial_scroll_delay")
SystemInfo["VFD_final_scroll_delay"] = fileCheck("/proc/stb/lcd/final_scroll_delay")
SystemInfo["LcdLiveTV"] = fileCheck("/proc/stb/fb/sd_detach") or fileCheck("/proc/stb/lcd/live_enable")
SystemInfo["MiniTV"] = fileCheck("/proc/stb/fb/sd_detach") or fileCheck("/proc/stb/lcd/live_enable")
SystemInfo["FastChannelChange"] = False
SystemInfo["3DMode"] = fileCheck("/proc/stb/fb/primary/3d")
SystemInfo["3DZNorm"] = fileCheck("/proc/stb/fb/primary/zoffset")
SystemInfo["IPV6"] = fileCheck("/proc/sys/net/ipv6/conf/all/disable_ipv6")
SystemInfo["Blindscan_t2_available"] = fileCheck("/proc/stb/info/vumodel")
SystemInfo["Bootvideo"] = fileCheck("/usr/bin/bootvideo")
SystemInfo["hasOSDAnimation"] = fileCheck("/proc/stb/fb/animation_mode")
SystemInfo["RcTypeChangable"] = pathExists('/proc/stb/ir/rc/type')
SystemInfo["HasFullHDSkinSupport"] = getBoxType() not in ('gb800solo', 'gb800se', 'gb800ue')
SystemInfo["HasForceLNBOn"] = fileCheck("/proc/stb/frontend/fbc/force_lnbon")
SystemInfo["HasForceToneburst"] = fileCheck("/proc/stb/frontend/fbc/force_toneburst")
SystemInfo["HasBypassEdidChecking"] = fileCheck("/proc/stb/hdmi/bypass_edid_checking")
SystemInfo["HasColorspace"] = fileCheck("/proc/stb/video/hdmi_colorspace")
SystemInfo["HasColorspaceSimple"] = SystemInfo["HasColorspace"] and getBoxType() in ('vusolo4k')
SystemInfo["HasMultichannelPCM"] = fileCheck("/proc/stb/audio/multichannel_pcm")
SystemInfo["HasMMC"] = getBoxType() in ('vusolo4k', 'hd51', 'hd52', 'gbquad4k')
SystemInfo["HasMultiBoot"] = fileCheck("/boot/STARTUP_1")
SystemInfo["CommonInterfaceCIDelay"] = fileCheck("/proc/stb/tsmux/rmx_delay")
SystemInfo["CanDoTranscodeAndPIP"] = getBoxType() in ('vusolo4k')
SystemInfo["HasColordepth"] = fileCheck("/proc/stb/video/hdmi_colordepth")
SystemInfo["HasFrontDisplayPicon"] = getBoxType() in ("vusolo4k", "et8500")
SystemInfo["HasHDMIpreemphasis"] = fileCheck("/proc/stb/hdmi/preemphasis")
SystemInfo["HasColorimetry"] = fileCheck("/proc/stb/video/hdmi_colorimetry")
SystemInfo["HasHDMI-CEC"] = HardwareInfo().has_hdmi() and fileExists("/usr/lib/enigma2/python/Plugins/SystemPlugins/HdmiCEC/plugin.pyo") and pathExists("/dev/hdmi_cec") or pathExists("/dev/misc/hdmi_cec0")
SystemInfo["HasAutoVolume"] = fileExists("/proc/stb/audio/avl_choices") and fileCheck("/proc/stb/audio/avl")
SystemInfo["HasAutoVolumeLevel"] = fileExists("/proc/stb/audio/autovolumelevel_choices") and fileCheck("/proc/stb/audio/autovolumelevel")
SystemInfo["Has3DSurround"] = fileExists("/proc/stb/audio/3d_surround_choices") and fileCheck("/proc/stb/audio/3d_surround")
SystemInfo["Has3DSpeaker"] = fileExists("/proc/stb/audio/3d_surround_speaker_position_choices") and fileCheck("/proc/stb/audio/3d_surround_speaker_position")
SystemInfo["Has3DSurroundSpeaker"] = fileExists("/proc/stb/audio/3dsurround_choices") and fileCheck("/proc/stb/audio/3dsurround")
SystemInfo["Has3DSurroundSoftLimiter"] = fileExists("/proc/stb/audio/3dsurround_softlimiter_choices") and fileCheck("/proc/stb/audio/3dsurround_softlimiter")
SystemInfo["HasHDMI-In"] = getBoxType() in ('gbquad4k')
SystemInfo["hasXcoreVFD"] = fileCheck("/sys/module/brcmstb_%s/parameters/pt6302_cgram" % HardwareInfo().get_device_model())
