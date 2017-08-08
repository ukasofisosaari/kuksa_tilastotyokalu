#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from StatisticsCalculatorBase import StatisticsCalculatorBase


class ZipCodeHistogram(StatisticsCalculatorBase):
    """
    Test Statistics class
    """
    def __init__(self):
        StatisticsCalculatorBase.__init__(self, "Zip Code Histogram")

    def calculate_statistics(self, parameters=[]):
        print("Lets start calculating")
        # Kuksa dependent indices
        vertical_offset = 4  # number of non data rows
        address_column = 2  # -1 w.r.t. excel index
        birthdate_column = 3
        # Kuksa dependent parse orders
        # 0 for LHS and 1 for RHS
        addresses_parse = [[", ", 1], [" ", 0]]
        birthdates_parse = [[".", 1], [".", 1]]
        # Desired dependent output variables
        age_bins = [15, 22]  # this means three bins: x <= 15, 15 < x <= 22, x > 22
        thisyear = 2017

        # get the adresses and birhtdates
        sheet = self._book.sheet_by_index(0)
        addresses = sheet.col_slice(colx=address_column,
                                    start_rowx=vertical_offset,
                                    end_rowx=sheet.nrows)
        birthdates = sheet.col_slice(colx=birthdate_column,
                                     start_rowx=vertical_offset,
                                     end_rowx=sheet.nrows)
        # for two parent members, there is extra 'None' cell for these members -> remove
        if len(addresses) != len(birthdates):
            raise NameError('Length of addresses and birthdates not equal.')
        i = 0
        while i in range(len(addresses)):
            if addresses[i].value is None and birthdates[i].value is None:
                del addresses[i]
                del birthdates[i]
            else:
                i = i + 1

        addresses = self._parsefromexcel(addresses, addresses_parse)
        birthdates = self._parsefromexcel(birthdates, birthdates_parse)

        # convert dates to ages
        ages = []
        for i in range(len(birthdates)):
            year = int(birthdates[i])
            ages.append(thisyear - year)

        zips, hist = self._zip_histogram(addresses, ages, age_bins)
        histogram = []
        for i in range(len(zips)):
            histogram.append([zips[i], hist[i]])

        sorted_histogram = sorted(histogram, key=lambda zipcode: zipcode[0])

        for i in range(len(sorted_histogram)):
            print(sorted_histogram[i])

    # ----------------------------------------------------------------------
    def _initialize_age_bins(self, age_bins):
        """
        Creates a list with 0 zeros where len(out) = len(age_bins)+1.
        """
        out = []
        for i in range(len(age_bins) + 1):
            out.append(0)
        return out

    # ----------------------------------------------------------------------
    def _update_age_bins(self, age_bins, age_bins_limits, age):
        """
        Adds one (int(1)) representing age to correct bin in age_bins w.r.t. age_bins_limits
        """
        out = age_bins
        check_added = False
        for i in range(len(age_bins_limits)):
            if age <= age_bins_limits[i] and not check_added:
                out[i] = out[i] + 1
                check_added = True
        if not check_added:
            out[len(out) - 1] = out[len(out) - 1] + 1
        return out

    # ----------------------------------------------------------------------
    def _zip_histogram(self, zips, ages, age_bins):
        """
        This function computes the histogram of the given zip codes w.r.t.
        age limit bins.
        """

        # output allocation
        outzips = []
        outages = []

        for i in range(len(zips)):
            if zips[i] in outzips:
                # only update outages
                idx = outzips.index(zips[i])
                outages[idx] = self._update_age_bins(outages[idx], age_bins, ages[i])
            else:
                # create new entries
                outzips.append(zips[i])
                outages.append(self._update_age_bins(self._initialize_age_bins(age_bins), age_bins, ages[i]))

        return outzips, outages

    def _parsefromexcel(self, s, parseorder):
        """
        Parse strings in list to single list of desired part w.r.t. parseorder.
        """

        out = s

        for i in range(len(s)):
            si = s[i].value
            for j in range(len(parseorder)):
                parsecommands = parseorder[j]
                parsestring = parsecommands[0]
                parseside = parsecommands[1]
                sp = si.split(parsestring, 1)
                si = sp[parseside]
            out[i] = si

        return out


def registerCalculatorPlugin():
    return ZipCodeHistogram