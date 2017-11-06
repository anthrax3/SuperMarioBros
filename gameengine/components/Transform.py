from gameengine.util.Vector2 import Vector2

from gameengine.core.Component import Component
from gameengine.util.EventHandler import EventHandler
from gameengine.util.Rect import Rect

class Pivot:
    """Point de centre de l'objet, exprimé en pourcentage sur chaque axe.
    ex: (0.5, 0.5) sera tout le temps au milieu
        (0, 0.2) sera 0% depuis la gauche(collé du côté gauche de l'objet) et à 20% depuis le haut."""
    def __init__(self, gameObject):
        self.gameObject = gameObject

        self.ratio = Vector2(0, 0)
        # self.ratioChanged = EventHandler(self)
        # self.ratioChanged(self.ratio)

        # Don't move the object
        def recalculateLocalPosition(sender, old, new):
            self.gameObject.transform.localPosition += (new - old) * self.gameObject.transform.size
            # print("da")

        self.ratio.hasChanged += recalculateLocalPosition


    def set(self, x, y):
        self.ratio.set(x, y)

        # if newRatio != self.ratio:
        #     oldLocalVector = self.getLocalVector()
        #     self.ratio = newRatio
        #     newLocalVector = self.getLocalVector()

            # self.gameObject.transform.localPosition += (newLocalVector - oldLocalVector)

            # self.ratioChanged(self.ratio)

    @property
    def x(self):
        return self.ratio.x

    @x.setter
    def x(self, value):
        self.set(value, self.ratio.y)

    @property
    def y(self):
        return self.ratio.y

    @y.setter
    def y(self, value):
        self.set(self.ratio.x, value)



    def getLocalVector(self) -> Vector2:
        return self.gameObject.transform.size.elementwise() * self.ratio

    def getWorldPosition(self) -> Vector2:
        topLeftCorner = self.gameObject.transform.worldRect.topLeft
        return topLeftCorner + self.getLocalVector()



class Anchor:
    """Point ancre de l'enfant dans un parent. Similaire au pivot mais c'est un point relatif au parent"""

    def __init__(self, gameObject):
        self.gameObject = gameObject

        self.ratio = Vector2(0, 0)
        # self.ratioChanged = EventHandler(self)
        # self.ratioChanged(self.ratio)

        # def recalculateLocalPosition(sender, old, new):
        #     self.gameObject.transform.localPosition += (new - old) * self.gameObject.transform.parent.size
        #     print("poate")
        #
        # self.ratio.hasChanged += recalculateLocalPosition

    def set(self, x, y, overridePivot=False, overridePosition=False):
        # pass
        self.ratio.set(x, y)


        # oldAnchorWorldPosition = self.getWorldPosition()
        # oldPivotWorldPosition = self.gameObject.transform.pivot.getWorldPosition()
        #
        # newRatio = Vector2(x, y)
        # if newRatio != self.ratio:
        #     self.ratio = newRatio
        #     self.ratioChanged(self.ratio)
        #
        # newAnchorWorldPosition = self.getWorldPosition()
        # oldAnchorToNewAnchorVector = newAnchorWorldPosition - oldAnchorWorldPosition
        #
        # self.gameObject.transform.localPosition = oldPivotWorldPosition - oldAnchorToNewAnchorVector
        #
        # if overridePivot:
        #     self.gameObject.transform.pivot.set(x, y)
        #
        # if overridePosition:
        #     self.gameObject.transform.localPosition = Vector2(0, 0)


    @property
    def x(self):
        return self.ratio.x

    @x.setter
    def x(self, value):
        self.set(value, self.ratio.y)

    @property
    def y(self):
        return self.ratio.y

    @y.setter
    def y(self, value):
        self.set(self.ratio.x, value)

    def getLocalVector(self) -> Vector2:
        return self.gameObject.transform.parent.size.elementwise() * self.ratio

    def getWorldPosition(self) -> Vector2:
        topLeftCorner = self.gameObject.transform.parent.worldRect.topLeft
        return topLeftCorner + self.getLocalVector()


