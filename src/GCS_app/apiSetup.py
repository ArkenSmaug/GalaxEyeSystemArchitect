#!/usr/bin/env python3
"""! @brief Main program for the GCS API."""
##
# @file apiSetup.py
#
# @brief Handle the UI functionalities
#
# @section author_doxygen_example Author(s)
# - Created by Saharsh Bansal on 30/08/2024.
# - Modified by Saharsh Bansal on 1/09/2024.
#

import sys
from datetime import datetime
import PyQt5.QtCore as Qt
from PyQt5.QtWidgets import QMessageBox, QListWidgetItem, QWidget, QListWidgetItem, QGridLayout, QPushButton
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtGui import QColor, QBrush

from api_ui import Ui_MainWindow

## Import ICD for communication from defined library
sys.path.append('../')
from ICD import c2LinkICD, databaseICD

MAX_No_List = 13
# sys.path.insert(0, '../')


class qtGUI(QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        """! Initializing function"""
        
        super().__init__(parent)
        self.mission_started=0
        self.setupUi(self)
        self.setupWidgets()
        self._translate = Qt.QCoreApplication.translate
        self.sent_list=[]
        self.frozen_image = []
        
        # c2LinkICD.icd_test()
        
    def setupWidgets(self):
        """! Setting up the widgets on the UI"""
        
        print("Inside setup Widgets")
        self.startMissionButton.clicked.connect(self.start_mission)
        self.abortMissionButton.setEnabled(False)
        self.endMissionButton.setEnabled(False)
        self.endMissionButton.clicked.connect(self.end_mission)
        self.abortMissionButton.clicked.connect(self.abort_mission)
        self.takeImageButton.clicked.connect(self.take_image)
        self.saveImageButton.clicked.connect(self.save_image)
        
    def start_mission(self):
        """Handle mission start and double confirmation
            Done on the same button to make user interface easu for user
        """
        
        if self.mission_started == 0:
            if self.startMissionCombo.currentText() == "None":
                QMessageBox(QMessageBox.Information, "Error",
                            "No mission ID selected").exec()
            else:
                self.listUpdate("Press Again", "Log")
                # print("Press Again")
                self.mission_started = 1
                self.startMissionButton.setStyleSheet("background-color: rgb(255, 255, 0);")
                # self.startMissionButton.setText(self._translate("MainWindow", "Press Again to start"))
                self.startMissionButton.setText("Press Again to start")
                self.abortMissionButton.setEnabled(True)
                self.abortMissionButton.setText("Cancel Mission Start")
        elif self.mission_started == 1:
            self.listUpdate("Started " + self.droneIDCombo.currentText() + " Drone with mission " + self.startMissionCombo.currentText(), "Log")
            self.abortMissionButton.setEnabled(True)
            self.endMissionButton.setEnabled(True)
            print("Press Again")
            self.startMissionButton.setStyleSheet("background-color: rgb(50, 50, 50);")
            # self.startMissionButton.setText(self._translate("MainWindow", "Mission Executing"))
            self.startMissionButton.setText("Mission Executing")
            self.startMissionButton.setEnabled(False)
            self.mission_started = 2
            self.sendC2Cmd("StartDrone: " + self.droneIDCombo.currentText() + " StartMission: " + self.startMissionCombo.currentText())
            
    def end_mission(self):
        """! Handle processes to end the mission"""
        
        self.abortMissionButton.setEnabled(False)
        self.endMissionButton.setEnabled(False)
        self.startMissionButton.setEnabled(True)
        self.startMissionButton.setStyleSheet("background-color: rgb(0, 255, 0);")
        self.startMissionButton.setText(self._translate("MainWindow", "Start Mission"))
        self.listUpdate("Mission ended with " + self.endMissionCombo.currentText(), "Warning")
        self.sendC2Cmd("MissionEnd: " + self.endMissionCombo.currentText())
        self.mission_started = 0
        self.ending_data()
        
    def abort_mission(self):
        """! Handle process to abort mission midway"""
        
        self.abortMissionButton.setEnabled(False)
        self.endMissionButton.setEnabled(False)
        self.startMissionButton.setEnabled(True)
        self.startMissionButton.setStyleSheet("background-color: rgb(0, 255, 0);")
        self.startMissionButton.setText(self._translate("MainWindow", "Start Mission"))
        if self.mission_started == 1:
            self.listUpdate("Mission start cancelled", "Warning")
            self.abortMissionButton.setText("Abort Mission")
        elif self.mission_started == 2:
            self.sendC2Cmd("MissionAbort")
            self.listUpdate("Mission Aborted MidWay:: Now Hovering", "Error")
        
        self.mission_started = 0
        self.ending_data()
    
    def ending_data(self):
        """! Sending mission log gathered during the mission to the database upon mission stop"""
        
        {}
    
    def listUpdate(self, message, prio_level):
        """! Handle message prompt for User
        
        @param message the message to display on screen for the user
        @param prio_level the priority level of the message to be listed 
        """
        
        if self.listWidget.count() > MAX_No_List:
            self.listWidget.takeItem(MAX_No_List)
        
        time_stmp = datetime.now().strftime("%H:%M:%S")
        message = time_stmp+"\t"+message
        new_item = QListWidgetItem(message)
        color = self.getColorCode(prio_level)
        new_item.setForeground(color)
        self.listWidget.insertItem(0,new_item)
        
    def getColorCode(self, prio):
        """! Returning color to be applied to message
        
        @param prio Priority level of the message
        
        @return the color to be assigned to message
        """
        
        if prio == "Error":
            return Qt.Qt.red
        elif prio == "Warning":
            return Qt.Qt.darkYellow
        elif prio == "Log":
            return Qt.Qt.darkGray
        elif prio == "Info":
            return Qt.Qt.green
        else:
            return Qt.Qt.black   
        
    def sendC2Cmd(self, message):
        """! Sending the c2link command to the drone
        
        @param message the message to be sent to the drone
        """
        
        message = "Sending C2 command: " + message
        self.listUpdate(message, "Info")
        
    def receiveC2Cmd(self):
        """! Receiving data from drone over c2link
        
        @return msg the message received from the drone
        """
        
        msg=''
        {}
        return msg  
    
    def receivedPayload(self):
        """! Receive payload stream from the drone"""
        
        msg = ''
        
      
    def take_image(self):
        """! Handling the image shown on screen to save image
            Handling basic errors
        """
        
        if self.payloadCombo.currentText() == "None":
            QMessageBox(QMessageBox.Information, "Error",
                            "No payload ID selected").exec()
            self.listUpdate("No payload selected", "Error")
        else:
            if self.frozen_image:
                self.listUpdate("Previous image not saved. Discarding for new screenshot", "Warning")    
                self.frozen_image=[]
            self.freeze_image()
        
    def freeze_image(self):
        """! Freezing the image shown on preview pane and displaying it on the screenshot pane"""
        self.frozen_image.append("image")
        
        self.listUpdate("Freezing Image. Review image in screenshot section", "Log")
        
    def save_image(self):
        """! Saving the screenshot currently viewed in pane"""
        
        if self.payloadCombo.currentText() == "None":
            QMessageBox(QMessageBox.Information, "Error",
                            "No payload ID selected").exec()
            self.listUpdate("Save Error: No payload selected", "Error")
            return
        
        if self.frozen_image == []:
            QMessageBox(QMessageBox.Information, "Error",
                            "No images screenshoted").exec()
            self.listUpdate("Save Error: No images screenshoted", "Error")  
            return  
        
        image_name = self.saveImageEdit.text()
        if image_name == "":
            self.listUpdate("Save Error: File Name not defined", "Error")
            return
        
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        
        self.listUpdate(image_name + ".png Saved", "Info")  