from dataclasses import dataclass as component
from typing import Any

import pygame


@component
class Velocity:
    x: float = 0.0
    y: float = 0.0


@component
class PlayerControlled:
    pass


@component
class Obstacle:
    pass


@component
class Destructible:
    live: bool


@component
class Renderable:
    image: pygame.image
    color: tuple[int, int, int]
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0


@component
class RenderableRect(Renderable):
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


@component
class RenderableCircle(Renderable):
    x: float = 0.0
    y: float = 0.0
    radius: float = 1.0

    def draw(self, window):
        self.image.fill(self.color)
        pygame.draw.circle(
            self.image,
            self.color,
            (self.x, self.y),
            self.radius,
        )
        window.blit(self.image, (self.x, self.y))