class Transform(Component):
    """Composante obligatoire dans chaque GameObject, gére le parentage, le positionnement.
    Sa position locale représente la position globale(absolue du monde) sauf quand il est enfant d'un parent"""

    def __init__(self, gameObject):
        super().__init__(gameObject)
        self._size = Vector2(0, 0)

        self._depth = 0

        self._parent: Transform = None
        self.children = []

        self.pivot = Pivot(self.gameObject)
        self.anchor = Anchor(self.gameObject)

        self.sizeChanged = EventHandler(self)

        self._localPosition = Vector2(0, 0)
        self._position = Vector2(0, 0)

        def recalcPosition(sender, oldLocalPosition, newLocalPosition):
            if self.parent is None:
                self.position = Vector2(newLocalPosition)
            else:
                # self.position = self.parent.position

                self.position = self.parent.position + newLocalPosition \
                # -Vector2(1, 1)
                # - self.parent.size * self.anchor.ratio \

                # + self.size * self.pivot.ratio
        def recalcLocalPosition(sender, oldPosition, newPosition):
            if self.parent is None:
                self.localPosition = Vector2(newPosition)
            else:
                self.localPosition = newPosition - self.parent.position \
                # +Vector2(1, 1)
                # + self.parent.size * self.anchor.ratio \

                # - self.size * self.pivot.ratio
        def recalcChildrenPosition(sender, oldPosition, newPosition):
            if self.children:
                for child in self.children:
                    child.position = newPosition + child.localPosition
                    # print(child.position)

        self.localPosition.hasChanged += recalcPosition
        self.position.hasChanged += recalcLocalPosition
        self.position.hasChanged += recalcChildrenPosition

    @property
    def localPosition(self):
        return self._localPosition

    @localPosition.setter
    def localPosition(self, value):
        self._localPosition.set(value)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position.set(value)

    @property
    def parent(self):
        return self._parent

    # @parent.setter
    # def parent(self, nextParent):
    #     if (self._parent is None) and (nextParent is not None):
    #         if nextParent._parent is self:
    #             nextParent.parent = None
    #
    #         oldLocalPosition = Vector2(self._localPosition)
    #
    #         oldDepth = int(self.depth)
    #         parentDepth = int(nextParent.depth)
    #
    #         self._parent = nextParent
    #         self._parent.children.append(self)
    #
    #         self.anchor.set(0.5, 0.5, False, False)
    #         self._localPosition = oldLocalPosition - self.anchor.getWorldPosition()
    #
    #         self.depth = oldDepth - parentDepth
    #
    #     elif (self._parent is not None) and (nextParent is None):
    #         oldPivotWorldPosition = self.pivot.getWorldPosition()
    #
    #         oldDepth = int(self.depth)
    #         parentDepth = int(self._parent.depth)
    #
    #         self._parent.children.remove(self)
    #         self._parent = None
    #
    #         self._localPosition = oldPivotWorldPosition
    #
    #         self.depth = parentDepth + oldDepth
    #
    #     elif (self._parent is not None) and (nextParent is not None):
    #         self.parent = None
    #         self.parent = nextParent


    @parent.setter
    def parent(self, nextParent):
        if (self._parent is None) and (nextParent is not None):
            if nextParent._parent is self:
                nextParent.parent = None

            self._parent = nextParent
            self._parent.children.append(self)

        elif (self._parent is not None) and (nextParent is None):
            self._parent.children.remove(self)
            self._parent = None


        elif (self._parent is not None) and (nextParent is not None):
            self.parent = None
            self.parent = nextParent



    # @property
    # def size(self) -> Vector2:
    #     return self._size
    #
    # @size.setter
    # def size(self, vec):
    #     self._size = vec
    #
    #     self.sizeChanged(self._size)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size.set(value)


    @property
    def worldRect(self) -> Rect:
        return Rect(*(self._position - self.pivot.ratio.elementwise() * self.size), *self.size)

    @worldRect.setter
    def worldRect(self, rect):
        if self.parent is None:
            self._localPosition = rect.topLeft
            self.size = rect.size


    def parents(self):
        currentParent = self.parent
        while currentParent is not None:
            yield currentParent
            currentParent = currentParent.parent
            # print("parent", currentParent, currentParent._parent, currentParent.gameObject)


    # @property
    # def position(self) -> Vector2:
    #     if self.parent is None:
    #         return self.localPosition
    #
    #     else:
    #         parentsRootToChild = list(self.parents())[::-1]
    #
    #         pivotPosition = Vector2()
    #         for iParent, parent in enumerate(parentsRootToChild):
    #             pivotToChildAnchorVector = (parentsRootToChild[iParent+1] if iParent+1 < len(parentsRootToChild) else self).anchor.getLocalVector() - parent.pivot.getLocalVector()
    #             pivotPosition += (parent.localPosition + pivotToChildAnchorVector)
    #
    #         pivotPosition += self.localPosition
    #
    #         return pivotPosition
    #
    # @position.setter
    # def position(self, vec: Vector2):
    #     # before = Vector2(self.localPosition)
    #
    #     if self.parent is None:
    #         self.localPosition = vec
    #
    #     else:
    #         delta = vec - self.position
    #         self.localPosition += delta


    @property
    def depth(self):
        if self.parent is not None:
            return self.parent.depth + self._depth
        else:
            return self._depth

    @depth.setter
    def depth(self, value):
        self._depth = value

        # Notify all managers of all components
        for component in self.gameObject.components:
            for manager in component.managers:
                manager.objectListChanged()

    def toString(self):
        return """[Transform]
    Position: {}""".format(self._position)
