#!/usr/bin/env python
# coding: utf-8

from erddapy import ERDDAP
import pandas as pd
from bokeh.models import DatetimeTickFormatter
import datetime as dt
import holoviews as hv
import panel as pn
import logging
import os

logging.basicConfig(level=logging.DEBUG)
pn.extension(css_files=["https://fonts.googleapis.com/css?family=Quicksand"])

# get water pressure
if os.path.exists("pressure.csv"):
    pressure = pd.read_csv("pressure.csv")
else:
    logging.info("Downloading pressure data")
    e = ERDDAP(
        server="https://cioosatlantic.ca/erddap",
        protocol="tabledap",
    )

    e.response = "csv"
    e.dataset_id = "DFO_Sutron_NHARB"
    e.constraints = {
        "time>=": "2021-09-09T00:00:00Z",
        "time<=": "2021-09-12T12:00:00Z",
    }
    e.variables = ["time", "water_pressure"]
    pressure = e.to_pandas()
    pressure["time (UTC)"] = pd.to_datetime(
        pressure["time (UTC)"], format="%Y-%m-%dT%H:%M:%SZ"
    )
    pressure["water_pressure (mbar)"] = pressure["water_pressure (mbar)"] / 100

    pressure.to_csv("pressure.csv")


pres_plot = pressure.hvplot.line(
    x="time (UTC)", y="water_pressure (mbar)", width=1000, height=250
).opts(
    xformatter=DatetimeTickFormatter(
        months="%b %Y", days="%b/%d", hours="%H:%M", minutes="%H:%M"
    ),
    line_width=5,
    xaxis=None,
    fontsize={"ylabel": "12px"},
    xlabel="",
    ylabel="Water Pressure 3m Depth (dbar)",
    color="#F1E268",
    tools=["hover"],
    bgcolor="white",
    toolbar=None,
)

box = hv.VSpan(dt.date(2021, 9, 11), dt.date(2021, 9, 12)).opts(
    fill_color="red", alpha=0.2
)
pres_fig = pres_plot * box


logging.info("Downloading wave data")
e2 = ERDDAP(
    server="https://cioosatlantic.ca/erddap",
    protocol="tabledap",
)

e2.response = "csv"
e2.dataset_id = "SMA_MouthofPlacentiaBayBuoy"
e2.constraints = {"time>=": "2021-09-09T00:00:00Z", "time<=": "2021-09-12T12:00:00Z"}
e2.variables = ["time", "wave_ht_max"]
wavedata = e2.to_pandas()
wavedata["time (UTC)"] = pd.to_datetime(
    wavedata["time (UTC)"], format="%Y-%m-%dT%H:%M:%SZ"
)
wavedata = wavedata[wavedata["wave_ht_max (m)"] != 0]


wave_plot = wavedata.hvplot.line(
    x="time (UTC)",
    y="wave_ht_max (m)",
    width=1000,
    height=300,
).opts(
    xformatter=DatetimeTickFormatter(
        months="%b %Y", days="%b/%d", hours="%H:%M", minutes="%H:%M"
    ),
    line_width=5,
    fontsize={"ylabel": "12px", "xticks": "20px", "xlabel": "17px"},
    xlabel="time (UTC)",
    ylabel="Max Wave Height (m)",
    color="#E55162",
    tools=["hover"],
    bgcolor="white",
    toolbar=None,
)

wave_fig = wave_plot * box


e3 = ERDDAP(
    server="https://cioosatlantic.ca/erddap",
    protocol="tabledap",
)

e3.response = "csv"
e3.dataset_id = "DFO_Sutron_KLUMI"
e3.constraints = {
    "time>=": "2021-09-09T00:00:00Z",
    "time<=": "2021-09-12T12:00:00Z",
}
e3.variables = ["time", "wind_spd_gust"]
winddata = e3.to_pandas()
winddata["time (UTC)"] = pd.to_datetime(
    winddata["time (UTC)"], format="%Y-%m-%dT%H:%M:%SZ"
)


wind_plot = winddata.hvplot.line(
    x="time (UTC)",
    y="wind_spd_gust (m s-1)",
    width=1000,
    height=250,
).opts(
    xformatter=DatetimeTickFormatter(
        months="%b %Y", days="%b/%d", hours="%H:%M", minutes="%H:%M"
    ),
    line_width=5,
    xaxis=None,
    fontsize={"ylabel": "12px"},
    xlabel="",
    ylabel="Wind Gust Speed (m/s)",
    color="#2FB8DA",
    tools=["hover"],
    bgcolor="white",
    toolbar=None,
)

wind_fig = wind_plot * box


plots = pres_fig + wind_fig + wave_fig
plotpane = pn.pane.HoloViews(plots.cols(1), background="#dbefe1", margin=30)

if os.path.exists("pressuresensor.png"):
    pressuresensor = pn.panel("pressuresensor.png", height=250)

if os.path.exists("wavesensor.png"):
    wavesensor = pn.panel("wavesensor.png", height=250)

if os.path.exists("windsensor.png"):
    windsensor = pn.panel("windsensor.png", height=250)

sensors = pn.Column(
    pressuresensor, windsensor, wavesensor, background="#dbefe1", align="center"
)

tileopts = hv.opts.Tiles(width=450, height=450, projection=True)
tiles = hv.element.tiles.EsriImagery().opts(tileopts)
gdata = [
    [-6088650.718395521, 5937765.984589193, "Mouth of Placentia Bay Buoy"],
    [-6022032.682325194, 6081315.981186565, "Placentia Bay: North Harbour - NHARB"],
    [-6041697.270373825, 6039507.057063816, "Placentia Bay: Ragged Islands - KLUMI"],
]
geodata = pd.DataFrame(gdata, columns=["x", "y", "name"])
geoplot = geodata.hvplot.points(
    "x", "y", color="red", alpha=1, hover_cols=["name"]
).opts(width=365, height=350, size=5)
mapplot = (tiles * geoplot).options(
    xlim=(-6.7e6, -5.8e6),
    ylim=(5.8e6, 6.6e6),
    aspect="equal",
    xaxis=None,
    yaxis=None,
    active_tools=["pan", "wheel_zoom"],
    toolbar=None,
)
geopane = pn.pane.HoloViews(mapplot, align="center", background="#dbefe1")


titlepane = pn.pane.Markdown(
    "Placentia Bay - Hurricane Larry",
    align="start",
    style={"font-size": "50px", "font-family": "Quicksand"},
    background="#dbefe1",
    width=750,
)
ciooslogo = pn.pane.SVG(
    "https://cioosatlantic.ca/wp-content/themes/cioos-siooc-wordpress-theme/img/atlantic/cioos-atlantic_EN.svg",
    width=450,
    link_url="https://cioosatlantic.ca/",
    embed=True,
)
if os.path.exists("canadamap.png"):
    canadamap = pn.panel("canadamap.png", height=450, width=450, align="center")

if os.path.exists("arrowindicator.png"):
    arrowindicator = pn.panel("arrowindicator.png", height=175)


col1 = pn.Column(
    canadamap,
    geopane,
    pn.layout.VSpacer(),
    ciooslogo,
)
header = pn.Row(titlepane, arrowindicator)
main = pn.Row(plotpane, pn.Spacer(width=50), sensors)
col2 = pn.Column(header, main)
dashboard = pn.Row(col1, pn.Spacer(width=50), col2, background="#dbefe1")

dashboard.servable()
