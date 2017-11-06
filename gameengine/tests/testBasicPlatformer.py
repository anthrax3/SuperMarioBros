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
        surface.fill((255, 0, 0))
        return surface

    def onKeyDown(self, key):
        if key == pygame.K_UP:
            self.physics.addForce(Vector2(0, -5))

    def onUpdate(self):
        print(self.customDraw.position)
        print(self.customDraw.worldRect)

    def onCollisionEnter(self, other, side):
        print("da9")

        print("o", other)
        if isinstance(other, Wall):
            self.physics.velocity.y = 0
            return True
        return True


class Player(GameObject):
    def __init__(self):
        super().__init__()
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
        PhysicsManager().gravity = Vector2(0, 0.1)

        w = Wall(700, 5)
        print(w.transform.position.hasChanged._listeners)

        w.transform.position = (50, 500)

        p = Player()
        p.transform.position = (400, 200)
        p.transform.size = (50, 50)


SceneManager().loadScene(MainScene)

while True:
    World.update()
    World.draw()
    clock.tick(60)
