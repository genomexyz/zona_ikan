#!/usr/bin/python3

import numpy as np
from netCDF4 import Dataset
from datetime import datetime
import matplotlib as mpl
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap
from PIL import Image
import matplotlib.patches as mpatches
import glob

#setting
#chl_ocx, sst, qual_sst
#Atau biar lebih spesifik tual aja kali ya, 131 - 135 BT dan - 4.0 - - 7.5 LS aja pals nanti
lllat = -7.5
lllon = 131.
urlat = -4.
urlon = 135.

def findidx(lat, lon, matlat, matlon):
	for k in range(len(matlat)):
		if lat > matlat[k]:
			idxlat1 = abs(lat - matlat[k])
			idxlat2 = abs(lat - matlat[k-1])
			latidx = k if idxlat1 < idxlat2 else k-1
			break
	for k in range(len(matlon)):
		if lon < matlon[k]:
			idxlon1 = abs(lon - matlon[k])
			idxlon2 = abs(lon - matlon[k-1])
			lonidx = k if idxlon1 < idxlon2 else k-1
			break
	return latidx, lonidx


def meandata(dirname, varname):
	allfile = glob.glob(dirname)
	dset = Dataset(allfile[0])
	lat = dset.variables['lat'][:]
	lon = dset.variables['lon'][:]
	lllatidx, lllonidx = findidx(lllat, lllon, lat, lon)
	urlatidx, urlonidx = findidx(urlat, urlon, lat, lon)
#	print(lllatidx, urlatidx, lllonidx, urlonidx)
#	print(lat)
	alldata = []
	alldataflag = []
	for i in range(len(allfile)):
		print('processing %s...'%(allfile[i]))
		dset = Dataset(allfile[i])
		data = np.array(dset.variables[varname][urlatidx:lllatidx, lllonidx:urlonidx])
		dataflag = np.zeros(np.shape(data))
		dataflag[data != -32767] = 1.
		data[data == -32767] = 0.
		alldata.append(data)
		alldataflag.append(dataflag)
		dset.close()
	
	alldata = np.asarray(alldata)
	alldataflag = np.asarray(alldataflag)
	
	datamean = np.zeros(np.shape(alldata[0]))
	for i in range(len(alldata[0])):
		for j in range(len(alldata[0,0])):
			if np.sum(alldataflag[:,i,j]) != 0:
				datamean[i,j] = np.sum(alldata[:,i,j]) / np.sum(alldataflag[:,i,j])
	return datamean

klorofil = meandata('Data Klorofil/Januari/*', 'chl_ocx')
sst_siang = meandata('Data SST Siang 2018/Januari/*', 'sst')
sst_malam = meandata('Data SST Malam 2018/Januari/*', 'sst')

#siang
ikansiang = np.zeros(np.shape(klorofil))
for i in range(len(klorofil)):
	for j in range(len(klorofil[0])):
		if klorofil[i,j] > 0.5 and sst_siang[i,j] > 26 and sst_siang[i,j] < 29:
			ikansiang[i,j] = 1.

#malam
ikanmalam = np.zeros(np.shape(klorofil))
for i in range(len(klorofil)):
	for j in range(len(klorofil[0])):
		if klorofil[i,j] > 0.5 and sst_malam[i,j] > 26 and sst_malam[i,j] < 29:
			ikanmalam[i,j] = 1.

print(ikansiang, np.mean(ikansiang))
