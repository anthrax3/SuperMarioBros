import pygame
from gameengine.util.Vector2 import Vector2

from gameengine.components.CustomDraw import CustomDraw
from gameengine.components.Input import Input
from gameengine.components.Script import Script
from gameengine.core.GameObject import GameObject
from gameengine.core.Scene import Scene
from gameengine.core.World import World
from gameengine.managers.SceneManager import SceneManager

pygame.init()
clock = pygame.time.Clock()
World.display = pygame.display.set_mode((800, 464), 0, 32)


class Square(GameObject, Script):
    def __init__(self):
        super().__init__()
        self.transform.size = Vector2(50, 50)

        self.addComponent(CustomDraw)
        self.addComponent(Input)
        self.addScript(self)

    def onDraw(self):
        surface = pygame.Surface(self.transform.size)
        surface.fill((0, 255, 255))
        return surface

    def onMouseDrag(self, pos, rel, buttons):
        def move(abs, rel):
            self.gameObject.transform.position += rel

        from gameengine.core.Interpolation import Interpolation
        from gameengine.core.Interpolation import CubicBezier
        Interpolation(Vector2(), Vector2(rel), 300, callback=move, method=CubicBezier,
                      args=(.04,.19,.12,1.57)).start()
        # (.22, 1.24, .65, 1.25)

class CameraSlerpDrag(Script):
    def onMouseDrag(self, pos, rel, buttons):
        def moveCamera(abs, rel):
            self.gameObject.transform.position -= rel

        from gameengine.core.Interpolation import Interpolation
        from gameengine.core.Interpolation import Ease
        from gameengine.core.Interpolation import EaseOut
        from gameengine.core.Interpolation import EaseIn
        Interpolation(Vector2(), Vector2(rel), 100, moveCamera, EaseOut).start()


class Test(Scene):
    def onLoad(self):
        self.mainCamera.addComponent(Input)
        self.mainCamera.addScript(CameraSlerpDrag)

        first = World.instantiate(Square, Vector2(50, 50))
        World.instantiate(Square, Vector2(100, 100), first.transform, True)
        World.instantiate(Square, Vector2(0, 0), first.transform, False)


SceneManager().loadScene(Test)

while True:
    World.update()
    World.draw()
    clock.tick(60)
