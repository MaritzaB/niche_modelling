import pytest
import pandas as pd
from ..src.notebooks.netcdf_tools import get_points

trayectories_df = pd.DataFrame({'date': ['2019-01-01', '2019-01-02', '2019-01-03'],
                                'longitude': [-10, -11, -12],
                                'latitude': [30, 31, 32]})

date = '2019-01-01'

def test_get_points():
    points = get_points(trayectories_df, date)
    assert len(points) == 1
    assert points['date'].iloc[0] == date
    assert points['longitude'].iloc[0] == -10
    assert points['latitude'].iloc[0] == 30

def test_get_points_wrong_date():
    points = get_points(trayectories_df, '2019-01-04')
    assert len(points) == 0



