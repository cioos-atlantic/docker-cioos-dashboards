import dash
from dash import html
from dash import dcc
from data_collect import DataCollect
from datetime import date


class Visualization:
    CIOOS_ATLANTIC_SITE_URL = "https://cioosatlantic.ca"
    CIOOS_IMAGE = CIOOS_ATLANTIC_SITE_URL + "/wp-content/" + \
        "themes/cioos-siooc-wordpress-theme/img/CIOOS-watermark.svg?x48800"
    CIOOS_ATLANTIC_IMAGE = CIOOS_ATLANTIC_SITE_URL + "/wp-content/" + \
        "themes/cioos-siooc-wordpress-theme/img/atlantic/cioos-atlantic_EN.svg?x79655"
    data_collect: DataCollect = None
    
    def __init__(self, data_collect):
        self.data_collect = data_collect

    def getHeader(self):
        return html.Header([
            self.getCIOOSHeader(),
            self.getCIOOSAtlanticHeader()
        ], className="page-header", id="masthead")


    def getCIOOSHeader(self):
        header = html.Div(
                html.Div([
                    html.Div(
                        html.Img(**{"data-src":self.CIOOS_IMAGE},
                        **{"data-was-processed":"true"}, 
                        src=self.CIOOS_IMAGE,
                        className="lazy loaded",
                        alt="CIOOS National Logo"), 
                        className="nationallogo"),
                    html.Div(
                        html.Aside(
                            html.Div(
                                html.P(
                                    html.A("A Regional Association of CIOOS",
                                    href="https://www.cioos.ca")
                                ), 
                                className="textwidget"),
                            className="text-3 widget widget-text"), 
                        className="logotype")], 
                    className="container"),
                className="pre-nav")
        return header
    
    def getCIOOSAtlanticHeader(self):
        header = html.Div(
            html.Div([
                html.Div(
                    html.A(
                        html.Img(className="lazy loaded",
                        src=self.CIOOS_ATLANTIC_IMAGE,
                        **{"data-src" : self.CIOOS_ATLANTIC_IMAGE},
                        **{"data-was-processed" : "true"},
                        alt="CIOOS Atlantic logo"
                        ),
                        rel="home", href=self.CIOOS_ATLANTIC_SITE_URL
                        ), 
                    className="sitelogo"),
                html.Nav([
                    html.Button(className="menu-toggle"), 
                    html.Div(
                        self.getNav(), 
                    className="menu-main-menu-en-container")
                    ], 
                    id="site-navigation", 
                    className="site-nav nav main-nav main-navigation"),
                ], 
                className="container"), 
            className="post-nav")
        return header

    def getNav(self):
        header = html.Ul([
            html.Li(
                html.A("Home", href=self.CIOOS_ATLANTIC_SITE_URL,
                    id="menu-item-1469", 
                    className="menu-item menu-item-type-post_type " + \
                        "menu-it em-object-page menu-item-home current-menu-item " + \
                        "current-menu-item page_item page-item-1395 " + \
                        "current_page_item menu_item-1469")
                ),
            html.Li(html.A("About", href=self.CIOOS_ATLANTIC_SITE_URL + "/about/")),
            html.Li(html.A("Data Tools", href=self.CIOOS_ATLANTIC_SITE_URL + "/data-tools/")),
            html.Li(html.A("Data Catalogue", href="https://catalogue.cioosatlantic.ca/")),
            html.Li(html.A("Resources", href=self.CIOOS_ATLANTIC_SITE_URL + "/resources/"))
        ], id="primary-menu", className="menu nav-menu")
        return header

    
    def getBody(self):
        body = html.Main([
            html.H3('About the Dataset'),
            html.P('(dataset description here)'),

            dcc.Dropdown(id="dataset_a", options=[
                {'label': j, 'value': i}
                for i, j in self.data_collect.unitdict.items()
            ], value= "sea_water_temperature", multi=False, searchable=True, placeholder="Select.."),

            html.Br(),

            dcc.Dropdown(id="dataset_b", options=[
                {'label': j, 'value': i}
                for i, j in self.data_collect.unitdict.items()],
                value="sea_water_temperature", multi=False, searchable=True, placeholder="Select.."
            ),

            html.Br(),

            dcc.DatePickerRange(id="datepicker",
              min_date_allowed=date(2018, 3, 30),
              max_date_allowed=date(2018, 5, 24),
              start_date=date(2018, 4, 1),
              end_date=date(2018, 4, 7),
              start_date_placeholder_text="Start Period",
              end_date_placeholder_text="End Period",
              reopen_calendar_on_clear=True,
              clearable=True,
              calendar_orientation="horizontal"
            ),
            
            dcc.Graph(id="linegraph_multiple", figure={},
              config = {
                "staticPlot" : False,
                "scrollZoom" : True,
                "doubleClick" : "reset",
                "showTips" : True,
                "displayModeBar" : True
              }
            ),
            html.Br(),
            dcc.RangeSlider(id="range_slider", 
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
                tooltip = {'always_visible': False, 'placement': 'bottom'}
                ),
            
            ]

        )
        return body

    def getFooter(self):
        footer = html.Footer(
            [html.P("footer")]
        )
        return footer
