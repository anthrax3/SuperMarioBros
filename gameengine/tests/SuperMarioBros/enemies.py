import pygame
from gameengine.util.Vector2 import Vector2

from gameengine.components.Collider import Collider
from gameengine.components.Physics import Physics
from gameengine.components.Script import Script
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.Constants import BOTTOM_SIDE, TOP_SIDE, LEFT_SIDE, RIGHT_SIDE, TOTAL_SIDES
from gameengine.core.GameObject import GameObject
from gameengine.core.Object import destroy
from gameengine.tests.SuperMarioBros.sprites import enemiesSprites
from gameengine.tests.SuperMarioBros.util import cancelVelocity, inverseXVelocity, bouncePlayer
from gameengine.util.Timer import Timer, timers


# @debug
class Enemy(GameObject, Script):
    def __init__(self):
        super().__init__()
        self.tags.append("Enemy")
        self.addScript(self)

        self.state = None
        self.deathBehaviour = None

        self.physics = self.addComponent(Physics)
        self.physics.mass = 0.9
        self.physics.velocity.x = -1

        self.collider = self.addComponent(Collider)
        self.spriteRenderer = self.addComponent(SpriteRenderer)

        from gameengine.tests.SuperMarioBros.scripts import DirectionalHeading
        self.addScript(DirectionalHeading).spriteDirection = DirectionalHeading.LEFT

    def onCollisionEnter(self, other, side):
        if "Block" in other.tags or "Enemy" in other.tags:
            if side == BOTTOM_SIDE or side == TOP_SIDE:
                cancelVelocity(self.physics, side)
            else:
                inverseXVelocity(self.physics, side)

            return True

        return False

    def alterSpriteFrame(self, frame):
        if self.state is None:
            return frame

        return self.state.alterSpriteFrame(frame)

    def hit(self, other, side):
        print("{} hit".format(self.gameObject))
        self.destroy()


class EnemyState(Script):
    def __init__(self):
        super().__init__()

    def onCollisionEnter(self, other, side):
        return True

    def alterSpriteFrame(self, frame):
        return frame


class FlipDeathBehaviour(EnemyState):
    def __init__(self, enemy):
        super().__init__()
        self.enemy = enemy

        self.enemy.spriteRenderer.interval = -1

        destroy(self.enemy.collider)
        self.enemy.physics.velocity.y = 0
        self.enemy.physics.addAcceleration(Vector2(0, -7))

    def alterSpriteFrame(self, frame):
        frame = pygame.transform.flip(frame, False, True)
        return frame


class Goomba(Enemy):
    def __init__(self):
        super().__init__()
        self.name = "Goomba"

        self.spriteRenderer.setSprite(enemiesSprites["goomba"]["walking"])

    def onCollisionEnter(self, other, side):
        if "Player" in other.tags:
            if side == TOP_SIDE:
                cancelVelocity(other.physics, TOTAL_SIDES - side)
                bouncePlayer(other)

                self.Death().transform.position = self.transform.position
                self.destroy()

            else:
                other.hit(self, TOTAL_SIDES - side)

            return False

        else:
            return super().onCollisionEnter(other, side)

    class Death(GameObject):
        def __init__(self):
            super().__init__()

            self.transform.depth = -999

            self.spriteRenderer = self.addComponent(SpriteRenderer).setSprite(enemiesSprites["goomba"]["stomped"])

            from gameengine.core.Object import destroy
            destroy(self, 1000)

    # def onBecameInvisible(self):
    #     destroy(self)


class KoopaTroopa(Enemy):
    def __init__(self):
        super().__init__()
        self.tags.append("Koopa Troopa")

        self.transform.pivot.set(0.5, 1)
        self.transform.size = Vector2(32, 32)

        # General to all enemies
        # self.addScript(InverseVelocity)

        self.state = WalkingKoopaTroopaState(self)

    def onCollisionEnter(self, other, side):
        return self.state.onCollisionEnter(other, side)


