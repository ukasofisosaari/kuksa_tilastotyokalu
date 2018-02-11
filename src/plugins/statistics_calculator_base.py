#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
Note that any classes inherited from StatisticsCalculatorBase must
have in the same python module a function called register_calculator_plugin.

"""

from abc import ABCMeta, abstractmethod
import configparser

import xlrd

class StatisticsCalculatorBase(object):
    """ Base class for statistics calculators"""
    __metaclass__ = ABCMeta
    def __init__(self, plugin_name, config_file):

        self._name = plugin_name
        self._book = None
        self._description = ''
        self._config = configparser.ConfigParser()
        self._config.read(config_file)
        print(config_file)
        print(self._config)
        report_template = self._config.get('General', 'report_template')

        with open(report_template, 'r') as template_file:
            self._template_file_content = template_file.read()

        #Holds raw data
        self._data = ''

    @classmethod
    def check_first_row(cls, label_indexes, list_of_first_row):
        """ for checking that first row matches"""
        i = 0
        for label in list_of_first_row:
            try:
                label_indexes[label] = i
                i += 1
            except KeyError:
                raise Exception("Problem with label: " + label)



    def get_name(self):
        """ Returns name of the calculator"""
        print("Called Get Name")
        return self._name

    def _set_description(self, description):
        """ Returns name of the calculator"""
        print("Called Set Description")
        self._description = description

    def get_description(self):
        """ Returns name of the calculator"""
        print("Called Get Description")
        return self._description

    @classmethod
    def return_parameters(cls):
        """ Returns calculator params, override in child class if using parameters"""
        return []

    def _replace_placeholder(self, placeholder, data):
        """ Replaces placeholders in report"""
        self._template_file_content = self._template_file_content.replace(placeholder, data)

    def save_report(self, report_location):
        """ Method for saving report"""
        with open(report_location+'.html', "w") as report_file:
            report_file.write(self._template_file_content)
        self._template_file_content = ''
        with open(report_location+'.csv', "w") as data_file:
            data_file.write(self._data)
        self._data = ''

    def load_excel_file(self, excelfile):
        """Loads excel file using xlrd """
        # open the excel
        # path = "jaakonsamoojat.xlsx"
        print("Loading file {0} into xlrd".format(excelfile))
        self._book = xlrd.open_workbook(excelfile)

    @abstractmethod
    def calculate_statistics(self, parameters=None):
        """Abstrac method"""
        assert()

def register_calculator_plugin():
    """Module method for registering plugin"""
    return None
