#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from StatisticsCalculatorBase import StatisticsCalculatorBase


class EventActivityCalculator(StatisticsCalculatorBase):
    """
    Test Statistics class
    """
    def __init__(self):
        StatisticsCalculatorBase.__init__(self, "Test Statistics Calculator", "plugins/TestStatisticsCalculator/TestStatisticsCalculator.cfg")

    def calculate_statistics(self, parameters=[]):
        print("This is a test class")



        # Kuksa dependent indices
        vertical_offset = 4  # number of non data rows
        member_names_column = 0
        members_column = 1  # -1 w.r.t. excel index
        group_column = 2

        # luetaan excel, lippukuntien nimet sisältävä sarake ja jäsennumerot sisältävä tiedosto

        sheet = self._book.sheet_by_index(0)
        group_names = sheet.col_slice(colx=group_column,
                                      start_rowx=vertical_offset,
                                      end_rowx=sheet.nrows)
        members = sheet.col_slice(colx=members_column,
                                  start_rowx=vertical_offset,
                                  end_rowx=sheet.nrows)

        # muodostetaan uniikki setti lippukuntien nimistä
        participating_groups = set()
        for x in group_names:
            participating_groups.add(x.value)

        # dicti missä lippukunnittain toisena parametrina osallistumiset ja toisessa osallistujat
        dict_participations = {}
        dict_participants = {}

        # laskentafunktio lippukuntien nimien esiintymismäärään = osallistumiset
        def count_instances(instance, excel_col):
            c = 0
            for x in excel_col:
                if x.value == instance:
                    c += 1
            return c

        # laskentafunktio lippukuntien sisällä esiintyviin jäsennumeroihin 1 per numero = osallistujat
        def count_participant_instances(instance, excel_groups, excel_members):
            p = set()
            for i in range(len(excel_groups)):
                if excel_groups[i].value == instance:
                    p.add(excel_members[i].value)
            return len(p)

        # loopataan lippukunnittain edelliset apufunktiot
        for x in participating_groups:
            dict_participations[x] = count_instances(x, group_names)
            dict_participants[x] = count_participant_instances(x, group_names, members)

        print(dict_participations)
        print('')
        print(dict_participants)


def registerCalculatorPlugin():
    return EventActivityCalculator