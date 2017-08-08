#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QFileDialog


class GUIStatisticsCalculation(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self._main_layout = QVBoxLayout()
        self._label = QLabel("Valitse tilastolaskin")
        self._main_layout.addWidget(self._label)
        self.setLayout(self._main_layout)

    def calculator_selected(self, calculator_params, calculator_name, calculator_desc):
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
        self._excel_file_name = QFileDialog.getOpenFileName()[0]
        print(self._excel_file_name)
        filename = QLabel(self._excel_file_name)
        self._main_layout.addWidget(filename)
        self.calculate_btn.setEnabled(True)

    def get_excel_file(self):
        return self._excel_file_name


