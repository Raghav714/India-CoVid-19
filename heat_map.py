import matplotlib.pyplot as plt
import pandas as pd
from itertools import groupby

import matplotlib.cm

from mpl_toolkits.basemap import Basemap

from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
import numpy as np

data = pd.read_csv('corona-virus-cases.csv')
states_group = data.groupby(by = 'Name of State / UT')
in_case_list = []
for_case_list = []
cured_list = []
dead_list = []

for key, group in states_group:
	in_case = 0
	for_case = 0
	dead = 0
	cure = 0	
	for row in group.iterrows():
        	in_case += row[1][1]
		for_case += row[1][2]
		dead += row[1][4]
		cure += row[1][3]
    	in_case_list.append((key,in_case))
	for_case_list.append((key,for_case))
	dead_list.append((key,dead))
	cured_list.append((key,cure))
fig, ax = plt.subplots() 
m = Basemap(resolution='c', projection='merc', lat_0=54.5, lon_0=-4.36, llcrnrlon=68., llcrnrlat=6., urcrnrlon=97., urcrnrlat=37.)

m.drawmapboundary(fill_color='#46bcec')
m.fillcontinents(color='#f2f2f2', lake_color='#46bcec')
m.drawcoastlines()

m.readshapefile('IND_adm/IND_adm1','INDIA')

in_satlist = []
dead_satlist = []
cured_satlist = []
for state_info in m.INDIA_info:
	state = state_info['NAME_1']
    	sat1 = 0
	sat3 = 0 
	sat4 = 0
	for i in range(0,len(in_case_list)):
		if in_case_list[i][0] == state:
			sat1 = in_case_list[i][1]+for_case_list[i][1]
			sat3 = dead_list[i][1]
			sat4 = cured_list[i][1]
            		break
	in_satlist.append(sat1)
	dead_satlist.append(sat3)
	cured_satlist.append(sat4)

df_case_in = pd.DataFrame({'shapes':[Polygon(np.array(shape), True) for shape in m.INDIA],
                       'area':[area['NAME_1'] for area in m.INDIA_info],
                       'satlist': in_satlist})    
shapes = [Polygon(np.array(shape), True) for shape in m.INDIA]

cmap_in = plt.get_cmap('Oranges')
pc_in = PatchCollection(shapes, zorder=2)

norm = Normalize()
pc_in.set_facecolor(cmap_in(norm(df_case_in['satlist'].fillna(0).values)))
ax.add_collection(pc_in)

mapper = matplotlib.cm.ScalarMappable(cmap=cmap_in)
mapper.set_array(in_satlist)
plt.colorbar(mapper, shrink=0.4)

ax.set_title('Total Indian case found')
plt.rcParams['figure.figsize'] = [15,15]
plt.savefig("static/image/heatmap_in.png")
#plt.show()


#------------------------------
fig, ax = plt.subplots() 
m = Basemap(resolution='c', projection='merc', lat_0=54.5, lon_0=-4.36, llcrnrlon=68., llcrnrlat=6., urcrnrlon=97., urcrnrlat=37.)

m.drawmapboundary(fill_color='#46bcec')
m.fillcontinents(color='#f2f2f2', lake_color='#46bcec')
m.drawcoastlines()

m.readshapefile('IND_adm/IND_adm1','INDIA')
df_case_cure = pd.DataFrame({'shapes':[Polygon(np.array(shape), True) for shape in m.INDIA],
                       'area':[area['NAME_1'] for area in m.INDIA_info],
                       'satlist': cured_satlist})
shapes = [Polygon(np.array(shape), True) for shape in m.INDIA]
cmap_cure = plt.get_cmap('Greens')
pc_cure = PatchCollection(shapes, zorder=2)

norm = Normalize()
pc_cure.set_facecolor(cmap_cure(norm(df_case_cure['satlist'].fillna(0).values)))
ax.add_collection(pc_cure)

mapper = matplotlib.cm.ScalarMappable(cmap=cmap_cure)
mapper.set_array(cured_satlist)
plt.colorbar(mapper, shrink=0.4)

ax.set_title('Total Cured cases')
plt.rcParams['figure.figsize'] = [15,15]
#plt.show()
plt.savefig("static/image/heatmap_cure.png")

#------------------------------

fig, ax = plt.subplots() 
m = Basemap(resolution='c', projection='merc', lat_0=54.5, lon_0=-4.36, llcrnrlon=68., llcrnrlat=6., urcrnrlon=97., urcrnrlat=37.)

m.drawmapboundary(fill_color='#46bcec')
m.fillcontinents(color='#f2f2f2', lake_color='#46bcec')
m.drawcoastlines()

m.readshapefile('IND_adm/IND_adm1','INDIA')
df_case_dead = pd.DataFrame({'shapes':[Polygon(np.array(shape), True) for shape in m.INDIA],
                       'area':[area['NAME_1'] for area in m.INDIA_info],
                       'satlist': dead_satlist})
shapes = [Polygon(np.array(shape), True) for shape in m.INDIA]
cmap_dead = plt.get_cmap('Reds')
pc_dead = PatchCollection(shapes, zorder=2)

norm = Normalize()
pc_dead.set_facecolor(cmap_dead(norm(df_case_dead['satlist'].fillna(0).values)))
ax.add_collection(pc_dead)

mapper = matplotlib.cm.ScalarMappable(cmap=cmap_dead)
mapper.set_array(dead_satlist)
plt.colorbar(mapper, shrink=0.4)

ax.set_title('Total Dead')
plt.rcParams['figure.figsize'] = [15,15]
#plt.show()
plt.savefig("static/image/heatmap_dead.png")

