from gameengine.util.Vector2 import Vector2

from gameengine.core.ObjectManager import ObjectManager
from gameengine.util.util import Singleton


@Singleton
class PhysicsManager(ObjectManager):
    def __init__(self):
        super().__init__()

        self.gravity = Vector2(0, 0)

    def onUpdate(self):
        for component in self.objects:
            if not component.enabled:
                continue

            component.addAcceleration(component.customGravity if component.customGravity is not None else self.gravity)
            component.step()
