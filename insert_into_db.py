#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import MySQLdb
import xlrd
notice_book = xlrd.open_workbook("notice_insurt.xlsx")
notice_sheet = notice_book.sheet_by_index(0)
import time
from dateutil.parser import parse
# Devel0per
db = MySQLdb.connect("localhost","root","Devel0per","notice_content")
cur = db.cursor()

	# cursor.execute("CREATE TABLE Notice (Id INT PRIMARY KEY AUTO_INCREMENT, \
	#                 publish_date varchar(50), notice LONGTEXT, publication_name varchar(200),publication_city_and_state varchar(50), publication_county varchar(50), notice_keywords varchar(50), notice_authentication_umber varchar(500)) ENGINE=INNODB")

	# CREATE TABLE Notice(Id INT PRIMARY KEY AUTO_INCREMENT,publish_date varchar(50), notice LONGTEXT, publication_name varchar(200),publication_city_and_state varchar(50), publication_county varchar(50), notice_keywords varchar(50), notice_authentication_umber varchar(500),city varchar(50),county varchar(50),insertion_date varchar(50));

for i in range(1,4182):
	o = notice_sheet.row_values(i)
	auth_num = o[6]
	print type(auth_num)
	cur.execute("""SELECT * FROM Notice WHERE notice_authentication_umber =%s""",(auth_num,))
	print cur.rowcount
	if cur.rowcount == 0:
		# try:
		dt = parse(o[0])
		da = dt.strftime('%Y-%m-%d')
		publish_date = da
		print publish_date
		notice = o[1].encode("utf-8")
		publication_name = o[2].encode("utf-8")
		publication_city_and_state = o[3].encode("utf-8")
		publication_county = o[4]
		notice_keywords = o[5]
		print notice_keywords
		notice_authentication_umber = o[6]
		city = o[7]
		county = o[8]
		insertion_date = time.strftime('%Y-%m-%d')

		cur.execute("""INSERT INTO Notice(publish_date, 
			notice, publication_name,publication_city_and_state, 
			publication_county, notice_keywords, 
			notice_authentication_umber,city,county,insertion_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(publish_date, 
			notice, publication_name,publication_city_and_state, 
			publication_county, notice_keywords, 
			notice_authentication_umber,city,county,insertion_date))
		db.commit()
		print "####################### INSERTED SUCCESSFULLY ################"
		# except:
		# 	continue
db.close()

