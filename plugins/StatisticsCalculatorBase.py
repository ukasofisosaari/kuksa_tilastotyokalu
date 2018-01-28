#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import xlrd
import configparser
"""
Note that any classes inherited from StatisticsCalculatorBase must have in the same python module a function called registerCalculatorPlugin.

"""
class StatisticsCalculatorBase(object):
    __metaclass__ = ABCMeta

    def __init__(self, plugin_name, config_file):

        self._name = plugin_name
        self._description = ''
        self._config = configparser.ConfigParser()
        self._config.read(config_file)
        report_template = self._config.get('General', 'report_template')

        with open(report_template, 'r') as template_file:
            self._template_file_content = template_file.read()

        #Holds raw data
        self._data = ''

    def checkFirstRow(self, labelIndexes, listOfFirstRow):
        i=0
        for label in listOfFirstRow:
            try:
                labelIndexes[label] = i
                i += 1
            except KeyError:
                raise Exception("Problem with label: " + label)



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

    def _replacePlaceholder(self, placeholder, data):
        self._template_file_content = self._template_file_content.replace(placeholder, data)

    def saveReport(self, report_location):
        with open(report_location+'.html', "w") as report_file:
            report_file.write(self._template_file_content)
        self._template_file_content=''
        with open(report_location+'.csv', "w") as data_file:
            data_file.write(self._data)
        self._data=''


    ##TODO: Insert excel file handling here
    def loadExcelFile(self, excelfile):
        # open the excel
        # path = "jaakonsamoojat.xlsx"
        print("Loading file {0} into xlrd".format(excelfile))
        self._book = xlrd.open_workbook(excelfile)

    @abstractmethod
    def calculate_statistics(self, parameters=[]):
        assert(False)

def registerCalculatorPlugin():
    return None