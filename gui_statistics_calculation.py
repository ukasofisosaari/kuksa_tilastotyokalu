#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel


class GUIStatisticsCalculation(QWidget):
    def __init__(self, parent=None):
        super(GUIStatisticsCalculation, self).__init__(parent)

        main_layout = QVBoxLayout()
        label = QLabel("Tilastolaskimen parametrit")
        main_layout.addWidget(label)


        self.setLayout(main_layout)
