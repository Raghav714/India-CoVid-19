# importing modules
import requests
import pandas as pd 
from bs4 import BeautifulSoup
import time
import os
from datetime import date
url = 'https://www.mohfw.gov.in/'
header = ["Name of State / UT", "Total Confirmed cases (Indian National)", "Total Confirmed cases ( Foreign National )", "Cured/Discharged/Migrated","Death"]
while True:
	today = date.today()
	print "Saving data for "+str(today)
	r = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data,'html.parser')
# Extracting table data
	tables = soup.find_all('tbody')
	table_rows = tables[-1].find_all('tr')
	s_no = []
	state = []
	in_conf = []
	for_conf = []
	cur = []
	dead = []
	total = len(table_rows)
	for tr in table_rows[0:total-1]:
		td = tr.find_all('td')
		s_no.append(td[0].text)
		state.append(td[1].text)
		in_conf.append(td[2].text.strip())
		for_conf.append(td[3].text.strip())
		cur.append(td[4].text.strip())
		dead.append(td[5].text.strip())
	df = pd.DataFrame(list(zip(state,in_conf,for_conf,cur,dead)),columns =header)
	df.sort_values(by=["Total Confirmed cases (Indian National)"])
# Saving it to csv file
	file_name =  "data/"+ str(today)+"_corona.csv"
	df.to_csv(file_name,index=False)
# plotting a graph
	time.sleep(86400)
