import os
import sys

sys.dont_write_bytecode = True

# Add parent directory to path
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from header_dialogs import *
from header_operations import *
from module_constants import *