from functools import reduce

from gameengine.core.Constants import TOP_SIDE, RIGHT_SIDE, BOTTOM_SIDE, LEFT_SIDE, TOTAL_SIDES
from gameengine.core.ObjectManager import ObjectManager
from gameengine.util.GridSpacePartition import GridSpacePartition
from gameengine.util.Rect import Rect
from gameengine.util.util import Singleton, vecToSide, print_timing


# from pygame.rect import Rect


@Singleton
class CollisionManagerMod(ObjectManager):
    """Géstion de collisions de type AABB
    source: https://gamedev.stackexchange.com/questions/69339/2d-aabbs-and-resolving-multiple-collisions

    Il devrait partitionner l'espace pour détécter les collisions des objets proches, et non pas vérifier contre chaque collider.

    Plus de détails sur: http://www.gameprogrammingpatterns.com/spatial-partition.html

    Un quadtree ou k-d tree serait bien, car le monde est grand, on a des objets de dimensions différentes, et partitionner ses coordonées
    dans des célules egales n'est pas très efficace mais je dois écrire un mécanisme qui détècte les changements de position et de dimension
    pour actualiser la grille proprement."""

    def __init__(self):
        super().__init__()

        self.movementsQueue = []

        self.touchCollisions = []
        self.enterCollisions = []
        self.stayCollisions = []

        # from gameengine.util.pyqtree import Index
        # self.quadtree = Index(bbox=(0, 0, 7000, 500))

        from gameengine.util.GridSpacePartition import GridSpacePartition
        self.grid = GridSpacePartition(64)

    def addObject(self, object):
        self.grid.insert(object, object.worldRect)
        # self.quadtree.insert(object, object.worldRect.tuple())
        super().addObject(object)

    def removeObject(self, object):
        for movement in self.movementsQueue:
            if movement.collider == object:
                self.movementsQueue.remove(movement)

        for pair in self.enterCollisions + self.stayCollisions:
            if pair.contains(object):
                if pair in self.enterCollisions:
                    self.enterCollisions.remove(pair)
                else:
                    self.stayCollisions.remove(pair)

        # self.quadtree.remove(object, object.worldRect.tuple())
        self.grid.remove(object, object.worldRect)
        super().removeObject(object)

    def queueMovement(self, collider, dx, dy):
        self.movementsQueue.append(ColliderMovement(collider, dx, dy))

    # @print_timing
    def resolveCollision(self, collidingList, collider, rect, dx=0, dy=0):
        if collider.gameObject is None:
            return

        if dx == 0 and dy == 0:
            return

        rect.move(dx, dy)
        side = vecToSide(dx, dy)

        # print(dx, dy, collider.gameObject, side)

        for other in collidingList:
            if not other.enabled:
                continue
            if other.gameObject is None:
                continue

            if not other.worldRect.collideRect(rect):
                continue

            pair = Pair(collider, other)

            if pair not in self.enterCollisions and pair not in self.stayCollisions:
                from functools import reduce
                firstResults = list(map(lambda script: script.onCollisionEnter(other.gameObject, side), collider.gameObject.scripts))
                first = reduce(lambda v1, v2: v1 or v2, firstResults, False)

                secondResults = list(map(lambda script: script.onCollisionEnter(collider.gameObject, TOTAL_SIDES - side), other.gameObject.scripts))
                second = reduce(lambda v1, v2: v1 or v2, secondResults, False)

                errorStr = "NoneType returned from onCollisionEnter callback on gameObject {}"
                if first is None:
                    raise RuntimeError(errorStr.format(collider.gameObject))
                elif second is None:
                    raise RuntimeError(errorStr.format(other.gameObject))

                if first and second:
                    self.touchCollisions.append(pair)
                    self.clampOff(rect, other.worldRect, side)
                    # print("CLAMPED_OFF", dx, dy)
                    # collidingList = self.getColliding(collider, rect)
                else:
                    self.enterCollisions.append(pair)

            elif pair in self.enterCollisions and pair not in self.stayCollisions:
                self.enterCollisions.remove(pair)
                self.stayCollisions.append(pair)

        inEnterStay = [pair.other(collider) for pair in self.enterCollisions + self.stayCollisions if pair.contains(collider)]

        exitCollisions = [other for other in inEnterStay if other not in collidingList]

        for other in exitCollisions:
            for script in collider.gameObject.scripts:
                script.onCollisionExit(other.gameObject, TOTAL_SIDES - side)

            for script in other.gameObject.scripts:
                script.onCollisionExit(collider.gameObject, side)

            pair = Pair(collider, other)
            if pair in self.enterCollisions:
                self.enterCollisions.remove(pair)
            if pair in self.stayCollisions:
                self.stayCollisions.remove(pair)

    # @print_timing
    def onUpdate(self):
        # print("mm", self.movementsQueue)
        self.touchCollisions = []

        for pair in self.stayCollisions:
            for script in pair.first.gameObject.scripts:
                script.onCollisionStay(pair.second.gameObject)
            for script in pair.second.gameObject.scripts:
                script.onCollisionStay(pair.first.gameObject)

        while self.movementsQueue:
            info = self.movementsQueue[0]

            # info.collider.gameObject.transform.position += (info.dx, info.dy)
            beforeColliderRect = info.collider.worldRect
            colliderRect = info.collider.worldRect

            finalRect = info.collider.worldRect
            finalRect.move(info.dx, info.dy)
            intersect = list(self.getColliding(info.collider, finalRect))

            self.resolveCollision(intersect, info.collider, colliderRect, info.dx, 0)

            # from gameengine.tests.SuperMarioBros import Player
            # if isinstance(info.collider.gameObject, Player):
            #     print("[crX]", colliderRect)

            self.resolveCollision(intersect, info.collider, colliderRect, 0, info.dy)

            # from gameengine.tests.SuperMarioBros import Player
            # if isinstance(info.collider.gameObject, Player):
            #     print("[crY]", colliderRect)
            #     print("inters", [col.gameObject for col in intersect])

            info.collider.gameObject.transform.position += (colliderRect.topLeft - beforeColliderRect.topLeft)

            # Maybe removed on component removal(see above)
            if info in self.movementsQueue:
                self.movementsQueue.remove(info)

    def clampOff(self, thisRect: Rect, otherRect: Rect, side):
        if side == TOP_SIDE:
            thisRect.top = otherRect.bottom
        elif side == RIGHT_SIDE:
            thisRect.right = otherRect.left
        elif side == BOTTOM_SIDE:
            thisRect.bottom = otherRect.top
        elif side == LEFT_SIDE:
            thisRect.left = otherRect.right

        # Add the difference relative to the pivot
        # collider.position += (temp.topLeft - collider.worldRect.topLeft)
        # thisRect.gameObject.transform.position += (temp.topLeft - thisRect.worldRect.topLeft)

    def getColliding(self, collider, rect):
        # l = self.quadtree.intersect(collider.worldRect.tuple())
        l = self.grid.intersect(rect)

        for other in l:
            if other != collider and rect.collideRect(other.worldRect):
                # if ("Player" in collider.gameObject.tags or "Player" in other.gameObject.tags) and \
                #         ("Enemy" in collider.gameObject.tags or "Enemy" in other.gameObject.tags):
                #     aze = 45

                if (not collider.layers) and (not other.layers):
                    yield other
                else:
                    commonLayers = [layer for layer in collider.layers if layer in other.layers]

                    if len(commonLayers) > 0:
                        yield other

    # # DO NOT USE
    # def getCollidingList(self, gameObject) -> list:
    #     from gameengine.components.Collider import Collider
    #     collider = gameObject.getComponent(Collider)
    #     if collider is None:
    #         raise RuntimeError("{} doesn't have a Collider".format(collider))
    #
    #     list = []
    #     for pair in self.touchCollisions + self.enterCollisions + self.stayCollisions:
    #         if pair.contains(collider):
    #             other = pair.other(collider)
    #             if other not in list:
    #                 list.append(other.gameObject)
    #
    #     return list


