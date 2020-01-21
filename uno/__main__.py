import sys
sys.uno_exec = True

try: from .main import *
except ImportError: from uno.main import *
main()