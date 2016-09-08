#!/usr/bin/python
# -*- coding: utf-8 -*- 

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import datetime
from dateutil.parser import parse
import MySQLdb

from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 600))
display.start()
driver = webdriver.Firefox()
driver.set_window_size(1366, 768)

data = []
try:
	driver.get("http://www.georgiapublicnotice.com/Search.aspx")
	for a in range(0,157):
		n = str(a)
		try:
			today = time.strftime("%m/%d/%Y")
			yesterday = datetime.datetime.now() - datetime.timedelta(days = 70)
			yest = yesterday.strftime("%m/%d/%Y")
			time.sleep(8)
			driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_txtSearch').setAttribute('value', 'Foreclosure')")
			driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_txtDateFrom').setAttribute('value', '" +yest+ "')")
			# driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_txtDateTo').setAttribute('value', '" +nxt+ "')")
			# time.sleep(8)
			driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_lstCounty_"+n+"').click()")
			
			# elem = driver.find_element_by_id("ctl00_ContentPlaceHolder1_as1_txtSearch")
			# elem.clear()

			# elem.send_keys("Foreclosure")
			

			go = driver.find_element_by_id("ctl00_ContentPlaceHolder1_as1_btnGo")
			go.click()
			time.sleep(15)
			try:
				page = driver.find_element_by_id("ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl14_lblTotalPages")
				p = page.text
				pag = int(p.replace("of","").replace("Pages",""))
				print "Total Page --- %s"%pag
				page_num = 0
				# if pag<=99:
				for k in range(pag):
					page_num = page_num + 1
					if page_num >=2:
						print "Next Page"
						# driver.get("http://www.georgiapublicnotice.com/Search.aspx")
						# time.sleep(5)
						next = driver.find_element_by_id("ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl14_btnNext")
						next.click()
						time.sleep(3)
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
							da = dt.strftime('%Y-%m-%d')
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
							data.append(output)
							print output
						driver.get("http://www.georgiapublicnotice.com/Search.aspx")
						# time.sleep(5)
						# yesterday = datetime.datetime.now() - datetime.timedelta(days = 1)
						# yest = yesterday.strftime("%m/%d/%Y")
						# driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_txtDateFrom').setAttribute('value', '" +yest+ "')")
						# # driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_txtDateTo').setAttribute('value', '" +nxt+ "')")
						# # time.sleep(8)
						# driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_lstCounty_"+n+"').click()")
						
						# elem = driver.find_element_by_id("ctl00_ContentPlaceHolder1_as1_txtSearch")
						# elem.clear()

						# elem.send_keys("Foreclosure")
						# go = driver.find_element_by_id("ctl00_ContentPlaceHolder1_as1_btnGo")
						# go.click()
						# time.sleep(20)

					else:
						# driver.get("http://www.georgiapublicnotice.com/Search.aspx")
						# time.sleep(3)
						su = BeautifulSoup(driver.page_source,"lxml")
						tag = su.find_all("table",class_="nested")

						for t in tag:
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
							time.sleep(3)
							sup = BeautifulSoup(driver.page_source, "lxml")
							date = sup.find("div", class_="notice").find_all("tr")[1].find("td", class_="right").find("span").text
							dt = parse(date)
							da = dt.strftime('%Y-%m-%d')
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
							data.append(output)
							print output
						driver.get("http://www.georgiapublicnotice.com/Search.aspx")
						# time.sleep(5)
						# yesterday = datetime.datetime.now() - datetime.timedelta(days = 1)
						# yest = yesterday.strftime("%m/%d/%Y")
						# driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_txtDateFrom').setAttribute('value', '" +yest+ "')")
						# # driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_txtDateTo').setAttribute('value', '" +nxt+ "')")
						# # time.sleep(8)
						# driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_lstCounty_"+n+"').click()")
						
						# elem = driver.find_element_by_id("ctl00_ContentPlaceHolder1_as1_txtSearch")
						# elem.clear()

						# elem.send_keys("Foreclosure")
						# go = driver.find_element_by_id("ctl00_ContentPlaceHolder1_as1_btnGo")
						# go.click()
						# time.sleep(15)
				# driver.get("http://www.georgiapublicnotice.com/Search.aspx")
				time.sleep(8)
				driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_lstCounty_"+n+"').click()")
				time.sleep(5)
				# else:
				# 	output["Publication County"] = n
				# 	data.append(output)
				# 	driver.get("http://www.georgiapublicnotice.com/Search.aspx")
				# 	driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_lstCounty_"+n+"').click()")
				# 	time.sleep(4)
				# 	continue	
			except Exception,e:
				# print e
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
						da = dt.strftime('%Y-%m-%d')
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
						data.append(output)
						print output
					driver.get("http://www.georgiapublicnotice.com/Search.aspx")
					time.sleep(8)
					driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_lstCounty_"+n+"').click()")
					time.sleep(5)
				except Exception, e:
					# driver.get("http://www.georgiapublicnotice.com/Search.aspx")
					driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_lstCounty_"+n+"').click()")
					time.sleep(4)
					continue
					# driver.get("http://www.georgiapublicnotice.com/Search.aspx")
					# driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_lstCounty_"+n+"').click()")
				

			driver.get("http://www.georgiapublicnotice.com/Search.aspx")
			driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_lstCounty_"+n+"').click()")
			time.sleep(4)
		except Exception,e:
			driver.get("http://www.georgiapublicnotice.com/Search.aspx")
			driver.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_as1_lstCounty_"+n+"').click()")
			time.sleep(4)
			continue

			

	
