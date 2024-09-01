#!/usr/bin/env python3
"""! @brief Main program for the GCS API."""
##
# @file main_api.py
#
# @brief Main program for the GCS UI
#
# @section author_doxygen_example Author(s)
# - Created by Saharsh Bansal on 30/08/2024.
# - Modified by Saharsh Bansal on 1/09/2024.
#

from PyQt5 import QtWidgets
from apiSetup import qtGUI
import sys

def main():
    """! Main Function"""
    
    app = QtWidgets.QApplication(sys.argv)
    
    mainWindow = qtGUI()
    mainWindow.show()
    
    sys.exit(app.exec())
    
if __name__ == '__main__':
    main()