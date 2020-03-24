from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import datetime
from datetime import date
to_date = date.today()
#Number of top countries to be reported
topCountryNum = 23

#Graph size matters
desired_width=360
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',120)

#Format the date time to present on the graph
dt = datetime.datetime.now()
today = dt.strftime("%A, %d %B %Y, %H:%M:%S")
todayDate = dt.strftime("%A, %d %B %Y")
#Local method to plot the bar graph
def plotGraph(dfname, rowname, colname, fignum, graphcolor, titlestr):
	x1 = dfname[rowname]
	y1 = dfname[colname]
	plt.figure(fignum, figsize=(16, 6))
	plt.title(titlestr + r"$\bf{" + colname + "}$" + ' - [Total states effected as of today = {}]'.format(cv.shape[0]))
	plt.suptitle(today)
	plt.xlabel("States")
	plt.ylabel(colname)
	plt.xticks(rotation=15)
	barplot = plt.bar(x1, y1, color=graphcolor)
	plt.grid(True)
	for bar in barplot:
		yval = bar.get_height()
		plt.text(bar.get_x() + bar.get_width() / 2.0, yval, int(yval), va='bottom')  # va: vertical alignment y positional argument
    #plt.show()
	plt.savefig("barchart"+str(fignum)+".png")
	return()

#----WORLD DATA----#
#Read the coronoa_virus.csv from the file system and transform into a DataFrame using read_csv() method
cv = pd.read_csv("data/"+str(to_date)+"_corona.csv")
cv = cv.fillna(0) #<-- Fill all NaN values with 0
cv["total case"] = cv['Total Confirmed cases (Indian National)']+cv['Total Confirmed cases ( Foreign National )']
#Plot the pie chart for World Data ('Total cases', 'Total recovered', 'Total deaths', 'Active cases')
s = cv.sum(axis=0) #<--Add all columns and create a series
totalCase = s['total case']
totalRecovered = s['Cured/Discharged/Migrated']
totalDeaths = s['Death']


# Pie chart plotting
labels = 'Total Recovered', 'Total Cases', 'Total Deaths'
sizes = [totalRecovered, totalCase, totalDeaths]
explode = (0.0, 0.0, 0.3)  # only "explode" the 3rd slice (i.e. 'Total Deaths')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.f%%',
        shadow=True, startangle=50)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set(aspect="equal", title='Total Global Cases as of {} = {}'.format(todayDate, totalCase))
#plt.show()
plt.savefig("pie_chart.png")
#Sorting the data based on a single column in a file and output using sort_values() method (descending order - ascending=False)
cv_TotalCases = cv.sort_values("total case", ascending=False)
cv_TotalRecovered = cv.sort_values('Cured/Discharged/Migrated', ascending=False)
#cv_TotalCasesPerMillion = cv.sort_values('Total cases per 1M pop.', ascending=False)
cv_TotalDeaths = cv.sort_values('Death', ascending=False)
#cv_NewCases = cv.sort_values('New cases', ascending=False)
#cv_NewDeaths = cv.sort_values('New deaths', ascending=False)

#Graph of top 'Total cases'
x = cv_TotalCases.head(topCountryNum)
rowcategory = "Name of State / UT"
columncategory = "total case"
figureNum = 1
graphColor = "Red"
titlestring = "Top {} states based on: ".format(topCountryNum)
plotGraph(x, rowcategory, columncategory, figureNum, graphColor, titlestring)

#Graph of top 'Total recovered'
x = cv_TotalRecovered.head(topCountryNum)
rowcategory = "Name of State / UT"
columncategory = "Cured/Discharged/Migrated"
figureNum = 2
graphColor = "limegreen"
titlestring = "Top {} States based on: ".format(topCountryNum)
plotGraph(x, rowcategory, columncategory, figureNum, graphColor, titlestring)

#Graph of top 'Total deaths'
x = cv_TotalDeaths.head(topCountryNum)
rowcategory = "Name of State / UT"
columncategory = "Death"
figureNum = 3
graphColor = "dimgray"
titlestring = "Top {} States based on: ".format(topCountryNum)
plotGraph(x, rowcategory, columncategory, figureNum, graphColor, titlestring)
