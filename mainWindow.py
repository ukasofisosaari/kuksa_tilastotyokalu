#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from PyQt5.QtWidgets import QHBoxLayout, QWidget

from gui_statistics_calculation import GUIStatisticsCalculation
from gui_statistics_selection import GUIStatisticsSelection

class GUIStatisticsTool(QWidget):
    def __init__(self, parent=None):
        super(GUIStatisticsTool, self).__init__(parent)



        main_layout = QHBoxLayout()
        self._statistics_selection_w = GUIStatisticsSelection(self)
        main_layout.addWidget(self._statistics_selection_w)


        self._statistics_calculation_w = GUIStatisticsCalculation(self)
        main_layout.addWidget(self._statistics_calculation_w)


        self.setLayout(main_layout)
        self.setWindowTitle("Kuksa Tilastotyökalu")



