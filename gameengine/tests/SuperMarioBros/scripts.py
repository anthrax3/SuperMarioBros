import pygame

from gameengine.components.Physics import Physics
from gameengine.components.Script import Script
from gameengine.tests.SuperMarioBros.util import inverseXVelocity, cancelVelocity


class DirectionalHeading(Script):
    LEFT = 0
    RIGHT = 1

    def __init__(self):
        super().__init__()
        self.spriteDirection = None

    def onCreate(self):
        self.physics = self.gameObject.getComponent(Physics)
        self.direction = self.RIGHT

    def onUpdate(self):
        if self.physics.velocity.x < 0:
            self.direction = self.LEFT
        elif self.physics.velocity.x > 0:
            self.direction = self.RIGHT

    def alterSpriteFrame(self, frame):
        if (self.direction == self.LEFT and self.spriteDirection == self.RIGHT) or \
                (self.direction == self.RIGHT and self.spriteDirection == self.LEFT):
            return pygame.transform.flip(frame, True, False)
        return frame


class BlockCollision(Script):
    def onCollisionEnter(self, other, side):
        if "Block" in other.tags:
            cancelVelocity(self.gameObject.getComponent(Physics), side)
            return True
        return False


class InverseVelocity(Script):
    def onCollisionEnter(self, other, side):
        if "Block" in other.tags or "Enemy" in other.tags:
            inverseXVelocity(self.gameObject.physics, side)
            return True
        return False
