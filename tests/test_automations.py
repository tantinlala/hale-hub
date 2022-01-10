import pytest
from hale_hub.automations import run_automations, add_automation, reset_automations, get_automation_states, toggle_automation_state

DUMMY_KEY = "Dummy Key"


def state_is_always_true():
    return True


def state_is_always_false():
    return False


class FakeStateMonitor:
    def __init__(self):
        self.num_times_state_polled = 0

    def get_state(self):
        state = False

        # Change state every time it is polled
        if (self.num_times_state_polled % 2) == 0:
            state = True
        self.num_times_state_polled += 1
        return state


class ActionDoerSpy:
    def __init__(self):
        self.num_times_action_done = 0

    def do_action(self):
        self.num_times_action_done += 1

    def get_num_times_action_done(self):
        return self.num_times_action_done


@pytest.fixture(scope="function")
def action_doer_spy():
    action_doer_spy = ActionDoerSpy()
    return action_doer_spy


@pytest.fixture(scope="function")
def second_action_doer_spy():
    second_action_doer_spy = ActionDoerSpy()
    return second_action_doer_spy


def setup_function():
    reset_automations()


def test_Given_NoAutomationsAdded_Expect_RunAutomationsDoesNothing(action_doer_spy):
    run_automations()
    assert action_doer_spy.get_num_times_action_done() == 0


def test_Given_OneChangeAutomationAdded_When_StateIsFalse_Expect_RunAutomationsDoesNothing(action_doer_spy):
    add_automation(state_is_always_false, action_doer_spy.do_action, DUMMY_KEY)
    run_automations()
    assert action_doer_spy.get_num_times_action_done() == 0


def test_Given_OneChangeAutomationAdded_When_StateIsTrue_Expect_RunAutomationsTwiceDoesOneAction(action_doer_spy):
    add_automation(state_is_always_true, action_doer_spy.do_action, DUMMY_KEY)
    run_automations()
    assert action_doer_spy.get_num_times_action_done() == 1
    run_automations()
    assert action_doer_spy.get_num_times_action_done() == 1


def test_Given_OneChangeAutomationAdded_When_StateChangesTrueFalseTrue_Expect_RunAutomationsDoesTwoActions(action_doer_spy):
    fake_state_monitor = FakeStateMonitor()
    add_automation(fake_state_monitor.get_state, action_doer_spy.do_action, DUMMY_KEY)
    run_automations()
    assert action_doer_spy.get_num_times_action_done() == 1
    run_automations()
    assert action_doer_spy.get_num_times_action_done() == 1
    run_automations()
    assert action_doer_spy.get_num_times_action_done() == 2


def test_Given_OneChangeAutomationAdded_When_StateChangesFalseTrueFalse_Expect_RunAutomationsDoesOneAction(action_doer_spy):
    fake_state_monitor = FakeStateMonitor()
    add_automation(fake_state_monitor.get_state, action_doer_spy.do_action, DUMMY_KEY)
    fake_state_monitor.get_state() # Force state to start off as False on next call
    run_automations()
    assert action_doer_spy.get_num_times_action_done() == 0
    run_automations()
    assert action_doer_spy.get_num_times_action_done() == 1
    run_automations()
    assert action_doer_spy.get_num_times_action_done() == 1


def test_Given_MultipleChangeAutomationsAdded_When_OnlyOneOfStatesIsTrue_Expect_RunAutomationsDoesCorrectAction(action_doer_spy, second_action_doer_spy):
    add_automation(state_is_always_false, action_doer_spy.do_action, DUMMY_KEY)
    add_automation(state_is_always_true, second_action_doer_spy.do_action, DUMMY_KEY)
    run_automations()
    assert action_doer_spy.get_num_times_action_done() == 0
    assert second_action_doer_spy.get_num_times_action_done() == 1


def test_Given_OneStateAutomationAdded_When_StateIsFalse_Expect_RunAutomationsDoesNothing(action_doer_spy):
    add_automation(state_is_always_false, action_doer_spy.do_action, DUMMY_KEY, only_on_changes=False)
    run_automations()
    assert action_doer_spy.get_num_times_action_done() == 0


