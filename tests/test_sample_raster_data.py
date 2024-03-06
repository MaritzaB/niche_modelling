import pandas as pd
from pandas.testing import assert_frame_equal
from ..src.sample_raster_data import get_years_months

file = 'tests/data_tests/points_tests.csv'

def test_get_years_months():
    expected = pd.DataFrame({'year': [2014, 2018], 'month': [1, 5]})
    result = get_years_months(file)
    assert_frame_equal(result, expected)
