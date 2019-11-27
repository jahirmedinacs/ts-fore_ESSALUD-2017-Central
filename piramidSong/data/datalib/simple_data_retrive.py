import sys
import os

sys.path.append("..")

import datalib.inteli_pattern as iP

import re

import datetime as DT
from pySmartDL import SmartDL as DL
from pandas import DataFrame as DF

SAMPLES = 50
INCREMENT = 1
SAVE_DESTINATION = "../data"

DEF_URL = "http://websdr.ewi.utwente.nl:8901/fullday/day16832.png"
DEF_PATTERN = "http://websdr.ewi.utwente.nl:8901/fullday/day"
DEF_EXTENSION = "png"
DEF_DATE = "2016-02-01"

url_base = iP.simplex_num_url	(
							DEF_URL,
							DEF_PATTERN,
							DEF_EXTENSION
							)

date_base = (DEF_DATE).split("-")
year = int(date_base[0])
month = int(date_base[1])
day = int(date_base[2]) 
date_base = DT.date(year, month, day)

meta_data = {}
meta_data["Url"] = [url_base.get_url()]
meta_data["Date"] = [str(date_base)]

dowload_object = DL(url_base.get_url(), SAVE_DESTINATION)
dowload_object.start()

meta_data["Size"] = [dowload_object.get_dl_size()]
meta_data["Speed"] = [dowload_object.get_speed()]
meta_data["Time"] = [dowload_object.get_dl_time()]

def_data_frame = DF(data=meta_data)

# here is jhonnyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
relative_date = date_base
for _ in range(1, SAMPLES):
	date_base = DT.date.fromordinal(date_base.toordinal() + INCREMENT)
	url = url_base.n_next(INCREMENT)
	
	dowload_object = DL(url_base.get_url(), SAVE_DESTINATION)
	dowload_object.start()

	# row =	[	url_base.get_url(),	
	# 			str(date_base),
	# 			dowload_object.get_dl_size(),
	# 			dowload_object.get_speed(),
	# 			dowload_object.get_dl_time()	
	# 		]

	# def_data_frame.append(row)

	row =	{	"Url" : [url_base.get_url()],	
				"Date" : [str(date_base)],
				"Size" : [dowload_object.get_dl_size()],
				"Speed" : [dowload_object.get_speed()],
				"Time" : [dowload_object.get_dl_time()]	
			}

	def_data_frame = def_data_frame.append(DF(data=row), ignore_index=True)

def_data_frame.to_csv(SAVE_DESTINATION + "/data_retrive.csv")
