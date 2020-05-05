import sys
_failed_libs = []

try: import numpy.random as nrandom
except ModuleNotFoundError: _failed_libs.append('numpy')
try: __import__('netsc')
except ModuleNotFoundError: _failed_libs.append('Network-Script')
try: from roman import int_to_roman
except ModuleNotFoundError: _failed_libs.append('Roman-Numerals-Simple')
try: import colorama
except ModuleNotFoundError: _failed_libs.append('colorama')

if sys.platform[:3] == 'wi#n':
    import winreg
    reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    set_to = True
    try: k = winreg.OpenKeyEx(reg, 'Console\\VirtualTerminalLevel')
    except OSError: set_to = False
    else:
        value_, type_ = winreg.QueryValueEx(reg, 'Console\\VirtualTerminalLevel')
        if not int(value_): set_to = False
    if not set_to:
        # k = winreg.CreateKey(reg, 'Console\\VirtualTerminalLevel')
        v = input('ANSI support is not enabled on your system.'
        ' ANSI is used for displaying card colors. Would you like to enable it? ')
        v = v.lower()
        if v[0] == 'y':
            ret = True
        elif v[0] == 't':
            ret = True
        elif v[0] == '1':
            ret = True
        else:
            ret = False
        if ret:
            # winreg.OpenKey(reg, 'Console\\VirtualTerminalLevel', winreg.REG_DWORD, winreg.KEY_WRITE)
            winreg.SetValueEx(reg, 'Console\\VirtualTerminalLevel', winreg.REG_DWORD, '1')
            print('Done')
        else:
            print('You have chosen not to enable it. Cards may not render properly.')
if _failed_libs:
    _libmsg = ', '.join(_failed_libs)
    import sys
    sys.uno_exec = True
    if hasattr(sys, 'uno_exec'):
        _libres = input('The following libraries need to be downloaded and instaled: %s.'
        ' Would you like to do that now? (y,n) ' % _libmsg)
        if _libres in ('Y', 'y'):
            import subprocess, sys
            subprocess.call([sys.executable, '-m', 'ensurepip', '--upgrade'])
            subprocess.call([sys.executable, '-m', 'pip', 'install', '--user', '--upgrade', *_failed_libs, '--no-warn-script-location'])
            print('Success!')
            
            import numpy.random as nrandom
            from roman import int_to_roman
            import colorama
        else: import sys; sys.exit()
    else: raise ImportError('The following libraries were unavailable: %s.' % _libmsg)

import math, random, socket, pickle, time, _thread, string, copy
ordinal = (lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4]))

# __all__ = dir()