from gameengine.util.Vector2 import Vector2
# from pygame.rect import Rect

from gameengine.core.GameObject import GameObject
from gameengine.managers.CameraManager import CameraManager
from gameengine.util.Rect import Rect


class Camera(GameObject):
    def __init__(self):
        super().__init__()

        self.managers = [] # TODO minor fix
        CameraManager().addObject(self)
        self.enabled = True

        self.windowRect = Rect(0, 0, 0, 0)
        self._zoom = 1.0

        self.backgroundColor = (128, 128, 255)

    @property
    def zoom(self) -> float:
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        if value <= 0.1:
            value = 0.1

        oldZoom = self._zoom
        self._zoom = value

        self.transform.size *= (oldZoom / self._zoom)

    def zoomAt(self, x, y, zoom):
        delta = Vector2(x, y) - self.transform.worldRect.topLeft
        print("delta", delta)
        oldZoom = self.zoom
        self.zoom = zoom
        newRect = Rect(*(self.transform.worldRect.topLeft + delta * (self.zoom - oldZoom) / self.zoom), *self.transform.size)
        self.transform.worldRect = newRect

    def windowToGamePos(self, windowX, windowY) -> Vector2:
        return ((Vector2(windowX, windowY)/self.zoom - self.windowRect.topLeft) + self.transform.worldRect.topLeft)

    def destroy(self):
        super().destroy()
        CameraManager().removeObject(self)