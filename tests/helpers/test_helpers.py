import pytest
import pandas as pd
from pdbtwitch.helpers import helper
from pandas._testing import assert_frame_equal

df = pd.DataFrame.from_dict({'city': ['New York', 'Los Angeles']})
df_expected = pd.DataFrame.from_dict({'city': {0: 'New York', 1: 'Los Angeles'},
                                      'lat': {0: 40.7127281, 1: 34.0536909},
                                      'long': {0: -74.0060152, 1: -118.2427666}})

city_dict_expected = {'New York': {'lat': 40.7127281, 'long': -74.0060152},
                      'Los Angeles': {'lat': 34.0536909, 'long': -118.2427666}}
city_list = [['New York', 'Los Angeles']]


@pytest.mark.parametrize("city_list", city_list)
def test_build_city_loc_mapping(city_list):
    city_dict = helper.build_city_loc_mapping(city_list)
    assert city_dict == city_dict_expected


@pytest.mark.parametrize("city_dict",
                         [{'New York': {'lat': 40.7127281, 'long': -74.0060152},
                           'Los Angeles': {'lat': 34.0536909, 'long': -118.2427666}}])
def test_extract_long_lat(city_dict):
    df = pd.DataFrame.from_dict({'city': ['New York', 'Los Angeles']})
    df[['lat', 'long']] = df.apply(helper.extract_long_lat, city_dict=city_dict,
                                   axis=1, result_type='expand')
    assert_frame_equal(df, df_expected, check_dtype=False)
