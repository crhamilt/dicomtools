#!/usr/bin/env python

# This script will copy DICOM series to a new location.

# usage:  copy_series.py <string in series description> <new location>

import sys
from os.path import basename as basename
import shutil
import find_series


def copy_series(substr, src, dest):
    # Find all series in the current directory whose descriptions contain substr
    #   and move them to dest.
    descr = find_series.find_series(substr,src)

    for key,value in descr.items():
        print('copying %s to %s' % (key, dest))
        shutil.copytree(key,dest+'/'+basename(key))

if __name__ == "__main__":

    if len(sys.argv) < 4:
        print('Usage: copy_series substring srcdir destdir')
        sys.exit()

    copy_series(sys.argv[1], sys.argv[2], sys.argv[3])

