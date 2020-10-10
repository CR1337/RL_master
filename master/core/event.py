class Event():

    def __init__(self, event_type, data={}):
        self._data = dict()
        self._event_type = ""

    @property
    def data(self):
        return self._data

    @property
    def event_type(self):
        return self._event_type
