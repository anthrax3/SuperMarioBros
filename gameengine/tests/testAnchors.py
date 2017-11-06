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

class Printy(Script):
    def onUpdate(self):
        pass
        # print(self.gameObject.transform.worldRect)
        # print(self.gameObject.getComponent(CustomDraw).worldRect)

        # print(self.gameObject.transform.localPosition)
        # print(self.gameObject.transform.position)
        # print(self.gameObject.transform.pivot.ratio)

        # print("piv", self.gameObject.transform.pivot.getWorldPosition())
        # if self.gameObject.transform.parent is not None:
        #     print("anself.gameObject.transform.pivot.getWorldPosition())
        # if self.gameObject.transform.parent is not None:
        #     print("anc", self.gameObject.transform.anchor.getWorldPosition())

        # rect = self.gameObject.transform.worldRect
        # rect.topLeft = Vector2(100, 100)
        # self.gameObject.transform.worldRect = rect

    def onBecameInvisible(self):
        print("Invisible")

class MoveCamera(Script):
    def onCreate(self):
        self.gameObject.addComponent(Input)

    def onMouseDrag(self, pos, rel, buttons):
        if buttons[0]:
            self.gameObject.transform.localPosition -= rel

    # def Update(self):
    #     print(self.gameObject.windowRect.topLeft)

class Resize(Script):
    def onCreate(self):
        self.gameObject.addComponent(Input)

    # def onMouseClicked(self, pos):
    #     self.gameObject.transform.pivot.set(0, 0)

    def onMouseDrag(self, pos, rel, buttons):
        if buttons[0]:
            self.gameObject.transform.localPosition += rel
        elif buttons[2]:
            self.gameObject.transform.size += rel

class Deparent(Script):
    def onMouseClicked(self, pos):
        if self.gameObject.transform.parent is None:
            self.gameObject.transform.parent = self.gameObject.scene.p.transform
        else:
            print("Deparenting")
            # print(self.gameObject.transform.pivot.ratio)
            self.gameObject.transform.parent = None
            # print(self.gameObject.transform.pivot.ratio)


class Square(GameObject, Script):
    def __init__(self, size, color):
        super().__init__()
        self.transform.size = Vector2(size)
        self.color = color

        self.addComponent(CustomDraw)
        self.addScript(Resize)
        self.addScript(self)

    def onUpdate(self):
        pass

    def onDraw(self):
        surface = pygame.Surface(self.transform.size)
        surface.fill(self.color)
        return surface


    def onMouseDown(self, pos, button):
        print("DOWN")


class Square2(GameObject, Script):
    def __init__(self):
        super().__init__()
        self.transform.size = Vector2(100, 100)
        self.transform.pivot.set(0.5, 1)
        self.transform.depth = 1

        self.addComponent(CustomDraw).size = Vector2(50, 50)
        # self.addComponent(CustomDraw).localPosition = Vector2(25, 50)
        self.addScript(self)

    def onDraw(self):
        surface = pygame.Surface(self.getComponent(CustomDraw).size)
        surface.fill((0, 255, 0))
        return surface

    def onUpdate(self):
        self.getComponent(CustomDraw).size += Vector2(0.5, 1)


class Scene1(Scene):
    def onLoad(self):
        self.mainCamera.addScript(MoveCamera)

        s2 = Square2()
        s2.transform.position = Vector2(0, 0)

        print("WORLDRECT: ", s2.transform.worldRect)
        print("WORLDRECT: ", s2.getComponent(CustomDraw).worldRect)



        self.p = Square((200, 150), (255, 0, 0))
        self.p.transform.pivot.set(0.5, 0.5)
        self.p.addComponent(Input).size = Vector2(self.p.transform.size / 2)

        print("INPUT_POS:", self.p.getComponent(Input).position)
        print("INPUT_SIZE:", self.p.getComponent(Input).size)
        print("INPUT_WORLD_RECT:", self.p.getComponent(Input).worldRect)

        # self.p.addScript(Printy)
        # self.p.transform.pivot.set(0.5, 0.5)
        #
        c = Square((20, 20), (0, 0, 255))
        c.transform.parent = self.p.transform
        c.addScript(Printy)
        c.transform.anchor.set(0, 0, overridePivot=True)
        c.addScript(Deparent)
        # c.transform.localPosition = Vector2(20, 20)
        # c.transform.pivot.set(0.8, 0.8)

        #
        c = Square((20, 20), (0, 0, 200))
        c.addScript(Deparent)
        c.addScript(Printy)
        # c.transform.localPosition += Vector2(10, 10)
        # print(c.transform.localPosition)

        c.transform.parent = self.p.transform
        # c.transform.parent = None
        c.transform.anchor.set(0.5, 0, overridePivot=True, overridePosition=True)
        # c.transform.pivot.set(0, 0)

        c = Square((20, 20), (0, 0, 200))
        print(c.transform.position)
        c.transform.parent = self.p.transform
        print(c.transform.position)
        c.transform.anchor.set(0, 0.5, overridePivot=True, overridePosition=True)

        c = Square((20, 20), (0, 0, 200))
        c.transform.parent = self.p.transform
        c.transform.anchor.set(0, 1, overridePivot=True, overridePosition=True)

        c = Square((20, 20), (0, 0, 200))
        c.transform.parent = self.p.transform
        c.transform.anchor.set(0.5, 0, overridePivot=True, overridePosition=True)

        c = Square((20, 20), (0, 0, 200))
        c.transform.parent = self.p.transform
        c.transform.anchor.set(0.5, 0.5, overridePivot=True, overridePosition=True)

        c = Square((20, 20), (0, 0, 200))
        c.transform.parent = self.p.transform
        c.transform.anchor.set(0.5, 1, overridePivot=True, overridePosition=True)

        c = Square((20, 20), (0, 0, 200))
        c.transform.parent = self.p.transform
        c.transform.anchor.set(1, 0, overridePivot=True, overridePosition=True)

        c = Square((20, 20), (0, 0, 200))
        c.transform.parent = self.p.transform
        c.transform.anchor.set(1, 0.5, overridePivot=True, overridePosition=True)

        c = Square((20, 20), (0, 0, 200))
        c.transform.parent = self.p.transform
        c.transform.anchor.set(1, 1, overridePivot=True, overridePosition=True)
        c.transform.pivot.set(1, 1)







SceneManager().loadScene(Scene1)


while True:
    World.update()
    World.draw()
    clock.tick(60)