class WalkingKoopaTroopaState(EnemyState):
    def __init__(self, koopaTroopa):
        super().__init__()
        self.koopaTroopa = koopaTroopa

        self.koopaTroopa.spriteRenderer.setSprite(enemiesSprites["koopa_troopa"]["walking"], overrideTransformSize=False)

        # rect = self.koopaTroopa.spriteRenderer.localRect
        # rect.bottom = self.koopaTroopa.transform.localRect.bottom
        # self.koopaTroopa.spriteRenderer.relPos = rect.topLeft

    def onCollisionEnter(self, other, side):
        if "Player" in other.tags:
            if side == TOP_SIDE:
                cancelVelocity(other.physics, TOTAL_SIDES - side)
                bouncePlayer(other)
                # self.gameObject.removeScript(self)
                self.koopaTroopa.state = StompedKoopaTroopaState(self.koopaTroopa)
            else:
                other.hit(self, TOTAL_SIDES - side)

            return False

        else:
            # print(other.tags)
            return super(KoopaTroopa, self.koopaTroopa).onCollisionEnter(other, side)


class StompedKoopaTroopaState(EnemyState):
    def __init__(self, koopaTroopa):
        super().__init__()
        self.koopaTroopa = koopaTroopa

        self.koopaTroopa.spriteRenderer.setSprite(enemiesSprites["koopa_troopa"]["stomped"], overrideTransformSize=False)

        self.koopaTroopa.physics.velocity *= 0

        def toRecoveringState():
            # self.gameObject.removeScript(self)
            self.koopaTroopa.state = RecoveringKoopaTroopaState(self.koopaTroopa)

        self.timer = Timer(5000, toRecoveringState, cycles=1).start()


    def onCollisionEnter(self, other, side):
        if "Player" in other.tags:
            self.timer.stop()

            if other.collider.worldRect.centerX < self.koopaTroopa.collider.worldRect.centerX:
                hitSide = LEFT_SIDE
            else:
                hitSide = RIGHT_SIDE


            # self.gameObject.removeScript(self)
            self.koopaTroopa.state = BowlingKoopaTroopaState(self.koopaTroopa, hitSide)
            return False

        else:
            return super(KoopaTroopa, self.koopaTroopa).onCollisionEnter(other, side)


class BowlingKoopaTroopaState(EnemyState):
    def __init__(self, koopaTroopa, side):
        print("bowling")

        super().__init__()
        self.koopaTroopa = koopaTroopa
        self.side = side

        # Special rules
        # self.koopaTroopa.removeScript(InverseVelocity)
        # self.koopaTroopa.addScript(self)

        self.koopaTroopa.spriteRenderer.setSprite(enemiesSprites["koopa_troopa"]["stomped"])
        self.koopaTroopa.physics.velocity *= 0

        if side == LEFT_SIDE:
            self.koopaTroopa.physics.velocity = Vector2(5, 0)
        elif side == RIGHT_SIDE:
            self.koopaTroopa.physics.velocity = Vector2(-5, 0)

    def onCollisionEnter(self, other, side):
        if "Block" in other.tags:
            if side == LEFT_SIDE or side == RIGHT_SIDE:
                other.hit()
                inverseXVelocity(self.koopaTroopa.physics, side)
                return True
            else:
                return super(KoopaTroopa, self.koopaTroopa).onCollisionEnter(other, side)

        elif "Player" in other.tags:
            if side == TOP_SIDE:
                cancelVelocity(other.physics, TOTAL_SIDES - side)
                other.physics.addForce(Vector2(0, -7))

                # self.gameObject.removeScript(self)
                self.koopaTroopa.state = StompedKoopaTroopaState(self.koopaTroopa)

                # self.koopaTroopa.addScript(InverseVelocity)
                # Reverse special rules
                # self.koopaTroopa.removeScript(self)

            else:
                print("kill")
                # if self.koopaTroopa.physics.velocity.dot(other.physics.velocity) <
                other.hit(self, TOTAL_SIDES - side)

            return False

        elif "Enemy" in other.tags:
            other.state = FlipDeathBehaviour(other)
            return False

        else:
            return super(KoopaTroopa, self.koopaTroopa).onCollisionEnter(other, side)


