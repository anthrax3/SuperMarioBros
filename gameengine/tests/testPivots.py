import pygame

from gameengine.components.Collider import Collider
from gameengine.components.CustomDraw import CustomDraw
from gameengine.components.Input import Input
from gameengine.components.Physics import Physics
from gameengine.components.Script import Script
from gameengine.components.Transform import Transform
from gameengine.core.GameObject import GameObject
from gameengine.core.Scene import Scene
from gameengine.core.World import World
from gameengine.managers.PhysicsManager import PhysicsManager
from gameengine.managers.SceneManager import SceneManager
from gameengine.util.Vector2 import Vector2

pygame.init()
clock = pygame.time.Clock()
World.display = pygame.display.set_mode((800, 600), 0, 32)


class PlayerScript(Script):
    def onCreate(self):
        self.physics = self.gameObject.addComponent(Physics)
        self.collider = self.gameObject.addComponent(Collider)
        self.input = self.gameObject.addComponent(Input)
        self.customDraw = self.gameObject.addComponent(CustomDraw)

    def onDraw(self):
        surface = pygame.Surface(self.gameObject.transform.size.tuple())
        surface.fill(self.gameObject.color)
        return surface

    def onMouseDrag(self, pos, rel, buttons):
        if buttons[0]:
            self.gameObject.transform.position += rel

        elif buttons[2]:
            self.gameObject.transform.size += rel
    # def onKeyDown(self, key):
    #     if key == pygame.K_UP:
    #         self.physics.addForce(Vector2(0, -5))

    # def onUpdate(self):
    #     print(self.customDraw.position)
    #     print(self.customDraw.worldRect)

    # def onMouseDown(self, pos, button):
    #     if button == 1:
    #         self.gameObject.transform.localPosition = (0, 0)
    #     elif button == 3:
    #         print(self.gameObject.transform.worldRect)

    def onMouseClicked(self, pos):
        # self.gameObject.transform.pivot.set(0, 0)
        self.gameObject.transform.localPosition = (0, 0)

    def onCollisionEnter(self, other, side):
        # print("da9")

        # print("o", other)
        if isinstance(other, Wall):
            self.physics.velocity.y = 0
            return True
        return True


class Player(GameObject):
    def __init__(self, color):
        super().__init__()
        self.color = color

        self.transform.position = (0, 0)
        self.transform.size = (50, 50)

        self.addScript(PlayerScript)


class WallScript(Script):
    def onCreate(self):
        self.collider = self.gameObject.addComponent(Collider)
        self.customDraw = self.gameObject.addComponent(CustomDraw)

    def onDraw(self):
        surface = pygame.Surface(self.gameObject.transform.size.tuple())
        surface.fill((0, 255, 255))
        return surface

    def onCollisionEnter(self, other, side):
        return True


class Wall(GameObject):
    def __init__(self, w, h):
        super().__init__()

        self.transform.size = (w, h)
        self.addScript(WallScript)


class MainScene(Scene):
    def onLoad(self):
        # PhysicsManager().gravity = Vector2(0, 0.1)

        w = Wall(700, 5)
        # print(w.transform.position.hasChanged._listeners)

        w.transform.position = (50, 500)

        p1 = Player((255, 0, 0))
        p1.transform.pivot.set(0.2, 0.2)
        # print(p1.transform.position)

        p2 = Player((0, 255, 0))

        p2.transform.parent = p1.transform

        p2.transform.pivot.set(0, 0)
        # p2.transform.anchor.set(0.5, 0.5)

        p2.transform.localPosition = (0, 0)



SceneManager().loadScene(MainScene)

while True:
    World.update()
    World.draw()
    clock.tick(60)
