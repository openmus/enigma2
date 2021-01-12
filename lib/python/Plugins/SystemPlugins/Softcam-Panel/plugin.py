from Plugins.Plugin import PluginDescriptor
from Components.config import config, ConfigSubsection, ConfigYesNo
from Tools.BoundFunction import boundFunction
import os

config.misc.softcam_panel = ConfigSubsection()
config.misc.softcam_panel.extension_menu = ConfigYesNo(default = True)

CamInstalled = False
for cam in os.listdir("/etc/init.d"):
	if cam.startswith('softcam.') and not cam.endswith('None'):
		CamInstalled = True
	elif cam.startswith('cardserver.') and not cam.endswith('None'):
		CamInstalled = True
	else:
		pass

def main(session, showExtentionMenuOption=False, **kwargs):
	import SoftcamPanel
	session.open(SoftcamPanel.SoftcamPanel, showExtentionMenuOption)

def menu(menuid, **kwargs):
	if menuid == "cam" and CamInstalled:
		return [(_("Softcam panel..."), boundFunction(main, showExtentionMenuOption=True), "softcam_panel", -1)]
	return []

def Plugins(path,**kwargs):
    return [
            PluginDescriptor(name="SoftCam Panel", description="softcam",where = PluginDescriptor.WHERE_MENU, fnc=mainmenu),
            #PluginDescriptor(name="Emu Panel", where = PluginDescriptor.WHERE_MENU, fnc=mainmenu)
            PluginDescriptor(name="SoftCam Panel", where = PluginDescriptor.WHERE_AUTOSTART,fnc=autostart)
           ]
