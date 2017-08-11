#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from StatisticsCalculatorBase import StatisticsCalculatorBase


class TestStatisticsCalculator(StatisticsCalculatorBase):
    """
    Test Statistics class
    """
    def __init__(self):
        StatisticsCalculatorBase.__init__(self, "Test Statistics Calculator", "plugins/TestStatisticsCalculator/TestStatisticsCalculator.cfg")

    def calculate_statistics(self, parameters=[]):
        print("This is a test class")


def registerCalculatorPlugin():
    return TestStatisticsCalculator