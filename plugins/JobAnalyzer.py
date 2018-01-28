#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import xlrd
import datetime
from datetime import date
import json

from StatisticsCalculatorBase import StatisticsCalculatorBase

DISCTRICT_JOBS = ('Lippukunnanjohtaja',
                 'Ohjelmajohtaja',
                 'Piirin lpk-postin saaja',
                 'Pestijohtaja',
                 'Joku testi joka varmasti puuttuu')
PESTI_DESCRIPTION_JS = """{
        	label: "<PESTI>",
            data: <DATA_ARRAY>,
            backgroundColor: "rgba(63,103,126,1)",
            hoverBackgroundColor: "rgba(50,90,100,1)"
        }"""


class JobAnalyzer(StatisticsCalculatorBase):
    """
    This calculator computes the persons who currently have posts and the duration of the active posts.
    """
    def __init__(self):
        StatisticsCalculatorBase.__init__(self, "Pestitesti", "plugins/JobAnalyzer/JobAnalyzer.cfg")


    def calculate_statistics(self, parameters=[]):
        print("This calculator computes the persons who currently have posts and the duration of the active posts.")

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
        for x in members_excel:
            members.append(x.value)
            members_key.add(x.value)


        # get all the begin and end dates of posts, convert to years
        begindates_excel = sheet.col_slice(colx=job_begindate_column,
                                           start_rowx=vertical_offset,
                                           end_rowx=sheet.nrows)
        enddates_excel = sheet.col_slice(colx=job_enddate_column,
                                         start_rowx=vertical_offset,
                                         end_rowx=sheet.nrows)
        # durations of the posts if they were to be held until today
        durations = self._yearsfromtodayfromexcel(begindates_excel, today, self._book.datemode)

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
        for i in range(len(members_excel)):
            dict_key_name[members_excel[i].value] = member_names[i].value

        # for each member, search all active posts and calculate their duration in years
        # creates a dict that has second dict embedded; outer includes members' names and inner posts and durations
        active_jobs = {}
        for x in members_key:
            indices = [i for i, y in enumerate(members) if y == x]
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

        self._formJobsArray(active_jobs)

        print(active_jobs)

        # ** check the list of posts that are required by the scout district
        required_jobs_covered = []
        required_jobs_missing = []
        # loop for covered posts
        for i in range(len(DISCTRICT_JOBS)):
            for key in active_jobs:
                if DISCTRICT_JOBS[i] in active_jobs[key]:
                    required_jobs_covered.append(DISCTRICT_JOBS[i])
        # loop for missing posts
        for i in range(len(DISCTRICT_JOBS)):
            if DISCTRICT_JOBS[i] not in required_jobs_covered:
                required_jobs_missing.append(DISCTRICT_JOBS[i])

        print('Seuraavat pestit on hoidossa:')
        print(required_jobs_covered)
        print('Nämä pestit puuttuvat:')
        print(required_jobs_missing)

        # ** scout with the most duty years
        # for each member, calculate the total of the years of their posts
        # (Note: the use of dictionary here turned out to be not used, though still left for possible further use.)
        member_years_of_duty = {}
        max_years = 0
        max_years_member = ''
        for x in members_key:
            indices = [i for i, y in enumerate(members) if y == x]
            years_of_duty = 0
            for j in indices:
                years_of_duty += durations[j]
            member_years_of_duty[dict_key_name[x]] = round(years_of_duty,1)
            # check if new candidate has more years than the previous candidate
            if years_of_duty > max_years:
                # update candidate
                max_years_member = dict_key_name[x]
                max_years = round(years_of_duty,1)
        max_years_member = (max_years_member,max_years)

        print('Kaikkien aikojen lippukuntalainen:')
        print(max_years_member)

        #self._replacePlaceholder("<ZIPS>", zips_s)

        return active_jobs, max_years_member, required_jobs_covered, required_jobs_missing

    def _yearsfromtodayfromexcel(self, d, today, datemode):
        """
        Converts the Julian date of excel and calculates how many days it is from today.
        """
        out = []
        for i in d:
            jnd_date = xlrd.xldate_as_tuple(i.value, datemode)
            jnd_date_datetime = date(jnd_date[0], jnd_date[1], jnd_date[2])
            delta = today - jnd_date_datetime
            out.append(delta.days / 365)
        return out

    def _getAllJobTypes(self, jobs):
        job_types = []
        for person in jobs.keys():
            for pesti in jobs[person].keys():
                if pesti not in job_types:
                    job_types.append(pesti)

        return job_types

    def _formJobsArray(self, jobs):
        job_types = self._getAllJobTypes(jobs)
        n_persons = len(jobs.keys())
        outputdict = {}

        for i in range(0, len(job_types)):
            job_typeDict = {}
            job_typeDict['label'] = job_types[i]
            job_typeDict['data'] = [0] * n_persons
            job_typeDict['backgroundColor'] = "rgba({0},{1},{2},1)".format(int(10+10*i/2), int(10+4*i/2), int(10+16*i/2) )
            job_typeDict['hoverBackgroundColor'] = "rgba({0},{1},{2},1)".format(int(25+10*i/2), int(25+4*i/2), int(25+16*i/2) )
            outputdict[job_types[i]] = job_typeDict
        persons_array = []
        i = 0
        for person in jobs.keys():
            persons_array.append("'{0}'".format(person))
            for persons_pesti in jobs[person].keys():
                outputdict[persons_pesti]['data'][i] += 1
            i += 1
        print(json.dumps(list(outputdict.values())))
        print(json.dumps(",".join(persons_array)))

        jobs_js = []
        i = 0
        for person in jobs.keys():
            for person_pesti in jobs[person].keys():
                if person_pesti in DISCTRICT_JOBS:
                    data_array = "["
                    for j in range(0, n_persons):
                        if j == i:
                            data_array += '1,'
                        else:
                            data_array += '0,'
                    data_array = data_array[:-1]+"]"
                    pesti_js_desc_tmp = PESTI_DESCRIPTION_JS.replace("<PESTI>", person_pesti)
                    pesti_js_desc_tmp = pesti_js_desc_tmp.replace("<DATA_ARRAY>", data_array)
                    jobs_js.append(pesti_js_desc_tmp)



                #PESTI_DESCRIPTION_JS = """{
                #        	label: "<PESTI>",
                #            data: <DATA_ARRAY>,
                #            backgroundColor: "rgba(63,103,126,1)",
                #            hoverBackgroundColor: "rgba(50,90,100,1)"
                #        }"""

            i += 1



        #Kuva 1
        #Henkilö placeholder on <PERSONS>, pitää näyttää tältä: 'Saku', 'Tero', 'Olli'
        #Alla esimerkki datasetistä mitä pitää insertoida. PLACEHOLDER on <JOB>
        #{
        #	label: "Lippukunnanjohtajat",
        #    data: [1,0,0],
        #   backgroundColor: "rgba(63,103,126,1)",
        #    hoverBackgroundColor: "rgba(50,90,100,1)"
        #},
        print("DONE")
        self._replacePlaceholder("<PERSONS>", ",".join(persons_array))
        self._replacePlaceholder("<JOBS>", json.dumps(list(outputdict.values())))



def registerCalculatorPlugin():
    return JobAnalyzer