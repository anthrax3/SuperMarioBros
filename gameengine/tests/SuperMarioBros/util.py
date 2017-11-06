from gameengine.util.Vector2 import Vector2

from gameengine.core.Constants import BOTTOM_SIDE, TOP_SIDE, LEFT_SIDE, RIGHT_SIDE


def _multVelocity(physics, side, xValue, yValue):
    if (side == LEFT_SIDE and physics.velocity.x < 0) or \
       (side == RIGHT_SIDE and physics.velocity.x > 0):
        physics.velocity.x *= xValue

    elif (side == BOTTOM_SIDE and physics.velocity.y > 0) or \
         (side == TOP_SIDE and physics.velocity.y < 0):
        physics.velocity.y *= yValue


def cancelVelocity(physics, side):
    _multVelocity(physics, side, 0, 0)


def inverseXVelocity(physics, side):
    _multVelocity(physics, side, -1, 0)

def bouncePlayer(player):
    player.physics.addAcceleration(Vector2(0, -8))