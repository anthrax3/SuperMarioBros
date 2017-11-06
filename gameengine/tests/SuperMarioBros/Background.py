from gameengine.util.Vector2 import Vector2

from gameengine.components.Script import Script
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.GameObject import GameObject
from gameengine.core.Sprite import Sprite
from gameengine.tests.SuperMarioBros.sprites import bgOverworldSurface


class Background(GameObject, Script):
    def __init__(self):
        super().__init__()
        self.transform.depth = -4138

        self.spriteRenderer = self.addComponent(SpriteRenderer).setSprite(Sprite(bgOverworldSurface))
        # self.spriteRenderer.size = Vector2(bgOverworldSurface.get_width(), bgOverworldSurface.get_height())