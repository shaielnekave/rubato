"""
The Rigidbody component contains an implementation of rigidbody physics. They
have hitboxes and can collide and interact with other rigidbodies.
"""
import math
from typing import TYPE_CHECKING
from rubato.classes.component import Component
from rubato.utils import Vector, Configs, Time, Math

if TYPE_CHECKING:
    from rubato.classes.components.hitbox import CollisionInfo


class RigidBody(Component):
    """
    A RigidBody implementation with built in physics and collisions.

    Attributes:
        # TODO Rigidbody attributes need documentation
    """

    def __init__(self, options: dict = {}):
        """
        Initializes a Rigidbody.

        Args:
            options: A rigidbody config. Defaults to the |default| for
                `RigidBody`
        """
        params = Configs.merge_params(options, Configs.rigidbody_defaults)

        super().__init__()

        self.gravity: Vector = params["gravity"]
        self.friction: float = params["friction"]
        self.max_speed: Vector = params["max_speed"]
        self.min_speed: Vector = params["min_speed"]

        self.velocity = Vector()

        self.angvel: float = 0
        self.rotation: float = params["rotation"]

        if params["mass"] == 0:
            self.inv_mass = 0
        else:
            self.inv_mass: float = 1 / params["mass"]

        self.bouncyness: float = Math.clamp(params["bouncyness"], 0, 1)

        self.debug: bool = params["debug"]

    @property
    def mass(self) -> float:
        if self.inv_mass == 0:
            return 0
        else:
            return 1 / self.inv_mass

    def physics(self):
        # Apply gravity
        self.add_force(self.gravity * self.mass)  # TODO fix to vector

        self.sprite.pos += self.velocity * Time.fixed_delta_time("sec")

    def add_force(self, force: Vector):
        accel = force * self.inv_mass

        self.velocity += accel * Time.fixed_delta_time("sec")

    def add_cont_force(self, impulse: Vector, time: int):
        if time <= 0:
            return
        else:
            self.add_force(impulse)

            Time.delayed_frames(
                1, lambda: self.add_impulse(impulse, time - Time.delta_time()))

    @staticmethod
    def handle_collision(col: "CollisionInfo"):
        rb_a: RigidBody = col.shape_b.sprite.get_component(RigidBody)
        rb_b: RigidBody = col.shape_a.sprite.get_component(RigidBody)

        inv_mass_a: float = (0 if rb_a is None else rb_a.inv_mass)
        inv_mass_b: float = (0 if rb_b is None else rb_b.inv_mass)

        # Relative velocity
        rv = (Vector() if rb_b is None else rb_b.velocity) - \
            (Vector() if rb_a is None else rb_a.velocity)

        # Relative velocity along collision normal
        collision_norm = col.sep.clone()
        collision_norm.normalize()
        vel_along_norm = rv.dot(collision_norm)

        if vel_along_norm > 0:
            return

        # Calculate restitution
        e = min(0 if rb_a is None else rb_a.bouncyness,
                0 if rb_b is None else rb_b.bouncyness)

        # Calculate impulse scalar
        j = -(1 + e) * vel_along_norm
        j /= inv_mass_a + inv_mass_b

        # Apply the impulse
        impulse = j * collision_norm

        if rb_a is not None:
            rb_a.velocity -= impulse * rb_a.inv_mass

        if rb_b is not None:
            rb_b.velocity += impulse * rb_a.inv_mass

        # Position correction
        percent = 0.2  # usually 20% to 80% interpolation
        slop = 0.01  # usually 0.01 to 0.1 correction threshold

        correction = max(col.sep.magnitude - slop, 0) / (
            inv_mass_a + inv_mass_b) * percent * collision_norm

        if rb_a is not None:
            rb_a.sprite.pos -= rb_a.inv_mass * correction

        if rb_b is not None:
            rb_b.sprite.pos += rb_b.inv_mass * correction

        # Friction

        # Relative velocity
        rv = (Vector() if rb_b is None else rb_b.velocity) - \
            (Vector() if rb_a is None else rb_a.velocity)

        # Tangent vector
        tangent = rv - rv.dot(collision_norm) * collision_norm
        tangent.normalize()

        # Solve for magnitude to apply along the friction vector
        jt = -rv.dot(tangent)
        jt /= inv_mass_a + inv_mass_b

        # Calculate mu
        if rb_a is None:
            mu = rb_b.friction
        elif rb_b is None:
            mu = rb_a.friction
        else:
            mu = math.sqrt((rb_a.friction**2) + (rb_b.friction**2))

        # Calculate friction impulse
        if abs(jt) < j * mu:
            friction_impulse = jt * tangent  # "Static friction"
        else:
            friction_impulse = -j * tangent * mu  # "Dynamic friction"

        if rb_a is not None:
            rb_a.velocity -= friction_impulse * rb_a.inv_mass

        if rb_b is not None:
            rb_b.velocity += friction_impulse * rb_a.inv_mass

    def fixed_update(self):
        """The update loop"""
        self.physics()
