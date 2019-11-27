#! /usr/bin/python3 -s

import sys
import os

import datalib.inteli_pattern as iP

import re

import datetime as DT
from pySmartDL import SmartDL as DL
from pandas import DataFrame as DF 

DATA_LABEL = "data"

class DataSource():
	"""
		Class Design for internet data retrive
		
		Actual Version	:	0.1 - Alpha
		
		See Doc	:	SOME_URL.SOMETING
	"""
	def __init__(self):
		super(DataSource, self).__init__()
		
		self.main_url = ""
		self.pattern = ""
		self.extesion = ""

		self.sample_size = 0
		self.ulrs = None

		self.curdir = os.getcwd()

	def set_main_url(self, main_url):
		self.main_url = main_url
	
	def set_pattern(self, pattern):
		self.pattern = pattern

	def set_extesion(self, extesion):
		self.extesion = extesion

	def detect_pattern(self, mode=None):
		if mode is None:
			iP.detection()
		elif mode == iP.SIMPLEX_AUTOINT:
			self.urls = iP.simplex_num_url(self.main_url, self.pattern, self.extesion)
		else:
			pass

	def samples(self, amount):
		self.sample_size = amount

	def generate_dataframe(self,verbos=False):
		self.data = DF.empty

	def asociate_label(self, base_label, mode=None):
		if mode is None:
			return None
		else:
			pass

		if mode == DATA_LABEL:
			self.base_label = base_label

			crry_date = self.base_label.split("-")

			year = int(crry_date[0])
			month = int(crry_date[1])
			day = int(crry_date[2]) 
			
			self.base_label = DT.date(year, month, day)
		else:
			return None

		
	def check(self):
		pass

	def download(self, destination_path=None):
		if destination_path is None:
			destination_path = self.curdir
		else:
			pass

		for str_ref in self.urls.range_auto(self.sample_size):
			print(str_ref)


if __name__ == "__main__":
	pass

		

# url = "http://mirror.ufs.ac.za/7zip/9.20/7za920.zip"
# dest = "C:\\Downloads\\" # or '~/Downloads/' on linux

# obj = SmartDL(url, dest)
# obj.start()

# path = obj.get_dest()

# # from calendar import monthrange as monthrange
# # import time
# # from datetime import datetime
# # from calendar import monthrange
# # int(time.mktime(datetime.now().timetuple()))

# text = open(SYS.argv[1], "r")

# dates = []
# start_url_number = 0
# basic_url = []

# for line in text:
# 	if line[0] == "#":
# 		pass
# 	else:
# 		line = line.replace('\n', '')
# 		alt_line = line.split("\t")

# 		clean_line = []
# 		for cad in alt_line:
# 			if cad == '':
# 				pass
# 			else:
# 				clean_line += [cad]

# 		if clean_line != []:
# 			[date, url] = [clean_line[0], clean_line[-1]]

# 			dates.append(date)
			
# 			if start_url_number == 0:
# 				alt_url = url.split('/')

# 				basic_url = url.split('/day')

# 				basic_url[0] += "/day"
# 				basic_url[1] = basic_url[1][-4:]

# 				# print(basic_url)

# 				start_url_number = int(alt_url[-1][3:-4])

# 				# print(start_url_number)

# 			# print(date, '\t', url)
# 		else:
# 			pass

# print (dates)
# print (start_url_number)
# print (basic_url)

# dates_dated = []

# first_time = True

# total_samples = 0

# for date_str in dates:
# 	crry_date = date_str.split("-")

# 	year = int(crry_date[0])
# 	month = int(crry_date[1])
# 	day = int(crry_date[2]) 
	
# 	# print(DT.date(year, month, day))

# # 	dates_dated.append(DT.date(year, month, day))

# 	print("Date \t :", dates_dated[-1])

# 	# print("\t\tTO DATE\t:")

# 	if first_time:
# 		pass
# 	else:
# 		print("Samples \t\t::")
# 		print((dates_dated[-1] - dates_dated[-2]).days)

# 		total_samples += (dates_dated[-1] - dates_dated[-2]).days

# 	print("\n")
# 	first_time = False

# print("TOTAL SAMPLES\t", total_samples)