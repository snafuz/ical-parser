#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 
    Parse ical file and report all events in the next 2 weeks 
"""

from datetime import datetime, timedelta, timezone, date
import pytz
import icalendar
from dateutil.rrule import *
import csv
import argparse

#interval to consider
now = datetime.now(timezone.utc)
delta = now + timedelta(days=15)
tz_desc = 'Asia/Kolkata'
date_fmt = "%m-%d-%Y %H:%M:%S"
tz_fmt = "%Z%z"

def set_defaults(args):
    global delta 
    global tz_desc
    global date_fmt 
    delta= now + timedelta(days=args.days)
    tz_desc = args.tz_desc
    date_fmt = args.date_format


def parse_recurrent_events(recur_rule, start, exclusions, tdelta):
    """ Find all reoccuring events """
    rules = rruleset()
    first_rule = rrulestr(recur_rule, dtstart=start)
    rules.rrule(first_rule)
    if not isinstance(exclusions, list):
        exclusions = [exclusions]
        for xdate in exclusions:
            try:
                rules.exdate(xdate.dts[0].dt)
            except AttributeError:
                pass
    dates = []
    for rule in rules.between(now, delta):
        rule = convert_date(rule)
        dates.append([rule,rule+tdelta])
    return dates


def convert_date(dt):
    """
    helper function to convert datetime.date --> datetime.datetime
    """
    my_datetime = dt if isinstance(dt, datetime) else datetime(dt.year, dt.month, dt.day, tzinfo=timezone.utc)
    if tz_desc:
        my_datetime = my_datetime.astimezone(pytz.timezone(tz_desc))
    return my_datetime

def filter_helper(c):
    """
    helper function to filter data. 
    Select only VEVENT recurrent or within the given interval. 
    Also leaves category is skiped.
    """
    if c.name != 'VEVENT' or str(c.get('categories').cats[0])=='leaves':
        return False
    return c.get('rrule') != None or (convert_date(c.get('dtstart').dt)>= now and convert_date(c.get('dtstart').dt)<= delta)

def output_file_name(s_file_name):
    import os
    filename, file_extension = os.path.splitext(s_file_name)
    return  '{0}.csv'.format(filename)

def parse_file(args):
    icalfile = open(args.source_file, 'rb')
    gcal = icalendar.Calendar.from_ical(icalfile.read())

    components = gcal.walk()
    components = filter(lambda c: filter_helper(c), components)
    components = sorted(components, key=lambda c: convert_date(c.get('dtstart').dt), reverse=False)

    my_list = []
    my_list_debug = []

    for component in components: 
        summary = component.get('summary')
        description = component.get('description')
        location = component.get('location')
        startdt = convert_date(component.get('dtstart').dt)
        enddt = convert_date(component.get('dtend').dt)
        tz=startdt.strftime(tz_fmt)
        duration = enddt-startdt
        category =  str(component.get('categories').cats[0])
        if component.get('rrule'):
            reoccur = component.get('rrule').to_ical().decode('utf-8')
            for item in parse_recurrent_events(reoccur, startdt, component.get('exdate'), duration):
                my_list.append([item[0],item[0].strftime(date_fmt), item[1].strftime(date_fmt),int(duration.total_seconds()/60), tz,summary,category, description, location, 'Recurrent'])
                my_list_debug.append([item[0], item[1],summary,category, description, location, component, 'Recurrent'])
        else:
            my_list.append([startdt,startdt.strftime(date_fmt), enddt.strftime(date_fmt),int(duration.total_seconds()/60), tz, summary,category, description, location, ''])
            my_list_debug.append([startdt, enddt,summary,category, description, location, component, ''])
    icalfile.close()
    my_list = sorted(my_list, key=lambda i: i[0], reverse=False)
    o_file_name = output_file_name(args.source_file)
    with open(o_file_name, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows([col for idx, col in enumerate(row) if idx >0 ]for row in my_list)
    csvFile.close()
    print('file {} generated.'.format(o_file_name))


#########################
# command line parser init
parser = argparse.ArgumentParser(description="Confluence calendar converter")
parser.add_argument('-f', '--file',
                    help='ics source file path',
                    dest='source_file')
parser.add_argument('--tz',
                    help='timezone [Default: Asia/Kolkata]',
                    dest='tz_desc',
                    default='Asia/Kolkata')
parser.add_argument('--days',
                    help='number of days from now to consider [Default: 15]',
                    default=15,
                    dest='days')
parser.add_argument('--date-format',
                    help='date format [Default: %%m-%%d-%%Y %%H:%%M:%%S]',
                    default='%m-%d-%Y %H:%M:%S',
                    dest='date_format')


def main():
    import sys
    if sys.version_info[0] < 3:
        raise Exception("I'm sorry, you're Python version must be >= 3.6")
    print(' ** confluence calendar converter **')
    args=parser.parse_args()
    set_defaults(args)
    parse_file(args)

if __name__ == '__main__':
    main()