import pygame
from gameengine.util.Vector2 import Vector2

from gameengine.components.Collider import Collider
from gameengine.components.CustomDraw import CustomDraw
from gameengine.components.Input import Input
from gameengine.components.Physics import Physics
from gameengine.components.Script import Script
from gameengine.core.Constants import LEFT_SIDE, RIGHT_SIDE, TOP_SIDE
from gameengine.core.GameObject import GameObject
from gameengine.core.Scene import Scene
from gameengine.core.World import World
from gameengine.managers.SceneManager import SceneManager
from gameengine.scripts.Debug import debug


class OneSideCollision(Script):
    def onCreate(self):
        self.gameObject.addComponent(Physics)
        self.gameObject.addComponent(Collider)

    def onCollisionEnter(self, other, side):
        if side == LEFT_SIDE or side == RIGHT_SIDE or side == TOP_SIDE:
            return True
        return False


# class White(Script):
#     def __init__(self, gameObject):
#         super().__init__(gameObject)

class Controls(Script):
    def onCreate(self):
        self.gameObject.addComponent(Input)
        print(self.gameObject)

    def onKeyDown(self, key):
        physics = self.gameObject.getComponent(Physics)

        if key == pygame.K_RIGHT:
            physics.move(10, 0)
        elif key == pygame.K_LEFT:
            physics.move(-10, 0)
        if key == pygame.K_UP:
            physics.move(0, -10)
        elif key == pygame.K_DOWN:
            physics.move(0, 10)

    def onMouseDrag(self, pos, rel, buttons):
        # self.gameObject.getComponent(Physics).move(*rel)
        self.gameObject.getComponent(Physics).move(*rel)


class Green(Script):
    def onDraw(self):
        surface = pygame.Surface(self.gameObject.getComponent(CustomDraw).size)
        surface.fill((0, 255, 0))
        return surface


class Extraction(Script):
    def onCreate(self):
        self.gameObject.addComponent(Input)
        self.gameObject.addComponent(CustomDraw)

    def onDraw(self):
        surface = pygame.Surface((50, 50))
        surface.fill((255, 0, 255))
        return surface


class Wall(GameObject, Script):
    def __init__(self):
        super().__init__()
        self.transform.size = Vector2(100, 10)

        self.addComponent(CustomDraw)
        self.addComponent(Collider)
        self.addScript(self)

    def onDraw(self):
        surface = pygame.Surface((50, 50))
        surface.fill((255, 255, 255))
        return surface

    def onCollisionEnter(self, other, side):
        return True


class Square(GameObject, Script):
    def __init__(self):
        super().__init__()
        self.addComponent(CustomDraw).size = Vector2(50, 50)

        self.addScript(self)
        self.addScript(Controls)
        s = self.addScript(Green)
        self.addScript(Extraction).order = -1
        self.addScript(OneSideCollision)
        self.transform.size = Vector2(50, 50)

    def onUpdate(self):
        print("da")


pygame.init()
clock = pygame.time.Clock()

World.display = pygame.display.set_mode((800, 464), 0, 32)

class Scene1(Scene):
    def onLoad(self):
        s = Square()
        # s.addScript(White)
        # s.addScript(OneSideCollision)
        # s.transform.position = Vector2(50, 50)

        # s = Square()
        # s.addScript(White)
        # s.addScript(Green)
        # s.addScript(OneSideCollision)
        # s.transform.position = Vector2(200, 200)

SceneManager().loadScene(Scene1)

while True:
    World.update()
    World.draw()
    clock.tick(60)
