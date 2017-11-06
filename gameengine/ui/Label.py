import pygame
from gameengine.util.Vector2 import Vector2

from gameengine.components.CustomDraw import CustomDraw
from gameengine.components.Script import Script
from gameengine.core.Color import Color
from gameengine.core.GameObject import GameObject
from gameengine.util.EventHandler import EventHandler


class Label(GameObject, Script):
    def __init__(self, text):
        super().__init__()
        self.addComponent(CustomDraw)
        self.addScript(self)

        self._text = text
        self.textChanged = EventHandler(self)

        self.color = Color.black

        self._fontFamily = pygame.font.get_default_font()
        self._fontSize = 16

        self._bold = False
        self._italic = False

        self.font: pygame.font.Font = None
        self._genFont()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, str):
        if self._text != str:
            self._text = str
            self._genFont()
            self.textChanged(self._text)


    @property
    def fontFamily(self):
        return self._fontFamily

    @fontFamily.setter
    def fontFamily(self, name):
        self._fontFamily = name
        self._genFont()

    @property
    def fontSize(self):
        return self._fontSize

    @fontSize.setter
    def fontSize(self, size):
        self._fontSize = size
        self._genFont()

    @property
    def bold(self):
        return self._bold

    @bold.setter
    def bold(self, bool):
        self._bold = bool
        self._genFont()

    @property
    def italic(self):
        return self._italic

    @italic.setter
    def italic(self, bool):
        self._italic = bool
        self._genFont()

    def _genFont(self):
        self.font = pygame.font.SysFont(self.fontFamily, self.fontSize, self.bold, self.italic)
        self.gameObject.transform.size = Vector2(self.font.size(self.text))


    def onDraw(self):
        return self.font.render(self.text, True, self.color)#, Color.magenta)