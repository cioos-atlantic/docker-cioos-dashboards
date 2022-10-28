import os
from erddapy import ERDDAP
from dotenv import load_dotenv
import yaml
import pandas as pd
import numpy as np
import re
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

load_dotenv()

class DataCollect:
    CIOOS_DEV_USERNAME = os.getenv('CIOOS_DEV_USERNAME')
    CIOOS_DEV_PASSWORD = os.getenv('CIOOS_DEV_PASSWORD')
    CIOOS_DEFAULT_SERVER = os.getenv('CIOOS_DEFAULT_SERVER')

    erddap = None
    server = CIOOS_DEFAULT_SERVER
    protocol = "tabledap"
    format = "csv"
    data_ids = []
    datasets = {}
    unitdict = {}

    def __init__(self, yaml_filename):
        if yaml_filename != None:
            with open(yaml_filename, "r") as stream:
                try:
                    self.data_ids = yaml.safe_load(stream)['id-list']
                except yaml.YAMLError as exc:
                    print(exc)
        self.erddap = ERDDAP(self.server, self.protocol)
        self.erddap.auth = (self.CIOOS_DEV_USERNAME, self.CIOOS_DEV_PASSWORD)
        self.erddap.response = self.format

    def collect(self):
        for id in self.data_ids:
            self.erddap.dataset_id = id
            self.erddap.constraints = { "time<=": "2018-03-30T20:17:33Z" }
            df = self.erddap.to_pandas()
            for col in df.columns:
                if len(df[col].unique()) == 1:
                    df.drop([col], axis=1, inplace=True)
            vars = list(df.columns)
            variables = [re.sub(r'\(.*?\) *', '', x).strip() for x in vars]
            variableList = list(df.columns)
            newdict = dict(zip(variables, variableList))
            self.unitdict.update(newdict)
            self.datasets.update({k: id for k in variables})
        del self.unitdict['time']

    def getData(self, varname):
        self.erddap.variables = ['time', varname]
        self.erddap.dataset_id = self.datasets.get(varname)
        self.erddap.constraints = {"time<=": "2018-05-23T17:47:30Z", "time>=": '2018-03-30T20:02:33Z'}
        try: 
            df = self.erddap.to_pandas()
        except HTTPError as http_error:
            print(http_error)


        df = df.sort_values(by=['time (UTC)'])
        df['time UTC'] = pd.to_datetime(df['time (UTC)'], format="%Y-%m-%dT%H:%M:%SZ")
        df = df.set_index(df['time (UTC)'].astype(np.datetime64))
        if varname == 'eastward_sea_water_velocity ' or 'upward_sea_water_velocity ' or 'northward_sea_water_velocity ':
           df = df[df[self.unitdict[varname]] != 0]
        if varname == 'sea_surface_wave_maximum_period ':
            df = df[df[self.unitdict[varname]] != -9]
        return df

    def processData(self, df):
        df = df.sort_values(by=['time (UTC)'])
        df['time UTC'] = pd.to_datetime(df['time (UTC)'], format="%Y-%m-%dT%H:%M:%SZ")
        df = df.set_index(df['time (UTC)'].astype(np.datetime64))
        if varname == 'eastward_sea_water_velocity ' or 'upward_sea_water_velocity ' or 'northward_sea_water_velocity ':
           df = df[df[self.unitdict[varname]] != 0]
        if varname == 'sea_surface_wave_maximum_period ':
            df = df[df[self.unitdict[varname]] != -9]
        return df


if __name__ == '__main__':
    pass