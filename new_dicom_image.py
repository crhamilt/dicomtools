#!/usr/bin/env python

import argparse
import numpy as np
import dicom
import cv2
import isdicom

parser = argparse.ArgumentParser(
    usage="new_dicom_image <DICOM file with header> <NPY or DCM file with data>",
    description="replace image data in a DICOM file with data from NPY or DCM file")
parser.add_argument("dicomfile", type=str,
                    help="name of DICOM file with desired header"),
parser.add_argument("datafile", type=str,
                    help="numpy or DCM file containing image data")

args = parser.parse_args()

# this code was a one-time conversion of png snapshot from article to a numpy array
if False:
    nparray = cv2.imread("T1MES.png") 
    print('nparray shape =',nparray.shape)
    print('nparray dtype =',nparray.dtype)
    nparray2 = cv2.resize(nparray[0:255,:], (256,256), interpolation=cv2.INTER_CUBIC)
    nparraygray = cv2.cvtColor(nparray2, cv2.COLOR_BGR2GRAY, 1)
    nparraygray16 = nparraygray.astype('int16')*10

    print('nparraygray16 shape =',nparraygray16.shape)
    print('nparraygray16 dtype =',nparraygray16.dtype)
    print('max = ', np.amax(nparraygray16), ' min = ',np.amin(nparraygray16))
    np.save('times.npy',nparraygray16)

# read files
ds = dicom.read_file(args.dicomfile, force=True)

if args.datafile.lower().endswith('dcm'):
    ds2 = dicom.read_file(args.datafile, force=True)

    # resize data file image to match the header image size
    rows_hdr = ds.Rows
    cols_hdr = ds.Columns
    rows_img = ds2.Rows
    cols_img = ds2.Columns

    if rows_hdr != rows_img or cols_hdr != cols_img:
        print('resizing image to match DICOM header...')
        nparray1d = np.fromstring(ds2.PixelData,dtype='int16')
        nparray2d = np.reshape(nparray1d, (cols_img, rows_img))
        npresized = cv2.resize(nparray2d,(cols_hdr,rows_hdr))
        ds.PixelData = npresized.tobytes()
    else:
        ds.PixelData = ds2.PixelData

else:
    nparray = np.load(args.datafile)
    ds.PixelData = nparray.tostring()     # saves as raw bytes


ds.save_as("new.DCM")







