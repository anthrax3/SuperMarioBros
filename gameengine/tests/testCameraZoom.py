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


class MoveCamera(Script):
    def onCreate(self):
        self.gameObject.addComponent(Input)

    def onMouseDrag(self, pos, rel, buttons):
        if buttons[0]:
            self.gameObject.transform.localPosition -= rel

    def onMouseDown(self, pos, button):
        if button == 4:
            self.gameObject.zoomAt(*pos, self.gameObject.zoom + 0.1)
        elif button == 5:
            self.gameObject.zoomAt(*pos, self.gameObject.zoom - 0.1)

        if button == 4 or button == 5:
            print("current zoom", self.gameObject.zoom)
            print(self.gameObject.transform.worldRect)

        # print("CAMERA INTERACTION")

class Resize(Script):
    def onCreate(self):
        self.gameObject.addComponent(Input)

    def onMouseDrag(self, pos, rel, buttons):
        if buttons[0]:
            self.gameObject.transform.localPosition += rel
        elif buttons[2]:
            self.gameObject.transform.size += rel


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

    # def Update(self):
    #     self.getComponent(CustomDraw).size += Vector2(0.5, 1)


class Scene1(Scene):
    def onLoad(self):
        self.mainCamera.addScript(MoveCamera)

        s2 = Square2()
        s2.transform.position = Vector2(0, 0)

        self.p = Square((200, 150), (255, 0, 0))
        self.p.transform.pivot.set(0.5, 0.5)


SceneManager().loadScene(Scene1)


while True:
    World.update()
    World.draw()
    clock.tick(60)