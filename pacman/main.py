from dataclasses import dataclass as component

import esper
import pygame
from components import Collectible, Ghost, Player, Renderable, Velocity, Wall
from consts import (
    FPS,
    GHOST_SPEED_MULT,
    PLAYER_X_SPEED,
    PLAYER_Y_SPEED,
    RESOLUTION,
    TILE_HEIGHT,
    TILE_WIDTH,
)
from processors import (
    CollectibleProcessor,
    GhostProcessor,
    RenderProcessor,
    VelocityProcessor,
)


def init_processors(window):
    esper.add_processor(RenderProcessor(window=window))
    esper.add_processor(VelocityProcessor())
    esper.add_processor(GhostProcessor(window=window))
    esper.add_processor(CollectibleProcessor(window=window))


def init_entities():
    with open("maze.txt") as f:
        for row_idx, row in enumerate(f.readlines()):
            for col_idx, col in enumerate(row):
                if col == "o":
                    esper.create_entity(
                        Collectible(),
                        Renderable(
                            image=pygame.Surface([TILE_WIDTH, TILE_HEIGHT]),
                            color=(0, 255, 255),
                            x=TILE_WIDTH * col_idx,
                            y=TILE_HEIGHT * row_idx,
                            width=TILE_WIDTH,
                            height=TILE_HEIGHT,
                        ),
                    )

                elif col == "P":
                    esper.create_entity(
                        Player(),
                        Velocity(),
                        Renderable(
                            image=pygame.Surface([TILE_WIDTH, TILE_HEIGHT]),
                            color=(255, 255, 0),
                            x=TILE_WIDTH * col_idx,
                            y=TILE_HEIGHT * row_idx,
                            width=TILE_WIDTH * 0.8,
                            height=TILE_HEIGHT * 0.8,
                        ),
                    )
                elif col == "G":
                    esper.create_entity(
                        Ghost(),
                        Velocity(),
                        Renderable(
                            image=pygame.Surface([TILE_WIDTH, TILE_HEIGHT]),
                            color=(255, 0, 0),
                            x=TILE_WIDTH * col_idx,
                            y=TILE_HEIGHT * row_idx,
                            width=TILE_WIDTH * 0.5,
                            height=TILE_HEIGHT * 0.5,
                        ),
                    )
                elif col == "x":
                    esper.create_entity(
                        Wall(),
                        Renderable(
                            image=pygame.Surface([TILE_WIDTH, TILE_HEIGHT]),
                            color=(50, 50, 50),
                            x=TILE_WIDTH * col_idx,
                            y=TILE_HEIGHT * row_idx,
                            width=TILE_WIDTH,
                            height=TILE_HEIGHT,
                        ),
                    )


def _cleanup():
    for p in esper._processors:
        esper.remove_processor(type(p))


def init_event_handlers():
    esper.set_handler("lose", _cleanup)
    esper.set_handler("win", _cleanup)


def run():
    pygame.init()
    window = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption("Pac-Man")
    clock = pygame.time.Clock()

    init_processors(window)
    init_entities()
    init_event_handlers()

    running = True
    _, (_, player_render, player_velocity) = esper.get_components(
        Player, Renderable, Velocity
    )[0]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player_velocity.x = PLAYER_X_SPEED
                elif event.key == pygame.K_LEFT:
                    player_velocity.x = -1 * PLAYER_X_SPEED
                elif event.key == pygame.K_UP:
                    player_velocity.y = -1 * PLAYER_Y_SPEED
                elif event.key == pygame.K_DOWN:
                    player_velocity.y = PLAYER_Y_SPEED
            elif event.type == pygame.KEYUP:
                player_velocity.x = 0
                player_velocity.y = 0

        esper.process()
        clock.tick(FPS)


if __name__ == "__main__":
    run()
    pygame.quit()
