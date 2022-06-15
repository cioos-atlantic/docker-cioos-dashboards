# %%
import pandas as pd
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
import plotly.express as px
from datetime import date
import dash_core_components as dcc
import dash
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
        value= "sea_water_temperature", multi=False, searchable= True, placeholder= "Select.."),
    
    html.Br(),

    dcc.Dropdown(id= "dropdown2", options=[
        {'label': j, 'value': i}
        for i,j in unitdict.items()],
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

def plot(dpvalue1, dpvalue2, start_date, end_date, months):
    
    dropdown1_data= getdata(dpvalue1)
    dropdown2_data= getdata(dpvalue2)
    slider_data1= getdata(dpvalue1)
    slider_data2= getdata(dpvalue2)
   
    for v1, v2 in unitdict.items():
        if v1 == dpvalue1:
            dpvalue1_1 = v2

    for v1, v2 in unitdict.items():
        if v1 == dpvalue2:
            dpvalue2_1 = v2
    
    dropdown2_data = dropdown2_data.loc[start_date:end_date]
    dropdown1_data = dropdown1_data.loc[start_date:end_date]

    start_date1 = "2018"+"-"+"0"+str(months[0])+"-"+"01"
    start_date1 =pd.to_datetime(start_date1)
    end_date1 = "2018"+"-"+"0"+str(months[1])+"-"+"30"
    end_date1 =pd.to_datetime(end_date1)
    slider_data1 = slider_data1.loc[start_date1:end_date1]
    slider_data2 = slider_data2.loc[start_date1:end_date1]
    
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

# %%
if __name__ == '__main__':
    app.run_server(debug=False)


