#!/usr/bin/env python
# coding: utf-8

# # Dashboard for interactively measures for Temperature and Dissolved Oxygen in Nova Scotia
# 
# Created By: Rine Zaman, Larissa Dos Santos Soares, and James Munroe
# 
# https://github.com/RineZaman/CMAR_Dashboard
# 
# 
# The Centre for Marine Applied Research (CMAR) leads and supports research projects in collaboration with industry, academia, associations, communities, government agencies, and stakeholder groups that utilize and support Nova Scotia’s coastal marine resources. CMAR’s partnership with CIOOS (Canadian Integrated Ocean Observing System) makes data Findable, Accessible, Interoperable, and Reusable (FAIR) for all stakeholders with an interest in the coastal ocean environment.
# 
# ## How to visualize the data?
# 
# CMAR currently maintains and supports over 60 sensor strings and is continuously expanding into new areas throughout coastal Nova Scotia (10 counties). There is a data server that allows a simple, consistent way to download subsets of scientific datasets in common file formats and make graphs and maps, which is ERDDAP (the Environmental Research Division's Data Access Program) using oceanographic data (for example, data from satellites and buoys).
# 
# ## Dissolved Oxygen
# 
# Dissolved oxygen (DO) is the amount of oxygen that is present in the water, usually measured in milligrams per liter (mg/L) (Chesapeake Bay Program, Dissolved Oxygen). DO is necessary to many forms of life including fish, invertebrates, bacteria and plants that use oxygen in respiration. These organisms obtain oxygen through their gills, while plant life and phytoplankton require dissolved oxygen for respiration when there is no light for photosynthesis (Plant Growth Factors, 2013).
# Dissolved oxygen enters water through the air slowly diffusing across its surface from the surrounding atmosphere (EPA, 2012) or as a plant byproduct (e.g., a waste product of photosynthesis from phytoplankton, algae, seaweed and other aquatic plants) (Watt, 2000).
# 
# The water will slowly absorb oxygen and other gasses from the atmosphere until it reaches equilibrium (Dissolved Gases, Oxygen), which means that the water is holding as many dissolved gas molecules as it can (American Public Health Assoc., American Water Works Assoc. & Water Environment Federation, 1999). 
# 
# Bottom feeders, crabs, oysters and worms need minimal amounts of oxygen (1-6 mg/L), while shallow water fish need higher levels (4-15 mg/L) 5. Coldwater fish like trout and salmon are most affected by low dissolved oxygen levels 19. 
# The mean DO level for adult salmonids is 6.5 mg/L, and the minimum is 4 mg/L ¹². For salmon and trout eggs, dissolved oxygen levels below 11 mg/L will delay their hatching, and below 8 mg/L will impair their growth and lower their survival rates. ¹⁹ When dissolved oxygen falls below 6 mg/L (considered normal for most other fish), the vast majority of trout and salmon eggs will die. ¹⁹
# 
# Billfish swim in areas with a minimum of 3.5 mg/L DO, while marlins and sailfish will dive to depths with DO concentrations of 1.5 mg/L ³⁰. Furthermore, white sharks are also limited in dive depths due to dissolved oxygen levels (above 1.5 mg/L).  Albacore tuna live in mid-ocean levels and require a minimum of 2.5 mg/L ³⁵, while halibut can maintain a minimum DO tolerance threshold of 1 mg/L ³⁶.
# 
# Crustaceans (e.g. crabs and lobsters) require minimum levels of dissolved oxygen depending on the species. Minimum DO requirements can range from 4 mg/L to 1 mg/L ¹³.  Mussels, oysters and clams also require a minimum of 1-2 mg/L of dissolved oxygen (EPA, 2000).
# <img src="https://www.fondriest.com/environmental-measurements/wp-content/uploads/2013/11/dissolvedoxygen_levels-salt.jpg" alt="Alt text that describes the graphic" title="Title text" />
# 
# 
# ## Temperature
# 
# Temperature limits the amount of oxygen that can dissolve in water: water can hold more oxygen during winter than during the hot summer months. However, even at the warmest temperatures seen in the Bay (around 91F), water is capable of having dissolved oxygen concentrations of 6 to 7 mg/L (Chesapeake Bay Program, Dissolved Oxygen). 
# 
# 
# ## Impact on living organisms on the ocean
# 
# According to the Atlantic Salmon Federation (2019), Canada's Cooke confirms that it has lost about 10,000 Atlantic salmon due to a “super chill” event at its Kelly Cove Salmon site off the coast of Coffin Island, in Nova Scotia. February and March are the coldest months of the year for seawater temperatures in Atlantic Canada and salmon farmers have been nervously keeping an eye on their stocks in the meantime. During most winters, Nova Scotia's marine waters stay above freezing holding cold air temperatures can drop the water below 0 Celsius, to the temperature that fish blood freezes, around -0.7 C.
# 
# A number of chemical reactions start immediately after the death of the fish. These include reactions that are responsible for how fish quality changes during chilled storage, such as: Rigor mortis, where death terminates the supply of oxygen to the muscle; Protein changes, once the post-mortem degradation of proteins is one of the most important processes influencing the textural quality of fish muscle (Delbarre-Ladrat et al., 2006); Lipid changes, that may produce a range of substances during post-mortem events (Undeland, 1997); and Microbial changes, where the influence on the chilled fish induces bacterial growth until the specific spoilage organisms have increased to a certain level (Gram and Huss, 1996).
# 
# ## Conlusion
# 
# Just like humans, all of the marine living creatures need oxygen to survive. Humans use their lungs to inhale oxygen from the air, but worms, fish, crabs and other underwater animals use gills to get oxygen from the water or through diffusion. These organisms breathe and develop better when there is more oxygen in the water. As dissolved oxygen levels decrease, it becomes harder for animals to get the oxygen they need to survive.
# 
# Using the sensor strings available around Nova Scotia, it is possible to predict and anticipate how and when these events may occur. It may also be helpful to optimize and maintain healthy fish living in the farms during infrequent events such as ‘super chill’.
# 
# 

