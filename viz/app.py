import dash
from dash import dcc
from dash import html
import pandas as pd
from viz import Visualization
from data_collect import DataCollect
from dash.dependencies import Input, Output
import plotly.express as px
from datetime import date
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging



app = dash.Dash(__name__)
data = DataCollect('./ids_sample.yaml')
data.collect()
viz = Visualization(data)
server = app.server

app.layout = html.Article([viz.getHeader(), viz.getBody(), viz.getFooter()])

@app.callback(
    [
        Output(component_id="linegraph_multiple", component_property="figure"),
       #  Output(component_id="linegraph_1", component_property="figure"),

    ],
    [ 
        Input(component_id="dataset_a", component_property="value"), 
        Input(component_id="dataset_b", component_property="value"),
        Input(component_id="datepicker", component_property="start_date"),
        Input(component_id="datepicker", component_property="end_date"),
        Input(component_id="range_slider", component_property="value")
    ])
def plot(selectA, selectB, start_date, end_date, months):
    dropdown1_data = viz.data_collect.getData(selectA)
    dropdown2_data = viz.data_collect.getData(selectB)
    slider_data1 = viz.data_collect.getData(selectA)
    slider_data2 = viz.data_collect.getData(selectB)
    select_value_1 = [v2 for v1, v2 in viz.data_collect.unitdict.items() if v1 == selectA][0]
    select_value_2 = [v2 for v1, v2 in viz.data_collect.unitdict.items() if v1 == selectB][0]
    dropdown2_data = dropdown2_data.loc[start_date:end_date]
    dropdown1_data = dropdown1_data.loc[start_date:end_date]
    start_date1 = "2018"+"-"+"0"+str(months[0])+"-"+"01"
    start_date1 = pd.to_datetime(start_date1)
    end_date1 = "2018"+"-"+"0"+str(months[1])+"-"+"30"
    end_date1 = pd.to_datetime(end_date1)
    slider_data1 = slider_data1.loc[start_date1:end_date1]
    slider_data2 = slider_data2.loc[start_date1:end_date1]
    
    linegraph_multiplefig= make_subplots(specs= [[{'secondary_y': True}]])
    linegraph_multiplefig.add_trace(
        go.Scatter(x=dropdown1_data['time (UTC)'], y=dropdown1_data[select_value_1], name=select_value_1),
        secondary_y=False,
    )
    linegraph_multiplefig.add_trace(
        go.Scatter(x= dropdown2_data['time (UTC)'], y= dropdown2_data[select_value_2], name=select_value_2),
        secondary_y=True,
    )

    #linegraph_1fig = px.line(data_frame = dropdown1_data, x = "time (UTC)", y = select_value_1 )
    # linegraph_2fig = px.line(data_frame = dropdown2_data, x = "time (UTC)", y = select_value_1 )

    slider_data1['Date']= pd.to_datetime(slider_data1['time (UTC)']).dt.date
    slider_data1.drop(slider_data1.columns[0], axis=1, inplace=True)
    slider_data2['Date']= pd.to_datetime(slider_data2['time (UTC)']).dt.date
    slider_data2.drop(slider_data2.columns[0], axis=1, inplace=True)

    # bargraph_slider1fig = px.box(data_frame = slider_data1, x = "Date", y = select_value_1 )
    # bargraph_slider2fig = px.box(data_frame = slider_data2, x = "Date", y = select_value_1 )

    return [linegraph_multiplefig]

if __name__ == "__main__":
    app.run_server(debug=False)
    