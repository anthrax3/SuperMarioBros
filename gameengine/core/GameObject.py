from typing import TypeVar, Optional

from gameengine.components.Transform import Transform
from gameengine.core.Events import Events
from gameengine.core.Object import Object
from gameengine.core.World import World
from gameengine.util.Queue import Queue

C = TypeVar("Component")
S = TypeVar("Script")


class GameObject(Object, Events):
    """Objet de jeu auquel on ajoute des composants et des scripts."""

    componentConstructionQueue = Queue()
    componentDestructionQueue = Queue()

    scriptConstructionQueue = Queue()
    scriptDestructionQueue = Queue()

    def __init__(self):
        super().__init__()
        World.gameObjectCreationQueue.put(self)

        from gameengine.managers.SceneManager import SceneManager
        self.scene = SceneManager().activeScene
        self.name = "GameObject"
        self.tags = ["Default"]

        self.components = []
        self.scripts = []

        self.transform = self.addComponent(Transform)

    # Don't add global queue to single gameObject

    def getComponent(self, Class: C) -> Optional[C]:
        for component in self.components:# + self.componentConstructionQueue.queue:
            if isinstance(component, Class):
                return component
        return None

    def getScript(self, Class: S) -> Optional[S]:
        for script in self.scripts:# + self.scriptConstructionQueue.queue:
            if isinstance(script, Class):
                return script
        return None

    def addComponent(self, Class: C) -> C:
        existing = self.getComponent(Class)
        if existing is not None:
            return existing

        component = Class(self)

        # TODO: put into queue ? -> make separate queues per GO -> getComponent gets components + creationQueue
        self.components.append(component)
        # GameObject.componentConstructionQueue.put(component)
        return component

    def addScript(self, Class: S) -> S:
        # Allow for passing a class or an instance(the gameObject itself)
        script = None

        from gameengine.components.Script import Script
        if isinstance(Class, type):
            existing = self.getScript(Class)
            if existing is not None:
                return existing

            script = Class()

        elif isinstance(Class, Script):
            script = Class

        else:
            raise RuntimeError("Argument passed is not a script")

        script.gameObject = self
        self.scriptConstructionQueue.put(script)

        # script.onCreate()
        return script

    def removeComponent(self, Class: C):
        from gameengine.core.Component import Component
        if isinstance(Class, type):
            component = self.getComponent(Class)
            if component is not None:
                self.componentDestructionQueue.put(component)

        elif isinstance(Class, Component):
            self.componentDestructionQueue.put(Class)

    def removeScript(self, Class: S):
        from gameengine.components.Script import Script
        if isinstance(Class, Script):
            script = Class
            self.scriptDestructionQueue.put(script)

        elif isinstance(Class, type):
            script = self.getScript(Class)
            if script is not None:
                self.scriptDestructionQueue.put(script)

    @classmethod
    def _addComponents(cls):
        for component in cls.componentConstructionQueue.get():
            components = component.gameObject.components
            components.append(component)

    @classmethod
    def _removeComponents(cls):
        for component in cls.componentDestructionQueue.get():
            if component is not None:
                component.onDestroy()

                for manager in component.managers:
                    manager.removeObject(component)

                component.gameObject.components.remove(component)
                component.gameObject = None

    @classmethod
    def _addScripts(cls):
        for script in cls.scriptConstructionQueue.get():
            scripts = script.gameObject.scripts

            scripts.append(script)
            scripts.sort(key=lambda script: script.order)

            script.onCreate()

    @classmethod
    def _removeScripts(cls):
        for script in cls.scriptDestructionQueue.get():
            script.onDestroy()

            scripts = script.gameObject.scripts
            scripts.remove(script)
            scripts.sort(key=lambda script: script.order)
            script.gameObject = None

    def destroy(self):
        World.destroyGameObject(self)

    def toString(self):
        string = ""
        for component in self.components:
            string += component.toString()
            string += "\n\n"
        return string