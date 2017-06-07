#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""

"""

import sys


from mainWindow import GUIStatisticsTool
from PyQt5 import QtWidgets

def main():
    app = QtWidgets.QApplication(sys.argv)

    hello_world = GUIStatisticsTool()
    hello_world.show()
    app.exec_()

if __name__ == '__main__':
    main()