# %%
import pandas as pd
import os
import numpy as np
import re

# %%
from erddapy import ERDDAP

# %%
IDlist = [
            'FORCE_Mar2018_ADCP_Currents',
    'FORCE_Mar2018_ADCP_Waves'
   #'force_3b1e_d478_b537' 3rd Dataset whhich is not found in cioos erdapp 
]

e = ERDDAP(server="https://dev.cioosatlantic.ca/erddap",
                 protocol="tabledap", )
e.auth = ("cioosatlantic", "4oceans")
e.response = "csv"

# %%
datasetdict = {}
unitdict = {}

# %%
for val in IDlist:
    e.dataset_id = val
    e.constraints = { "time<=": "2018-03-30T20:17:33Z",
                    }
    df = e.to_pandas()
    for col in df.columns:      
        if len(df[col].unique()) == 1:          
            df.drop([col], axis=1, inplace=True) 
    
    variables = list(df.columns)
    for i in range(len(variables)):
        variables[i] =  re.sub(r'\(.*?\) *', '', variables[i])
        
    variablelist = list(df.columns)
    newdict = dict(zip(variables, variablelist))
    unitdict.update(newdict)
    
    for i in range(len(variables)):
        datasetdict[variables[i]] = val
del unitdict['time ']          

# %%
def getdata(varname):
    e = ERDDAP(server="https://dev.cioosatlantic.ca/erddap",
                 protocol="tabledap", )
    e.auth = ("cioosatlantic", "4oceans")
    e.response = "csv"
    e.dataset_id = datasetdict.get(varname)
    e.variables = ['time', varname]
    e.constraints = {"time<=": "2018-05-23T17:47:30Z", "time>=": '2018-03-30T20:02:33Z'}
    df = e.to_pandas()
    df = df.sort_values(by=['time (UTC)'])
    df['time (UTC)'] = pd.to_datetime(df['time (UTC)'], format="%Y-%m-%dT%H:%M:%SZ")
    df = df.set_index(df['time (UTC)'].astype(np.datetime64))
    if varname == 'eastward_sea_water_velocity ' or 'upward_sea_water_velocity ' or 'northward_sea_water_velocity ':
        df = df[df[unitdict[varname]] !=0]
    if varname == 'sea_surface_wave_maximum_period ':
        df = df[df[unitdict[varname]] !=-9]
    return df


print(df)

# %%
import datetime as dt
import hvplot.pandas
import panel as pn
from holoviews import opts
import datashader as ds
import holoviews.operation.datashader as hd
from bokeh.models.formatters import DatetimeTickFormatter
import holoviews as hv

# %%

pn.extension(css_files=['https://fonts.googleapis.com/css?family=Quicksand'])


opts = dict(show_grid=True, frame_height=350, frame_width=800,shared_axes=False,
            xformatter=DatetimeTickFormatter(months='%b %Y' ,days="%b/%d",hours="%H:%M",minutes="%H:%M"), tools = ["hover"], bgcolor='white')


def plotVar(varname, start, end):
    data = getdata(varname)
    start = dt.date(start.year,start.month,start.day)
    end = dt.date(end.year,end.month,end.day)
    data = data.loc[start:end]
    
    plot = data.hvplot.scatter(x = 'time (UTC)', y = unitdict[varname] , datashade = True, aggregator = 'mean').opts(**opts)
    spreadplot = hd.dynspread(plot, threshold=.999, max_px=2)
    histogram = data.hvplot.hist(unitdict[varname], width =860,height=250, bins = 100, normed = True, ).opts(show_grid=True, shared_axes=False)
    plots = (spreadplot+histogram).opts(toolbar='right')
    return plots.cols(1)


var_selector = pn.widgets.Select(name = "Select Variable:", options = list(unitdict.keys()), value = list(unitdict.keys())[0] )

date_picker_start = pn.widgets.DatetimePicker(name='Start:', 
                        enable_time=False,
                        start=dt.date(2018, 3, 30), 
                        end = dt.date(2018,5,24), 
                        value = dt.datetime(2018,4,1)                      
                                             )

