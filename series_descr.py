#!/usr/bin/env python
#  series_descr.py:   list the descriptions for all series in a study

import sys
import os
import argparse
import glob
import dicom as dcm
import isdicom

def series_descr(dname):

    # print('serie_descr fcn: dname = %s' % (dname))

    descriptions = {}  # dictionary

    for root, dirs, files in os.walk(dname):
        for fname in files:
            fullname = os.path.join(root,fname)
            if isdicom.isdcm(fullname):
                # print('checking ',fullname)
                try:
                    ds = dcm.read_file(fullname)
                except dcm.errors.InvalidDicomError:
                    print('Bad DICOM')

                sernum = ''
                if "SeriesNumber" in ds:
                    sernum = 'Ser %s' % (ds.SeriesNumber)

                if "SeriesDescription" in ds:
                    descriptions[root]=sernum+':'+ds.SeriesDescription
                elif "ProtocolName" in ds:
                    descriptions[root]=sernum+':'+ds.ProtocolName



                break

    return descriptions # dictionary

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="series_descr dname : get DICOM series descriptions in directory 'dname'.")
    parser.add_argument("dname", type=str,
                        help="Directories containing DICOM series directories. [Wildcards in quotes].")
    args = parser.parse_args()

    for dirname in glob.glob(args.dname):

        descr = series_descr(dirname)

        sortedDescr = sorted(descr.items(),key=descr.get(0))  # a list

        for row in sortedDescr:
            print(row[0],'(serDescr): ', row[1])

