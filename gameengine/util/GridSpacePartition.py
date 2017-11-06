from gameengine.util.util import print_timing


class GridSpacePartition:
    def __init__(self, cellSize):
        self.cellSize = cellSize
        self.grid = {}

    @staticmethod
    def keyFromIndices(i: int, j: int) -> str:
        return "{},{}".format(i, j)

    @print_timing
    def insert(self, collider, rect):
        iTopLeft = int(rect.topLeft.x / self.cellSize)
        jTopLeft = int(rect.topLeft.y / self.cellSize)

        iBottomRight = int(rect.bottomRight.x / self.cellSize)
        jBottomRight = int(rect.bottomRight.y / self.cellSize)

        for i in range(iTopLeft, iBottomRight+1):
            for j in range(jTopLeft, jBottomRight+1):
                key = self.keyFromIndices(i, j)
                if key not in self.grid.keys():
                    # Create empty list for containing references to colliders
                    self.grid[key] = []

                self.grid[key].append(collider)

    @print_timing
    def remove(self, collider, rect):
        iTopLeft = int(rect.topLeft.x / self.cellSize)
        jTopLeft = int(rect.topLeft.y / self.cellSize)

        iBottomRight = int(rect.bottomRight.x / self.cellSize)
        jBottomRight = int(rect.bottomRight.y / self.cellSize)

        for i in range(iTopLeft, iBottomRight + 1):
            for j in range(jTopLeft, jBottomRight + 1):
                key = self.keyFromIndices(i, j)
                self.grid[key].remove(collider)

                if not self.grid[key]:
                    del self.grid[key]

    @print_timing
    def intersect(self, rect):
        colliding = []

        iTopLeft = int(rect.topLeft.x / self.cellSize)
        jTopLeft = int(rect.topLeft.y / self.cellSize)

        iBottomRight = int(rect.bottomRight.x / self.cellSize)
        jBottomRight = int(rect.bottomRight.y / self.cellSize)

        for i in range(iTopLeft, iBottomRight + 1):
            for j in range(jTopLeft, jBottomRight + 1):
                key = self.keyFromIndices(i, j)

                if key not in self.grid.keys():
                    continue

                for otherCollider in self.grid[key]:
                    if otherCollider not in colliding:
                        colliding.append(otherCollider)

        return colliding


# class GridSpacePartition:
#     def __init__(self, x, y, cellSize):
#         self.x = x
#         self.y = y
#         self.cellSize = cellSize
#
#         self.grid = [[[]] * self.x] * self.y
#
#     @print_timing
#     def add(self, collider, rect):
#         iTopLeft = int(rect.topLeft.x / self.cellSize)
#         jTopLeft = int(rect.topLeft.y / self.cellSize)
#
#         iBottomRight = int(rect.bottomRight.x / self.cellSize)
#         jBottomRight = int(rect.bottomRight.y / self.cellSize)
#
#         for i in range(iTopLeft, iBottomRight + 1):
#             for j in range(jTopLeft, jBottomRight + 1):
#                 self.grid[i][j].append(collider)
#
#     @print_timing
#     def remove(self, collider, rect):
#         iTopLeft = int(rect.topLeft.x / self.cellSize)
#         jTopLeft = int(rect.topLeft.y / self.cellSize)
#
#         iBottomRight = int(rect.bottomRight.x / self.cellSize)
#         jBottomRight = int(rect.bottomRight.y / self.cellSize)
#
#         for i in range(iTopLeft, iBottomRight + 1):
#             for j in range(jTopLeft, jBottomRight + 1):
#                 self.grid[i][j].remove(collider)
#
#     @print_timing
#     def getColliding(self, collider, rect):
#         colliding = []
#
#         iTopLeft = int(rect.topLeft.x / self.cellSize)
#         jTopLeft = int(rect.topLeft.y / self.cellSize)
#
#         iBottomRight = int(rect.bottomRight.x / self.cellSize)
#         jBottomRight = int(rect.bottomRight.y / self.cellSize)
#
#         for i in range(iTopLeft, iBottomRight + 1):
#             for j in range(jTopLeft, jBottomRight + 1):
#                 for otherCollider in self.grid[i][j]:
#                     if otherCollider != collider and otherCollider not in colliding:
#                         colliding.append(otherCollider)
#
#         return colliding
