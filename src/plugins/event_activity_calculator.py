#!/usr/bin/env python3
#-*- coding: utf-8 -*-
""" Module for event activity calculator"""
from statistics_calculator_base import StatisticsCalculatorBase


class EventActivityCalculator(StatisticsCalculatorBase):
    """
    Event activity calculator. Will calculate how active troops are in participitating in events
    """
    def __init__(self):
        StatisticsCalculatorBase.__init__(self, "Event Activity Calculator",
                                          "plugins/event_activity_calculator/"
                                          "EventActivityCalculator.cfg")

    def calculate_statistics(self, parameters=None):
        """Method for calculating statistics"""
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
        for group_name in group_names:
            participating_groups.add(group_name.value)

        # dicti missä lippukunnittain toisena parametrina osallistumiset ja toisessa osallistujat
        dict_participations = {}
        dict_participants = {}

        # loopataan lippukunnittain edelliset apufunktiot
        for participitating_group in participating_groups:
            dict_participations[participitating_group] = self._count_instances(
                participitating_group, group_names)
            dict_participants[participitating_group] = self._count_participant_instances(
                participitating_group, group_names, members)

        print(dict_participations)
        print('')
        print(dict_participants)

    @classmethod
    # laskentafunktio lippukuntien nimien esiintymismäärään = osallistumiset
    def _count_instances(cls, instance, excel_col):
        i = 0
        for cell in excel_col:
            if cell.value == instance:
                i += 1
        return i

    @classmethod
    # laskentafunktio lippukuntien sisällä esiintyviin jäsennumeroihin 1 per numero = osallistujat
    def _count_participant_instances(cls, instance, excel_groups, excel_members):
        participitants = set()
        for i in enumerate(excel_groups):
            if excel_groups[i].value == instance:
                participitants.add(excel_members[i].value)
        return len(participitants)


def register_calculator_plugin():
    """Module method for registering plugin"""
    return EventActivityCalculator