# In[2]:


import pandas as pd
import os
from erddapy import ERDDAP
import numpy as np

IDlist = ['wpsu-7fer','knwz-4bap',
                  'eb3n-uxcb','x9dy-aai9','a9za-3t63','eda5-aubu','adpu-nyt8','v6sa-tiit','mq2k-54s4','9qw2-yb2f']
stationdict = {}
e = ERDDAP(server="https://dev.cioosatlantic.ca/erddap",
                 protocol="tabledap", )
e.auth = ("cioosatlantic", "4oceans")
e.response = "csv"
for val in IDlist:
    e.dataset_id = val
    e.variables = ['waterbody_station']
    df = e.to_pandas()
    df.waterbody_station= df.waterbody_station.astype(str)
    stations = sorted(list(df.waterbody_station.unique()))
    for i in range(len(stations)):
        stationdict[stations[i]]= val

stationlist = list(stationdict.keys())
        


# In[3]:


def getdata(station_name):
    e = ERDDAP(server="https://dev.cioosatlantic.ca/erddap",
                 protocol="tabledap", )
    e.auth = ("cioosatlantic", "4oceans")
    e.response = "csv"
    e.variables = ['waterbody_station', 'latitude', 'longitude', 'time', 'Temperature', 'Dissolved_Oxygen', 'depth']
    e.dataset_id = stationdict.get(station_name)
    e.constraints = {"waterbody_station=":station_name}
    df = e.to_pandas()
    df = df.sort_values(by=['time (UTC)'])
    df['time (UTC)'] = pd.to_datetime(df['time (UTC)'], format="%Y-%m-%dT%H:%M:%SZ")
    df = df.set_index(df['time (UTC)'].astype(np.datetime64))
    df['DO mg/L']  = ((df['Temperature (degrees Celsius)']*0.0026)**2-(df['Temperature (degrees Celsius)']*0.2567)+11.698)*(df['Dissolved_Oxygen (% saturation)']/100)
    df = df.rename(columns={'depth (m)': "depth"})
    df = df.rename(columns={'latitude (degrees_north)': "latitude"})
    df = df.rename(columns={'longitude (degrees_east)': "longitude"})
    df = df.rename(columns={'Temperature (degrees Celsius)':'Temperature'})
    df = df.rename(columns={'Dissolved_Oxygen (% saturation)': 'DO %'})
    df.depth= df.depth.astype('category')
    
    return df


