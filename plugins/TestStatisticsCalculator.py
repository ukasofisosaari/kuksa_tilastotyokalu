#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from categories import StatisticsCalculatorBase


class TestStatisticsCalculator(StatisticsCalculatorBase):
    """
    Test Statistics class
    """
    def __init__(self):
        super(TestStatisticsCalculator, self).__init__("Test Statistics Calculator")

    def calculate_statistics(self, parameters=[]):
        print("This is a test class")