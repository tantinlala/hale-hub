class _Automation:
    def __init__(self, trigger, action, only_on_changes, data=None):
        self.triggered = trigger
        self.do_action = action
        self.only_on_changes = only_on_changes
        self.data = data
        self.previous_state = False
        self.active = True  # Automation is active by default


class _Automations:
    def __init__(self):
        self.automations = dict()

    def run_automations(self):
        for key, automation in self.automations.items():
            triggered = automation.triggered()
            try:
                if automation.active is True and triggered is True:
                    if automation.only_on_changes is True:
                        if automation.previous_state is False:
                            automation.do_action()
                    else:
                        automation.do_action()
            finally:
                automation.previous_state = triggered

    def add_automation(self, trigger, action, key, only_on_changes=True, data=None):
        new_automation = _Automation(trigger, action, only_on_changes, data)
        self.automations[key] = new_automation

    def reset_automations(self):
        self.automations.clear()

    def get_automation_states(self):
        automation_states = dict()
        for key in self.automations.keys():
            automation_states[key] = self.automations[key].active
        return automation_states

    def toggle_automation_state(self, key):
        if self.automations[key].active is True:
            self.automations[key].active = False
        else:
            self.automations[key].active = True


_automations = _Automations()
run_automations = _automations.run_automations
add_automation = _automations.add_automation
reset_automations = _automations.reset_automations
get_automation_states = _automations.get_automation_states
toggle_automation_state = _automations.toggle_automation_state
