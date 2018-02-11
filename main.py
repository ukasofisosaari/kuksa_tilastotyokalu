#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
Main module
"""

import sys

from PyQt5 import QtWidgets

from main_window import GUIStatisticsTool

def main():
    """ Main function for program"""
    app = QtWidgets.QApplication(sys.argv)

    hello_world = GUIStatisticsTool()
    hello_world.show()
    app.exec_()

if __name__ == '__main__':
    main()
