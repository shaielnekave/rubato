"""
A module that houses all of the default options.
"""

from rubato.utils import Vector, RGB, Polygon, Math, COL_TYPE

# [start-defaults]
game_defaults = {
    "name": "Untitled Game",
    "window_width": 600,
    "window_height": 400,
    "aspect_ratio": 1.5,
    "fps": 60,
    "reset_display": True,
    "better_clock": True,
}

rigidbody_defaults = {
    "pos": Vector(),
    "mass": 1,
    "hitbox": Polygon.generate_polygon(4),
    "do_physics": True,
    "gravity": 100,
    "max_speed": Vector(Math.INFINITY, Math.INFINITY),
    "min_speed": Vector(-Math.INFINITY, -Math.INFINITY),
    "friction": Vector(1, 1),
    "img": "default",
    "col_type": COL_TYPE.STATIC,
    "scale": Vector(1, 1),
    "debug": False,
    "z_index": 0,
    "rotation": 0,
}

image_defaults = {
    "image_location": "default",
    "pos": Vector(),
    "scale_factor": Vector(1, 1),
    "z_index": 0,
    "rotation": 0,
}

sprite_defaults = {
    "pos": Vector(),
    "z_index": 0,
}

button_defaults = {
    "text": "default_text",
    "pos": Vector(),
    "size": 16,
    "z_index": 0,
    "font_name": "Arial",
    "color": RGB.black,
}

rect_defaults = {
    "pos": Vector(),
    "dims": Vector(),
    "color": RGB.black,
    "z_index": 0,
}

text_defaults = {
    "text": "default_text",
    "pos": Vector(),
    "size": 16,
    "z_index": 0,
    "font_name": "Arial",
    "color": RGB.black,
    "static": False,
    "onto_surface": None,
}
# [end-defaults]


def merge_params(options: dict, defaults: dict) -> dict:
    """
    Merges an incomplete options dictionary with the defaults dictionary

    Args:
        options: The incomplete options dictionary
        defaults: The default dictionary

    Returns:
        dict: The merged dictionary
    """
    merged = {}
    keys = defaults.keys()

    for key in keys:
        merged[key] = options.get(key, defaults[key])

    return merged