from abc import ABC


class ObjectManager(ABC):
    """Classe de base de tous les manageurs de composants ou autre chose."""

    managers = []

    def __init__(self):
        super().__init__()
        ObjectManager.managers.append(self)
        self.objects = []

    def addObject(self, object):
        self.objects.append(object)
        object.managers.append(self)

        self.objectListChanged()

    def removeObject(self, object):
        if object not in self.objects:
            return

        self.objects.remove(object)
        object.managers.remove(self)

        self.objectListChanged()

    def toString(self):
        string = ""
        for objects in self.objects:
            string += objects.toString()
            string += "\n\n"
        return string

    def objectListChanged(self):
        pass

    def onUpdate(self):
        pass