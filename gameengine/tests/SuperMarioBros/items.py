from gameengine.util.Vector2 import Vector2

from gameengine.components.Collider import Collider
from gameengine.components.Physics import Physics
from gameengine.components.Script import Script
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.Constants import BOTTOM_SIDE, TOP_SIDE, LEFT_SIDE, RIGHT_SIDE
from gameengine.core.GameObject import GameObject
from gameengine.core.Object import destroy
from gameengine.tests.SuperMarioBros.sprites import itemsSprites


class Item(GameObject, Script):
    def __init__(self):
        super().__init__()
        self.transform.depth = -2
        self.tags.append("Item")
        self.addScript(self)

        self.physics = self.addComponent(Physics)
        self.physics.customGravity = Vector2(0, 0)
        self.physics.mass = 0.8

        self.collider = self.addComponent(Collider)
        self.spriteRenderer = self.addComponent(SpriteRenderer)

        self.popped = False

    def onUpdate(self):
        if not self.popped:
            self.physics.customGravity = Vector2(0, 0)
            self.physics.velocity = Vector2(0, -0.4)
        else:
            self.physics.customGravity = None

    def onCollisionExit(self, other, side):
        if not self.popped and "Block" in other.tags:
            self.physics.velocity.x = 1.5
            self.popped = True

    def onCollisionEnter(self, other, side):
        if "Player" in other.tags:
            self.destroy()
            print(side)
            return False

        elif "Enemy" in other.tags:
            return False

        else:
            if not self.popped:
                return False

            if (side == BOTTOM_SIDE and self.physics.velocity.y > 0) or \
                (side == TOP_SIDE and self.physics.velocity.y < 0):
                self.physics.velocity.y = 0

            elif (side == LEFT_SIDE and self.physics.velocity.x < 0) or \
                (side == RIGHT_SIDE and self.physics.velocity.x > 0):
                self.physics.velocity.x *= -1

            return True


class Coin(GameObject, Script):
    def __init__(self):
        super().__init__()
        self.tags.append("Item")
        self.tags.append("Coin")
        self.addScript(self)

        self.collider = self.addComponent(Collider)
        self.spriteRenderer = self.addComponent(SpriteRenderer)

        self.spriteRenderer.setSprite(itemsSprites["coin"])

    def onCollisionEnter(self, other, side):
        if "Player" in other.tags:
            destroy(self)

        return False


class Mushroom(Item):
    def __init__(self):
        super().__init__()

        self.spriteRenderer.setSprite(itemsSprites["mushroom"])

    def onCollisionEnter(self, other, side):
        if "Player" in other.tags:
            from gameengine.tests.SuperMarioBros import Player
            # # TODO Don't modify transform size on spriteRenderer init
            # other.transform.position += Vector2(0, -35)
            other.type = Player.Big(other)

        return super().onCollisionEnter(other, side)


class SuperStar(Item):
    def __init__(self):
        super().__init__()

        self.spriteRenderer.setSprite(itemsSprites["superStar"])

        self.addScript(self.Bounce)

    def onCollisionEnter(self, other, side):
        if "Player" in other.tags:
            pass

        return super().onCollisionEnter(other, side)


    class Bounce(Script):
        def onCollisionEnter(self, other, side):
            if "Block" in other.tags and side == BOTTOM_SIDE:
                self.gameObject.physics.velocity.y = 0
                self.gameObject.physics.addForce(Vector2(0, -12))

                return True

            return super().onCollisionEnter(other, side)