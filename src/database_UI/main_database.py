#!/usr/bin/env python3
"""! @brief Main program for the database UI."""
##
# @file main_database.py
#
# @brief Main program for the database UI
#
# @section author_doxygen_example Author(s)
# - Created by Saharsh Bansal on 30/08/2024.
# - Modified by Saharsh Bansal on 1/09/2024.
#

from PyQt5 import QtWidgets
from databaseSetup import qtGUI
import sys

def main():
    """! Main Function"""
    
    app = QtWidgets.QApplication(sys.argv)
    
    mainWindow = qtGUI()
    mainWindow.show()
    
    sys.exit(app.exec())
    
if __name__ == '__main__':
    main()