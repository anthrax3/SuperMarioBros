import pygame
from gameengine.util.Vector2 import Vector2

from gameengine.components.Collider import Collider
from gameengine.components.CustomDraw import CustomDraw
from gameengine.components.Input import Input
from gameengine.components.Physics import Physics
from gameengine.components.Script import Script
from gameengine.core.GameObject import GameObject
from gameengine.core.Interpolation import Interpolation
from gameengine.core.Scene import Scene
from gameengine.core.World import World
from gameengine.managers.SceneManager import SceneManager

pygame.init()
clock = pygame.time.Clock()

World.display = pygame.display.set_mode((800, 464), 0, 32)

class DragScript(Script):
    def onCreate(self):
        self.gameObject.addComponent(Input)

class ObjScript(Script):
    def onCreate(self):
        self.physics = self.gameObject.getComponent(Physics)


class Obj(GameObject, Script):
    def __init__(self):
        super().__init__()
        self.transform.size = Vector2(50, 50)

        self.addComponent(Input)
        self.addComponent(CustomDraw)
        self.addComponent(Physics)
        self.addComponent(Collider)
        self.addScript(self)

        self.physics = self.getComponent(Physics)

    def onMouseDrag(self, pos, rel, buttons):
        self.move(rel)


    def onDraw(self):
        surface = pygame.Surface(self.transform.size.tuple())
        surface.fill((255, 0, 0))
        return surface

    def onCollisionEnter(self, other, side):
        return True

    def move(self, rel):
        if self == self.scene.obj1:
            self.physics.move(*rel)

            def followObj2(abs, rel):
                self.scene.obj2.move(rel)

            Interpolation(Vector2(), Vector2(rel), 100, Interpolation.SLERP, followObj2).start()

        elif self == self.scene.obj2:
            self.physics.move(*rel)

            def followObj3(abs, rel):
                self.scene.obj3.move(rel)

            Interpolation(Vector2(), Vector2(rel), 100, Interpolation.SLERP, followObj3).start()

        elif self == self.scene.obj3:
            self.physics.move(*rel)


class Listener(GameObject, Script):
    def __init__(self):
        super().__init__()

        self.addComponent(Input)
        self.addScript(self)

    def onKeyDown(self, key):
        if key == pygame.K_a:
            self.scene.obj1.transform.parent = None
            self.scene.obj2.transform.parent = self.scene.obj1.transform
            self.scene.obj3.transform.parent = self.scene.obj2.transform

            # obj1 None []
            # obj2 None []
            # CASE 1
            # obj1 None [obj1]
            # obj2 obj1 []

        elif key == pygame.K_z:
            # self.scene.obj2.transform.parent = None
            self.scene.obj3.transform.parent = None
            self.scene.obj2.transform.parent = self.scene.obj3.transform
            self.scene.obj1.transform.parent = self.scene.obj2.transform


class Scene1(Scene):
    def onLoad(self):
        self.obj1 = Obj()
        self.obj1.addScript(ObjScript)

        self.obj2 = Obj()
        self.obj2.transform.position = Vector2(100, 100)
        # TODO add property to position and localPosition


        self.obj3 = Obj()
        self.obj3.transform.position = Vector2(200, 200)
        # self.obj3.transform.parent = self.obj2.transform
        # self.obj2.transform.parent = self.obj1.transform

        self.mainCamera.transform.depth = -999
        self.mainCamera.addScript(DragScript)
        # self.mainCamera.transform.parent = self.obj1.transform
        self.mainCamera.transform.localPosition = Vector2(-100, -100)

        Listener()

        pos = self.obj2.transform.position
        pos = Vector2(0, 0)

        # self.obj2.transform.position = Vector2(0, 0)

        # l = lambda value: value * 2

SceneManager().loadScene(Scene1)


# for i in (smooth_interpolate(Vector2(0, 0), Vector2(100, 50), 10)):
#     print(i)

while True:

    World.update()
    World.draw()
    clock.tick(60)