def test_Given_OneStateAutomationAdded_When_StateIsTrue_Expect_RunAutomationsTwiceDoesTwoActions(action_doer_spy):
    add_automation(state_is_always_true, action_doer_spy.do_action, DUMMY_KEY, only_on_changes=False)
    run_automations()
    assert action_doer_spy.get_num_times_action_done() == 1
    run_automations()
    assert action_doer_spy.get_num_times_action_done() == 2


def test_Given_MultipleStateAutomationsAdded_When_OneMonitoredStateTrue_Expect_RunAutomationsDoesCorrectAction(action_doer_spy, second_action_doer_spy):
    add_automation(state_is_always_false, action_doer_spy.do_action, DUMMY_KEY, only_on_changes=False)
    add_automation(state_is_always_true, second_action_doer_spy.do_action, DUMMY_KEY, only_on_changes=False)
    run_automations()
    assert action_doer_spy.get_num_times_action_done() == 0
    assert second_action_doer_spy.get_num_times_action_done() == 1


def test_Given_AutomationsAdded_When_AutomationsReset_Expect_RunAutomationsDoesNothing(action_doer_spy):
    add_automation(state_is_always_true, action_doer_spy.do_action, DUMMY_KEY)
    add_automation(state_is_always_true, action_doer_spy.do_action, DUMMY_KEY, only_on_changes=False)
    reset_automations()
    run_automations()
    assert action_doer_spy.get_num_times_action_done() == 0


def test_Given_NoAutomationsAdded_Expect_GetCurrentAutomationStatesReturnsNothing():
    current_automations = get_automation_states()
    assert not current_automations


def test_Given_AutomationsAdded_Expect_GetCurrentAutomationStatesReturnsKeys(action_doer_spy):
    add_automation(state_is_always_true, action_doer_spy.do_action, "Key 1")
    add_automation(state_is_always_true, action_doer_spy.do_action, "Key 2", only_on_changes=False)
    automation_states = get_automation_states()
    assert "Key 1" in automation_states.keys()
    assert "Key 2" in automation_states.keys()
    assert len(automation_states) == 2


def test_Given_AutomationAddedAndToggled_Expect_RunAutomationsDoesNothing(action_doer_spy):
    add_automation(state_is_always_true, action_doer_spy.do_action, DUMMY_KEY, only_on_changes=False)
    toggle_automation_state(DUMMY_KEY)
    run_automations()
    assert action_doer_spy.get_num_times_action_done() == 0


def test_Given_AutomationAddedAndToggled_When_ToggledAgain_Expect_RunAutomationsDoesAction(action_doer_spy):
    add_automation(state_is_always_true, action_doer_spy.do_action, DUMMY_KEY, only_on_changes=False)
    toggle_automation_state(DUMMY_KEY)
    toggle_automation_state(DUMMY_KEY)
    run_automations()
    assert action_doer_spy.get_num_times_action_done() == 1


def test_Given_AutomationAdded_Expect_GetCurrentAutomationStatesReturnsActiveState(action_doer_spy):
    add_automation(state_is_always_true, action_doer_spy.do_action, DUMMY_KEY, only_on_changes=False)
    automation_states = get_automation_states()
    active = automation_states[DUMMY_KEY]
    assert active is True


def test_Given_AutomationAddedAndToggled_Expect_GetCurrentAutomationStatesReturnsInactiveState(action_doer_spy):
    add_automation(state_is_always_true, action_doer_spy.do_action, DUMMY_KEY, only_on_changes=False)
    toggle_automation_state(DUMMY_KEY)
    automation_states = get_automation_states()
    active = automation_states[DUMMY_KEY]
    assert active is False


def test_Given_AutomationAddedAndToggled_When_ToggledAgain_Expect_GetCurrentAutomationStatesReturnsActiveState(action_doer_spy):
    add_automation(state_is_always_true, action_doer_spy.do_action, DUMMY_KEY, only_on_changes=False)
    toggle_automation_state(DUMMY_KEY)
    toggle_automation_state(DUMMY_KEY)
    automation_states = get_automation_states()
    active = automation_states[DUMMY_KEY]
    assert active is True
