#!/usr/bin/env python3
"""! @brief Program to handle the UI."""
##
# @file databaseSetup.py
#
# @brief Program to handle the UI
#
# @section author_doxygen_example Author(s)
# - Created by Saharsh Bansal on 30/08/2024.
# - Modified by Saharsh Bansal on 1/09/2024.
#
import sys
import csv
import pandas as pd
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox, QListWidget, QWidget, QListWidgetItem, QGridLayout, QPushButton
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from database_ui import Ui_Database
import time

sys.path.append('../')
from ICD import databaseICD
database_file = "data.csv"

class qtGUI(QMainWindow, Ui_Database):
    
    def __init__(self, parent=None):
        """! Initialize the UI"""
        
        super().__init__(parent)
        self.data_dictionary = pd.DataFrame()
        self.list_disp_count=0
        self.mission_started=0
        self.setupUi(self)
        self.setupWidgets()
        self._translate = QtCore.QCoreApplication.translate
        self.sent_list=[]
        self.mission_loaded = 0
        self.payload_loaded = 0
        
    def setupWidgets(self):
        """! Initial setup of widgets"""
        
        print("Inside setup Widgets")
        self.load_database()
        self.setup_mission_id(self.payloadMissionCombo)
        self.setup_mission_id(self.databaseIDCombo)
        self.MissionRetriveButton.clicked.connect(self.loadData)
        self.payloadMissionButton.clicked.connect(self.loadPayload)
        self.logProgress.setValue(0)
        self.payloadProgress.setValue(0)
        self.missionDownloadButton.clicked.connect(self.download_logs)
        self.payloadDownloadButton.clicked.connect(self.download_payload)
        {}
        
    def load_database(self):
        """! Loading of the database which for this project is simply a csv file with pre loaded data"""
        
        file = open(database_file)
        csvreader = csv.reader(file)
        for index, row in enumerate(csvreader):
            if index == 0:
                continue
            self.data_dictionary = self.data_dictionary.append(pd.Series({'id': row[0], 'drones': row[1], 'datetime': row[2], 'length': row[3], 'freq': row[4], 'payload': row[5]}), ignore_index = True)
            
    def setup_mission_id(self, combo):
        """! Updates the list of mission ids in database on the UI
        
        @param combo The combo box on which the list needs to be updated 
        
        """
        
        combo.addItems(self.data_dictionary['id'].tolist())
        
    def loadData(self):
        """! Display base data parameters to the user to be able to choose if the log file needs to be downloaded"""
        
        self.mission_loaded = 1
        index = self.databaseIDCombo.currentIndex()
        if index == 0:
            self.detailsTable.item(0, 1).setText('')
            self.detailsTable.item(1, 1).setText('')
            self.detailsTable.item(2, 1).setText('')
            self.detailsTable.item(3, 1).setText('')
            self.detailsTable.item(4, 1).setText('')
        else:    
            index=index-1
            self.detailsTable.item(0, 1).setText(self.data_dictionary['id'][index])
            self.detailsTable.item(1, 1).setText(self.data_dictionary['drones'][index])
            self.detailsTable.item(2, 1).setText(self.data_dictionary['datetime'][index])
            self.detailsTable.item(3, 1).setText(self.data_dictionary['length'][index])
            self.detailsTable.item(4, 1).setText(self.data_dictionary['freq'][index])
        
    def loadPayload(self):
        """! Display list of payload files in the mission selected for user to choose from"""
        
        self.payload_loaded = 1
        index = self.payloadMissionCombo.currentIndex()
        self.payloadList.clear()
        if index == 0:
            return
        index = index-1
        list_images = self.data_dictionary['payload'][index].split(";")
        for i in list_images:
            self.payloadList.addItem(i)
            
    def download_logs(self):
        """! Download log files on local machine with selected timeseries. Performing basic checks beforehand to avoid error scenarios"""
        
        self.logProgress.setValue(0)
        if self.mission_loaded == 0:
            QMessageBox(QMessageBox.Information, "Error",
                            "No mission selected").exec()
            return
        try:
            start_log = int(self.StartTimeEdit.text())
        except:
            QMessageBox(QMessageBox.Information, "Error",
                            "No valid start time provided").exec()
            return
        try:
            end_log = int(self.EndTimeEdit.text())
        except:
            QMessageBox(QMessageBox.Information, "Error",
                            "No valid end time provided").exec()
            return
        if end_log<start_log:
            QMessageBox(QMessageBox.Information, "Error",
                            "End time less than start time").exec()
            return
        start = time.time()
        while time.time()-start < 0.5:
            {}
        self.logProgress.setValue(100)
        
    def download_payload(self):
        """! Download selected payload. Performing basic checks beforehand to avoid error scenarios"""
        
        self.payloadProgress.setValue(0)
        if self.payloadList.currentRow()==-1:
            QMessageBox(QMessageBox.Information, "Error",
                            "No File selected").exec()
            return
        start = time.time()
        while time.time()-start < 0.5:
            {}
        self.payloadProgress.setValue(100)