@Singleton
class CollisionManager(ObjectManager):
    def __init__(self):
        super().__init__()

        self.grid = GridSpacePartition(64)

        # from gameengine.util.pyqtree import Index
        # self.quadtree = Index(bbox=(0, 0, 7000, 500))

        self.movementsQueue = []

        self.touchCollisions = []
        self.enterCollisions = []
        self.stayCollisions = []

    def queueMovement(self, collider, dx, dy):
        self.movementsQueue.append(ColliderMovement(collider, dx, dy))
        # print("mqueue", self.movementsQueue)

    def clampOff(self, thisRect: Rect, otherRect: Rect, side):
        if side == TOP_SIDE:
            thisRect.top = otherRect.bottom
        elif side == RIGHT_SIDE:
            thisRect.right = otherRect.left
        elif side == BOTTOM_SIDE:
            thisRect.bottom = otherRect.top
        elif side == LEFT_SIDE:
            thisRect.left = otherRect.right

    def addObject(self, object):
        self.grid.insert(object, object.worldRect)
        super().addObject(object)

    def removeObject(self, object):
        self.grid.remove(object, object.worldRect)

        for movement in reversed(self.movementsQueue):
            if movement.collider == object:
                self.movementsQueue.remove(movement)

        for pair in reversed(self.enterCollisions):
            if pair.contains(object):
                self.enterCollisions.remove(pair)

        for pair in reversed(self.stayCollisions):
            if pair.contains(object):
                self.stayCollisions.remove(pair)

        super().removeObject(object)

    @print_timing
    def onUpdate(self):
        for pair in self.stayCollisions:
            for script in pair.first.gameObject.scripts:
                script.onCollisionStay(pair.second.gameObject)
            for script in pair.second.gameObject.scripts:
                script.onCollisionStay(pair.first.gameObject)

        for movement in self.movementsQueue:
            colliderRectBefore = movement.collider.worldRect

            # Get collisions on both axes to have a list of all possible collisions.
            colliderRectMoved = movement.collider.worldRect
            colliderRectMoved.move(movement.dx, movement.dy)
            possibilities = self.grid.intersect(colliderRectMoved)

            if movement.collider in possibilities:
                possibilities.remove(movement.collider)

            colliderRectToResolve = movement.collider.worldRect

            self.resolveRectangle(movement.collider, colliderRectToResolve, possibilities, movement.dx, movement.dy)

            movement.collider.gameObject.transform.position += (colliderRectToResolve.topLeft - colliderRectBefore.topLeft)

            self.movementsQueue = []

    def resolveRectangle(self, collider, rect, possibilities, dx=0, dy=0):
        if dx == 0 and dy == 0:
            return

        if dx != 0 and dy != 0:
            self.resolveRectangle(collider, rect, possibilities, dx, 0)
            self.resolveRectangle(collider, rect, possibilities, 0, dy)
            return

        currentlyColliding = []

        clampOffWith = (None, None)

        rect.move(dx, dy)
        for other in possibilities:
            pair = Pair(collider, other)
            otherRect = other.worldRect

            if rect.collideRect(otherRect):
                currentlyColliding.append(other)

                side = vecToSide(dx, dy)

                if pair not in self.enterCollisions and pair not in self.stayCollisions:

                    firstResults = list(map(lambda script: script.onCollisionEnter(other.gameObject, side), collider.gameObject.scripts))
                    first = reduce(lambda v1, v2: v1 or v2, firstResults, False)

                    secondResults = list(map(lambda script: script.onCollisionEnter(collider.gameObject, TOTAL_SIDES - side), other.gameObject.scripts))
                    second = reduce(lambda v1, v2: v1 or v2, secondResults, False)

                    errorStr = "NoneType returned from onCollisionEnter callback on gameObject {}"
                    if first is None:
                        raise RuntimeError(errorStr.format(collider.gameObject))
                    elif second is None:
                        raise RuntimeError(errorStr.format(other.gameObject))

                    if first and second:
                        clampOffWith = (otherRect, side)

                    else:
                        self.enterCollisions.append(pair)

                elif pair in self.enterCollisions and pair not in self.stayCollisions:
                    self.enterCollisions.remove(pair)
                    self.stayCollisions.append(pair)

        if None not in clampOffWith:
            self.clampOff(rect, clampOffWith[0], clampOffWith[1])

        # TODO: Exit collisions
        colliding = []
        for pair in self.enterCollisions + self.stayCollisions:
            if pair.contains(collider):
                colliding.append(pair.other(collider))

        exitCollisions = [col for col in colliding if col not in currentlyColliding]

        for other in exitCollisions:
            collider.gameObject.onCollisionExit(other.gameObject, -1)
            other.gameObject.onCollisionExit(collider.gameObject, -1)

            pair = Pair(collider, other)

            if pair in self.enterCollisions:
                self.enterCollisions.remove(pair)

            elif pair in self.stayCollisions:
                self.stayCollisions.remove(pair)

        currentlyColliding = []

        



class ColliderMovement:
    def __init__(self, collider, dx, dy):
        self.collider = collider
        self.dx = dx
        self.dy = dy


class Pair:
    def __init__(self, first, second):
            self.first = first
            self.second = second

    def contains(self, collider):
        return collider == self.first or collider == self.second

    def other(self, collider):
        if collider == self.first:
            return self.second
        elif collider == self.second:
            return self.first

    def __eq__(self, other):
        return (self.first == other.first and self.second == other.second) or (
            self.first == other.second and self.second == other.first)

    def __str__(self):
        return "Pair: {} {}".format(self.first, self.second)