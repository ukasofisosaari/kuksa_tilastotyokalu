#!/usr/bin/env python3
#-*- coding: utf-8 -*-


from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QListView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSignal


class GUIStatisticsSelection(QWidget):

    calculator_selected = pyqtSignal('QString')
    def __init__(self, parent, plugins_available):
        QWidget.__init__(self, parent)

        main_layout = QVBoxLayout()
        label = QLabel("Tilastolaskimen valinta")
        main_layout.addWidget(label)

        list = QListView()

        model = QStandardItemModel(list)

        for plugin_name in plugins_available:
            print(plugin_name)
            item = QStandardItem(plugin_name)
            model.appendRow(item)
        list.setModel(model)
        list.clicked.connect(self._on_item_changed)

        main_layout.addWidget(list)
        list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setLayout(main_layout)


    def _on_item_changed(self, index):
        plugin_name = index.data()
        self.calculator_selected.emit(plugin_name)
