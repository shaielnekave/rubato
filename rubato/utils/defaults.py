"""
A module that houses all of the default options.
"""

from rubato.utils import Math, Vector, Color

# [start-defaults]
game_defaults = {
    "name": "Untitled Game",  # . . . . . . . . . . . . . . . . str
    # The title that appears at the top of the window
    "window_size": Vector(640, 360),  # . . . . . . . . . . . . Vector
    # The actual size of the window
    "resolution": Vector(1920, 1080),  #. . . . . . . . . . . . Vector
    # The pixel resolution of the game
    "fps_cap": 0,  #. . . . . . . . . . . . . . . . . . . . . . int
    # The max FPS of the game
    "physics_timestep": 20,  #. . . . . . . . . . . . . . . . . int
    # The length of the physics timestep in milliseconds
    "reset_display": True,  # . . . . . . . . . . . . . . . . . bool
    # Wether or not to white out the display every frame.
}

rigidbody_defaults = {
    "mass": 1,  # . . . . . . . . . . . . . . . . . . . . . . . float
    # The mass of the RB. (0 for infinite)
    "bounciness": 0,  # . . . . . . . . . . . . . . . . . . . . float
    # The percent bounciness of the RB. (as a decimal)
    "gravity": Vector(0, 100),  # . . . . . . . . . . . . . . . Vector
    # The gravity applied to the RB.
    "max_speed": Vector(Math.INFINITY, Math.INFINITY),  # . . . Vector
    # The maximum speed of the RB.
    "velocity": Vector(),  #. . . . . . . . . . . . . . . . . . Vector
    # The starting velocity of the RB.
    "friction": 0,  # . . . . . . . . . . . . . . . . . . . . . float
    # The amount of friction experienced by the RB.
    "rotation": 0,  # . . . . . . . . . . . . . . . . . . . . . float
    # The starting rotation of the RB.
    "static": False  #. . . . . . . . . . . . . . . . . . . . . bool
    # Whether the RB is static or not.
}

image_defaults = {
    "image_location": "",  #. . . . . . . . . . . . . . . . . . str
    # The relative path of the image. (from the cwd)
    "scale_factor": Vector(1, 1),  #. . . . . . . . . . . . . . Vector
    # The initial scale factor of the image.
    "rotation": 0,  # . . . . . . . . . . . . . . . . . . . . . float
    # The initial rotation of the image.
}

sprite_defaults = {
    "pos": Vector(),  # . . . . . . . . . . . . . . . . . . . . Vector
    # The starting position of the sprite.
    "z_index": 0,  #. . . . . . . . . . . . . . . . . . . . . . int
    # The z_index of the sprite.
}

animation_defaults = {
    "scale_factor": Vector(1, 1),  #. . . . . . . . . . . . . . Vector
    # The startin scale factor of the animation.
    "default_animation_length": 5,  # . . . . . . . . . . . . . int
    # The default number of frames in the animation.
    "rotation": 0,  # . . . . . . . . . . . . . . . . . . . . . float
    # The rotation of the animation.
    "fps": 24,  # . . . . . . . . . . . . . . . . . . . . . . . int
    # The FPS that the animation should run at.
}

polygon_defaults = {
    "verts": [],  # . . . . . . . . . . . . . . . . . . . . . . List[Vector]
    # A list of vectors representing the vertices of the Polygon going CCW.
    "rotation": 0,  # . . . . . . . . . . . . . . . . . . . . . float
    # The rotation of the polygon
    "debug": False,  #. . . . . . . . . . . . . . . . . . . . . bool
    # Whether to draw a green outline around the Polygon or not.
    "trigger": False,  #. . . . . . . . . . . . . . . . . . . . bool
    # Whether this hitbox is just a trigger or not.
    "scale": 1,  #. . . . . . . . . . . . . . . . . . . . . . . int
    # The scale of the polygon
    "callback": lambda c: None,  #. . . . . . . . . . . . . . . Callable
    # The callback function to call when a collision happens with this hitbox.
    "color": None  #. . . . . . . . . . . . . . . . . . . . . . Color
    # The color to fill this hitbox with.
}

rectangle_defaults = {
    "width": 10,  # . . . . . . . . . . . . . . . . . . . . . . int
    # The width of the rectangle.
    "height": 10  # . . . . . . . . . . . . . . . . . . . . . . int
    # The height of the rectangle.
}

circle_defaults = {
    "radius": 10,  #. . . . . . . . . . . . . . . . . . . . . . int
    # The radius of the circle.
    "debug": False,  #. . . . . . . . . . . . . . . . . . . . . bool
    # Whether to draw a green outline around the Circle or not.
    "trigger": False,  #. . . . . . . . . . . . . . . . . . . . bool
    # Whether this hitbox is just a trigger or not.
    "scale": 1,  #. . . . . . . . . . . . . . . . . . . . . . . int
    # The scale of the polygon
    "callback": lambda c: None,  #. . . . . . . . . . . . . . . Callable
    # The callback function to call when a collision happens with this hitbox.
    "color": None  #. . . . . . . . . . . . . . . . . . . . . . Color
    # The color to fill this hitbox with.
}
# [end-defaults]

button_defaults = {
    "text": "default_text",  #. . . . . . . . . . . . . . . . . str
    "pos": Vector(),  # . . . . . . . . . . . . . . . . . . . . Vector
    "size": 16,  #. . . . . . . . . . . . . . . . . . . . . . . int
    "z_index": 0,  #
    "font_name": "Arial",  #
    "color": Color.black,  #
}

text_defaults = {
    "text": "default_text",
    "pos": Vector(),
    "size": 16,
    "z_index": 0,
    "font_name": "Arial",
    "color": Color.black,
    "static": False,
    "onto_surface": None,
}