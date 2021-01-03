installdir = $(pkglibdir)/python/Plugins/SystemPlugins

SUBDIRS = SoftwareManager PositionerSetup Satfinder \
	SatelliteEquipmentControl Videomode VideoTune Hotplug \
	DefaultServicesScanner DiseqcTester CommonInterfaceAssignment \
	CableScan FastScan OSDPositionSetup OSD3DSetup HdmiCEC VideoClippingSetup \
	VideoEnhancement WirelessLan NetworkWizard CleanupWizard CrashlogAutoSubmit \ 
	DBusInterfaceProxy DevShell FSBLUpdater FrontprocessorUpgrade  InputDeviceManager \ 
	JSONApi MediaDatabaseManager NetworkManager RemoteControlSelection SkinSelector \
	StreamServer TempFanControl UPnP 

if HAVE_TEMPFANCONTROL
SUBDIRS += TempFanControl
endif

install_PYTHON =	\
	__init__.py
