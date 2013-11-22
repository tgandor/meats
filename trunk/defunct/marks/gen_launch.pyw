# replaces a batch file with the contents:
# c:\Python26\python c:\meats\marks\generator.py
# allowing to run the window without terminal

# (customize) the path to generator: 
prog_dir = r'c:\meats\marks'

import sys
sys.path.append(prog_dir)
import os
execfile(os.path.join(prog_dir,'generator.py'))
