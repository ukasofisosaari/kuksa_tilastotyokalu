#!/usr/bin/env python3
#-*- coding: utf-8 -*-
""" Module for test statistics calculator. Only for test purposes"""

from statistics_calculator_base import StatisticsCalculatorBase


class TestStatisticsCalculator(StatisticsCalculatorBase):
    """
    Test Statistics class
    """
    def __init__(self):
        StatisticsCalculatorBase.__init__(self, "Test Statistics Calculator",
                                          "plugins/test_statistics_calculator/"
                                          "TestStatisticsCalculator.cfg")

    def calculate_statistics(self, parameters=None):
        print("This is a test class")


def register_calculator_plugin():
    """Module method for registering plugin"""
    return TestStatisticsCalculator