date_picker_end = pn.widgets.DatetimePicker(name='End:',
                        enable_time=False, 
                        start=dt.date(2018, 3, 30), 
                        end = dt.date(2018,5,24), 
                        value = dt.datetime(2018,4,7)
                                           )
def update(event):
    main.loading = True
    main[3].object = plotVar(var_selector.value,date_picker_start.value, date_picker_end.value)
    main.loading=False


button = pn.widgets.Button(name="Update", button_type="primary")
button.on_click(update)

plotpane = pn.pane.HoloViews(plotVar(var_selector.value,date_picker_start.value, date_picker_end.value))
main = pn.Column(var_selector ,pn.Row(date_picker_start,date_picker_end),button ,plotpane)

###

tileopts = hv.opts.Tiles(width=365, height=350, projection=True )
tiles = hv.element.tiles.OSM().opts(tileopts)
gdata =[[-7172033.398401788, 5678872.595825182]]
geodata = pd.DataFrame(gdata, columns = ['x','y'])
geoplot = geodata.hvplot.points('x','y', color='red', alpha = 1).opts(width=365, height=350, size=5)
mapplot = (tiles*geoplot).options(xlim=(-7.05e6, -7e6), ylim=(5.2e6, 6e6), aspect='equal', xaxis=None,yaxis=None,
                                      active_tools=['pan', 'wheel_zoom'], toolbar=None)

geopane = pn.pane.HoloViews(mapplot)
###

c = ERDDAP(server="https://dev.cioosatlantic.ca/erddap",
                 protocol="tabledap", )
c.auth = ("cioosatlantic", "4oceans")
c.response = "csv"
c.dataset_id = 'FORCE_Mar2018_ADCP_Currents'
c.constraints = { "time<=": "2018-05-23T17:47:30Z", 
                  "time>=": '2018-03-30T20:02:33Z',
                 "eastward_sea_water_velocity!=":0,
               #  "upward_sea_water_velocity!=":0,
                 "northward_sea_water_velocity!=":0,
                }
c.variables = ['time',
               'eastward_sea_water_velocity',
               'northward_sea_water_velocity',
               'cell_range'
               ]
df1 = c.to_pandas()
df1['time (UTC)'] = pd.to_datetime(df1['time (UTC)'], format="%Y-%m-%dT%H:%M:%SZ")
###

X = df1.iloc[:,1:3].values
covariance_matrix = np.cov(X.T)
eigen_values, eigen_vectors = np.linalg.eig(covariance_matrix)

variance_explained = []
for i in eigen_values:
     variance_explained.append((i/sum(eigen_values))*100)

cumulative_variance_explained = np.cumsum(variance_explained)

projection_matrix = (eigen_vectors.T[:][:1]).T

X_pca = X.dot(projection_matrix)

df_pca = pd.DataFrame(X_pca, columns = ['Channel Velocity (m/s)'])

fulldata = pd.concat([df1, df_pca], axis=1)
fulldata = fulldata.sort_values(by=['time (UTC)'])
fulldata = fulldata.set_index(fulldata['time (UTC)'].astype(np.datetime64))
fulldata.index.name = 'time'


def channelplot(start, end):
    data1 = fulldata.copy()
    start = dt.date(start.year,start.month,start.day)
    end = dt.date(end.year,end.month,end.day)
    data = data1.loc[start:end]
    
    scatter = data.hvplot.scatter(x = 'time (UTC)', y=['Channel Velocity (m/s)'], cmap = 'Reds'
                               ,datashade=True,height=335, width=510,aggregator = 'mean').opts(
                                    tools=['hover'],xformatter=DatetimeTickFormatter(months='%b %Y' ,days="%b/%d",hours="%H:%M",minutes="%H:%M"))

    channelplot = hd.dynspread(scatter, threshold=.999, max_px=2).opts(show_grid=True)
    
    heatmap = data.hvplot.heatmap(x='time (UTC)',y='cell_range (m)', C = 'Channel Velocity (m/s)',height=335, 
                                  width=510, colorbar=True, cmap = 'Spectral', clim = (-3,3), 
                                     ylim =(0,data['cell_range (m)'].max()) ).opts(show_grid=True,
                                    tools=['hover'],xformatter=DatetimeTickFormatter(months='%b %Y' ,days="%b/%d",hours="%H:%M",minutes="%H:%M"))
    
    channel_plots = (channelplot + heatmap).opts(toolbar='right')
    return channel_plots.cols(1)

    
    return heatmap.aggregate(function=np.mean)


