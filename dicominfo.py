#!/usr/bin/env python

# display dicom header

import argparse
import pydicom
import isdicom
import glob

parser = argparse.ArgumentParser(
    description="dicominfo: print DICOM header(s)")
parser.add_argument("dicomimages", type=str,
                    help="DICOM image(s) - can use wild cards.")
args = parser.parse_args()

print('args.dicomimages = ',args.dicomimages)

for img in glob.glob(args.dicomimages):
    print('checking ',img)
    ds = pydicom.read_file(img, force=True)
    print(ds)

# just the element names
#   print(*(ds.dir()),sep='\n')


