from gameengine.util.util import Singleton


@Singleton
class MessageBus:
    """Moyen de communication entre les différents GameObjects."""

    def __init__(self):
        self.listeners = []

    def register(self, listener):
        if listener not in self.listeners:
            self.listeners.append(listener)

    def unregister(self, listener):
        self.listeners.remove(listener)

    def broadcastMessage(self, this, keyword, message):
        for i in range(len(self.listeners)):
            listener = self.listeners[i]
            if this == listener:
                continue

            listener.onMessageReceived(keyword, message)