date_picker_start2 = pn.widgets.DatetimePicker(name='Start:', 
                        enable_time=False,
                        start=dt.date(2018, 3, 30), 
                        end = dt.date(2018,5,24), 
                        value = dt.datetime(2018,4,1)                      
                                             )

date_picker_end2 = pn.widgets.DatetimePicker(name='End:',
                        enable_time=False, 
                        start=dt.date(2018, 3, 30), 
                        end = dt.date(2018,5,24), 
                        value = dt.datetime(2018,4,7))

button2 = pn.widgets.Button(name='Update', button_type = 'primary')


def updatechannel(event):
    channelpane.loading = True
    channel[1].object = channelplot(date_picker_start2.value, date_picker_end2.value)
    channelpane.loading= False


button2.on_click(updatechannel)
    
times = pn.Column(pn.Column(date_picker_start2,date_picker_end2,width = 225,sizing_mode = 'stretch_width'),
                  button2, width = 225, sizing_mode = 'stretch_width')
channelpane = pn.pane.HoloViews(channelplot(date_picker_start2.value, date_picker_end2.value))

channel = pn.Column(times,channelpane)
###

moreinfo = pn.pane.HTML(""" 
<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.6.1/css/all.css">

<style>
.tooltip {
  position: relative;
  display: inline-block;
}

.tooltip .tooltiptext {
  visibility: hidden;
  width: 600px;
  background-color: black;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px 0;
  position: absolute;
  z-index: 1;
  top: -5px;
  right: 110%;
}

.tooltip .tooltiptext::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 100%;
  margin-top: -5px;
  border-width: 5px;
  border-style: solid;
  border-color: transparent black transparent transparent;
}
.tooltip:hover .tooltiptext {
  visibility: visible;
}
</style>
<body style="text-align:center;">

<a href="https://github.com/RineZaman/FORCE-Visualization" target="_blank" title="GitHub Repository"><i class="fab fa-github" style='font-size:30px'></i></a>
<a href="https://twitter.com/CIOOSAtlantic?s=20" target="_blank" title="Twitter"><i class="fab fa-twitter-square" style='font-size:30px'></i>
<div class="tooltip">
  
  <a href="https://dev.cioosatlantic.ca/erddap/search/advanced.html?page=1&itemsPerPage=1000&searchFor=FORCE&protocol=%28ANY%29&cdm_data_type=%28ANY%29&institution=%28ANY%29&ioos_category=%28ANY%29&keywords=%28ANY%29&long_name=%28ANY%29&standard_name=%28ANY%29&variableName=%28ANY%29&maxLat=&minLon=&maxLon=&minLat=&minTime=&maxTime=" target="_blank" ><i class="fas fa-info-circle" style='font-size:30px'></i>

  <span class="tooltiptext">This seabed-mounted ADCP, deployed for two months in spring 2018, collected 3-D velocity profiles and surface wave statistics at a location within the FORCE Crown Lease Area. Data are provided in raw (*ad2cp) form, and as processed currents and waves. These data were collected as part of a project on evaluating fish sensor capabilities at high flow sites.</span>
</div>
<p>ERDDAP Access</p>
</body>
""", align = 'start')
###

titlepane = pn.pane.Markdown('FORCE ADCP Data Visualization',align='start',style={'font-size':'50px', 'font-family':'Quicksand'}, background='#dbefe1',width = 750,)
ciooslogo = pn.pane.SVG('https://cioosatlantic.ca/wp-content/themes/cioos-siooc-wordpress-theme/img/atlantic/cioos-atlantic_EN.svg?x70378'
                   , width=350, link_url="https://cioosatlantic.ca/", align='center')
