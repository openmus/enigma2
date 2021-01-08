from Screens.Screen import Screen
from Plugins.Plugin import PluginDescriptor
from Screens.ChoiceBox import ChoiceBox
from Screens.MessageBox import MessageBox
from Components.FileList import FileEntryComponent, FileList
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap, NumberActionMap
from Components.Button import Button
from Components.Label import Label
from Components.config import config, ConfigElement, ConfigSubsection, ConfigSelection, ConfigSubList, getConfigListEntry, KEY_LEFT, KEY_RIGHT, KEY_OK
from Components.ConfigList import ConfigList
from Components.Pixmap import Pixmap
from Components.Sources.List import List
from enigma import eTimer, eDVBCI_UI, eListboxPythonStringContent, eListboxPythonConfigContent, iServiceInformation
from Screens.Console import Console
from Components.ScrollLabel import ScrollLabel
from Components.Sources.StaticText import StaticText
from Components.Harddisk import harddiskmanager
from Components.NimManager import nimmanager
from Tools.DreamboxHardware import getFPVersion
from Tools.Directories import SCOPE_SKIN_IMAGE, resolveFilename
from Tools import Notifications
from Tools.LoadPixmap import LoadPixmap
import xml.dom.minidom
from ServiceReference import ServiceReference
import os, sys
from os import listdir
from twisted.web.client import downloadPage 
import urllib

###################################            
class CamConfig:
    
    def __init__(self, name):
        self.name = name
        self.link = '/etc/rcS.3/S40' + name
        if not os.path.exists(self.link):
            lname = 'S40' + name
            for l in os.listdir('/etc/rc3.d'):
                if l.startswith(lname):
                    self.link = '/etc/rc3.d/' + l

    def getList(self):
        result = []
        prefix = self.name + '_'
        for f in os.listdir("/etc/init.d"):
            if f.startswith(prefix):
                result.append(f[len(prefix):])
        return result

    def current(self):
        try: 
            l = os.readlink(self.link)
            return os.path.split(l)[1].split('_')[1]
        except:
            pass
        return None

    def command(self, cmd):
        if os.path.exists(self.link):
            print "Executing", self.link + ' ' + cmd
            os.system(self.link + ' ' + cmd)

    def select(self, which):
        print "Selecting CAM:", which
        try:
            os.unlink(self.link)
        except:
            pass
        if not which:
            return
        dst = '../init.d/' + self.name + '_' + which
        if not os.path.exists('/etc/init.d/' + self.name + '_' + which):
            return # probably "None" was selected here
        try:
            newlink = '/etc/rc3.d/S40' + self.name + '_' + which
            os.symlink(dst, newlink);
        except:
            print "Failed to create symlink for softcam:", dst
            import sys
            print sys.exc_info()[:2]
            
class SrvConfig:

    def __init__(self, name):
        self.name = name
        self.link = '/etc/rc3.d/S40'+ name
        if not os.path.exists(self.link):
            lname = 'S40' + name
            for l in os.listdir('/etc/rc3.d'):
                if l.startswith(lname):
                    self.link = '/etc/rc3.d/' + l

    def getList(self):
        result = []
        prefix = self.name + '_'
        for f in os.listdir("/etc/init.d"):
            if f.startswith(prefix):
                result.append(f[len(prefix):])
        return result

    def current(self):
        try: 
            l = os.readlink(self.link)
            return os.path.split(l)[1].split('_')[1]
        except:
            pass
        return None

    def command(self, cmd):
        if os.path.exists(self.link):
            print "Executing", self.link + ' ' + cmd
            os.system(self.link + ' ' + cmd)

    def select(self, which):
        print "Selecting Cardserver:", which
        try:
            os.unlink(self.link)
        except:
            pass
        if not which:
            return
        dst = '../init.d/' + self.name + '_' + which
        if not os.path.exists('/etc/init.d/' + self.name + '_' + which):
            return # probably "None" was selected here
        try:
            newlink = '/etc/rc3.d/S40' + self.name + '_' + which
            os.symlink(dst, newlink);
        except:
            print "Failed to create symlink for cardserver:", dst
            import sys
            print sys.exc_info()[:2]
 ###########################""           
