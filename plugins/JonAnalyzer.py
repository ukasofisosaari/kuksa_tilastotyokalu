#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from StatisticsCalculatorBase import StatisticsCalculatorBase


class TestStatisticsCalculator(StatisticsCalculatorBase):
    """
    Test Statistics class
    """
    def __init__(self):
        StatisticsCalculatorBase.__init__(self, "Test Statistics Calculator", "plugins/JobAnalyzer/JobAnalyzer.html")

    def calculate_statistics(self, parameters=[]):
        print("This is a test class")

        #Kuva 1
        #Henkilö placeholder on <PERSONS>, pitää näyttää tältä: 'Saku', 'Tero', 'Olli'
        #Alla esimerkki datasetistä mitä pitää insertoida. PLACEHOLDER on <JOB>
        #{
		#	label: "Lippukunnanjohtajat",
        #    data: [1,0,0],
        #   backgroundColor: "rgba(63,103,126,1)",
        #    hoverBackgroundColor: "rgba(50,90,100,1)"
        #},



def registerCalculatorPlugin():
    return TestStatisticsCalculator