# In[4]:


import panel as pn
import holoviews as hv
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.models import CategoricalColorMapper
from datashader.colors import Greys9, Hot, Elevation, Sets1to3
import datashader as ds
import holoviews.operation.datashader as hd
import hvplot.pandas


hv.extension("bokeh")
pn.extension(sizing_mode='fixed')



depthlist = list(range(1,32))
varlist = ['Temperature (degrees Celsius)', 'Dissolved_Oxygensizing_mode (% saturation)']

station_selector = pn.widgets.Select(name="Select Station", options = stationlist, value=stationlist[0], width=800,)


############################################################################################################
tileopts = hv.opts.Tiles(width=400, height=400, projection=True )
tiles = hv.element.tiles.EsriImagery().opts(tileopts)

def geoplot(station_name):
    data = getdata(station_name)
    locations = data.groupby('waterbody_station')['longitude', 'latitude'].mean()
    x, y = ds.utils.lnglat_to_meters(locations.longitude, locations.latitude)
    stationlocation = locations.assign(x=x,y=y)
    plotlocs = stationlocation.hvplot.points('x','y',hover_cols=['waterbody_station']).opts(color='red')
    mapplot = (tiles*plotlocs).options(xlim=(-7.05e6, -7e6), ylim=(5.2e6, 6e6), aspect='equal', xaxis=None,yaxis=None,
                                      active_tools=['pan', 'wheel_zoom'], toolbar=None)
    return mapplot

def updategeo(target, event):
    target.object = geoplot(event.new)
    
geopane = pn.pane.HoloViews(geoplot(station_selector.value), background='#dbefe1', )

station_selector.link(geopane, callbacks ={"value":updategeo})
###########################################################################################################
opts = dict(show_grid=True, frame_height=450, frame_width=1100,
            xformatter=DatetimeTickFormatter(months='%b %Y' ,days="%b/%d",hours="%H:%M",minutes="%H:%M"), tools = ["hover"], bgcolor='white')

colors = Elevation+Hot+Greys9+Sets1to3[0:5]
colorkey = dict(zip(depthlist, colors))


def plot(station_name):
    data = getdata(station_name)
    plottemp = data.hvplot.points(x='time (UTC)', y='Temperature', c='depth',
                                  color_key = colorkey, 
                                   datashade=True, 
                                   aggregator= ds.count_cat('depth')).opts(**opts)
    
    spreadtemp = hd.dynspread(plottemp, threshold=.999, max_px=2).opts(bgcolor='white', 
                        width=1000, height=450, show_grid=True,tools = ["hover"],alpha=1)
    plotoxy = data.hvplot.points(x='time (UTC)',y= 'DO mg/L' , c='depth',
                                  color_key = colorkey, datashade=True, 
                                   aggregator= ds.count_cat('depth') ).opts(**opts)
    spreadoxy = hd.dynspread(plotoxy, threshold=.999, max_px=2).opts(bgcolor='white', 
                        width=1000, height=450, show_grid=True,tools = ["hover"],alpha=1)
    #oxylimit1 = hv.HLine(6).opts(color='red', line_dash='dashed', line_width=4.0)*hv.Text(data['time (UTC)'].median(),6.2, "oxygen limit for x" )
    oxyspan = hv.HSpan(0,6).opts(fill_color='red' )
    tempspan = hv.HSpan(-100, -0.7).opts(fill_color='blue', alpha=0.5)
    

    
    plots = (spreadtemp*tempspan+spreadoxy*oxyspan).opts(shared_axes=True, toolbar='right')
    return plots.cols(1)



