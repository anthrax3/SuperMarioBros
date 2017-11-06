import pygame
from gameengine.util.Vector2 import Vector2

from gameengine.components.CustomDraw import CustomDraw
from gameengine.components.Input import Input
from gameengine.core.GameObject import GameObject
from gameengine.components.Script import Script
from gameengine.ui.Label import Label
from gameengine.util.EventHandler import EventHandler


class Slider(GameObject, Script):
    def __init__(self, width, min, max, startValue=None, wholeNumbers=False, decimals=1):
        super().__init__()
        self.addComponent(CustomDraw)
        self.addComponent(Input)
        self.addScript(self)

        self.transform.pivot.set(0, 0.5)
        self.transform.size = Vector2(width, 8)

        self.min = min
        self.max = max
        self._value = 0

        self.wholeNumbers = wholeNumbers
        self.decimals = decimals


        self.handle = self.Handle(self)
        self.handle.transform.parent = self.transform

        self.handle.transform.pivot.set(0.5, 0.5)
        self.handle.transform.anchor.set(0, 0.5, overridePivot=False, overridePosition=True)


        self.label = LabelListener(str(self._value))
        self.label.transform.parent = self.transform

        self.label.transform.anchor.set(1, 0.5, False, False)
        self.label.transform.pivot.set(0, 0.5)
        self.label.transform.localPosition = Vector2(20, 0)

        self.label.fontSize = 24

        self.valueChanged = EventHandler(self)
        self.valueChanged += self.handle.notify
        self.valueChanged += self.label.notify


        self.value = startValue if (startValue is not None) else min

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        from gameengine.util.util import clamp
        val = clamp(val, self.min, self.max)
        val = round(val, self.decimals)

        if self.wholeNumbers:
            val = int(round(val, 0))

        if self._value == val:
            return

        self._value = val
        self.valueChanged(self._value)

    def distanceToValue(self, dist):
        from gameengine.util.util import mapValue
        return mapValue(dist, 0, self.transform.size.x, self.min, self.max)

    def onDraw(self):
        from gameengine.util.util import svgToSurface
        bg = svgToSurface("../ui/res/slider-bg.svg", *self.transform.size)
        return bg

    def onMouseDown(self, pos, button):
        if button == 1:
            self.value = self.distanceToValue(pos.x - self.transform.position.x)
            from gameengine.managers.InputManager import InputManager
            self.handle.onMouseDown(pos, button)
            InputManager().gameObject = self.handle

    class Handle(GameObject, Script):
        def __init__(self, slider):
            super().__init__()
            self.transform.size = Vector2(20, 20)
            self.addComponent(CustomDraw)
            self.addComponent(Input)
            self.addScript(self)

            self.slider = slider

        def move(self, rel):
            self.transform.position += Vector2(rel, 0)
            from gameengine.util.util import clamp
            self.transform.localPosition.x = clamp(self.transform.localPosition.x, 0, self.slider.transform.size.x)
            self.slider.value = self.slider.distanceToValue(self.transform.localPosition.x)

        def onDraw(self):
            from gameengine.util.util import svgToSurface
            handle = svgToSurface("../ui/res/slider-handle.svg", *self.transform.size)
            return handle

        def onMouseDown(self, pos, button):
            if button == 1:
                self.localMousePosition = pos - self.transform.position

        def onMouseDrag(self, pos, rel, buttons):
            if buttons[0]:
                potentialMove = (pos - (self.transform.position + self.localMousePosition)).x

                value = self.slider.distanceToValue(self.transform.localPosition.x + potentialMove)
                self.slider.value = value

        def notify(self, sender, value):
            from gameengine.util.util import mapValue
            self.transform.localPosition.x = mapValue(value, self.slider.min, self.slider.max, 0, self.slider.transform.size.x)


class LabelListener(Label):
    def notify(self, sender, value):
        self.text = str(value)