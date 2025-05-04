import math
from dataclasses import dataclass as component

import pygame


@component
class Velocity:
    x: float = 0.0
    y: float = 0.0

    @property
    def speed(self):
        return math.sqrt(self.x**2 + self.y**2)


@component
class Renderable:
    image: pygame.image
    color: tuple[int, int, int]
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0

    def draw(self, window):
        self.image.fill(self.color)
        pygame.draw.rect(self.image, self.color, [0, 0, self.width, self.height])
        window.blit(
            self.image,
            (
                self.x,
                self.y,
            ),
        )

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def normalized_vector_to(self, other):
        horiz = other.x - self.x
        vert = other.y - self.y
        dist = math.sqrt((horiz**2 + vert**2))
        return pygame.Vector2(horiz / dist, vert / dist)


@component
class Collectible:
    eaten: bool = False


@component
class Wall:
    pass


@component
class Player:
    pass


@component
class Ghost:
    pass
