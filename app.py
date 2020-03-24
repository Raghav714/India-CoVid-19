from flask import Flask, request, render_template, session, redirect, Markup
import numpy as np
import pandas as pd
import os
from datetime import date
from datetime import datetime
FOLDER = os.path.join('static', 'image')
to_date = date.today()

app = Flask(__name__)
app.config['IMAGE'] = FOLDER
df = pd.read_csv("data/"+str(to_date)+"_corona.csv")
tot_conf = 0
death = 0
cured = 0
for ele in df["Total Confirmed cases (Indian National)"]: 
    tot_conf = tot_conf + ele 
for ele in df["Total Confirmed cases ( Foreign National )"]: 
    tot_conf = tot_conf + ele
for ele in df["Cured/Discharged/Migrated"]: 
    cured = cured + ele
for ele in df["Death"]: 
    death = death + ele 
colors = ["#FFC300", "#FF0000", "#008000"]



files = os.listdir("data/")
date_file_pair = {}
dates = []
for f in files:
	or_date = f.split("_")[0]
	date_file_pair[f]=or_date
	dates.append(or_date)
dates.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
date_total_in = {}
date_total_dead = {}
date_total_cured = {}
for f in files:
	file_name = "data/"+f
	df1 = pd.read_csv(file_name)
	total = df1.sum()
	date_total_in[date_file_pair[f]] = total[1]+total[2]
	date_total_dead[date_file_pair[f]] = total[4]
	date_total_cured[date_file_pair[f]] = total[3]
total_in = []
total_dead = []
total_cured = []
for date in dates:
	total_in.append(date_total_in[date])
	total_dead.append(date_total_dead[date])
	total_cured.append(date_total_cured[date])

print total_dead
@app.route('/', methods=("POST", "GET"))
def html_table():
	filename_case = os.path.join(app.config['IMAGE'], 'heatmap_in.png')
	pie = zip([tot_conf,death, cured],["Total Confirm Case","Total Death","Total Cured"],colors)
	print df
	return render_template('index.html',  tables=[df.to_html(classes='data')], titles=df.columns.values, confirmed_total=tot_conf, total_in=total_in,total_dead=total_dead,total_cured=total_cured, dates = dates, death_total=death, recovered_total=cured,set = pie, max1=max(list(df["Total Confirmed cases (Indian National)"]+df["Total Confirmed cases ( Foreign National )"])),case= filename_case,values_cases=list(df["Total Confirmed cases (Indian National)"]+df["Total Confirmed cases ( Foreign National )"]),max2=max(list(df["Death"])),values_dead=list(df["Death"]),max3=max(list(df["Cured/Discharged/Migrated"])),max4=max(total_in),max5=max(total_dead),max6=max(total_cured),values_cured=list(df["Cured/Discharged/Migrated"]),labels=list(df["Name of State / UT"]))



if __name__ == '__main__':
    app.run(debug=True)
