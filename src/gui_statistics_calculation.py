#!/usr/bin/env python3
#-*- coding: utf-8 -*-
""" Module for statistics calculation side of the ui"""

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QFileDialog


class GUIStatisticsCalculation(QWidget):
    """ Right side of UI, ie. the statistics calculation settings and parameters."""
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self._main_layout = QVBoxLayout()
        self._label = QLabel("Valitse tilastolaskin")
        self._main_layout.addWidget(self._label)
        self.setLayout(self._main_layout)
        self._load_file_btn = None
        self.calculate_btn = None
        self._excel_file_name = ""

    def calculator_selected(self, calculator_params, calculator_name, calculator_desc):
        """ when calculator has been selected, this willc reate ui for for the calculation side """
        while self._main_layout.count() > 0:
            self._main_layout.itemAt(0).widget().setParent(None)

        title = QLabel(calculator_name)
        self._main_layout.addWidget(title)
        desc = QLabel(calculator_desc)
        self._main_layout.addWidget(desc)
        self._load_file_btn = QPushButton("Lataa excel tiedosto")
        self._load_file_btn.clicked.connect(self._load_file)
        self._main_layout.addWidget(self._load_file_btn)


        self.calculate_btn = QPushButton("Laske tilasto")
        self.calculate_btn.setEnabled(False)
        self._main_layout.addWidget(self.calculate_btn)


    def _load_file(self):
        """Method that is called when load file button is pushed"""
        self._excel_file_name = QFileDialog.getOpenFileName()[0]
        print(self._excel_file_name)
        filename = QLabel(self._excel_file_name)
        self._main_layout.addWidget(filename)
        self.calculate_btn.setEnabled(True)

    def get_excel_file(self):
        """ Method for returning selected excel"""
        return self._excel_file_name