except Exception, e:
	pass


finally:
	# uniqe_list = []
	# new_list = [x["Notice Authentication Number"] for x in data if x.has_key("Notice Authentication Number")]
	# uniqe = list(set(new_list))
	# for u in uniqe:
	# 	z = 0
	# 	for d in data:
	# 			if d.has_key("Notice Authentication Number"):
	# 				if u == d["Notice Authentication Number"]:
	# 					if z == 0:
	# 						z = z+1
	# 						uniqe_list.append(d)
	# 					else:
	# 						continue

	db = MySQLdb.connect("localhost","root","Devel0per","notice_content")
	cur = db.cursor()

	# cursor.execute("CREATE TABLE Notice (Id INT PRIMARY KEY AUTO_INCREMENT, \
	#                 publish_date varchar(50), notice LONGTEXT, publication_name varchar(200),publication_city_and_state varchar(50), publication_county varchar(50), notice_keywords varchar(50), notice_authentication_umber varchar(500)) ENGINE=INNODB")

	# CREATE TABLE Notice(Id INT PRIMARY KEY AUTO_INCREMENT,publish_date varchar(50), notice LONGTEXT, publication_name varchar(200),publication_city_and_state varchar(50), publication_county varchar(50), notice_keywords varchar(50), notice_authentication_umber varchar(500),city varchar(50),county varchar(50),insertion_date varchar(50));

	for obj in data:
		auth_num = obj["Notice Authentication Number"] if obj.has_key("Notice Authentication Number") else ""
		cur.execute("""SELECT * FROM Notice WHERE notice_authentication_umber =%s""",(auth_num,))
		if cur.rowcount == 0:
			try:
				publish_date = obj["Publish Date"]
				notice = obj["Notice"]
				publication_name = obj["Publication Name"]
				publication_city_and_state = obj["Publication City and State"]
				publication_county = obj["Publication County"]
				notice_keywords = obj["Notice Keywords"]
				notice_authentication_umber = obj["Notice Authentication Number"]
				city = obj["City"] if obj.has_key("City") else ""
				county = obj["County"] if obj.has_key("County") else ""
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
			except:
				continue
	db.close()
	driver.quit()
	display.stop()
	


# Crontab 0 15 * * *
# chmod a+x notice_final.py

# 0 18 * * * root cd /home/notice && /usr/bin/python notice_final.py >> /home/notice/cronlog.txt