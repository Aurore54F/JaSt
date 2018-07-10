"""
    Init file for the package clustering.
"""

import sys
import os

SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


sys.path.insert(0, os.path.join(SRC_PATH, 'features'))  # To add a directory to import modules from
sys.path.insert(0, os.path.join(SRC_PATH, 'features', 'tokens2int'))
sys.path.insert(0, os.path.join(SRC_PATH, 'features', 'ngrams2int'))
sys.path.insert(0, os.path.join(SRC_PATH, 'js'))
