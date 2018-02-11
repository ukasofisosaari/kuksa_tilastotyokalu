#!/usr/bin/env python3
#-*- coding: utf-8 -*-

""" Module for main gui """
import sys
import os
import webbrowser

from PyQt5.QtWidgets import QHBoxLayout, QWidget, QFileDialog

from gui_statistics_calculation import GUIStatisticsCalculation
from gui_statistics_selection import GUIStatisticsSelection
from defs import STATISTICS_CALCULATOR_PLUGINS_DIR

class GUIStatisticsTool(QWidget):
    """ Main gui class """
    def __init__(self, parent=None):
        """ Init """
        QWidget.__init__(self, parent)
        self._calculator_plugin = None
        self._plugins_available = {}
        self._load_plugins()
        print(self._plugins_available)
        main_layout = QHBoxLayout()
        self._statistics_selection_w = GUIStatisticsSelection(self, self._plugins_available.keys())
        main_layout.addWidget(self._statistics_selection_w)


        self._statistics_calculation_w = GUIStatisticsCalculation(self)
        main_layout.addWidget(self._statistics_calculation_w)

        self._statistics_selection_w.calculator_selected.connect(self._calculator_selected)


        self.setLayout(main_layout)
        self.setWindowTitle("Kuksa Tilastotyökalu")


    def _calculator_selected(self, calculator_name):
        """ Private function, called when calculator has been selected"""
        self._calculator_plugin = self._plugins_available[calculator_name]
        print(repr(self._calculator_plugin))
        name = self._calculator_plugin.get_name()
        description = self._calculator_plugin.get_description()
        params = self._calculator_plugin.return_parameters()
        self._statistics_calculation_w.calculator_selected(params, name, description)

        self._statistics_calculation_w.calculate_btn.clicked.connect(self._calculate)


    def _calculate(self):
        """ Private function, connected to calculate button. """
        excel_file = self._statistics_calculation_w.get_excel_file()
        self._calculator_plugin.load_excel_file(excel_file)
        if self._calculator_plugin.calculate_statistics():
            report_file = QFileDialog.getSaveFileName(self, 'Tallenna raportti tiedosto')[0]
            print(report_file)
            self._calculator_plugin.saveReport(report_file)

            webbrowser.open(report_file+'.html')



    def _load_plugins(self):
        """ Loads all available plugins. Private function """
        # Load plugins
        sys.path.insert(0, STATISTICS_CALCULATOR_PLUGINS_DIR)
        for file in os.listdir(STATISTICS_CALCULATOR_PLUGINS_DIR):
            fname, ext = os.path.splitext(file)
            if ext == '.py':
                mod = __import__(fname)
                print(mod)
                print(fname)
                plugin_register_function = mod.register_calculator_plugin()
                if plugin_register_function:
                    plugin_object = plugin_register_function()
                    print(plugin_object)
                    print(plugin_object.get_name())
                    print(plugin_object.get_description())
                    print(plugin_object.return_parameters())
                    self._plugins_available[plugin_object.get_name()] = plugin_object
