import pandas
import typing
from datetime import datetime

from viz.data_classes import buoy_generic, dataset

NAME_ALTERNATES = ["station_name", "buoy_name", "name" ]
LAT_ALTERNATES = ["latitude", "lat", "latit"]
LON_ALTERNATES = ["longitude", "lon", "long", "longit"]
BATTERY_ALTERNATES = ['batt_v', 'battery_voltage']

class DataFactory:
    __dataset_name = None
    def __init__(self, dataset_name):
        self.__dataset_name = dataset_name

    def convertIsoDate(self, date: str) -> datetime:
        pass

    def create_buoy(self) -> dataset:
        pass

    def create_weather_station(self) -> dataset:
        pass

if __name__ == '__main__':
    pass
