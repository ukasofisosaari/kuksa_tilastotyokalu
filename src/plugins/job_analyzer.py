#!/usr/bin/env python3
#-*- coding: utf-8 -*-
""" Pesti analysaattori moduuli"""
import datetime
from datetime import date
import json
import xlrd

from statistics_calculator_base import StatisticsCalculatorBase

DISCTRICT_JOBS = ('Lippukunnanjohtaja',
                  'Ohjelmajohtaja',
                  'Piirin lpk-postin saaja',
                  'Pestijohtaja',
                  'Joku testi joka varmasti puuttuu')



class JobAnalyzer(StatisticsCalculatorBase):
    """
    This calculator computes the persons who currently have posts
    and the duration of the active posts.
    """
    def __init__(self):
        """Init"""
        StatisticsCalculatorBase.__init__(self, "Pestitesti",
                                          "plugins/job_analyzer/JobAnalyzer.cfg")


    def calculate_statistics(self, parameters=None):
        """Metodi joka laskee statistiikan."""
        print("This calculator computes the persons who currently have \
        posts and the duration of the active posts.")

        # Kuksa dependent indices
        vertical_offset = 1  # number of non data rows
        member_names_column = 0
        members_column = 1  # -1 w.r.t. excel index
        job_begindate_column = 5
        job_enddate_column = 6
        job_name_column = 4
        # Kuksa dependent parse orders
        # 0 for LHS and 1 for RHS
        # dates_parse = [[".", 1], [".", 1]]

        # Desired dependent output variables
        # today as date
        now = datetime.datetime.now()
        today = date(now.year, now.month, now.day)
        # district required posts


        # get the member IDs in the post list and make two versions of it: unique and values
        sheet = self._book.sheet_by_index(0)
        members_excel = sheet.col_slice(colx=members_column,
                                        start_rowx=vertical_offset,
                                        end_rowx=sheet.nrows)
        members_key = set()
        members = []
        for member in members_excel:
            members.append(member.value)
            members_key.add(member.value)


        # get all the begin and end dates of posts, convert to years
        begindates_excel = sheet.col_slice(colx=job_begindate_column,
                                           start_rowx=vertical_offset,
                                           end_rowx=sheet.nrows)
        enddates_excel = sheet.col_slice(colx=job_enddate_column,
                                         start_rowx=vertical_offset,
                                         end_rowx=sheet.nrows)
        # durations of the posts if they were to be held until today
        durations = self._years_from_to_day_from_excel(begindates_excel, today, self._book.datemode)

        # get the names of the posts for output
        job_names = sheet.col_slice(colx=job_name_column,
                                    start_rowx=vertical_offset,
                                    end_rowx=sheet.nrows)
        # get the names of the members for output
        member_names = sheet.col_slice(colx=member_names_column,
                                       start_rowx=vertical_offset,
                                       end_rowx=sheet.nrows)
        # create a dictionary of the keys and names
        dict_key_name = {}
        for i in enumerate(members_excel):
            dict_key_name[members_excel[i].value] = member_names[i].value

        # for each member, search all active posts and calculate their duration in years
        # creates a dict that has second dict embedded; outer includes members' names and
        # inner posts and durations
        active_jobs = {}
        for member_key in members_key:
            indices = [i for i, y in enumerate(members) if y == member_key]
            member_jobs = {}
            has_jobs = False
            name = ''
            for j in indices:
                if enddates_excel[j].value == '':
                    has_jobs = True
                    name = member_names[j].value
                    member_jobs[job_names[j].value] = round(durations[j], 1)
                    # print(member_names[j].value, round(durations[j],1), job_names[j].value)
            if has_jobs:
                active_jobs[name] = member_jobs

        self._form_jobs_array(active_jobs)

        print(active_jobs)

        # ** check the list of posts that are required by the scout district
        required_jobs_covered = []
        required_jobs_missing = []
        # loop for covered posts
        for i in enumerate(DISCTRICT_JOBS):
            for key in active_jobs:
                if DISCTRICT_JOBS[i] in active_jobs[key]:
                    required_jobs_covered.append(DISCTRICT_JOBS[i])
        # loop for missing posts
        for i in enumerate(DISCTRICT_JOBS):
            if DISCTRICT_JOBS[i] not in required_jobs_covered:
                required_jobs_missing.append(DISCTRICT_JOBS[i])

        print('Seuraavat pestit on hoidossa:')
        print(required_jobs_covered)
        print('Nämä pestit puuttuvat:')
        print(required_jobs_missing)

        # ** scout with the most duty years
        # for each member, calculate the total of the years of their posts
        # (Note: the use of dictionary here turned out to be not used, though
        # still left for possible further use.)
        member_years_of_duty = {}
        max_years = 0
        max_years_member = ''
        for member_key in members_key:
            indices = [i for i, y in enumerate(members) if y == member_key]
            years_of_duty = 0
            for j in indices:
                years_of_duty += durations[j]
            member_years_of_duty[dict_key_name[member_key]] = round(years_of_duty, 1)
            # check if new candidate has more years than the previous candidate
            if years_of_duty > max_years:
                # update candidate
                max_years_member = dict_key_name[member_key]
                max_years = round(years_of_duty, 1)
        max_years_member = (max_years_member, max_years)

        print('Kaikkien aikojen lippukuntalainen:')
        print(max_years_member)

        #self._replace_placeholder("<ZIPS>", zips_s)

        return active_jobs, max_years_member, required_jobs_covered, required_jobs_missing

    @classmethod
    def _years_from_to_day_from_excel(cls, dates, today, datemode):
        """
        Converts the Julian date of excel and calculates how many days it is from today.
        """
        out = []
        for i in dates:
            jnd_date = xlrd.xldate_as_tuple(i.value, datemode)
            jnd_date_datetime = date(jnd_date[0], jnd_date[1], jnd_date[2])
            delta = today - jnd_date_datetime
            out.append(delta.days / 365)
        return out

    @classmethod
    def _get_all_job_types(cls, jobs):
        """Get all job types"""
        job_types = []
        for person in jobs.keys():
            for pesti in jobs[person].keys():
                if pesti not in job_types:
                    job_types.append(pesti)

        return job_types

    def _form_jobs_array(self, jobs):
        """form array for report"""
        job_types = self._get_all_job_types(jobs)
        n_persons = len(jobs.keys())
        outputdict = {}

        for i in enumerate(job_types):
            job_type_dict = {}
            job_type_dict['label'] = job_types[i]
            job_type_dict['data'] = [0] * n_persons
            job_type_dict['backgroundColor'] = "rgba({0},{1},{2},1)".format(
                int(10+10*i/2), int(10+4*i/2), int(10+16*i/2))
            job_type_dict['hoverBackgroundColor'] = "rgba({0},{1},{2},1)".format(
                int(25+10*i/2), int(25+4*i/2), int(25+16*i/2))
            outputdict[job_types[i]] = job_type_dict
        persons_array = []
        i = 0
        for person in jobs.keys():
            persons_array.append("'{0}'".format(person))
            for persons_pesti in jobs[person].keys():
                outputdict[persons_pesti]['data'][i] += 1
            i += 1
        print(json.dumps(list(outputdict.values())))
        print(json.dumps(",".join(persons_array)))
        print("DONE")
        self._replace_placeholder("<PERSONS>", ",".join(persons_array))
        self._replace_placeholder("<JOBS>", json.dumps(list(outputdict.values())))



def register_calculator_plugin():
    """Module method for registering plugin"""
    return JobAnalyzer
