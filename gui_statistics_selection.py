#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import sys
import os

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QListView
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from defs import statistics_calculator_plugins_dir



class GUIStatisticsSelection(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        main_layout = QVBoxLayout()
        label = QLabel("Tilastolaskimen valinta")
        main_layout.addWidget(label)

        list = QListView()

        model = QStandardItemModel(list)
        self._plugins_available = {}
        self._loadPlugins()
        for plugin_name in self._plugins_available.keys():
            print(plugin_name)
            item = QStandardItem(plugin_name)
            model.appendRow(item)
        list.setModel(model)
        main_layout.addWidget(list)

        self.setLayout(main_layout)

    def _loadPlugins(self):
        # Load plugins
        sys.path.insert(0, statistics_calculator_plugins_dir)
        for f in os.listdir(statistics_calculator_plugins_dir):
            fname, ext = os.path.splitext(f)
            if ext == '.py':
                mod = __import__(fname)
                try:
                    print(fname)
                    plugin_class = mod.registerCalculatorPlugin()()
                    print(plugin_class)
                    print(plugin_class.getName())
                    self._plugins_available[plugin_class.getName()] = plugin_class
                except AttributeError:
                    pass








