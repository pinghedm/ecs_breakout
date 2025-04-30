import esper
import pygame
from components import (
    Destructible,
    Obstacle,
    PlayerControlled,
    RenderableCircle,
    RenderableRect,
    Velocity,
)
from utils import ball_colliding_with_rect


class RenderProcessor:
    def __init__(self, window, clear_color=(0, 0, 0)):
        self.window = window
        self.clear_color = clear_color

    def process(self):
        self.window.fill(self.clear_color)
        for _, renderable in esper.get_component(RenderableRect) + esper.get_component(
            RenderableCircle
        ):
            renderable.draw(self.window)
        pygame.display.flip()


class PlayerControlledProcessor:
    def process(self):
        ball_entity, (ball_vel, ball_circ) = esper.get_components(
            Velocity,
            RenderableCircle,
        )[0]
        paddle_entity, (_, paddle_rect) = esper.get_components(
            PlayerControlled,
            RenderableRect,
        )[0]
        if ball_colliding_with_rect(ball_circ, paddle_rect, check_from="top"):
            print("hit paddle!")
            ball_vel.y = -1


class DesctructibleProcessor:
    def process(self):
        for entity, (destructible, rect) in esper.get_components(
            Destructible, RenderableRect
        ):
            if not destructible.live:
                rect.color = (0, 0, 0)


class ObstacleProcessor:
    def process(self):
        ball_entity, (ball_vel, ball_circ) = esper.get_components(
            Velocity,
            RenderableCircle,
        )[0]

        for entity, (obstacle, destructible) in esper.get_components(
            Obstacle, Destructible
        ):
            rect = esper.component_for_entity(entity, RenderableRect)
            if destructible.live and ball_colliding_with_rect(ball_circ, rect, entity):
                print("hitting brick", entity)
                destructible.live = False
                ball_vel.y = 1


class VelocityProcessor:
    def process(self):
        for _, (vel, rect) in esper.get_components(Velocity, RenderableRect):
            rect.x += vel.x
            rect.y += vel.y
            if rect.x < 0:
                rect.x = 0
            elif rect.x > 710:
                rect.x = 710
            if rect.y < 0:
                rect.y = 0
            elif rect.y > 470:
                rect.y = 470
        for _, (vel, circ) in esper.get_components(Velocity, RenderableCircle):
            circ.x += vel.x
            circ.y += vel.y
            if circ.x < 0:
                circ.x = 0
            elif circ.x > 710:
                circ.x = 710
            if circ.y < 0:
                circ.y = 0
            elif circ.y > 470:
                circ.y = 470
