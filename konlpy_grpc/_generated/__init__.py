import os
import sys


_TOUCHED = False
if not _TOUCHED:
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    _TOUCHED = True
