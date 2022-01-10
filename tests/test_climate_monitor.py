import pytest
from hale_hub.monitors.climate_monitor import ClimateMonitor

TEST_LOW_TO_HIGH_THRESHOLD = 50
TEST_HIGH_TO_LOW_THRESHOLD = -50


class FakeClimateDataSource:
    def __init__(self):
        self.data = 0

    def get_climate_data(self):
        return self.data

    def set_climate_data_to_return(self, data):
        self.data = data


@pytest.fixture(scope="function")
def low_is_normal_climate_monitor_data_source_pair():
    fake_climate_data_source = FakeClimateDataSource()
    climate_monitor = ClimateMonitor(fake_climate_data_source.get_climate_data, TEST_LOW_TO_HIGH_THRESHOLD, TEST_HIGH_TO_LOW_THRESHOLD)
    return climate_monitor, fake_climate_data_source


@pytest.fixture(scope="function")
def high_is_normal_climate_monitor_data_source_pair():
    fake_climate_data_source = FakeClimateDataSource()
    climate_monitor = ClimateMonitor(fake_climate_data_source.get_climate_data, TEST_LOW_TO_HIGH_THRESHOLD, TEST_HIGH_TO_LOW_THRESHOLD, low_is_normal=False)
    return climate_monitor, fake_climate_data_source


def test_Given_LowIsNormal_When_DataEqualsLowToHighThreshold_Expect_Normal(
        low_is_normal_climate_monitor_data_source_pair):
    climate_monitor, fake_climate_data_source = low_is_normal_climate_monitor_data_source_pair
    fake_climate_data_source.set_climate_data_to_return(TEST_LOW_TO_HIGH_THRESHOLD)
    abnormal = climate_monitor.is_climate_abnormal()
    assert abnormal is False


def test_Given_LowIsNormal_When_DataEqualsHighToLowThreshold_Expect_Normal(
        low_is_normal_climate_monitor_data_source_pair):
    climate_monitor, fake_climate_data_source = low_is_normal_climate_monitor_data_source_pair
    fake_climate_data_source.set_climate_data_to_return(TEST_HIGH_TO_LOW_THRESHOLD)
    abnormal = climate_monitor.is_climate_abnormal()
    assert abnormal is False


def test_Given_LowIsNormal_When_DataIsHigherThanLowToHighThreshold_Expect_Abnormal(
        low_is_normal_climate_monitor_data_source_pair):
    climate_monitor, fake_climate_data_source = low_is_normal_climate_monitor_data_source_pair
    fake_climate_data_source.set_climate_data_to_return(TEST_LOW_TO_HIGH_THRESHOLD + 1.0)
    abnormal = climate_monitor.is_climate_abnormal()
    assert abnormal is True


def test_Given_LowIsNormal_When_DataIsHigherThenLowerThanLowToHighThreshold_Expect_Abnormal(
        low_is_normal_climate_monitor_data_source_pair):
    climate_monitor, fake_climate_data_source = low_is_normal_climate_monitor_data_source_pair
    fake_climate_data_source.set_climate_data_to_return(TEST_LOW_TO_HIGH_THRESHOLD + 1.0)
    climate_monitor.is_climate_abnormal()
    fake_climate_data_source.set_climate_data_to_return(TEST_LOW_TO_HIGH_THRESHOLD - 1.0)
    abnormal = climate_monitor.is_climate_abnormal()
    assert abnormal is True


def test_Given_LowIsNormal_When_DataIsHigherThanLowToHighThresholdThenLowerThanHighToLowThreshold_Expect_Normal(
        low_is_normal_climate_monitor_data_source_pair):
    climate_monitor, fake_climate_data_source = low_is_normal_climate_monitor_data_source_pair
    fake_climate_data_source.set_climate_data_to_return(TEST_LOW_TO_HIGH_THRESHOLD + 1.0)
    climate_monitor.is_climate_abnormal()
    fake_climate_data_source.set_climate_data_to_return(TEST_HIGH_TO_LOW_THRESHOLD - 1.0)
    abnormal = climate_monitor.is_climate_abnormal()
    assert abnormal is False


def test_Given_HighIsNormal_When_DataEqualsHighToLowThreshold_Expect_Normal(
        high_is_normal_climate_monitor_data_source_pair):
    climate_monitor, fake_climate_data_source = high_is_normal_climate_monitor_data_source_pair
    fake_climate_data_source.set_climate_data_to_return(TEST_HIGH_TO_LOW_THRESHOLD)
    abnormal = climate_monitor.is_climate_abnormal()
    assert abnormal is False


def test_Given_HighIsNormal_When_DataEqualsLowToHighThreshold_Expect_Normal(
        high_is_normal_climate_monitor_data_source_pair):
    climate_monitor, fake_climate_data_source = high_is_normal_climate_monitor_data_source_pair
    fake_climate_data_source.set_climate_data_to_return(TEST_LOW_TO_HIGH_THRESHOLD)
    abnormal = climate_monitor.is_climate_abnormal()
    assert abnormal is False


def test_Given_HighIsNormal_When_DataIsLowerThanHighToLowThreshold_Expect_Abnormal(
        high_is_normal_climate_monitor_data_source_pair):
    climate_monitor, fake_climate_data_source = high_is_normal_climate_monitor_data_source_pair
    fake_climate_data_source.set_climate_data_to_return(TEST_HIGH_TO_LOW_THRESHOLD - 1.0)
    abnormal = climate_monitor.is_climate_abnormal()
    assert abnormal is True


def test_Given_HighIsNormal_When_DataIsLowerThenHigherThanHighToLowThreshold_Expect_Abnormal(
        high_is_normal_climate_monitor_data_source_pair):
    climate_monitor, fake_climate_data_source = high_is_normal_climate_monitor_data_source_pair
    fake_climate_data_source.set_climate_data_to_return(TEST_HIGH_TO_LOW_THRESHOLD - 1.0)
    climate_monitor.is_climate_abnormal()
    fake_climate_data_source.set_climate_data_to_return(TEST_HIGH_TO_LOW_THRESHOLD + 1.0)
    abnormal = climate_monitor.is_climate_abnormal()
    assert abnormal is True


def test_Given_HighIsNormal_When_DataIsLowerThanHighToLowThresholdThenHigherThanLowToHighThreshold_Expect_Normal(
        high_is_normal_climate_monitor_data_source_pair):
    climate_monitor, fake_climate_data_source = high_is_normal_climate_monitor_data_source_pair
    fake_climate_data_source.set_climate_data_to_return(TEST_HIGH_TO_LOW_THRESHOLD - 1.0)
    climate_monitor.is_climate_abnormal()
    fake_climate_data_source.set_climate_data_to_return(TEST_LOW_TO_HIGH_THRESHOLD + 1.0)
    abnormal = climate_monitor.is_climate_abnormal()
    assert abnormal is False