class Emupanel(Screen):
    skin = """
        <screen name="Emupanel" position="center,center" size="570,410" title="SoftCam Panel 2.0">
                <widget name="entries" position="20,100" size="500,160" />
                <widget name="info" position="40,190" zPosition="4" size="360,220" font="Regular;18" foregroundColor="#ffffff" transparent="1" halign="left" valign="center" />
                <widget name="ecmtext" position="130,60" zPosition="4" size="360,220" font="Regular;18" foregroundColor="#ffffff" transparent="1" halign="left" valign="center" />
                <ePixmap name="red" position="0,0" zPosition="1" size="150,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />
                <ePixmap name="green" position="140,0" zPosition="1" size="150,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />
                <ePixmap name="yellow" position="280,0" zPosition="1" size="150,40" pixmap="skin_default/buttons/yellow.png" transparent="1" alphatest="on" />
                <ePixmap name="blue" position="420,0" zPosition="1" size="150,40" pixmap="skin_default/buttons/blue.png" transparent="1" alphatest="on" />
                <widget name="key_red" position="0,0" zPosition="2" size="150,40" valign="center" halign="center" font="Regular;21" transparent="1" backgroundColor="#9f1313" shadowColor="black" shadowOffset="-1,-1" />
                <widget name="key_green" position="140,0" zPosition="2" size="150,40" valign="center" halign="center" font="Regular;21" transparent="1" backgroundColor="#1f771f" shadowColor="black" shadowOffset="-1,-1" />
                <widget name="key_yellow" position="280,0" zPosition="2" size="150,40" valign="center" halign="center" font="Regular;21" transparent="1" backgroundColor="#a08500" shadowColor="black" shadowOffset="-1,-1" />
                <widget name="key_blue" position="420,0" zPosition="2" size="150,40" valign="center" halign="center" font="Regular;21" transparent="1" backgroundColor="#a08500" shadowColor="black" shadowOffset="-1,-1" />
        </screen>"""
        
    def __init__(self, session):
        Screen.__init__(self, session)

        self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "CiSelectionActions"],
            {
                "left": self.keyLeft,
                "right": self.keyRight,
                "cancel": self.cancel,
                "green": self.reset_both,
                "yellow": self.reset_sc,
                "red": self.cancel,
                "blue": self.download,
            },-1)

        self.list = [ ]

        self.softcam = CamConfig('emu')
        self.cardserver = SrvConfig('crdsrv')

        menuList = ConfigList(self.list)
        menuList.list = self.list
        menuList.l.setList(self.list)
        self["entries"] = menuList
        self["info"] = Label("")
        self["ecmtext"] = Label("")
        self.ecm()
        self.service()
        self.onShown.append(self.openTest) 
        self.mytimer = eTimer()
        self.mytimer.callback.append(self.ecm)
        self.mytimer.start(1000)

        
        softcams = [_("None")] + self.softcam.getList()
        cardservers = [_("None")] + self.cardserver.getList() 


        self.softcams = ConfigSelection(choices = softcams)
        self.softcams.value = self.softcam.current() or _("None")
        self.cardservers = ConfigSelection(choices = cardservers)
        self.cardservers.value = self.cardserver.current() or _("None")

        self.list.append(getConfigListEntry(_("Select Cam:"), self.softcams))
        self.list.append(getConfigListEntry(_("Select Cardserver:"), self.cardservers))

        self["key_red"] = Label(_("Cancel"))
        self["key_yellow"] = Label(_("Start"))
        self["key_green"] = Label(_("Restart"))
        self["key_blue"] = Label(_("Download"))

    def keyLeft(self):
        self["entries"].handleKey(KEY_LEFT)

    def keyRight(self):
        self["entries"].handleKey(KEY_RIGHT)
    
    def download(self):
            self.session.open(Getipklist)
            self.close()
    
    def openTest(self):
            return

    def restart(self):
        self.activityTimer.stop()
        if self.what == "both":
            self.cardserver.command('stop')
        self.softcam.command('stop')
        self.oldref = self.session.nav.getCurrentlyPlayingServiceReference()
        self.session.nav.stopService()

        self.softcam.select(self.softcams.value)
        if self.what == "both":
                        self.cardserver.select(self.cardservers.value)
        self.cardserver.command('start')
        self.softcam.command('start')
        self.mbox.close()
        self.close()
        self.session.nav.playService(self.oldref)

    def reset_both(self):
        self.what = "both"
        self.mbox = self.session.open(MessageBox, _("Please wait, Restarting softcam and cardserver."), MessageBox.TYPE_INFO)
        self.activityTimer = eTimer()
        self.activityTimer.timeout.get().append(self.restart)
        self.activityTimer.start(100, False)
        os.system("rm /tmp/ecm.info")
        #self["info"].setText("No ECM info")

    def reset_sc(self):
        self.what = "sc"
        self.mbox = self.session.open(MessageBox, _("Please wait, starting softcam."), MessageBox.TYPE_INFO)
        self.activityTimer = eTimer()
        self.activityTimer.timeout.get().append(self.restart)
        self.activityTimer.start(100, False)
        os.system("rm /tmp/ecm.info") 
        #self["info"].setText("No ECM info")
        
    def cancel(self):
        self.close()

    def ecm(self):
        service = self.session.nav.getCurrentService()
        info = service and service.info()

        ecmi = ""
        
        if os.path.isfile('/tmp/ecm.info') is True:
            f = open('/tmp/ecm.info')
            ecmi = f.read()
            ecmi = ecmi.replace('=', '')
            ecmi = ecmi.replace(' ', '', 1)
            
        

        if info is not None:
                if info.getInfo(iServiceInformation.sIsCrypted): 
                    self["info"].setText(ecmi)
                else:
                    self["info"].setText("Free To Air")
        else:
            self["info"].setText("")
        return
