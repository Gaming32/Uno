import sys
sys.uno_exec = True

try: from ._main import *
except ImportError: from uno._main import *
main()