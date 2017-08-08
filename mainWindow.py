#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import sys
import os
import webbrowser

from PyQt5.QtWidgets import QHBoxLayout, QWidget, QFileDialog

from gui_statistics_calculation import GUIStatisticsCalculation
from gui_statistics_selection import GUIStatisticsSelection
from defs import statistics_calculator_plugins_dir

class GUIStatisticsTool(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self._plugins_available = {}
        self._loadPlugins()
        print(self._plugins_available)
        main_layout = QHBoxLayout()
        self._statistics_selection_w = GUIStatisticsSelection(self, self._plugins_available.keys())
        main_layout.addWidget(self._statistics_selection_w)


        self._statistics_calculation_w = GUIStatisticsCalculation(self)
        main_layout.addWidget(self._statistics_calculation_w)

        self._statistics_selection_w.calculator_selected.connect(self._calculatorSelected)


        self.setLayout(main_layout)
        self.setWindowTitle("Kuksa Tilastotyökalu")


    def _calculatorSelected(self, calculator_name):
        self._calculator_plugin = self._plugins_available[calculator_name]
        print(repr(self._calculator_plugin))
        name = self._calculator_plugin.getName()
        description = self._calculator_plugin.getDescription()
        params = self._calculator_plugin.return_parameters()
        self._statistics_calculation_w.calculator_selected(params, name, description)

        self._statistics_calculation_w.calculate_btn.clicked.connect(self.calculate)


    def calculate(self):
        excel_file = self._statistics_calculation_w.get_excel_file()
        self._calculator_plugin.loadExcelFile(excel_file)
        if self._calculator_plugin.calculate_statistics():
            report_file = QFileDialog.getSaveFileName(self, 'Tallenna raportti tiedosto')[0]
            print(report_file)
            self._calculator_plugin.saveReport(report_file)

            webbrowser.open(report_file+'.html')



    def _loadPlugins(self):
        # Load plugins
        sys.path.insert(0, statistics_calculator_plugins_dir)
        for f in os.listdir(statistics_calculator_plugins_dir):
            fname, ext = os.path.splitext(f)
            if ext == '.py':
                mod = __import__(fname)
                try:
                    plugin_object = mod.registerCalculatorPlugin()()
                    print(plugin_object)
                    print(plugin_object.getName())
                    print(plugin_object.getDescription())
                    print(plugin_object.return_parameters())
                    self._plugins_available[plugin_object.getName()] = plugin_object
                except AttributeError:
                    pass



