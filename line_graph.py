import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from datetime import datetime
files = os.listdir("data/")
date_file_pair = {}
dates = []
for f in files:
	date = f.split("_")[0]
	date_file_pair[f]=date
	dates.append(date)
dates.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
print dates
date_total_in = {}
date_total_for = {}
date_total_dead = {}
date_total_cured = {}
for f in files:
	file_name = "data/"+f
	df = pd.read_csv(file_name)
	total = df.sum()
	date_total_in[date_file_pair[f]] = total[1]
	date_total_for[date_file_pair[f]] = total[2]
	date_total_dead[date_file_pair[f]] = total[3]
	date_total_cured[date_file_pair[f]] = total[4]
total_in = []
total_for = []
total_dead = []
total_cured = []
for date in dates:
	total_in.append(date_total_in[date])
	total_for.append(date_total_for[date])
	total_dead.append(date_total_dead[date])
	total_cured.append(date_total_cured[date])
plt.scatter(dates, total_cured)
plt.scatter(dates, total_in)
plt.scatter(dates, total_dead)
plt.scatter(dates, total_for)
plt.plot(dates, total_cured, color='g',label = "Cured")
plt.plot(dates, total_in, color='orange',label = "Indian National cases")
plt.plot(dates, total_dead, color='red',label = "Dead")
plt.plot(dates, total_for, color='grey',label = "Foreign National cases")
plt.xlabel('Date')
plt.ylabel('Total Cases')
plt.title('Total cases on each date')
plt.legend() 
plt.savefig("bar_graph.png")
#plt.show()