def updatestation(target, event):
    plotpane.loading = True
    target.object = plot(event.new)
    plotpane.loading = False


plotpane = pn.pane.HoloViews(plot(station_selector.value) ,background='#dbefe1', )

station_selector.link(plotpane, callbacks={"value":updatestation})

########################################################################################################
def title(station_name):
    title = station_name
    return title

def updatetitle(target, event):
    target.object = title(event.new)

titlepane = pn.pane.Markdown(title(station_selector.value), align='center',style={'font-size':'40px', 'font-family':'Quicksand'}, background='#dbefe1', width=500, height=100)

station_selector.link(titlepane, callbacks = {"value":updatetitle})
#######################################################################################################
ciooslogo = pn.pane.SVG('https://cioosatlantic.ca/wp-content/themes/cioos-siooc-wordpress-theme/img/atlantic/cioos-atlantic_EN.svg?x70378'
                   , width=400, link_url="https://cioosatlantic.ca/", embed =True)

if os.path.exists("CMARlogo.png"):
    cmarlogo = pn.panel("CMARlogo.png", width = 400)
#canadamap = pn.panel('https://choosebetter.me/images/unnamed.png', width=400)
if os.path.exists("canadamap.png"):
    canadamap = pn.panel("canadamap.png", height=400, width=400)
#'No machine-readable author provided. Golbez assumed (based on copyright claims)., CC BY-SA 3.0 <http://creativecommons.org/licenses/by-sa/3.0/>, via Wikimedia Commons'

if os.path.exists("tempsensor.png"):
    oxysensor = pn.panel("oxysensor.png", height=350)
# Adapted from https://www.innovasea.com/wp-content/uploads/2021/10/Innovasea-Aquaculture-Intelligence-Spec-Sheet.pdf

if os.path.exists("tempsensor.png"):
    tempsensor = pn.panel("tempsensor.png", height=350)

widgets = pn.WidgetBox(pn.Column(station_selector, width = 825),align = 'center')
rightcolumn = pn.Column(pn.Spacer(height=225),oxysensor,pn.Spacer(height=100),tempsensor)
midcolumn = pn.Column( titlepane, widgets, plotpane)
leftcolumn = pn.Column(canadamap,pn.Spacer(height=50), geopane ,pn.Spacer(height=50),ciooslogo, cmarlogo)
dashboard = pn.Row(leftcolumn, pn.Spacer(width=200),midcolumn, pn.Spacer(width=200),rightcolumn,background='#dbefe1',)

dashboard.servable()


