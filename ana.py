import csv
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pandas as pd
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

'''
Taken largely from http://ramiro.org/notebook/basemap-choropleth/
'''


g_CSVDATAFILE="./API_BN.CAB.XOKA.CD_DS2_en_csv_v2/API_BN.CAB.XOKA.CD_DS2_en_csv_v2.csv"
g_SHAPEFILE = './ne_10m_admin_0_countries/ne_10m_admin_0_countries'
g_NUMCOLORS=9
cm = plt.get_cmap('Greens')
g_SCHEME = [cm(i / g_NUMCOLORS) for i in range(g_NUMCOLORS)]
g_OUTPUTIMGFILE="img.png"

def plotmap(year=2016, description="DESCRIPTION"):
  # mpl.style.use('map')
  fig = plt.figure(figsize=(22, 12))

  ax = fig.add_subplot(111, axisbg='w', frame_on=False)
  fig.suptitle('Forest area as percentage of land area in {}'.format(year), fontsize=30, y=.95)

  m = Basemap(lon_0=0, projection='robin')
  m.drawmapboundary(color='w')

  m.readshapefile(g_SHAPEFILE, 'units', color='#444444', linewidth=.2)

  for info, shape in zip(m.units_info, m.units):
    iso3 = info['ADM0_A3']
    ##### TEMP
    color = '#dddddd'
    # if iso3 not in df.index:
    #     color = '#dddddd'
    # else:
    #     color = g_SCHEME[df.ix[iso3]['bin']]
    #### END TEMP
    patches = [Polygon(np.array(shape), True)]
    pc = PatchCollection(patches)
    pc.set_facecolor(color)
    ax.add_collection(pc)

  # Cover up Antarctica so legend can be placed over it.
  ax.axhspan(0, 1000 * 1800, facecolor='w', edgecolor='w', zorder=2)

  # Draw color legend.
  ax_legend = fig.add_axes([0.35, 0.14, 0.3, 0.03], zorder=3)
  color_map = mpl.colors.ListedColormap(g_SCHEME)

  # cb = mpl.colorbar.ColorbarBase(ax_legend, cmap=color_map, ticks=bins, boundaries=bins, orientation='horizontal')
  # cb.ax.set_xticklabels([str(round(i, 1)) for i in bins])

  # Set the map footer.
  plt.annotate(description, xy=(-.8, -3.2), size=14, xycoords='axes fraction')

  plt.savefig(g_OUTPUTIMGFILE, bbox_inches='tight', pad_inches=.2)

def main():

  with open(g_CSVDATAFILE, 'rb') as csvfile:
    data_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    # for row in data_reader:
    #   if len(row) > 0:
    #     print(row[0])
      # print ', '.join(row)

  # plt.figure(figsize=(8, 8))
  # m = Basemap(projection='ortho', resolution=None, lat_0=50, lon_0=-100)
  # m.bluemarble(scale=0.5);

  plotmap()

if __name__ == "__main__":

  print("\n*** This program will analyse data on current account balances in the world using WDI (World Development Index) data from the World Bank")
  print("")


  main()
