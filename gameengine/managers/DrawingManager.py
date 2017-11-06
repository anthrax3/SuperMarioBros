from gameengine.core.ObjectManager import ObjectManager

from gameengine.util.util import Singleton


@Singleton
class DrawingManager(ObjectManager):
    def __init__(self):
        super().__init__()

    def objectListChanged(self):
        self.sort()

    def sort(self):
        self.objects.sort(key=lambda c: c.gameObject.transform.depth)