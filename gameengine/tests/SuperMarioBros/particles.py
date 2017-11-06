from gameengine.util.Vector2 import Vector2

from gameengine.components.Physics import Physics
from gameengine.components.Script import Script
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.GameObject import GameObject
from gameengine.core.Object import destroy
from gameengine.tests.SuperMarioBros.sprites import blocksSprites, blocksSheet


class Particle(GameObject, Script):
    def __init__(self):
        super().__init__()
        self.addScript(self)

    def onBecameInvisible(self):
        destroy(self)

class BrickPiece(Particle):
    def __init__(self, pos, numStr):
        super().__init__()

        self.physics = self.addComponent(Physics)
        self.physics.mass = 0.8

        self.spriteRenderer = self.addComponent(SpriteRenderer)

        self.spriteRenderer.setSprite(blocksSprites["brick"]["pieces"][numStr])

        rect = self.transform.worldRect
        rect.center = pos
        self.transform.position = rect.topLeft

        if numStr == '1':
            self.physics.addForce(Vector2(-2, -8))
        elif numStr == '2':
            self.physics.addForce(Vector2(2, -8))
        elif numStr == "3":
            self.physics.addForce(Vector2(-2, -4))
        elif numStr == "4":
            self.physics.addForce(Vector2(2, -4))

def brickPieces(pos):
    for i in range(1, 5):
        BrickPiece(pos, str(i))