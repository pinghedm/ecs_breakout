import pyclbr
import random

import esper
import pygame
from components import Collectible, Ghost, Player, Renderable, Velocity, Wall
from consts import (
    GHOST_SPEED_MULT,
    PLAYER_X_SPEED,
    PLAYER_Y_SPEED,
    RESOLUTION,
    TILE_HEIGHT,
    TILE_WIDTH,
)


class RenderProcessor:
    def __init__(self, window, clear_color=(0, 0, 0)):
        self.window = window
        self.clear_color = clear_color

    def process(self):
        self.window.fill(self.clear_color)
        for _, (renderable, _) in esper.get_components(Renderable, Wall):
            renderable.draw(self.window)
        for _, (renderable, collectible) in esper.get_components(
            Renderable, Collectible
        ):
            if not (collectible.eaten):
                renderable.draw(self.window)
        for _, (renderable, _) in esper.get_components(Renderable, Ghost):
            renderable.draw(self.window)

        _, (_, player_render) = esper.get_components(Player, Renderable)[0]
        player_render.draw(self.window)

        pygame.display.flip()


class CollectibleProcessor:
    def __init__(
        self,
        window,
        clear_color=(0, 0, 0),
    ):
        self.window = window
        self.clear_color = clear_color

    def process(self):
        cs = [x[1] for x in esper.get_component(Collectible)]
        all_eaten = all(c.eaten for c in cs)
        if all_eaten:
            pygame.font.init()
            self.window.fill(self.clear_color)
            font = pygame.font.Font(None, 64)
            text = font.render("You Win!", True, (255, 255, 255))
            text_pos = text.get_rect(
                centerx=RESOLUTION[0] / 2, centery=RESOLUTION[0] / 2
            )
            self.window.blit(text, text_pos)
            pygame.display.flip()
            esper.dispatch_event("win")


class GhostProcessor:
    def __init__(
        self,
        window,
        clear_color=(0, 0, 0),
    ):
        self.window = window
        self.clear_color = clear_color

    def process(self):
        _, (_, ghost_render) = esper.get_components(Ghost, Renderable)[0]
        _, (_, player_render) = esper.get_components(Player, Renderable)[0]

        if ghost_render.rect.colliderect(player_render.rect):
            self.window.fill(self.clear_color)
            pygame.display.flip()
            font = pygame.font.Font(None, 64)
            text = font.render("You Lose!", True, (255, 255, 255))
            text_pos = text.get_rect(
                centerx=RESOLUTION[0] / 2, centery=RESOLUTION[0] / 2
            )
            self.window.blit(text, text_pos)
            pygame.display.flip()
            esper.dispatch_event("lose")


class VelocityProcessor:
    def get_proposed_rect(self, renderable, velocity):
        new_x, new_y = (
            renderable.x + velocity.x,
            renderable.y + velocity.y,
        )
        if new_x < 0:
            renderable.x = RESOLUTION[0]
            new_x = RESOLUTION[0]
        elif new_x > RESOLUTION[0]:
            renderable.x = 0
            new_x = 0

        return pygame.Rect(new_x, new_y, TILE_WIDTH, TILE_HEIGHT)

    def get_wall_renderables(self):
        return [x[1][0].rect for x in esper.get_components(Renderable, Wall)]

    def update_player(self):
        _, (_, player_render, player_velocity) = esper.get_components(
            Player, Renderable, Velocity
        )[0]
        player_next_rect = self.get_proposed_rect(player_render, player_velocity)
        walls = self.get_wall_renderables()
        would_collide = player_next_rect.collidelist(walls) != -1

        if not would_collide:
            player_render.x += player_velocity.x
            player_render.y += player_velocity.y

        uneaten_pellets = [
            x[1]
            for x in esper.get_components(Renderable, Collectible)
            if not x[1][1].eaten
        ]
        just_eaten_idx = player_next_rect.collidelist(
            [x[0].rect for x in uneaten_pellets]
        )
        just_eaten_pellet = (
            uneaten_pellets[just_eaten_idx] if just_eaten_idx != -1 else None
        )
        if just_eaten_pellet:
            just_eaten_pellet[1].eaten = True

    def update_ghost(self):
        _, (_, ghost_render, ghost_velocity) = esper.get_components(
            Ghost, Renderable, Velocity
        )[0]
        _, (_, player_render, player_velocity) = esper.get_components(
            Player, Renderable, Velocity
        )[0]
        if player_velocity.speed <= 0:
            return

        walls = self.get_wall_renderables()
        vec_to_player = ghost_render.normalized_vector_to(player_render)
        ghost_velocity.x, ghost_velocity.y = (
            vec_to_player.x * GHOST_SPEED_MULT * PLAYER_X_SPEED
        ), (vec_to_player.y * GHOST_SPEED_MULT * PLAYER_Y_SPEED)
        ghost_next_rect = self.get_proposed_rect(ghost_render, ghost_velocity)
        would_collide = ghost_next_rect.collidelist(walls) != -1
        if would_collide:
            # eh pick a random direction, dont get stuck at a wall
            ghost_velocity.x = (
                random.choice([-1, 1]) * GHOST_SPEED_MULT * PLAYER_X_SPEED
            )
            ghost_velocity.y = (
                random.choice([-1, 1]) * GHOST_SPEED_MULT * PLAYER_X_SPEED
            )

        ghost_render.x += ghost_velocity.x
        ghost_render.y += ghost_velocity.y

        went_into_wall = ghost_render.rect.collidelist(walls) != -1
        if went_into_wall:
            ghost_render.x -= ghost_velocity.x
            ghost_render.y -= ghost_velocity.y

    def process(self):
        self.update_player()
        self.update_ghost()
