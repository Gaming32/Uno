_failed_libs = []

try: import numpy.random as nrandom
except ImportError: _failed_libs.append('numpy')

if _failed_libs:
    _libmsg = ', '.join(_failed_libs)
    import sys
    if hasattr(sys, 'uno_exec'):
        _libres = input('The following libraries need to be downloaded and instaled: %s.'
        ' Would you like to do that now? (y,n) ' % _libmsg)
        if _libres in ('Y', 'y'):
            import subprocess, sys
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', '--upgrade', 'pip'])
            for _lib in _failed_libs:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', _lib])
            print('Success!')
            
            import numpy.random as nrandom
        else: import sys; sys.exit()
    else: raise ImportError('The following libraries were unavailable: %s.' % _libmsg)

import math, random, socket, pickle, time, _thread, string, copy
_ordinal = (lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4]))

__all__ = dir()