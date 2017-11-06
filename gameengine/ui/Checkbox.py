import pygame
from gameengine.util.Vector2 import Vector2

from gameengine.components.CustomDraw import CustomDraw
from gameengine.components.Input import Input
from gameengine.components.Script import Script
from gameengine.core.GameObject import GameObject
from gameengine.util.EventHandler import EventHandler


class Checkbox(GameObject, Script):
    _size = Vector2(25, 25)

    png = pygame.image.load("../ui/res/checkbox-unchecked.png").convert_alpha()
    _imgUnchecked = pygame.transform.smoothscale(png, (int(_size.x), int(_size.y)))

    png = pygame.image.load("../ui/res/checkbox-checked.png").convert_alpha()
    _imgChecked = pygame.transform.smoothscale(png, (int(_size.x), int(_size.y)))

    def __init__(self, checked=False):
        super().__init__()
        self.transform.size = Vector2(self._size)

        self.addComponent(CustomDraw)
        self.addComponent(Input)
        self.addScript(self)

        self._checked = checked

        self.checkedChanged = EventHandler(self)

    @property
    def checked(self):
        return self._checked

    @checked.setter
    def checked(self, bool):
        if bool != self._checked:
            self._checked = bool
            self.checkedChanged(self._checked)

    def onDraw(self):
        # surface = pygame.Surface(self.transform.size)
        # surface.fill((0, 255, 0) if self.checked else (255, 0, 0))
        # return surface
        return self._imgChecked if self.checked else self._imgUnchecked

    def onMouseClicked(self, pos):
        self.checked = not self.checked