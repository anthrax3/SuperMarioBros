from gameengine.util.GridSpacePartition import GridSpacePartition
from gameengine.util.Rect import Rect
from gameengine.util.util import print_timing

from gameengine.util.util import print_timing


class GridSpacePartitionModified:
    def __init__(self, x, y, cellSize):
        self.x = x
        self.y = y
        self.cellSize = cellSize

        self.grid = [[[]] * self.x] * self.y

    @print_timing
    def add(self, collider, rect):
        iTopLeft = int(rect.topLeft.x / self.cellSize)
        jTopLeft = int(rect.topLeft.y / self.cellSize)

        iBottomRight = int(rect.bottomRight.x / self.cellSize)
        jBottomRight = int(rect.bottomRight.y / self.cellSize)

        for i in range(iTopLeft, iBottomRight+1):
            for j in range(jTopLeft, jBottomRight+1):
                self.grid[i][j].append(collider)

    @print_timing
    def remove(self, collider, rect):
        iTopLeft = int(rect.topLeft.x / self.cellSize)
        jTopLeft = int(rect.topLeft.y / self.cellSize)

        iBottomRight = int(rect.bottomRight.x / self.cellSize)
        jBottomRight = int(rect.bottomRight.y / self.cellSize)

        for i in range(iTopLeft, iBottomRight + 1):
            for j in range(jTopLeft, jBottomRight + 1):
                self.grid[i][j].remove(collider)

    @print_timing
    def getColliding(self, collider, rect):
        colliding = []

        iTopLeft = int(rect.topLeft.x / self.cellSize)
        jTopLeft = int(rect.topLeft.y / self.cellSize)

        iBottomRight = int(rect.bottomRight.x / self.cellSize)
        jBottomRight = int(rect.bottomRight.y / self.cellSize)

        for i in range(iTopLeft, iBottomRight + 1):
            for j in range(jTopLeft, jBottomRight + 1):
                for otherCollider in self.grid[i][j]:
                    if otherCollider != collider and otherCollider not in colliding:
                        colliding.append(otherCollider)

        return colliding


class Element:
    pass


grid = GridSpacePartition(64)
gridM = GridSpacePartitionModified(1000, 1000, 64)

e = Element()
r = Rect(100, 100, 56, 600)

grid.insert(e, r)
gridM.add(e, r)

grid.remove(e, r)
gridM.remove(e, r)
