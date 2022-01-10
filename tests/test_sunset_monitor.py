import pytest
from hale_hub.monitors.sunset_monitor import is_sun_set, set_latitude_and_longitude, set_offset_before_sunset, set_offset_after_sunrise
import datetime


@pytest.fixture
def mock_now(mocker):
    return mocker.patch('hale_hub.monitors.sunset_monitor.get_now_time')


@pytest.fixture
def mock_sun(mocker):
    return mocker.patch('hale_hub.monitors.sunset_monitor.Sun')


@pytest.fixture
def mock_rise_and_set(mock_sun):
    mock_sun().get_local_sunrise_time.return_value = datetime.datetime(2021, 12, 30, 6, 0, 1)
    mock_sun().get_local_sunset_time.return_value = datetime.datetime(2021, 12, 30, 17, 2, 0)


def test_Given_LatitudeAndLongitudeNotSet_WhenTimeIs1SecAfterSunset_Expect_SunNotSet(mock_now, mock_rise_and_set):
    mock_now.return_value = datetime.datetime(2021, 12, 30, 17, 2, 1)
    sun_has_set = is_sun_set()
    assert sun_has_set is False


def test_Given_OffsetBeforeSunsetNotSet_When_TimeIsSunset_Expect_SunNotSet(mock_now, mock_rise_and_set):
    set_latitude_and_longitude(0, 0)
    mock_now.return_value = datetime.datetime(2021, 12, 30, 17, 2, 0)
    sun_has_set = is_sun_set()
    assert sun_has_set is False


def test_Given_OffsetBeforeSunsetNotSet_When_TimeIs1SecAfterSunset_Expect_SunSet(mock_now, mock_rise_and_set):
    set_latitude_and_longitude(0, 0)
    mock_now.return_value = datetime.datetime(2021, 12, 30, 17, 2, 1)
    sun_has_set = is_sun_set()
    assert sun_has_set is True


def test_Given_OffsetBeforeSunset10Min_When_TimeIs9MinBeforeSunset_Expect_SunSet(mock_now, mock_rise_and_set):
    set_latitude_and_longitude(0, 0)
    set_offset_before_sunset(10)
    mock_now.return_value = datetime.datetime(2021, 12, 30, 16, 52, 1)
    sun_has_set = is_sun_set()
    assert sun_has_set is True


def test_Given_OffsetAfterSunsetNotSet_When_TimeIsSunrise_Expect_SunNotSet(mock_now, mock_rise_and_set):
    set_latitude_and_longitude(0, 0)
    mock_now.return_value = datetime.datetime(2021, 12, 30, 6, 0, 1)
    sun_has_set = is_sun_set()
    assert sun_has_set is False


def test_Given_OffsetAfterSunsetNotSet_When_TimeIs1SecBeforeSunrise_Expect_SunSet(mock_now, mock_rise_and_set):
    set_latitude_and_longitude(0, 0)
    mock_now.return_value = datetime.datetime(2021, 12, 30, 6, 0, 0)
    sun_has_set = is_sun_set()
    assert sun_has_set is True


def test_Given_OffsetAfterSunrise10Min_When_TimeIs9MinAfterSunrise_Expect_SunSet(mock_now, mock_rise_and_set):
    set_latitude_and_longitude(0, 0)
    set_offset_after_sunrise(10)
    mock_now.return_value = datetime.datetime(2021, 12, 30, 6, 9, 1)
    sun_has_set = is_sun_set()
    assert sun_has_set is True
