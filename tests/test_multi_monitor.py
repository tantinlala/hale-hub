import pytest
from hale_hub.monitors.multi_monitor import MultiMonitor


def state_is_always_true():
    return True


def state_is_always_false():
    return False


def test_Given_NoTriggersInMultiMonitor_Expect_NotTriggered():
    multi_monitor = MultiMonitor()
    assert multi_monitor.is_triggered() is False


def test_Given_OneTriggerInMultiMonitor_When_SubTriggerNotTriggered_Expect_NotTriggered():
    multi_monitor = MultiMonitor()
    multi_monitor.add_trigger(state_is_always_false)
    assert multi_monitor.is_triggered() is False


def test_Given_OneTriggerInMultiMonitor_When_SubTriggerTriggered_Expect_Triggered():
    multi_monitor = MultiMonitor()
    multi_monitor.add_trigger(state_is_always_true)
    assert multi_monitor.is_triggered() is True


def test_Given_TwoTriggersInMultiMonitor_When_OneSubTriggerTriggered_Expect_NotTriggered():
    multi_monitor = MultiMonitor()
    multi_monitor.add_trigger(state_is_always_false)
    multi_monitor.add_trigger(state_is_always_true)
    assert multi_monitor.is_triggered() is False


def test_Given_TwoTriggersInMultiMonitor_When_BothSubTriggersTriggered_Expect_Triggered():
    multi_monitor = MultiMonitor()
    multi_monitor.add_trigger(state_is_always_true)
    multi_monitor.add_trigger(state_is_always_true)
    assert multi_monitor.is_triggered() is True
