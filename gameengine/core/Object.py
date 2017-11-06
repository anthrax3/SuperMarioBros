from abc import ABC, abstractmethod

from gameengine.util.Timer import Timer


class Object(ABC):
    """Classe de base pour toutes les composantes et gameObjects."""

    def __init__(self):
        self.instanceID = InstanceIDGenerator.getNextID()

    @abstractmethod
    def destroy(self):
        pass

    @abstractmethod
    def toString(self):
        pass

    def onDestroy(self):
        pass


def destroy(obj: Object, millis: int=0):
    if millis <= 0:
        obj.destroy()

    else:
        timer = Timer(millis, lambda: obj.destroy(), cycles=1)
        timer.start()


class InstanceIDGenerator(ABC):
    nextID = -1

    @classmethod
    def getNextID(cls):
        cls.nextID += 1
        return cls.nextID
