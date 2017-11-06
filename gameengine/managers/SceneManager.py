from gameengine.core.Object import destroy
from gameengine.core.ObjectManager import ObjectManager
from gameengine.core.World import World
from gameengine.util.util import Singleton


@Singleton
class SceneManager(ObjectManager):
    def __init__(self):
        super().__init__()

        self.activeScene = None

    def loadScene(self, Class: type):
        # Destroy all previous gameObjects
        for gameObject in World().gameObjects:
            destroy(gameObject)

        from gameengine.util.Timer import timers
        timers.clear()

        self.activeScene = Class()
        self.activeScene.onLoad()