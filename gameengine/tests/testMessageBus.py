import pygame
from gameengine.util.Vector2 import Vector2

from gameengine.components.CustomDraw import CustomDraw
from gameengine.components.Input import Input
from gameengine.components.Script import Script
from gameengine.core.GameObject import GameObject
from gameengine.core.MessageBus import MessageBus
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

        MessageBus().register(self)

    def onDraw(self):
        surface = pygame.Surface(self.transform.size)
        surface.fill((0, 255, 255))
        return surface

    def onMouseDrag(self, pos, rel, buttons):
        self.transform.position += Vector2(rel)

    def onMouseClicked(self, pos):
        MessageBus().broadcastMessage(self, "Bonjour", SimpleMessage("Je suis {}".format(self)))

    def onMessageReceived(self, keyword, message):
        if keyword != "Bonjour":
            return

        print("Received: {} {}".format(keyword, message.arg))


class SimpleMessage():
    def __init__(self, arg):
        self.arg = arg



class Test(Scene):
    def onLoad(self):
        Square()
        Square()
        Square()


SceneManager().loadScene(Test)

while True:
    World.update()
    World.draw()
    clock.tick(60)
