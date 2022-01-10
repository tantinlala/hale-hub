import requests


# TODO: allow people to dynamically subscribe to an event by providing their API key
class IftttLogger:
    def __init__(self):
        self.api_key = None
        self.event = None

    def set_ifttt_logger_configs(self, api_key, event):
        """Construct event sender with user's api key and event
        Parameters:
        ----------
        api_key : string
            Your IFTTT API key
        event : string
            The name of the IFTTT event to trigger
        """
        self.api_key = api_key
        self.event = event

    def send_ifttt_log(self, value1=None, value2=None, value3=None):

        print(value1)
        print(value2)
        print(value3)

        """Send an event to the IFTTT maker channel
        Parameters:
        -----------
        value1 :
            Optional: Extra data sent with the event (default: None)
        value2 :
            Optional: Extra data sent with the event (default: None)
        value3 :
            Optional: Extra data sent with the event (default: None)
        """

        url = 'https://maker.ifttt.com/trigger/{e}/with/key/{k}/'.format(e=self.event,
                                                                         k=self.api_key)
        payload = {'value1': value1, 'value2': value2, 'value3': value3}
        return requests.post(url, data=payload)


_ifttt_logger = IftttLogger()
set_ifttt_logger_configs = _ifttt_logger.set_ifttt_logger_configs
send_ifttt_log = _ifttt_logger.send_ifttt_log