if os.path.exists("canadamap.png"):
    canadamap = pn.panel("canadamap.png", height=350, width=350, align='center')

if os.path.exists("FORCE_logo.png"):
    forcelogo = pn.panel("FORCE_logo.png",  width=300, align='center')
    
col1 = pn.Column(canadamap,pn.layout.VSpacer(),geopane,pn.layout.VSpacer(),forcelogo,ciooslogo)
row1 = pn.Row(titlepane,pn.Spacer(width=610),moreinfo)
row2 = pn.Row(main, pn.Spacer(width=20),channel,pn.Spacer(width=20))
col2 = pn.Column(row1,pn.layout.Divider(),row2)
dashboard = pn.Row(col1,pn.Spacer(width=20),col2,background='#dbefe1', )

dashboard.servable()

# %%
import plotly.express as px
from datetime import date
import dash_core_components as dcc
import dash
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# %%
print(datasetdict)

df1 = getdata('sea_water_pressure ')
print(df1)

print(unitdict.items())

# %%

##'northward_sea_water_velocity (m/s)'] but received: northward_sea_water_velocity
# for v1, v2 in unitdict.items():
#     if v1 == "northward_sea_water_velocity ":
#         print(v2)
df['Date']=pd.to_datetime(df['time (UTC)'])
df['Month']=df['Date'].dt.month
df['Day']=df['Date'].dt.day
print(df['Month'])
#print(df['Month'])


# %%
footrtxt = "The Fundy Ocean Research Centre for Energy (FORCE) is Canada's leading research centre for tidal stream energy, located in the Bay of Fundy, Nova Scotia."
app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.Center(html.H3(["A Regional Association of CIOOS"]), className= 'topnav'),

    html.Br(),
    html.Center(html.Img(src='https://cioosatlantic.ca/wp-content/themes/cioos-siooc-wordpress-theme/img/atlantic/cioos-atlantic_EN.svg?x70378',
    style={'height': '20%','width': '30%'})),
    html.H3('The Canadian Integrated Ocean Observing System (CIOOS) is a powerful open-access platform for sharing information about the state of our oceans', style={'text-align':'center'}),
    
    html.H1([dcc.Link('Hurricane Visualizations', href=''),
    ], className='topnav'),

    html.H3('About the Dataset:'), 
    html.P('This seabed-mounted Acoustic Doppler Current Profiler (ADCP), deployed for two months in spring 2018, collected 3-D velocity profiles and surface wave statistics at a location within the FORCE Crown Lease Area. Data are provided in raw (*ad2cp) form, and as processed currents and waves. These data were collected as part of a project on evaluating fish sensor capabilities at high flow sites (cf. Viehman et al 2019 in the metadata attachment).'),
    html.Br(),

    dcc.Dropdown(id= "dropdown", options=[
        {'label': j, 'value': i}
        for i,j in unitdict.items()],
        #list(unitdict)], value = list(unitdict.keys())[0],
        value= "sea_water_temperature", multi=False, searchable= True, placeholder= "Select.."),
    
    html.Br(),

    dcc.Dropdown(id= "dropdown2", options=[
        {'label': j, 'value': i}
        for i,j in unitdict.items()],
        #list(unitdict)], value = list(unitdict.keys())[0],
        value= "sea_water_temperature", multi=False, searchable= True, placeholder= "Select.."),

    html.Br(),
    
    dcc.DatePickerRange(id= "datepicker",
    min_date_allowed= date(2018, 3, 30),
    max_date_allowed= date(2018, 5, 24),
    start_date= date(2018, 4, 1),
    end_date= date(2018, 4, 7),
    start_date_placeholder_text= "Start Period",
    end_date_placeholder_text= "End Period",
    reopen_calendar_on_clear= True,
    clearable= True, 
    calendar_orientation="horizontal"),

    html.Br(),
    html.P('The following chart shows the comparison of the 2 attributes selected from Dropdown 1 and Dropdown 2'),
    
    dcc.Graph(id="linegraph_multiple", figure={}, 
        config = {
        "staticPlot": False,
        "scrollZoom": True,
        "doubleClick": "reset",
        "showTips": True,
        "displayModeBar": True
    }),

    html.Br(),
    html.P('The following charts show the 2 attributes selected from Dropdown 1 and Dropdown 2 separately'),
    html.Br(),
    dcc.Graph(id="linegraph_1", figure={}, 
        config = {
        "staticPlot": False,
        "scrollZoom": True,
        "doubleClick": "reset",
        "showTips": True,
        "displayModeBar": True
    }),

    html.Br(),

    dcc.Graph(id="linegraph_2", figure={}, 
        config = {
        "staticPlot": False,
        "scrollZoom": True,
        "doubleClick": "reset",
        "showTips": True,
        "displayModeBar": True
    }),

    html.Br(),

    dcc.RangeSlider(id="rangeslider", 
        marks = {
        3: {'label': 'March', 'style': {'color': '#000000', 'font': 'bold'}},
        4: {'label': 'April', 'style': {'color': '#000000', 'font': 'bold'}},
        5: {'label': 'May', 'style': {'color': '#000000', 'font': 'bold'}},
    },
    min = 3,
    max = 5,
    step = 1,
    dots = True,
    value = [3,4],
    updatemode = 'drag', 
    included = True,
    tooltip = {'always visible': False, 'placement': 'bottom'}
    ),

    html.Br(),

    html.P('The following box plots show 2 attributes selected from Dropdown 1 and Dropdown 2 separately to depict the variations in the day for the range of months selected in the Range Slider'),
    html.Br(),

    dcc.Graph(id="bargraph_slider1", figure={}, 
        config = {
        "staticPlot": False,
        "scrollZoom": True,
        "doubleClick": "reset",
        "showTips": True,
        "displayModeBar": True
    }),

    html.Br(),

    dcc.Graph(id="bargraph_slider2", figure={}, 
        config = {
        "staticPlot": False,
        "scrollZoom": True,
        "doubleClick": "reset",
        "showTips": True,
        "displayModeBar": True
    }),

    html.Br(),

    html.Footer(
        [html.Center([
            html.Img(src='assets/FORCE_logo.png',style={'height': '20%','width': '30%','margin-bottom': '-20px'}),
            html.H3(footrtxt), 
            html.Br()])
        ], className = 'body')


])

