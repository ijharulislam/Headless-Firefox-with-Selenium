#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from selenium import webdriver
import urllib
import urllib2
from datetime import datetime
import xlrd
from lxml import html
import requests
from bs4 import BeautifulSoup
import xlsxwriter
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv 
import time
import datetime
from dateutil.parser import parse
import datetime
import pandas as pd
from datetime import date


data = []
date_list = []
d1 = "1/1/2014"
d2 = datetime.datetime.today()
daterange = pd.date_range(d1, d2)
for single_date in daterange:
	date_list.append(single_date.strftime("%m/%d/%Y"))

from itertools import tee, islice, chain, izip

def next_(some_iterable):
	items, nexts = tee(some_iterable, 2)
	nexts = chain(islice(nexts, 1, None), [None])
	return izip(items, nexts)




try:
	driver=webdriver.Firefox()
	driver.get("http://www.georgiapublicnotice.com/Search.aspx")
	# driver.get("http://www.georgiapublicnotice.com/Search.aspx")
	# # for item, nxt in next_(date_list):
	# # 	if nxt is not None:
	# item = "1/1/2014"
	# nxt = "12/30/2014"
	# driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_txtDateFrom').setAttribute('value', '" +item+ "')")
	# driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_txtDateTo').setAttribute('value', '" +nxt+ "')")
	# else:
	# 	driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_txtDateFrom').setAttribute('value', '" +item+ "')")
	for a in range(33,157):
		n = str(a)
		try:
			# for item, nxt in next_(date_list):
			# 	if nxt is not None:
			item = "1/1/2015"
			nxt = "3/1/2015"
			time.sleep(5)
			driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_txtDateFrom').setAttribute('value', '" +item+ "')")
			driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_txtDateTo').setAttribute('value', '" +nxt+ "')")
			driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_lstCounty_"+n+"').click()")
			# driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_lstCounty_2').click()")
			# driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_lstCounty_3').click()")
			# driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_lstCounty_4').click()")
			
			# d = driver.find_element_by_id("ctl00_ContentPlaceHolder1_as1_divDateRange")
			# d.click()


			today = time.strftime("%m/%d/%Y")

			yesterday = datetime.datetime.now() - datetime.timedelta(days = 100)
			yes = yesterday.strftime("%m/%d/%Y")

			
			elem = driver.find_element_by_id("ctl00_ContentPlaceHolder1_as1_txtSearch")
			elem.clear()

			elem.send_keys("Foreclosure")
			go = driver.find_element_by_id("ctl00_ContentPlaceHolder1_as1_btnGo")
			go.click()
			time.sleep(15)
			try:
				page = driver.find_element_by_id("ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl14_lblTotalPages")
				p = page.text
				pag = int(p.replace("of","").replace("Pages",""))
				page_num = 0
				print "Total Page"
				print pag
				if pag<=99:
					for k in range(pag):
						page_num = page_num + 1
						if page_num >=2:
							print "Next Page"
							driver.get("http://www.georgiapublicnotice.com/Search.aspx")
							time.sleep(6)
							next = driver.find_element_by_id("ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl14_btnNext")
							next.click()
							time.sleep(3)
							su = BeautifulSoup(driver.page_source,"lxml")
							tag = su.find_all("table",class_="nested")

							for t in tag:
								time.sleep(2)
								output = {}
								c = t.find("div", class_="right")
								if c is not None:
									cit = str(c).split("<br/>")
									city = cit[0].replace("City:","").replace('<div class="right">',"")
									county = cit[1].replace("County:","").replace("</div>","")
									output["City"] = city.strip()
									output["County"] = county.strip()
								
								link = t.find("td", class_="view bdrBrownTop bdrBrownRight bdrBrownBottom bdrBrownLeft mobileL mobileT").find("input")
								url = "http://www.georgiapublicnotice.com/"+ li
								driver.get(url)
								
								sup = BeautifulSoup(driver.page_source, "lxml")
								date = sup.find("div", class_="notice").find_all("tr")[1].find("td", class_="right").find("span").text
								dt = parse(date)
								da = dt.strftime("%m/%d/%Y")
								output["Publish Date"] = da
								notice = sup.find("article").find_all("p")[1].text
								if "PLEASE NOTE:" not in notice:
									output["Notice"] = notice.encode("utf-8")
								else:
									notic = sup.find("article").find_all("p")[2].text
									output["Notice"] = notic.encode("utf-8")

								publication_name = sup.find("div",attrs={"id":"detail"}).find_all("p")[0].find("span").text
								output["Publication Name"] = publication_name.encode("utf-8")
								pub_city = sup.find("div",attrs={"id":"detail"}).find_all("p")[2].text
								output["Publication City and State"] = pub_city.replace("Publication City and State:","").strip().encode("utf-8")
								pub_county = sup.find("div",attrs={"id":"detail"}).find_all("p")[3].text
								output["Publication County"] = pub_county.replace("Publication County:","").strip().encode("utf-8")
								notice_keyword = sup.find("div",attrs={"id":"detail"}).find_all("p")[5].text
								output["Notice Keywords"] = notice_keyword.replace("Notice Keywords:","").strip().encode("utf-8")
								notice_auth_num = sup.find("div",attrs={"id":"detail"}).find_all("p")[6].text
								output["Notice Authentication Number"] = notice_auth_num.replace("Notice Authentication Number:","").strip().encode("utf-8")
								print output
								data.append(output)
						else:
							driver.get("http://www.georgiapublicnotice.com/Search.aspx")
							su = BeautifulSoup(driver.page_source,"lxml")
							tag = su.find_all("table",class_="nested")

							for t in tag:
								time.sleep(2)
								output = {}
								c = t.find("div", class_="right")
								if c is not None:
									cit = str(c).split("<br/>")
									city = cit[0].replace("City:","").replace('<div class="right">',"")
									county = cit[1].replace("County:","").replace("</div>","")
									output["City"] = city.strip()
									output["County"] = county.strip()
								
								link = t.find("td", class_="view bdrBrownTop bdrBrownRight bdrBrownBottom bdrBrownLeft mobileL mobileT").find("input")
								li = link["onclick"].replace("javascript:location.href='", "").replace("';return false;","")
								url = "http://www.georgiapublicnotice.com/"+ li
								driver.get(url)
								
								sup = BeautifulSoup(driver.page_source, "lxml")
								date = sup.find("div", class_="notice").find_all("tr")[1].find("td", class_="right").find("span").text
								dt = parse(date)
								da = dt.strftime("%m/%d/%Y")
								output["Publish Date"] = da
								notice = sup.find("article").find_all("p")[1].text
								if "PLEASE NOTE:" not in notice:
									output["Notice"] = notice.encode("utf-8")
								else:
									notic = sup.find("article").find_all("p")[2].text
									output["Notice"] = notic.encode("utf-8")

								publication_name = sup.find("div",attrs={"id":"detail"}).find_all("p")[0].find("span").text
								output["Publication Name"] = publication_name.encode("utf-8")
								pub_city = sup.find("div",attrs={"id":"detail"}).find_all("p")[2].text
								output["Publication City and State"] = pub_city.replace("Publication City and State:","").strip().encode("utf-8")
								pub_county = sup.find("div",attrs={"id":"detail"}).find_all("p")[3].text
								output["Publication County"] = pub_county.replace("Publication County:","").strip().encode("utf-8")
								notice_keyword = sup.find("div",attrs={"id":"detail"}).find_all("p")[5].text
								output["Notice Keywords"] = notice_keyword.replace("Notice Keywords:","").strip().encode("utf-8")
								notice_auth_num = sup.find("div",attrs={"id":"detail"}).find_all("p")[6].text
								output["Notice Authentication Number"] = notice_auth_num.replace("Notice Authentication Number:","").strip().encode("utf-8")
								print output
								data.append(output)
				else:
					output = {}
					output["Publication County"] = n
					data.append(output)
					driver.get("http://www.georgiapublicnotice.com/Search.aspx")
					driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_lstCounty_"+n+"').click()")
					time.sleep(4)
					continue	
			except Exception,e:
				print "Error in Pagination"
				print e
				try:
					su = BeautifulSoup(driver.page_source,"lxml")
					tag = su.find_all("table",class_="nested")

					for t in tag:
						time.sleep(3)
						output = {}
						c = t.find("div", class_="right")
						if c is not None:
							cit = str(c).split("<br/>")
							city = cit[0].replace("City:","").replace('<div class="right">',"")
							county = cit[1].replace("County:","").replace("</div>","")
							output["City"] = city.strip()
							output["County"] = county.strip()
						
						link = t.find("td", class_="view bdrBrownTop bdrBrownRight bdrBrownBottom bdrBrownLeft mobileL mobileT").find("input")
						li = link["onclick"].replace("javascript:location.href='", "").replace("';return false;","")
						url = "http://www.georgiapublicnotice.com/"+ li
						driver.get(url)
						
						sup = BeautifulSoup(driver.page_source, "lxml")
						date = sup.find("div", class_="notice").find_all("tr")[1].find("td", class_="right").find("span").text
						dt = parse(date)
						da = dt.strftime("%m/%d/%Y")
						output["Publish Date"] = da
						notice = sup.find("article").find_all("p")[1].text
						if "PLEASE NOTE:" not in notice:
							output["Notice"] = notice.encode("utf-8")
						else:
							notic = sup.find("article").find_all("p")[2].text
							output["Notice"] = notic.encode("utf-8")
						publication_name = sup.find("div",attrs={"id":"detail"}).find_all("p")[0].find("span").text
						output["Publication Name"] = publication_name.encode("utf-8")
						pub_city = sup.find("div",attrs={"id":"detail"}).find_all("p")[2].text
						output["Publication City and State"] = pub_city.replace("Publication City and State:","").strip().encode("utf-8")
						pub_county = sup.find("div",attrs={"id":"detail"}).find_all("p")[3].text
						output["Publication County"] = pub_county.replace("Publication County:","").strip().encode("utf-8")
						notice_keyword = sup.find("div",attrs={"id":"detail"}).find_all("p")[5].text
						output["Notice Keywords"] = notice_keyword.replace("Notice Keywords:","").strip().encode("utf-8")
						notice_auth_num = sup.find("div",attrs={"id":"detail"}).find_all("p")[6].text
						output["Notice Authentication Number"] = notice_auth_num.replace("Notice Authentication Number:","").strip().encode("utf-8")
						print output
						data.append(output)
					# driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_lstCounty_"+n+"').click()")
				except Exception, e:
					print "Error in non Pagination"
					print e

					driver.get("http://www.georgiapublicnotice.com/Search.aspx")
					driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_lstCounty_"+n+"').click()")
					time.sleep(4)
					continue
					# driver.get("http://www.georgiapublicnotice.com/Search.aspx")
					# driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_lstCounty_"+n+"').click()")
				

			driver.get("http://www.georgiapublicnotice.com/Search.aspx")
			driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_lstCounty_"+n+"').click()")
			time.sleep(4)
		except Exception,e:
			print "Error in First Block"
			print e
			driver.get("http://www.georgiapublicnotice.com/Search.aspx")
			driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_lstCounty_"+n+"').click()")
			time.sleep(4)
			continue

			

	
except Exception, e:
	print "Ending Error"
	print e
	pass


finally:
	def WriteDictToCSV(csv_columns,dict_data):
		with open("notice6.csv", 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
			writer.writeheader()
			for row in dict_data:
				writer.writerow(row)
	csv_columns =['Publish Date','Notice','Publication Name','Publication City and State', 'Publication County', 'Notice Keywords',"Notice Authentication Number","City","County"]
	WriteDictToCSV(csv_columns,data)
	driver.close()
	



# 5/26/2016

# Problems County 1. banks
# bartow more than 100 / first loop 1/1/2015 . second loop 2/1/2015 third 2/15/2015