# ICAL Calendar file converter

## Introduction

Convert calendar .ical file into csv files filtering all the events in a secified intervall of days.

## Installation

* Setup a virtualenv and install the dependencies.
* ***The script requires python 3.6 or above***

```bash
    $ git clone https://github.com/snafuz/oci-tools.git
    $ cd ical-parser

    $ pip3 install virtualenv
    $ virtualenv icalparser
    $ . icalparser/bin/activate

    (icalparser) $ pip3 install -r requirements.txt

```

## Usage

Run the from inside the above virtualenv
```bash
    $ python3 ical_parser.py -f <ical_file_path>
```

By default the script extract the events in the next 15 days from now and show them in IST timezone

For a complete overview of all the parameters execute:
```bash
(icalparser) $ python ical_parser.py -h
** confluence calendar converter **
usage: ical_parser.py [-h] [-f SOURCE_FILE] [--tz TZ_DESC] [--days DAYS]
                      [--date-format DATE_FORMAT]

Confluence calendar converter

optional arguments:
  -h, --help            show this help message and exit
  -f SOURCE_FILE, --file SOURCE_FILE
                        ics source file path
  --tz TZ_DESC          timezone [Default: Asia/Kolkata]
  --days DAYS           number of days from now to consider [Default: 15]
  --date-format DATE_FORMAT
                        date format [Default: %m-%d-%Y %H:%M:%S]
```









