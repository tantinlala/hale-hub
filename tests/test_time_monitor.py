from hale_hub.monitors.time_monitor import TimeMonitor
import pytest
import datetime


@pytest.fixture
def mock_now(mocker):
    return mocker.patch('hale_hub.monitors.time_monitor.get_now_time')


def test_When_HourAndMinuteNotEqual_Expect_AlarmDoesNotTrigger(mock_now):
    time_monitor = TimeMonitor(17, 2)
    mock_now.return_value = datetime.datetime(2021, 12, 30, 0, 0, 0)
    alarm_triggered = time_monitor.did_alarm_trigger()
    assert alarm_triggered is False


def test_When_HourAndMinuteEqual_Expect_AlarmTriggers(mock_now):
    time_monitor = TimeMonitor(17, 2)
    mock_now.return_value = datetime.datetime(2021, 12, 30, 17, 2, 35)
    alarm_triggered = time_monitor.did_alarm_trigger()
    assert alarm_triggered is True
