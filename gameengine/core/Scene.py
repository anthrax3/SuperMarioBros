from abc import ABC, abstractmethod

from gameengine.util.Vector2 import Vector2

from gameengine.core.Camera import Camera
from gameengine.core.World import World


class Scene(ABC):
    """Classe de base pour toutes les scènes.
    Une caméra principale est par défaut definie qui prend toute la fenêtre."""

    def __init__(self):
        self.mainCamera = Camera()
        self.mainCamera.scene = self
        self.mainCamera.windowRect.size = Vector2(World.display.get_size())
        self.mainCamera.transform.size = Vector2(World.display.get_size())

    @abstractmethod
    def onLoad(self):
        pass