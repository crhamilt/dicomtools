#!/usr/bin/env python

# This script will display the start and stop time of each series and the running time.
# It searches the current directory for series directories.
# The DICOM element SeriesTime is searched for the begin time info (hhmmss.frac)

# It is setup so that it prints if called on the bash command line, and if called as
#   a function, it returns a dictionary containing start time of each scan
# usage:  exam_timing.py <examlocation>

import os
import argparse
import datetime
import dicom
import isdicom

def get_timing(dname):

    # print('get_timing fcn: dname = %s' % (dname))

    timing = {}  # dictionary

    for root, dirs, files in os.walk(dname):
            for fname in files:
                fullname = os.path.join(root,fname)
                # print('checking ', fullname)
                if isdicom.isdcm(fullname):
                    try:
                        ds = dicom.read_file(fullname)
                    except dicom.errors.InvalidDicomError:
                        print('Bad DICOM')

                    if "SeriesDescription" in ds:
                        descr = "%s" % (ds.SeriesNumber) +":"+ds.SeriesDescription
                    elif "ProtocolName" in ds:
                        descr = "%s" % (ds.SeriesNumber) +":"+ds.ProtocolName
                    else:
                        descr = root

                    if ds.SeriesNumber.real < 1000 and 'MERGED' not in descr:  # skip screensaves
                        if "AcquisitionDuration" in ds:
                            durstr = ds.AcquisitionDuration
                        else:
                            durstr = ds[0x51,0x100a].value
                        # there is also lScanTimeSec in ASCCONV
                            
                        if "SeriesTime" in ds:
                            timestr0 = ds.SeriesTime
                            timestr = timestr0[0:2]+":"+timestr0[2:4]+":"+timestr0[4:6]
                        else:
                            timestr = '0'

                        timing[descr] = (timestr, durstr)

                        break


    # timing dictionary has a key (serdescr) and a value, value is a tuple (start,duration).
    # sorted() will turn this into a list with each row containing a key and
    # tuple, so access key as sorted_timing[row][0] and access start time as
    # sorted_timing[row][1][0] and duration as sorted_timing[row][1][1]

    sorted_timing = sorted(timing.items(),key=lambda t: t[1][0])  # turns dict into list

    return sorted_timing


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="exam_timing: extract timing of exam")
    parser.add_argument("loc", type=str,
                        help="Directory containing DICOM series directories.")
    args = parser.parse_args()

    timing = get_timing(args.loc)

    print('StartTime Duration Description')

    for row in timing:
        print(row[1][0],"  ",row[1][1],": ",row[0])

    tdstart = datetime.timedelta(hours=int(timing[0][1][0][0:2]),minutes=int(timing[0][1][0][3:5]),seconds=int(timing[0][1][0][6:8]))
    tdend = datetime.timedelta(hours=int(timing[-1][1][0][0:2]),minutes=int(timing[-1][1][0][3:5]),seconds=int(timing[-1][1][0][6:8]))

    duration = tdend - tdstart
    print("duration = ", duration, "(excluding last scan)")
