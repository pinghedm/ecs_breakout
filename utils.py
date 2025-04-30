import pygame


def ball_colliding_with_rect(ball_circ, rect, check_from="bottom", entity=None):
    ball_top = ball_circ.y - ball_circ.radius
    ball_bot = ball_circ.y + ball_circ.radius
    ball_left = ball_circ.x - ball_circ.radius
    ball_right = ball_circ.x + ball_circ.radius

    rect_top = rect.y
    rect_bot = rect.y + rect.height

    return pygame.Rect(rect.x, rect.y, rect.width, rect.height).collidepoint(
        ball_left, ball_top if check_from == "bottom" else ball_bot
    )

    hit_in_x = ball_left >= rect.x and (rect.x + rect.width) <= ball_right
    if check_from == "bottom":
        hit_in_y = rect_bot - 1 <= ball_top <= rect_bot + 1
    else:
        hit_in_y = rect_top - 1 <= ball_bot <= rect_top + 1

    print(ball_circ, rect, hit_in_x, hit_in_y, entity)
    return hit_in_x and hit_in_y
