#!/usr/bin/env python3
#-*- coding: utf-8 -*-


from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QListView
from PyQt5.QtGui import QStandardItemModel, QStandardItem



class GUIStatisticsSelection(QWidget):
    def __init__(self, parent=None):
        super(GUIStatisticsSelection, self).__init__(parent)

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
        pass