##################################
        
    def service(self):
        service = self.session.nav.getCurrentService()
        info = service and service.info()
         
        self.Provider= None
        self.ServiceName= None
        service = self.session.nav.getCurrentService()
        info = service and service.info()
        self.Provider = info.getInfoString(iServiceInformation.sProvider)
        self.ServiceName = info.getName().replace('\xc2\x86', '').replace('\xc2\x87', '')
        
        service = ""
        
        service = _("Provider") + " :" + self.Provider + "  " + _("Service") + " :" + self.ServiceName
        
        
        if info is not None:
            if info.getInfo(iServiceInformation.sIsCrypted):
                self["ecmtext"].setText(service)
            else:
                self["ecmtext"].setText(service)
        else:
            self["ecmtext"].setText("")
        
        
 ############################################
              
class Getipklist(Screen):

    skin = """
        <screen position="center,center" size="600,400" title="SoftCam Addons Manager 2.0" > 
            <widget name="list" position="50,20" size="500,300" scrollbarMode="showOnDemand" />
            <eLabel position="70,100" zPosition="-1" size="100,69" backgroundColor="#222222" />
            <widget name="info" position="150,50" zPosition="4" size="300,300" font="Regular;24" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" />
            <widget name="key_red" position="290,350" zPosition="2" size="150,40" valign="center" halign="center" font="Regular;21" transparent="1" backgroundColor="#9f1313" shadowColor="black" shadowOffset="-1,-1" />
            <widget name="key_green" position="150,350" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" /> 
            <ePixmap name="red" position="290,350" zPosition="1" size="150,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />
            <ePixmap name="green"  position="150,350" zPosition="2" size="140,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />
        </screen>"""

    def __init__(self, session):
        self.skin = Getipklist.skin
        Screen.__init__(self, session)

        self.list = []
               
        self["list"] = MenuList([])
        self["info"] = Label()
                
        self.addon = "emu"
        self.icount = 0
        self.downloading=False
        #self.onLayoutFinish.append(self.openTest)
        self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "CiSelectionActions"], {"ok": self.okClicked, "cancel": self.close, "red": self.about, "green": self.script,}, -1)        
        self["info"].setText("Connetting to addons server...please wait")
        self.timer = eTimer()
        self.timer.callback.append(self.openTest)
        self.timer.start(200, 1)
        self["key_red"] = Button(_("About"))
        self["key_green"] = Button(_("User Script"))
    def openTest(self):
                
   
                xurl = "http://viaccess.free.fr/emupanel.xml"
                print "xurl =", xurl
                xdest = "/usr/lib/enigma2/python/Plugins/Extensions/SoftcamPanel/emupanel.xml"
                print "xdest =", xdest
                
                try:
                    xlist = urllib.urlretrieve(xurl, xdest)
                    myfile = file(r"/usr/lib/enigma2/python/Plugins/Extensions/SoftcamPanel/emupanel.xml")
                    self.data = []
                    self.names = []
                    icount = 0
                    list = []
                    xmlparse = xml.dom.minidom.parse(myfile)
                    self.xmlparse=xmlparse
                    for plugins in xmlparse.getElementsByTagName("plugins"):
                   
                       self.names.append(plugins.getAttribute("cont").encode("utf8"))
                                                          
                             
                       self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.okClicked, "cancel": self.close}, -1)        
                       self.list=list
                       self["info"].setText("")
                       self["list"].setList(self.names)
                       self.downloading=True
                except:
                        
                       self.downloading=False
                       self["info"].setText("Addons Download Failure,please check internet connection !")
                      # self.session.openWithCallback(self.close, MessageBox, _("Check internet connection"), type = 1, timeout = 4)
    def about(self):
            self.session.open(AboutScreen)
            self.close()
            
    def script(self):
            self.session.open(ScriptExecuter)
            self.close()
            
    def setWindowTitle(self):
        self.setTitle(_("Dowanloding"))
    
    def okClicked(self):
        selection = str(self["list"].getCurrent())
        self.session.open(SelectCountry, self.xmlparse, selection)
        #self.close 
    
            
