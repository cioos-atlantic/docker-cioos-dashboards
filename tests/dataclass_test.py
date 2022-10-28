
from datetime import datetime
from viz.data_classes import BuoyGeneric, DatasetGeneric, IDataset
import pytest


class TestDataset:

    def testDatasetInterface(self):
        dc = IDataset.from_id(id="id")
        with pytest.raises(NotImplementedError):
            dc.data()

    def testDatasetResult(self):
        dc = DatasetGeneric(dataset_id="id", time=datetime.now(), name="name", lat=1.0, lon=2.0, battery_voltage=4.0)
        data = dc.data()
        print(data)
        assert(data['lat'] == 1.0)
        assert(data['lon'] == 2.0)
        assert(data['battery_voltage'] == 4.0)
        with pytest.raises(KeyError):
            data["__new__"]

    def testBuoyDatasetResult(self):
        dc = BuoyGeneric(air_pressure= 100.0)
        dc.air_pressure = 100.0
        data = dc.data()
        print(data)
        assert(data['air_pressure'] == 100.0)
        assert(data['lat'] == None)