# ## References
# 
# [1]American Public Health Assoc., American Water Works Assoc. & Water Environment Federation. (1999). Standard Methods for the Examination of Water and Wastewater (20th ed.). Baltimore, MD: American Public Health Association.
# 
# [2]Canadian Integrated Ocean Observing System (CIOOS Atlantic), 2019. Retrieved October 20, 2021, from https://cioosatlantic.ca/.
# 
# [3]Carter, K. (2005, August). The Effects of Dissolved Oxygen on Steelhead Trout, Coho Salmon, and Chinook Salmon Biology and Function by Life Stage. In California Regional Water Quality Control Board, North Coast Region. Retrieved from http://www.swrcb.ca.gov/northcoast/water_issues/programs/tmdls/shasta_river/060707/29appendixbetheeffectsofdissolvedoxygenonsteelheadtroutcohosalmonandchinooksalmonbiologyandfunction.pdf
# 
# [4]Centre for Marine Applied Research (CMAR), 2017. Retrieved October 20, 2021, from https://cmar.ca/.
# 
# [5]Chesapeake Bay Program. Dissolved Oxygen. Retrieved October 20, 2021 from https://www.chesapeakebay.net/discover/ecosystem/dissolved_oxygen
# 
# [6]Cold Temperatures Causing Problems on Fish Farms, Fisheries and Aquaculture March 3, 2015. Retrieved October 20, 2021 from https://novascotia.ca/news/release/?id=20150303003
# 
# [7]Courtney, D., & Brodziak, J. (2010). Oceanographic Features in the Vicinity of a North Pacific Swordfish Stock Boundary. Honolulu, HI: NOAA Fisheries, Pacific Islands Fisheries Science Center. Retrieved from http://isc.ac.affrc.go.jp/pdf/BILL/ISC10_BILL_1/BILL_Apr10_FINAL_WP04.pdf
# 
# [8]Dissolved Gases – Oxygen. (n.d.). In Lecture – Water Chemistry. Retrieved from http://www.esf.edu/efb/schulz/Limnology/Oxygen.html
# 
# [9]Dissolved Oxygen. (n.d.). In Chesapeake Bay Program. Retrieved from http://www.chesapeakebay.net/discover/bayecosystem/dissolvedoxygen
# 
# [10]EOL. (n.d.). Xiphias gladius; Swordfish. In Encyclopedia of Life. Retrieved from http://eol.org/pages/206878/details
# 
# [11]EPA. (1986). Quality Criteria for Water. Washington DC: Office of Water Regulations and Standards.
# 
# [12]EPA. (2000, November). Ambient Aquatic Life Water Quality Criteria for Dissolved Oxygen (Saltwater): Cape Cod to Cape Hatteras. 
# 
# [13]Washington DC: Office of Water: Office of Science and Technology. Retrieved from http://water.epa.gov/scitech/swguidance/standards/upload/2007_03_01_criteria_dissolved_docriteria.pdf
# 
# [14]EPA. (2012). 5.2 Dissolved Oxygen and Biochemical Oxygen Demand. In Water Monitoring and Assessment. Retrieved from http://water.epa.gov/type/rsl/monitoring/vms52.cfm
# 
# [15]Fisheries and Aquaculture Department. (2000). Biological characteristics of tuna. In FAO Fisheries and Aquaculture Department. Retrieved from http://www.fao.org/fishery/topic/16082/en
# 
# [16]Fondriest Environmental, Inc. “Dissolved Oxygen.” Fundamentals of Environmental Measurements. 19 Nov. 2013. Retrieved October 20, 2021 from https://www.fondriest.com/environmental-measurements/parameters/water-quality/dissolved-oxygen/.
# 
# [17]HUFFMAN , J. Cooke experiences ‘super chill’ event off Nova Scotia coast. Mar 17, 2019. Retrieved October 20, 2021 from https://www.asf.ca/news-and-magazine/salmon-news/cooke-experiences-super-chill-event-off-nova-scotia-coast
# 
# [18]Nasby-Lucas, N., Dewar, H., Lam, C. H., Goldman, K. J., & Domeier, M. L. (2009, December). White Shark Offshore Habitat: A Behavioral and Environmental Characterization of the Eastern Pacific Shared Offshore Foraging Area. In PLOS ONE. Retrieved from http://www.plosone.org/article/info%3Adoi%2F10.1371%2Fjournal.pone.0008163
# 
# [19]Plant Growth Factors: Photosynthesis, Respiration, and Transpiration. (2013). In CMG Garden Notes. Retrieved from http://www.ext.colostate.edu/mg/gardennotes/141.html
# 
# [20]Sadorus, L. L. (2012). The influence of environmental factors on halibut distribution as observed on the IPHC stock assessment survey: A preliminary examination. Report of Assessment and Research Activities. Retrieved from http://www.iphc.int/publications/rara/2012/rara2012401_environ_haldist.pdf
# 
# [21]Watt, M. K. (2000). A Hydrologic Primer for New Jersey Watershed Management (Water-Resources Investigation Report 00-4140). West Trenton, NJ: U.S. Geological Survey.
# 

# In[ ]:




