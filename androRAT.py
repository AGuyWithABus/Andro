# Part 1: Start of androRAT.py

#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils import *
import argparse
import sys
import platform
try:
    from pyngrok import ngrok, conf
except ImportError as e:
    print(stdOutput("error") + "\033[1mpyngrok not found")
    print(stdOutput("info") + "\033[1mRun pip3 install -r requirements.txt")
    exit()

clearDirec()

# Part 1: End of androRAT.py