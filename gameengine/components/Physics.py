from gameengine.util.Vector2 import Vector2

from gameengine.core.Component import Component
from gameengine.managers.PhysicsManager import PhysicsManager


class Physics(Component):
    """Simulation basique des physiques, peut être utilisé sans Collider sans inclure les collisions."""

    def __init__(self, gameObject):
        super().__init__(gameObject)

        self.velocity = Vector2()
        self.acceleration = Vector2()
        self.drag = 1.0

        self.mass = 1.0
        self.customGravity = None

        PhysicsManager().addObject(self)

    def addAcceleration(self, vec: Vector2):
        self.acceleration += vec

    def addForce(self, vec: Vector2):
        self.acceleration += (vec / self.mass)

    def step(self):
        self.velocity += self.acceleration
        self.velocity *= self.drag
        self.acceleration *= 0

        self.move(self.velocity.x, self.velocity.y)

    def move(self, dx, dy):
        if dx == 0 and dy == 0:
            return

        # No collider
        from gameengine.components.Collider import Collider
        collider = self.gameObject.getComponent(Collider)
        if collider == None or not collider.enabled:
            self.gameObject.transform.position += Vector2(dx, dy)
            return

        collider._move(dx, dy)

    def toString(self):
        return """[Physics]
    Velocity: {}
    Acceleration: {}""".format(self.velocity, self.acceleration)
