

from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass(kw_only=True)
class IDataset:
    __create_key = object()
    dataset_id: str = None
    name: str = None
    time: datetime = None
    lat: float = None
    lon: float = None
    battery_voltage: float = None

    def __init__(self, key, id):
        assert key == self.__create_key, "Can only instantiate through IDataset.from_id method"
        self.datasetid = id

    @classmethod
    def from_id(cls, id):
        return cls(cls.__create_key, id)

    """Return a dictionary containing the associated values"""
    def data(cls) -> dict:
        raise NotImplementedError('')

@dataclass(kw_only=True)
class DatasetGeneric(IDataset):
    """A generic class for ingestion of data.

    This class handles the base values for Ocean data objects including time, lat, lon and battery_voltage. It acts as a template
    for other classes which will call on it to deal with the values.
    """

    """Return a dictionary containing the associated values"""
    def data(self) -> dict:
        return {k: v for k, v in asdict(self).items()}


@dataclass(kw_only=True)
class BuoyGeneric(DatasetGeneric):
    temp_c: float = None
    wave_ht_sig: float = None
    wave_period_max: float = None
    wave_ht_max: float = None
    wave_dir_avg: float = None
    wave_spread_avg: float = None
    sample_quality: int = None
    sea_water_temperature: float = None
    wind_speed: float = None
    air_pressure: float = None
    humidity_percent: float = None
    air_temperature: float = None
    precip_rain_int: float = None
    precip_hail_int: float = None
    compass_deci_deg: float = None
    wind_bearing: float = None

@dataclass(kw_only=True)
class WeatherStationGeneric(DatasetGeneric):
    wind_speed_average: float = None
    wind_direction_average: float = None
    wind_direction_sd: float = None
    wind_max: float = None
    wind_min: float = None
    air_temperature_average: float = None
    air_temperature_max: float = None
    air_temperature_min: float = None
    relative_humidity: float = None
    air_dewpoint_average: float = None
    average_solar_irradience: float = None
    rain_gauge_1: float = None
    rain_gauge_2: float = None


if __name__ == '__main__':
    pass 