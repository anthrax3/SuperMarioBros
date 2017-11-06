from gameengine.util.Vector2 import Vector2

from gameengine.util.Rect import Rect


class Grid:
    def __init__(self, center: Vector2, cellSize: Vector2):
        super().__init__()

        self.center = center
        self.cellSize = cellSize

    def at(self, i, j) -> Rect:
        return Rect(self.center.x + i * self.cellSize.x, self.center.y + j * self.cellSize.y, *self.cellSize)