@app.callback(
    [Output(component_id= "linegraph_multiple", component_property= "figure"), Output(component_id= "linegraph_1", component_property= "figure"), Output(component_id= "linegraph_2", component_property= "figure"), Output(component_id="bargraph_slider1", component_property="figure"), Output(component_id="bargraph_slider2", component_property="figure")],
    [Input(component_id="dropdown", component_property="value"), Input(component_id="dropdown2", component_property="value"), Input(component_id="datepicker", component_property="start_date"), 
        Input(component_id="datepicker", component_property="end_date"), Input(component_id="rangeslider", component_property="value")]
)


# def update_graph(selected_geography):
#     filtered_avocado = avocado[avocado["geography"] == selected_geography]
#     fig = px.line(filtered_avocado, x = "date", y = "average_price", color= "type",
#     title= f"Avocado Prices in {selected_geography}" )
#     return fig



def plot(dpvalue1, dpvalue2, start_date, end_date, months):
    #start_date = dt.date(start_date.year,start_date.month,start_date.day)
    #end_date = dt.date(end_date.year,end_date.month,end_date.day)
    #value1= f"'{value} '"
    
    dropdown1_data= getdata(dpvalue1)
    dropdown2_data= getdata(dpvalue2)
    slider_data1= getdata(dpvalue1)
    slider_data2= getdata(dpvalue2)
    #frames = [dropdown1_data, dropdown2_data]
    #combined_data = pd.concat(frames)

    for v1, v2 in unitdict.items():
        if v1 == dpvalue1:
            dpvalue1_1 = v2

    for v1, v2 in unitdict.items():
        if v1 == dpvalue2:
            dpvalue2_1 = v2
    
    dropdown2_data = dropdown2_data.loc[start_date:end_date]
    dropdown1_data = dropdown1_data.loc[start_date:end_date]
    #dfff = dfff.loc[months[1]:months[0]]

    start_date1 = "2018"+"-"+"0"+str(months[0])+"-"+"01"
    start_date1 =pd.to_datetime(start_date1)
    end_date1 = "2018"+"-"+"0"+str(months[1])+"-"+"30"
    end_date1 =pd.to_datetime(end_date1)
    slider_data1 = slider_data1.loc[start_date1:end_date1]
    slider_data2 = slider_data2.loc[start_date1:end_date1]
    
    
    # print(slider_data.columns)
    # print("\n")
    #slider_data.drop(slider_data.columns[0], axis=1, inplace=True)
    #print("Number and names of coolumns:",slider_data.columns)
    #print("\n")
    #columnName = slider_data.iloc[1] 
    # colName1 = slider_data.columns[0]
    # colName2 = slider_data.columns[1]   
    # print("Column Name is:",colName1)
    # print("Column Name is:",colName2) 
    # count_row = slider_data.shape[0] 
    # print("Number of Initial Rows:",count_row)   
    # print("_______________END 1 _________________")
    #slider_data.set_index('time (UTC)',inplace=True) 
    #slider_data.groupby([colName1, colName2 ]).mean()
    # result = slider_data.groupby([slider_data['time (UTC)'].dt.year, df['time (UTC)'].dt.month]).agg({colName2:sum})
    # print(result)
    #slider_data.groupby(slider_data.time(UTC).dt.month)[colName2].mean()
    # count_row1 = slider_data.shape[0]
    # print("Number of Final Rows:",count_row1)
    #slider_data.groupby(slider_data['time (UTC)'].dt.day)[columnName].mean()


    linegraph_multiplefig= make_subplots(specs= [[{'secondary_y': True}]])
    linegraph_multiplefig.add_trace(
        go.Scatter(x= dropdown1_data['time (UTC)'], y= dropdown1_data[dpvalue1_1], name= dpvalue1_1),
        secondary_y=False,
    )
    linegraph_multiplefig.add_trace(
        go.Scatter(x= dropdown2_data['time (UTC)'], y= dropdown2_data[dpvalue2_1], name= dpvalue2_1),
        secondary_y=True,
    )

    linegraph_1fig = px.line(data_frame = dropdown1_data, x = "time (UTC)", y = dpvalue1_1 )
    linegraph_2fig = px.line(data_frame = dropdown2_data, x = "time (UTC)", y = dpvalue2_1 )

    slider_data1['Date']= pd.to_datetime(slider_data1['time (UTC)']).dt.date
    slider_data1.drop(slider_data1.columns[0], axis=1, inplace=True)
    slider_data2['Date']= pd.to_datetime(slider_data2['time (UTC)']).dt.date
    slider_data2.drop(slider_data2.columns[0], axis=1, inplace=True)

    bargraph_slider1fig = px.box(data_frame = slider_data1, x = "Date", y = dpvalue1_1 )
    bargraph_slider2fig = px.box(data_frame = slider_data2, x = "Date", y = dpvalue2_1 )

    return linegraph_multiplefig, linegraph_1fig, linegraph_2fig, bargraph_slider1fig, bargraph_slider2fig


   

#sts 

# def update_output(value, start_date, end_date):
    
#     string_prefix = "You have selected: {}".format(value, start_date, end_date)

#     if start_date is not None:
#         start_date_object = date.fromisoformat(start_date)
#         start_date_string = start_date_object.strftime('%B %d, %Y')
#         string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
#     if end_date is not None:
#         end_date_object = date.fromisoformat(end_date)
#         end_date_string = end_date_object.strftime('%B %d, %Y')
#         string_prefix = string_prefix + 'End Date: ' + end_date_string
#     if len(string_prefix) == len('You have selected: '):
#         return 'Select a date to see it displayed here'
    
#     else:
#         return string_prefix
    
#     return string_prefix 

# %%
if __name__ == '__main__':
    app.run_server(debug=False)


