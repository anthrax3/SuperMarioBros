import pygame
from gameengine.util.Vector2 import Vector2

from gameengine.components.Input import Input
from gameengine.components.Script import Script
from gameengine.core.Scene import Scene
from gameengine.core.World import World
from gameengine.managers.SceneManager import SceneManager
from gameengine.ui.Button import Button
from gameengine.ui.Slider import Slider

pygame.init()
clock = pygame.time.Clock()

World.display = pygame.display.set_mode((800, 464), 0, 32)

class random(Script):
    def onCreate(self):
        self.i = 0

    def onUpdate(self):
        self.gameObject.transform.position += Vector2(0.1, 0.2)

        self.i += 1

        if self.i % 60 == 0:
            self.gameObject.label.text = "Alex {}".format(self.i)
            self.gameObject.label.italic = not self.gameObject.label.italic
        # print(self.gameObject.transform.size)


class moveCamera(Script):
    def onCreate(self):
        self.gameObject.addComponent(Input)

    def onMouseDrag(self, pos, rel, buttons):
        self.gameObject.transform.position -= rel

class moveGO(Script):
    def onCreate(self):
        self.gameObject.addComponent(Input)

    def onMouseDrag(self, pos, rel, buttons):
        self.gameObject.transform.position += rel


class Scene1(Scene):
    def onLoad(self):


        s = Slider(width=500, min=0, max=100, startValue=30, wholeNumbers=True, decimals=2)
        # s.addScript(ss)
        s.transform.position = Vector2(50, 50)

        lbd = lambda sender, value: print("Changed to", value)
        s.valueChanged += lbd
        # s.onValueChanged -= c


        button = Button("Click")
        button.label.fontSize = 20
        button.label.fontFamily = "dejavusans"

        button.transform.depth = 24
        button.transform.position = Vector2(300, 100)

        def appendLetter(button):
            button.label.text += button.label.text[-1]

        def incrementSlider(button):
            if s.value >= 50:
                button.click -= incrementSlider
                return
            s.value += 1

        button.click += appendLetter
        button.click += incrementSlider


        from gameengine.ui.Checkbox import Checkbox
        checkbox = Checkbox(True)
        checkbox.transform.position = Vector2(100, 200)

        def printCheckboxStatus(sender, status):
            print(sender, "changed to", status)

        checkbox.checkedChanged += printCheckboxStatus

        # label.transform.size = Vector2(100, 100)

SceneManager().loadScene(Scene1)

while True:
    World.update()
    World.draw()
    clock.tick(60)
