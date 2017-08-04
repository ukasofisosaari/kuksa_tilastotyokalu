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
        self._description = ''

    def getName(self):
        print("Called Get Name")
        return self._name

    def _setDescription(self, description):
        print("Called Set Description")
        self._description = description

    def getDescription(self):
        print("Called Get Description")
        return self._description

    def return_parameters(self):
        return []


    ##TODO: Insert excel file handling here
    def loadExcelFile(self, excelfile):
        print(excelfile)

    @abstractmethod
    def calculate_statistics(self, parameters=[]):
        assert(False)