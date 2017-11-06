class EventHandler:
    def __init__(self, sender):
        self._sender = sender
        self._listeners = []

    def notify(self, *args):
        for l in self._listeners:
            l(self._sender, *args)

    def add(self, l):
        if l not in self._listeners:
            self._listeners.append(l)
        return self

    def remove(self, l):
        if l in self._listeners:
            self._listeners.remove(l)
        return self

    def clearHandlers(self):
        self._listeners = []

    __iadd__ = add
    __isub__ = remove
    __call__ = notify