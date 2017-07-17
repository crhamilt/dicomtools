#!/usr/bin/env python

# This script will find DICOM series that contain a string specified as an argument.
# It searches the current directory for series directories.
# The DICOM element SeriesDescription is searched for the string.

# It is setup so that it prints if called on the bash command line, and if called as
#   a function, it returns a
# usage:  find_series.py <string> <location>

import sys
import argparse
import series_descr


def find_series(substr,loc):
    descr = series_descr.series_descr(loc)

    matches = {}

    # items() returns a list!  so, it is not iterating over a dictionary!
    for key,value in descr.items():
        # print(key,'(find): ', value)
        if substr in value:
            matches[key]=value
            # print(key,'(find-match): ', value)

    return matches

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="find_series: find DICOM series with descriptions containing case-sensitive 'substr' in directory 'loc'.")
    parser.add_argument("substr", type=str,
                        help="string to search for in DICOM series descriptions.")
    parser.add_argument("loc", type=str,
                        help="Directory containing DICOM series directories.")
    args = parser.parse_args()

    found = find_series(args.substr, args.loc)

    for key,value in found.items():
        print(key,': ',value)