class SelectCountry(Screen):
    skin = """
        <screen position="center,center" size="600,430" title=" SoftPanel Addons Manager v2.0" >
              <widget name="countrymenu" position="10,0" size="550,380" scrollbarMode="showOnDemand" />
            </screen>
        """

    def __init__(self, session, xmlparse, selection):
        self.skin = SelectCountry.skin
        Screen.__init__(self,session)

        self.xmlparse = xmlparse
        self.selection = selection
    
        list = []
    
        for plugins in self.xmlparse.getElementsByTagName("plugins"):
            if str(plugins.getAttribute("cont").encode("utf8")) == self.selection:
                for plugin in plugins.getElementsByTagName("plugin"):
                    list.append(plugin.getAttribute("name").encode("utf8"))
                list.sort()
        self["countrymenu"] = MenuList(list)
        self["actions"] = ActionMap(["SetupActions"],
        {
            "ok"    	:	self.selCountry,
            "cancel"  :	self.close,
        }, -2)
        
    def selCountry(self):
    
        selection_country = self["countrymenu"].getCurrent()
                
        for plugins in self.xmlparse.getElementsByTagName("plugins"):
            if str(plugins.getAttribute("cont").encode("utf8")) == self.selection:
                for plugin in plugins.getElementsByTagName("plugin"):
                            
                    if plugin.getAttribute("name").encode("utf8") == selection_country:
                        urlserver = str(plugin.getElementsByTagName("url")[0].childNodes[0].data)
                        pluginname = plugin.getAttribute("name").encode("utf8")
                                   
                        self.prombt(urlserver,pluginname)
                        
                        
    def prombt(self, com,dom):
        self.com=com
        self.dom=dom
        if self.selection=="Skins":
            self.session.openWithCallback(self.callMyMsg, MessageBox, _("Do not install any skin unless you are sure it is compatible with your image.Are you sure?"), MessageBox.TYPE_YESNO)
        else:
            self.session.open(Console,_("downloading-installing: %s") % (dom), ["opkg install -force-overwrite %s" % com])
                
    def callMyMsg(self, result):
    
        if result:
            dom=self.dom
            com=self.com
            self.session.open(Console,_("downloading-installing: %s") % (dom), ["ipkg install -force-overwrite %s" % com])
    def close_session(self):
        self.close()

###################################          

class AboutScreen(Screen):
    skin = """
    <screen position="center,center" size="550,460" title="Softcampanel V 2.0" >
        <widget name="text" position="0,10" size="550,320" font="Regular;24" />
    </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        info="\n Softcampanel V 2.0- Fixed by aitchala\n --------------------------- \n  Softcampanel Plugin to manage cams and cardserver in all images...\n  --------------------------- \n                      www.azboxforum.ma"
                                
                                
        self["text"] = ScrollLabel(info)
        
        self["actions"] = ActionMap(["SetupActions"],
            {
                "ok": self.close,
                "cancel": self.close,
                
            }, -1)  
############################################

class ScriptExecuter(Screen):
        skin = """
        <screen position="center,center" size="420,400" title="Script Executer" >
                <widget name="list" position="0,0" size="420,400" scrollbarMode="showOnDemand" />
        </screen>"""

        def __init__(self, session, args=None):
                Screen.__init__(self, session)
                self.session = session
               
                try:
                        list = listdir("/usr/script")
                        list = [x[:-3] for x in list if x.endswith('.sh')]
                except:
                        list = []
               
                self["list"] = MenuList(list)
               
                self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.run, "cancel": self.close}, -1)

        def run(self):
                script = self["list"].getCurrent()
                if script is not None:
                        self.session.open(Console, script.replace("_", " "), cmdlist=[("/usr/script/%s.sh" % script)])
                                     
################################################            
def startConfig(session, **kwargs):
        session.open(Emupanel)

def mainmenu(menuid):
        if menuid != "setup":
                return [ ]
        return [(_("SoftCam Panel"), startConfig, "softcam", None)]
        
def autostart(reason, session=None, **kwargs):
    "called with reason=1 to during shutdown, with reason=0 at startup?"
    print "[Softcam] Started"
    if reason == 0:
        try:
            os.system("mv /usr/bin/dccamd /usr/bin/dccamdOrig &")
            os.system("ln -sf /usr/bin /var/bin")
            os.system("ln -sf /etc/rc3.d/emu_")
            os.system("sleep 2")
            os.system("/etc/init.d/S40")
            os.system("ln -sf /etc/rc3.d/S40crdsrv")
            os.system("sleep 2") 
            os.system("/etc/init.d/S40")


        except:
            pass	
    else:
        pass  
    
        
def Plugins(path,**kwargs):
    return [
            PluginDescriptor(name="SoftCamPanel", description="softcam",where = PluginDescriptor.WHERE_MENU, fnc=mainmenu),
            #PluginDescriptor(name="Emu Panel", where = PluginDescriptor.WHERE_MENU, fnc=mainmenu)
            PluginDescriptor(name="SoftCamPanel", where = PluginDescriptor.WHERE_AUTOSTART,fnc=autostart)
           ]
