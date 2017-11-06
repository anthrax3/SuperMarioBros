import pygame
from gameengine.util.Vector2 import Vector2

from gameengine.components.Collider import Collider
from gameengine.components.Input import Input
from gameengine.components.Physics import Physics
from gameengine.components.Script import Script
from gameengine.components.SpriteRenderer import SpriteRenderer
from gameengine.core.Constants import BOTTOM_SIDE, TOP_SIDE, LEFT_SIDE, RIGHT_SIDE
from gameengine.core.Events import Events
from gameengine.core.GameObject import GameObject
from gameengine.tests.SuperMarioBros.sprites import playerSprites, playerSheet


class Player(GameObject, Script):
    def __init__(self):
        super().__init__()
        self.transform.pivot.set(0.5, 1)

        self.addScript(self)

        self.tags.append("Player")
        self.transform.depth = 99999

        self.spriteRenderer = self.addComponent(SpriteRenderer)

        self.input = self.addComponent(Input)
        self.physics = self.addComponent(Physics)
        self.collider = self.addComponent(Collider)

        from gameengine.tests.SuperMarioBros.scripts import DirectionalHeading
        self.addScript(DirectionalHeading).spriteDirection = DirectionalHeading.RIGHT

        self.type = self.Small(self)
        self.movement = self.Walk(self)
        # self.superPower

        self.onGround = False

        self.moveForce = 0.25
        self.jumpForce = 13

        self.walkLimit = 2.3
        self.runLimit = 5

    def cancelVelocity(self, side):
        if (side == LEFT_SIDE and self.physics.velocity.x < 0) or \
                (side == RIGHT_SIDE and self.physics.velocity.x > 0):
            self.physics.velocity.x = 0

        elif (side == BOTTOM_SIDE and self.physics.velocity.y > 0) or \
                (side == TOP_SIDE and self.physics.velocity.y < 0):
            self.physics.velocity.y = 0

    def nearestTopBlock(self, blocks):
        nearestBlock = None
        nearestDistance = 999999
        for block in blocks:
            distance = abs(self.collider.worldRect.centerX - block.collider.worldRect.centerX)
            if distance < nearestDistance:
                nearestDistance = distance
                nearestBlock = block
        return nearestBlock

    def onPreUpdate(self):
        self.onGround = False
        self.topBlocksHit = []

        self.movement.onPreUpdate()

    def onCollisionEnter(self, other, side):
        # print("o", other)

        if "Block" in other.tags and side == BOTTOM_SIDE:
            self.onGround = True

        self.type.onCollisionEnter(other, side)
        self.movement.onCollisionEnter(other, side)

        if "Block" in other.tags:
            self.cancelVelocity(side)
            if side == TOP_SIDE:
                self.topBlocksHit.append(other)

            return True

        return False

    def hit(self, other, side):
        self.type.hit(other, side)

    def onKeyDown(self, key):
        self.movement.onKeyDown(key)

    def onUpdate(self):
        def move(abs, rel):
            self.scene.mainCamera.transform.position.x = abs

        from gameengine.core.Interpolation import Interpolation
        from gameengine.core.Interpolation import Ease


        if 12*32 < self.transform.position.x:
            cameraX = self.scene.mainCamera.transform.position.x
            newCameraX = self.transform.worldRect.topLeft.x - (400-32)

            if newCameraX > cameraX:
                Interpolation(self.scene.mainCamera.transform.position.x, self.transform.worldRect.topLeft.x - (400-32), 200, move, Ease).start()

        if self.transform.position.x < self.scene.mainCamera.transform.position.x:
            playerRect = self.transform.worldRect
            self.transform.position.x = self.scene.mainCamera.transform.position.x
            self.physics.velocity.x = 0

        if not isinstance(self.type, self.Dying):
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                self.physics.addForce(Vector2(-self.moveForce, 0))
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.physics.addForce(Vector2(self.moveForce, 0))

        # Apply drag
        if not (pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_RIGHT]):
            self.physics.velocity.x *= 0.85 if self.onGround else 0.95

        # Fix very small movements(== 0)
        if -0.15 < self.physics.velocity.x < 0.15:
            self.physics.velocity.x = 0

        # Limit speed
        value = self.runLimit if pygame.key.get_mods() & pygame.KMOD_SHIFT else self.walkLimit
        self.physics.velocity.x = max(min(self.physics.velocity.x, value), -value)

        self.type.onUpdate()
        self.movement.onUpdate()


    class Small(Events):
        def __init__(self, player):
            self.player = player
            self.player.collider.size = Vector2(26, 26)

        def hit(self, other, side):
            from gameengine.core.Object import destroy
            # destroy(self.player)
            self.player.kill()

        def onUpdate(self):
            # Trigger the nearest block
            if self.player.topBlocksHit:
                self.player.nearestTopBlock(self.player.topBlocksHit).trigger()

        def __str__(self):
            return "small"


    class Big(Events):
        def __init__(self, player):
            self.player = player
            self.player.collider.size = Vector2(26, 58)

        def hit(self, other, side):
            self.player.type = Player.Small(self.player)

        def onUpdate(self):
            # Hit the nearest block
            if self.player.topBlocksHit:
                self.player.nearestTopBlock(self.player.topBlocksHit).hit()

        def __str__(self):
            return "big"


    class Walk(Events):
        def __init__(self, player):
            self.player = player

        def onKeyDown(self, key):
            if key == pygame.K_UP and self.player.onGround:
                self.player.movement = Player.Jump(self.player)

        def onUpdate(self):
            # Sprint sprite interval
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.player.spriteRenderer.interval = 60
            else:
                self.player.spriteRenderer.interval = playerSprites[str(self.player.type)]["walk"].interval

            # Sprites
            threshold = 0.2
            if -threshold < self.player.physics.velocity.x < threshold:
                self.player.spriteRenderer.setSprite(playerSprites[str(self.player.type)]["stand"])

            else:
                if self.player.physics.velocity.x > 0 and pygame.key.get_pressed()[pygame.K_LEFT] or \
                   self.player.physics.velocity.x < 0 and pygame.key.get_pressed()[pygame.K_RIGHT]:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        self.player.spriteRenderer.setSprite(playerSprites[str(self.player.type)]["break"])
                else:
                    self.player.spriteRenderer.setSprite(playerSprites[str(self.player.type)]["walk"])

            # Pause animation in air
            self.player.spriteRenderer.pause() if not self.player.onGround else self.player.spriteRenderer.resume()


    class Jump(Events):
        def __init__(self, player):
            self.player = player
            self.player.physics.addForce(Vector2(0, -self.player.jumpForce))

        def onUpdate(self):
            self.player.spriteRenderer.setSprite(playerSprites[str(self.player.type)]["jump"])

        def onCollisionEnter(self, other, side):
            if "Block" in other.tags and side == BOTTOM_SIDE:
                self.player.movement = Player.Walk(self.player)


    def kill(self):
        self.type = self.Dying(self)
        self.movement = self.NoMovement()

    class Dying(Events):
        def __init__(self, player):
            self.player = player
            self.player.spriteRenderer.setSprite(playerSprites["small"]["dying"])

            self.player.collider.destroy()

            self.player.physics.velocity = Vector2(0, 0)
            self.player.physics.addAcceleration(Vector2(0, -15))


        def hit(self, other, side):
            pass

        def __str__(self):
            return "dying"

    class NoMovement(Events):
        pass
