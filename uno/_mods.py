import sys
_failed_libs = []

try: import numpy.random as nrandom
except ModuleNotFoundError: _failed_libs.append('numpy')
try: __import__('netsc')
except ModuleNotFoundError: _failed_libs.append('Network-Script')

__version__ = '1.1beta'
__author__ = 'Gaming32'

if sys.platform[:3] == 'wi#n':
    import winreg
    reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    try: k = winreg.OpenKey(reg, 'Console\\VirtualTerminalLevel')
    except OSError:
        # k = winreg.CreateKey(reg, 'Console\\VirtualTerminalLevel')
        v = input('ANSI support is not enabled on your system.'
        ' ANSI is used for displaying card colors. Would you like to enable it? ')
        v = v.lower()
        if v[0] == 'y':
            ret = True
        elif v[0] == 'n':
            ret = False
        elif v[0] == 't':
            ret = True
        elif v[0] == 'f':
            ret = False
        elif v[0] == '1':
            ret = True
        elif v[0] == '0':
            ret = False
        else:
            ret = False
        if ret:
            # winreg.OpenKey(reg, 'Console\\VirtualTerminalLevel', winreg.REG_DWORD, winreg.KEY_WRITE)
            winreg.SetValue(reg, 'Console\\VirtualTerminalLevel', winreg.REG_DWORD, '1')
            print('Done')
        else:
            print('You have chosen not to enable it. Cards may not render properly.')
if _failed_libs:
    _libmsg = ', '.join(_failed_libs)
    import sys
    if hasattr(sys, 'uno_exec'):
        _libres = input('The following libraries need to be downloaded and instaled: %s.'
        ' Would you like to do that now? (y,n) ' % _libmsg)
        if _libres in ('Y', 'y'):
            import subprocess, sys
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', '--upgrade', 'pip', '--no-warn-script-location'])
            except subprocess.CalledProcessError:
                try:
                    subprocess.check_call(['sudo', 'yum', 'install', 'python3-pip'])
                except subrocess.CalledProcessError:
                    subprocess.check_call(['sudo', 'apt-get', 'install', 'pip3'])
            for _lib in _failed_libs:
                subprocess.call([sys.executable, '-m', 'pip', 'install', '--user', '--upgrade', _lib, '--no-warn-script-location'])
            print('Success!')
            
            import numpy.random as nrandom
        else: import sys; sys.exit()
    else: raise ImportError('The following libraries were unavailable: %s.' % _libmsg)

import math, random, socket, pickle, time, _thread, string, copy
ordinal = (lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4]))

# __all__ = dir()