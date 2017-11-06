from abc import ABC

from gameengine.util.Vector2 import Vector2

from gameengine.components.Collider import Collider
from gameengine.components.Physics import Physics
from gameengine.components.Script import Script
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.Constants import TOP_SIDE, TOTAL_SIDES
from gameengine.core.GameObject import GameObject
from gameengine.tests.SuperMarioBros.enemies import FlipDeathBehaviour, BulletBill
from gameengine.tests.SuperMarioBros.particles import brickPieces
from gameengine.tests.SuperMarioBros.sprites import blockSize1, blocksSprites, tilesetSprites
from gameengine.tests.SuperMarioBros.util import cancelVelocity


class Block(GameObject, Script, ABC):
    def __init__(self):
        super().__init__()
        self.tags.append("Block")
        self.addScript(self)

        self.transform.depth = -1
        self.transform.size = Vector2(blockSize1)

        self.collider = self.addComponent(Collider)
        self.spriteRenderer = self.addComponent(SpriteRenderer)

    def onCollisionEnter(self, other, side):
        if "Player" in other.tags:
            cancelVelocity(other.physics, TOTAL_SIDES - side)
        return True

    def trigger(self):
        pass

    def hit(self):
        self.trigger()


class Ground(Block):
    def __init__(self):
        super().__init__()
        self.tags.append("Ground")

        self.spriteRenderer.repeatImage = True

        spriteInfo = tilesetSprites["ground"]
        self.spriteRenderer.setSprite(tilesetSprites["ground"])


class BrickBlock(Block):
    def __init__(self, isEmpty=True):
        super().__init__()
        self.tags.append("Brick")

        self.spriteRenderer.setSprite(blocksSprites["brick"]["normal"])
        self.isEmpty = isEmpty

        self.topEnemies = []

    def onPreUpdate(self):
        self.topEnemies = []

    def onCollisionEnter(self, other, side):
        if "Enemy" in other.tags and side == TOP_SIDE:
            if other not in self.topEnemies:
                self.topEnemies.append(other)

        return super().onCollisionEnter(other, side)

    def hit(self):
        # from gameengine.core.Timer import Timer
        # Timer(100, lambda: brickPieces(self.transform.worldRect.center)).start()
        brickPieces(self.transform.worldRect.center)
        self.destroy()

    def onDestroy(self):
        for enemy in self.topEnemies:
            enemy.state = FlipDeathBehaviour(enemy)
            # enemy.destroy()
            # enemy.physics.addForce(Vector2(0, -5))


class QuestionBlock(Block):
    def __init__(self, classContentItem):
        super().__init__()
        self.tags.append("Question")

        self.classContentItem = classContentItem

        self.spriteRenderer.setSprite(blocksSprites["question"]["normal"])

        self.isHit = False


    def onCollisionEnter(self, other, side):
        if "Player" in other.tags:
            cancelVelocity(other.physics, TOTAL_SIDES - side)
        return True
        # return False

    def trigger(self):
        if not self.isHit:
            self.isHit = True
            self.spriteRenderer.setSprite(blocksSprites["question"]["hit"])

            self.classContentItem().transform.position = Vector2(self.transform.position)

    class SpinningCoin(GameObject, Script):
        def __init__(self):
            super().__init__()
            self.transform.depth = -2
            self.addScript(self)
            self.spriteRenderer = self.addComponent(SpriteRenderer)
            self.physics = self.addComponent(Physics)

        def onCreate(self):
            from gameengine.tests.SuperMarioBros.sprites import itemsSprites

            self.spriteRenderer.setSprite(itemsSprites["rotatingCoin"])

            self.physics.addForce(Vector2(0, -10))

            def kill():
                self.destroy()

            from gameengine.util.Timer import Timer
            Timer(400, kill, cycles=1).start()


class HardBlock(Block):
    def __init__(self):
        super().__init__()
        self.tags.append("Brick")

        self.spriteRenderer.setSprite(tilesetSprites["hard"])


class BillBlaster(Block):
    def __init__(self):
        super().__init__()
        self.transform.depth = 0
        self.tags.append("Bill Blaster")

        self.spriteRenderer.setSprite(tilesetSprites["bill_blaster"])

        from gameengine.util.Timer import Timer
        self.timer = Timer(3000, self.shoot, startNow=True).start()

    def shoot(self):
        bill = BulletBill()
        bill.transform.position = Vector2(self.transform.position)

        if self.scene.player.transform.position.x > self.transform.position.x:
            bill.physics.velocity.x *= -1


class Pipe(GameObject, Script):
    def __init__(self, length=None):
        super().__init__()
        self.tags.append("Block")
        self.addScript(self)

        self.transform.depth = -2

        self.collider = self.addComponent(Collider)
        self.spriteRenderer = self.addComponent(SpriteRenderer)

        self.head = None

        self.length = length

    def onCreate(self):
        self.transform.pivot.set(0.5, 1)

        self.spriteRenderer.setSprite(tilesetSprites["pipeBody"])

        self.head = self._PipeHead()
        # self.head.transform.parent = self.transform
        self.head.transform.depth = -1
        # self.head.transform.anchor.set(0.5, 0, overridePosition=True)

        if self.length is not None:
            self.spriteRenderer.repeatImage = True
            self.transform.size.y = self.length

        self.head.transform.position = self.transform.position + Vector2(0, -self.transform.size.y)

    def onCollisionEnter(self, other, side):
        if "Player" in other.tags:
            cancelVelocity(other.physics, TOTAL_SIDES - side)
        return True

    def trigger(self):
        pass

    def hit(self):
        pass


    class _PipeHead(GameObject, Script):
        def __init__(self):
            super().__init__()
            self.tags.append("Block")
            self.addScript(self)

            # self.transform.anchor.set()
            self.transform.pivot.set(0.5, 1)
            # self.transform.localPosition = (0, 0)

            self.collider = self.addComponent(Collider)
            self.spriteRenderer = self.addComponent(SpriteRenderer)

        def onCreate(self):
            self.spriteRenderer.setSprite(tilesetSprites["pipeHead"])
            # self.collider.size.x -= 2*4
            self.collider.size = Vector2(self.collider.size.x - 2 * 4, self.collider.size.y)

        def onCollisionEnter(self, other, side):
            if "Player" in other.tags:
                cancelVelocity(other.physics, TOTAL_SIDES - side)
            return True

        def trigger(self):
            pass
            # TODO: Fix this

        def hit(self):
            pass