class RecoveringKoopaTroopaState(EnemyState):
    def __init__(self, koopaTroopa):
        super().__init__()
        self.koopaTroopa = koopaTroopa

        # TEMP
        self.koopaTroopa.spriteRenderer.setSprite(enemiesSprites["koopa_troopa"]["recovering"])

        def toWalkingState():

            self.koopaTroopa.state = WalkingKoopaTroopaState(self.koopaTroopa)

            if self.koopaTroopa.scene.player.transform.position.x <= self.koopaTroopa.transform.position.x:
                self.koopaTroopa.physics.velocity.x = -1
            else:
                self.koopaTroopa.physics.velocity.x = 1

        self.timer = Timer(2000, toWalkingState, cycles=1).start()


    def onCollisionEnter(self, other, side):
        if "Player" in other.tags:
            self.timer.stop()

            if side == TOP_SIDE:
                cancelVelocity(other.physics, TOTAL_SIDES - side)
                bouncePlayer(other)
                self.koopaTroopa.state = StompedKoopaTroopaState(self.koopaTroopa)

                return True

            else:
                if other.collider.worldRect.centerX < self.koopaTroopa.collider.worldRect.centerX:
                    hitSide = LEFT_SIDE
                else:
                    hitSide = RIGHT_SIDE

                self.koopaTroopa.state = BowlingKoopaTroopaState(self.koopaTroopa, hitSide)

            return False

        else:
            # return False
            return super(KoopaTroopa, self.koopaTroopa).onCollisionEnter(other, side)



class KoopaParatroopa(KoopaTroopa):
    def __init__(self):
        super().__init__()
        self.name = "Koopa Paratroopa"
        self.state = FlyingKoopaParatroopaState(self)


class Bouncing(Script):
    def onCollisionEnter(self, other, side):
        if ("Block" in other.tags or "Enemy" in other.tags) and side == BOTTOM_SIDE:
            self.gameObject.physics.velocity.y = 0
            self.gameObject.physics.addForce(Vector2(0, -12))
            return True
        return False


class FlyingKoopaParatroopaState(EnemyState):
    def __init__(self, koopaParatroopa):
        super().__init__()
        self.koopaParatroopa = koopaParatroopa

        # self.koopaParatroopa.addScript(self)
        self.koopaParatroopa.addScript(Bouncing)

        self.koopaParatroopa.spriteRenderer.setSprite(enemiesSprites["koopa_troopa"]["flying"])
        self.koopaParatroopa.transform.size = Vector2(32, 32)

    def onCollisionEnter(self, other, side):
        if "Player" in other.tags:
            if side == TOP_SIDE:
                cancelVelocity(other.physics, TOTAL_SIDES - side)
                cancelVelocity(self.koopaParatroopa.physics, side)
                bouncePlayer(other)

                self.koopaParatroopa.state = WalkingKoopaTroopaState(self.koopaParatroopa)
                # self.koopaParatroopa.removeScript(self)
                self.koopaParatroopa.removeScript(Bouncing)
            else:
                other.hit(self, TOTAL_SIDES - side)

            return False

        return super(KoopaTroopa, self.koopaParatroopa).onCollisionEnter(other, side)




class BulletBill(Enemy):
    def __init__(self):
        super().__init__()
        self.tags.append("Bullet Bill")

        self.transform.depth = -1

        self.physics.customGravity = Vector2(0, 0)

        self.physics.velocity.x = -3
        self.spriteRenderer.setSprite(enemiesSprites["bullet_bill"]["rects"])

        self.dead = False

    def onUpdate(self):
        if self.dead:
            collider = self.getComponent(Collider)
            if collider is not None:
                collider.destroy()
                self.physics.velocity = Vector2(0, 0)
            self.physics.addForce(Vector2(0, 0.4))

    def onCollisionEnter(self, other, side):
        # if "Block" in other.tags:
        #     self.destroy()

        if "Player" in other.tags:
            if side == TOP_SIDE:
                cancelVelocity(other.physics, TOTAL_SIDES - side)
                bouncePlayer(other)
                self.dead = True
            else:
                other.hit(self, TOTAL_SIDES - side)

            return False

        return False
        # return super(BulletBill, self.koopaTroopa).onCollisionEnter(other, side)

