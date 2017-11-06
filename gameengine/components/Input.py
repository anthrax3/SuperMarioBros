from gameengine.core.Component import Component
from gameengine.managers.InputManager import InputManager


class Input(Component):
    def __init__(self, gameObject):
        super().__init__(gameObject)
        InputManager().addObject(self)

    def toString(self):
        return """[Input]"""
