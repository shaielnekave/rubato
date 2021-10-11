from pgp.sprite.sprite import Sprite
from pygame.image import load
from pgp.utils import Vector

class Image(Sprite):
    """
    A subclass of Sprite that handles Images.

    :param image_location: The path to the image.
    :param pos: The position of the sprite.
    """
    # TODO Sprite Scaling
    def __init__(self, image_location: str, pos: Vector = Vector()):
        self.image = load(image_location if image_location != "" else "pgp/static/default.png")
        super().__init__(pos)

    def update(self):
        pass

    def draw(self, camera):
        """
        Draws the image if the z index is below the camera's

        :param camera: The current Camera viewing the scene
        """
        super().draw(self.image, camera)