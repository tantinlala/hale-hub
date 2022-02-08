class MultiMonitor:
    def __init__(self):
        self.trigger_functions = list()
        self.trigger_data = list()

    def add_trigger(self, trigger_function, trigger_data=None):
        self.trigger_functions.append(trigger_function)
        self.trigger_data.append(trigger_data)

    def is_triggered(self):
        if not self.trigger_functions:
            is_triggered = False
        else:
            is_triggered = True
            for trigger_function in self.trigger_functions:
                if not trigger_function():
                    is_triggered = False
                    break
        return is_triggered
