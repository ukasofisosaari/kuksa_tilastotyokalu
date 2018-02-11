#!/usr/bin/env python3
#-*- coding: utf-8 -*-
""" Module for selecting statistics calculator"""

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QListView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSignal


class GUIStatisticsSelection(QWidget):
    """ UI class for handling calculator selection"""
    calculator_selected = pyqtSignal('QString')
    def __init__(self, parent, plugins_available):
        QWidget.__init__(self, parent)

        main_layout = QVBoxLayout()
        label = QLabel("Tilastolaskimen valinta")
        main_layout.addWidget(label)

        calculator_list_view = QListView()

        model = QStandardItemModel(calculator_list_view)

        for plugin_name in plugins_available:
            print(plugin_name)
            item = QStandardItem(plugin_name)
            model.appendRow(item)
            calculator_list_view.setModel(model)
            calculator_list_view.clicked.connect(self.on_item_changed)

        main_layout.addWidget(calculator_list_view)
        calculator_list_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setLayout(main_layout)


    def on_item_changed(self, index):
        """ SLOT called when item changes """
        plugin_name = index.data()
        self.calculator_selected.emit(plugin_name)
