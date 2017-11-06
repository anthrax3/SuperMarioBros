import pygame

from gameengine.components.CustomDraw import CustomDraw
from gameengine.components.Script import Script
from gameengine.util.Rect import Rect

class Debug(Script):
    def onCreate(self):
        self.order = 999
        self.gameObject.addComponent(CustomDraw)

    def onDraw(self):
        # transform borders
        surface = pygame.Surface(self.gameObject.transform.size, pygame.SRCALPHA).convert_alpha()
        pygame.draw.rect(surface, (255, 255, 255), Rect(0, 0, *surface.get_size()).toPygameRect(), 1)
        return surface


def debug(GameObject):
    class Debugging(GameObject):
        def __init__(self):
            super(Debugging, self).__init__()
            self.addScript(Debug)

    return Debugging
