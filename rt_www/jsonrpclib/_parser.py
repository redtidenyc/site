class JSONParser:
    def __init__(self, target):
        self._target = target
    def feed(self, data):
        self._target.data(data)
    def close(self):
        self._target.end()
