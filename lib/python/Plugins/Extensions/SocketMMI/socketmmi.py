# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.12
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (3, 0, 0):
    new_instancemethod = lambda func, inst, cls: _socketmmi.SWIG_PyInstanceMethod_New(func)
else:
    from new import instancemethod as new_instancemethod
if _swig_python_version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = '.'.join((pkg, '_socketmmi')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_socketmmi')
    _socketmmi = swig_import_helper()
    del swig_import_helper
elif _swig_python_version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_socketmmi', [dirname(__file__)])
        except ImportError:
            import _socketmmi
            return _socketmmi
        try:
            _mod = imp.load_module('_socketmmi', fp, pathname, description)
        finally:
            if fp is not None:
                fp.close()
        return _mod
    _socketmmi = swig_import_helper()
    del swig_import_helper
else:
    import _socketmmi
del _swig_python_version_info

try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        object.__setattr__(self, name, value)
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError("'%s' object has no attribute '%s'" % (class_type.__name__, name))


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_method(set):
    def set_attr(self, name, value):
        if (name == "thisown"):
            return self.this.own(value)
        if hasattr(self, name) or (name == "this"):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add attributes to %s" % self)
    return set_attr


try:
    import weakref
    weakref_proxy = weakref.proxy
except __builtin__.Exception:
    weakref_proxy = lambda x: x


import enigma
class eSocket_UI(enigma.eMMI_UI):
    """Proxy of C++ eSocket_UI class."""

    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    socketStateChanged = _swig_property(_socketmmi.eSocket_UI_socketStateChanged_get, _socketmmi.eSocket_UI_socketStateChanged_set)

    def getInstance():
        """getInstance() -> eSocket_UI"""
        return _socketmmi.eSocket_UI_getInstance()

    getInstance = staticmethod(getInstance)

    def setInit(self, slot):
        """setInit(eSocket_UI self, int slot)"""
        return _socketmmi.eSocket_UI_setInit(self, slot)


    def setReset(self, slot):
        """setReset(eSocket_UI self, int slot)"""
        return _socketmmi.eSocket_UI_setReset(self, slot)


    def startMMI(self, slot):
        """startMMI(eSocket_UI self, int slot) -> int"""
        return _socketmmi.eSocket_UI_startMMI(self, slot)


    def stopMMI(self, slot):
        """stopMMI(eSocket_UI self, int slot) -> int"""
        return _socketmmi.eSocket_UI_stopMMI(self, slot)


    def answerMenu(self, slot, answer):
        """answerMenu(eSocket_UI self, int slot, int answer) -> int"""
        return _socketmmi.eSocket_UI_answerMenu(self, slot, answer)


    def answerEnq(self, slot, val):
        """answerEnq(eSocket_UI self, int slot, char * val) -> int"""
        return _socketmmi.eSocket_UI_answerEnq(self, slot, val)


    def cancelEnq(self, slot):
        """cancelEnq(eSocket_UI self, int slot) -> int"""
        return _socketmmi.eSocket_UI_cancelEnq(self, slot)


    def getState(self, slot):
        """getState(eSocket_UI self, int slot) -> int"""
        return _socketmmi.eSocket_UI_getState(self, slot)


    def getMMIState(self, slot):
        """getMMIState(eSocket_UI self, int slot) -> int"""
        return _socketmmi.eSocket_UI_getMMIState(self, slot)


    def numConnections(self):
        """numConnections(eSocket_UI self) -> int"""
        return _socketmmi.eSocket_UI_numConnections(self)


    def getName(self, slot):
        """getName(eSocket_UI self, int slot) -> char const *"""
        return _socketmmi.eSocket_UI_getName(self, slot)

eSocket_UI.setInit = new_instancemethod(_socketmmi.eSocket_UI_setInit, None, eSocket_UI)
eSocket_UI.setReset = new_instancemethod(_socketmmi.eSocket_UI_setReset, None, eSocket_UI)
eSocket_UI.startMMI = new_instancemethod(_socketmmi.eSocket_UI_startMMI, None, eSocket_UI)
eSocket_UI.stopMMI = new_instancemethod(_socketmmi.eSocket_UI_stopMMI, None, eSocket_UI)
eSocket_UI.answerMenu = new_instancemethod(_socketmmi.eSocket_UI_answerMenu, None, eSocket_UI)
eSocket_UI.answerEnq = new_instancemethod(_socketmmi.eSocket_UI_answerEnq, None, eSocket_UI)
eSocket_UI.cancelEnq = new_instancemethod(_socketmmi.eSocket_UI_cancelEnq, None, eSocket_UI)
eSocket_UI.getState = new_instancemethod(_socketmmi.eSocket_UI_getState, None, eSocket_UI)
eSocket_UI.getMMIState = new_instancemethod(_socketmmi.eSocket_UI_getMMIState, None, eSocket_UI)
eSocket_UI.numConnections = new_instancemethod(_socketmmi.eSocket_UI_numConnections, None, eSocket_UI)
eSocket_UI.getName = new_instancemethod(_socketmmi.eSocket_UI_getName, None, eSocket_UI)
eSocket_UI_swigregister = _socketmmi.eSocket_UI_swigregister
eSocket_UI_swigregister(eSocket_UI)

def eSocket_UI_getInstance():
    """eSocket_UI_getInstance() -> eSocket_UI"""
    return _socketmmi.eSocket_UI_getInstance()



