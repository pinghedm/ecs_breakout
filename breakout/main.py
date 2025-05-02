from dataclasses import dataclass as component

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
from processors import (
    DesctructibleProcessor,
    ObstacleProcessor,
    PlayerControlledProcessor,
    RenderProcessor,
    VelocityProcessor,
)

FPS = 60
RESOLUTION = 720, 480


def init_entities():
    # paddle
    esper.create_entity(
        Velocity(0, 0),
        RenderableRect(
            image=pygame.Surface([100, 20]),
            color=(255, 255, 255),
            x=0,
            y=480 - 20,
            width=100,
            height=20,
        ),
        PlayerControlled(),
    )
    esper.create_entity(
        Velocity(0, -1.0),
        RenderableCircle(
            image=pygame.Surface([10, 10]),
            color=(255, 255, 255),
            radius=10,
            x=200,
            y=200,
        ),
    )
    for row_idx in range(3):
        for col_idx in range(10):
            # bricks
            esper.create_entity(
                RenderableRect(
                    image=pygame.Surface([60, 19]),
                    color=(255, 255, 255),
                    x=10 + (col_idx * 720 / 10),
                    y=1 + (20 * row_idx),
                    width=100,
                    height=20,
                ),
                Obstacle(),
                Destructible(live=True),
            )


def init_processors(window):
    esper.add_processor(VelocityProcessor())
    esper.add_processor(ObstacleProcessor())
    esper.add_processor(PlayerControlledProcessor())
    esper.add_processor(DesctructibleProcessor())
    esper.add_processor(RenderProcessor(window=window))


def run():
    pygame.init()
    window = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption("Breakout!")
    clock = pygame.time.Clock()

    init_entities()
    init_processors(window)

    running = True
    _, (_, paddle_vel) = esper.get_components(PlayerControlled, Velocity)[0]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    paddle_vel.x = 1
                elif event.key == pygame.K_LEFT:
                    paddle_vel.x = -1
            elif event.type == pygame.KEYUP:
                paddle_vel.x = 0
        esper.process()
        clock.tick(FPS)


if __name__ == "__main__":
    run()
    pygame.quit()
