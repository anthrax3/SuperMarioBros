from gameengine.core.Component import Component
from gameengine.managers.CollisionManager import CollisionManager


class Collider(Component):
    """Composante qui représente le collider, on peut séparer les collisions en couches(layers)."""

    def __init__(self, gameObject):
        super().__init__(gameObject)
        CollisionManager().addObject(self)

        self.layers = []

        def updateQuadtreeOnPosition(sender, oldPosition, newPosition):
            # print(self.worldRect, oldPosition)
            from gameengine.util.Rect import Rect
            old = Rect(*(oldPosition - self.gameObject.transform.pivot.ratio.elementwise() * self.size), *self.size)

            # print(old)

            try:
                # CollisionManager().quadtree.remove(self, old.tuple())
                CollisionManager().grid.remove(self, old)
                # print("da")
            except:
                # print("FAIL")
                pass

            # CollisionManager().quadtree.insert(self, self.worldRect.tuple())
            CollisionManager().grid.insert(self, self.worldRect)

        def updateQuadtreeOnSize(sender, oldSize, newSize):
            # print(self.worldRect, oldPosition)
            from gameengine.util.Rect import Rect
            old = Rect(*(self.position - self.gameObject.transform.pivot.ratio.elementwise() * oldSize), *oldSize)

            # print(old)

            try:
                # CollisionManager().quadtree.remove(self, old.tuple())
                CollisionManager().grid.remove(self, old)
                # print("da")
            except:
                # print("FAIL")
                pass

            # CollisionManager().quadtree.insert(self, self.worldRect.tuple())
            CollisionManager().grid.insert(self, self.worldRect)
            # print(self.gameObject)

        self.position.hasChanged += updateQuadtreeOnPosition
        self.size.hasChanged += updateQuadtreeOnSize

    def _move(self, dx, dy):
        if not self.enabled:
            return

        if self.gameObject is not None:
            CollisionManager().queueMovement(self, dx, dy)

    def toString(self):
        return """[Collider]"""