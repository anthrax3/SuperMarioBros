from abc import ABC

from gameengine.util.Vector2 import Vector2

from gameengine.core.Object import Object
from gameengine.util.Rect import Rect


class Component(Object, ABC):
    """Classe de base d'une composante. Elle a une position locale relative à la composante Transform et une dimension."""

    def __init__(self, gameObject):
        super().__init__()

        self.enabled = True

        self.managers = []
        self.gameObject = gameObject

        self._localPosition = Vector2(0, 0)
        self._position = Vector2(0, 0)

        # self._size = Vector2(0, 0)

        def recalcPosition(sender, oldLocalPosition, newLocalPosition):
            self.position = self.gameObject.transform.position + newLocalPosition

        def recalcLocalPosition(sender, oldPosition, newPosition):
            self.localPosition = newPosition - self.gameObject.transform.position

        self.localPosition.hasChanged += recalcPosition
        self.position.hasChanged += recalcLocalPosition

        # TODO: HACKY SOLUTION
        def recalcPositionFromTransform(sender, oldTransformPos, newTransformPos):
            self.position = newTransformPos + self.localPosition

        from gameengine.components.Transform import Transform
        if not isinstance(self, Transform):
            self._position = Vector2(self.gameObject.transform.position)
            self.gameObject.transform.position.hasChanged += recalcPositionFromTransform

        if not isinstance(self, Transform):
            self._size = Vector2(self.gameObject.transform.size)
            self.gameObject.transform.size.hasChanged += self.getSizeFromTransform

    def getSizeFromTransform(self, sender, oldSize, newSize):
        self.size = newSize

    def destroy(self):
        self.gameObject.removeComponent(self)

    def onDestroy(self):
        self.localPosition.hasChanged.clearHandlers()
        self.position.hasChanged.clearHandlers()
        self.size.hasChanged.clearHandlers()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size.set(value)

    def inheritSize(self, bool):
        if bool:
            self.gameObject.transform.size.hasChanged += self.getSizeFromTransform
            self.size = self.gameObject.transform.size
        else:
            self.gameObject.transform.size.hasChanged -= self.getSizeFromTransform

    # @property
    # def size(self) -> Vector2:
    #     if self._size != None:
    #         return self._size
    #     return self.gameObject.transform.size
    #
    # @size.setter
    # def size(self, value):
    #     self._size = value


    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position.set(value)

    @property
    def localPosition(self):
        return self._localPosition

    @localPosition.setter
    def localPosition(self, value):
        self._localPosition.set(value)

    # @property
    # def position(self) -> Vector2:
    #     return self.localPosition + self.gameObject.transform.position
    #
    # @position.setter
    # def position(self, vec):
    #     delta = vec - self.position
    #     self.gameObject.transform.position += delta

    # def

    @property
    def localRect(self):
        return Rect(*self._localPosition, *self.size)

    @localRect.setter
    def localRect(self, rect):
        self._localPosition = rect.topLeft
        self.size = rect.size

    # @property
    # def worldRect(self) -> Rect:
    #     return Rect(*(self.localPosition + self.gameObject.transform.worldRect.topLeft), *self.size)

    @property
    def worldRect(self) -> Rect:
        return Rect(*(self._position - self.gameObject.transform.pivot.ratio.elementwise() * self.size), *self.size)

    @worldRect.setter
    def worldRect(self, rect):
        self._localPosition = rect.topLeft - self.gameObject.transform.worldRect.topLeft
        self.size = rect.size