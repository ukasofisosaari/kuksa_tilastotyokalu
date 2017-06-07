#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
helloqt.py
PyQt5 で Hello, world!
"""

import sys


from mainWindow import HelloWorld
from PyQt5 import QtWidgets

def main():
    app = QtWidgets.QApplication(sys.argv)

    hello_world = HelloWorld()
    hello_world.show()
    app.exec_()

if __name__ == '__main__':
    main()