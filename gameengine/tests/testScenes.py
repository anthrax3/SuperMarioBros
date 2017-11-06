import pygame
from gameengine.util.Vector2 import Vector2

from gameengine.components.CustomDraw import CustomDraw
from gameengine.components.Input import Input
from gameengine.components.Script import Script
from gameengine.core.GameObject import GameObject
from gameengine.core.Scene import Scene
from gameengine.core.World import World
from gameengine.managers.SceneManager import SceneManager
from gameengine.util.Timer import Timer

pygame.init()
clock = pygame.time.Clock()

World.display = pygame.display.set_mode((800, 464), 0, 32)


class Square(GameObject, Script):
    def __init__(self):
        super().__init__()
        self.addComponent(CustomDraw)
        self.addComponent(Input)

        self.addScript(self)

        self.transform.size = Vector2(50, 50)

    def onMouseDrag(self, pos, rel, buttons):
        self.transform.position += rel

    def onDraw(self):
        surface = pygame.Surface((50, 50))
        surface.fill((0, 255, 0))
        return surface

    def onKeyDown(self, key):
        if key == pygame.K_RIGHT:
            self.transform.position += Vector2(10, 0)


class Square2(Square):
    def __init__(self):
        super().__init__()
        self.transform.size = Vector2(100, 100)

    def onDraw(self):
        surface = pygame.Surface((100, 100))
        surface.fill((255, 0, 0))
        return surface

    def onKeyDown(self, key):
        pass


class Level1(Scene):
    def onLoad(self):
        Square().transform.position = Vector2(200, 200)


        # destroy(self.mainCamera)
        # destroy(self.mainCamera)
        Timer(1000, lambda: SceneManager().loadScene(Level2), cycles=1).start()


class Level2(Scene):
    def onLoad(self):
        self.mainCamera.transform.size = Vector2(400, 232)
        self.mainCamera.transform.position = Vector2(400, 232)

        Square2().transform.position = Vector2(50, 50)

        Timer(1000, lambda: SceneManager().loadScene(Level1), cycles=1).start()


SceneManager().loadScene(Level1)
# SceneManager().loadScene(Level2)

# Timer(2000, lambda: SceneManager().loadScene(Level1), startNow=True).start()
# Timer(2000, lambda: SceneManager().loadScene(Level2)).start()

while True:
    World.update()
    World.draw()
    clock.tick(60)