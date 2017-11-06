from gameengine.util.Vector2 import Vector2

from gameengine.components.CustomDraw import CustomDraw
from gameengine.components.Input import Input
from gameengine.components.Script import Script
from gameengine.core.GameObject import GameObject
from gameengine.ui.Label import Label
from gameengine.util.EventHandler import EventHandler


class Button(GameObject, Script):
    def __init__(self, text):
        super().__init__()
        self.addComponent(CustomDraw)
        self.addComponent(Input)
        self.addScript(self)

        self.transform.pivot.set(0.5, 0.5)

        self.label = Label(text)
        self.label.transform.parent = self.transform
        self.label.transform.depth = 1

        self.label.transform.anchor.set(0.5, 0.5, True, True)

        def updateButtonSize(label, size: Vector2):
            self.transform.size = Vector2(size)
            self.transform.size += Vector2(10, 5) # Padding

        self.label.transform.sizeChanged += updateButtonSize

        self.click = EventHandler(self)


    def onDraw(self):
        from gameengine.util.util import svgToSurface
        bg = svgToSurface("../ui/res/button-bg.svg", *self.transform.size)
        return bg

    def onMouseClicked(self, pos):
        self.click()