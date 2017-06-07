#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

"""
Note that any classes inherited from StatisticsCalculatorBase must have in the same python module a function called registerCalculatorPlugin.

"""
class StatisticsCalculatorBase(object):
    __metaclass__ = ABCMeta

    def __init__(self, plugin_name):

       self._name = plugin_name

    def getName(self):
        print("Called Get Name")
        return self._name

    def _setDescription(self, description):
        self._description = description

    def getDescription(self):
        return self._description

    def loadExcelFile(self, excelfile):
        pass

    @abstractmethod
    def calculate_statistics(self, parameters=[]):
        assert(False)