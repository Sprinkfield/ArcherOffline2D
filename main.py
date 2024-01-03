"""Run this file to play the game."""
import pygame
import random
import time
from objects import *


def main():
    run = True
    game_clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    start_time = time.time()
    player_speed = 7
    arrow_speed = 40
    target_counter = 0
    time_limit = 10
    score_limit = 20

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Archer")

    # Flags
    defeat = False
    victory = False

    # Defining objects
    player = Player(WIDTH//2 - 100, HEIGHT*0.8, 200, 80, player_picture)
    target1 = Target(random.randint(20, WIDTH - 100), 60, 80, 80, target_texture)
    target2 = Target(random.randint(20, WIDTH - 100), 160, 80, 80, target_texture)

    ammo = pygame.sprite.Group()
    targets = pygame.sprite.Group()
    targets.add(target1, target2)

    while run and (not defeat) and (not victory):
        screen.blit(pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT)), (0, 0))
        if target_counter >= score_limit:
            victory = True
        elif time.time() - start_time >= time_limit:
            defeat = True

        # Events handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # Movement handler
            if event.type == pygame.MOUSEBUTTONDOWN:
                    player.fire(ammo, arrow_speed)
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    player.x_speed = player_speed
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    player.x_speed = -player_speed
                elif event.key == pygame.K_SPACE:
                    player.fire(ammo, arrow_speed)
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_RIGHT, pygame.K_d, pygame.K_LEFT, pygame.K_a]:  # Horizontal
                    player.x_speed = 0

        # Movement handler
        for trgt in targets:
            trgt.update()

        for arrow in ammo:
            screen.blit(pygame.transform.scale(arrow.image, (arrow.width, arrow.height)), arrow.rect)
            arrow.fly()

        # Collision handler
        for trgt in targets:
            for arrow in ammo:
                if pygame.sprite.collide_rect(arrow, trgt):
                    target_counter += 1
                    arrow.kill()
                    trgt.rect.x = random.randint(20, WIDTH - 100)

        # Drawing (updating) objects
        player.update(screen)

        for trgt in targets:
            screen.blit(trgt.image, trgt.rect)

        # Screen render
        game_clock.tick(FPS)
        font_type = pygame.font.SysFont("Arial", 25, True, False)
        text_object = font_type.render(f"Score: {str(target_counter)}/{score_limit}", False, pygame.Color(10, 255, 10))
        text_location = pygame.Rect(3, 0, WIDTH, 100)
        screen.blit(text_object, text_location)
        text_object = font_type.render("Time: " + str(time_limit - int(time.time() - start_time)), False, pygame.Color(255, 255, 10))
        text_location = pygame.Rect(WIDTH - 110, 0, WIDTH, 100)
        screen.blit(text_object, text_location)
        pygame.display.flip()

    if defeat:
        new_background = pygame.image.load("images/game_over.png")
        render_end_screen(screen, start_time, new_background, target_counter, False)
    elif victory:
        new_background = pygame.image.load("images/victory.png")
        render_end_screen(screen, start_time, new_background, start_time, True)


def render_end_screen(screen, game_clock, new_background, score, victory):
    exit_flag = False
    new_time = time.time()

    while not exit_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_flag = True
            elif time.time() - new_time >= 2.5 and event.type == pygame.MOUSEBUTTONDOWN:
                return main()  # Start a new game

        screen.blit(pygame.transform.scale(new_background, (WIDTH, HEIGHT)), (0, 0))
        if victory:
            draw_end_text(screen, round(new_time - game_clock, 2), victory)
        else:
            draw_end_text(screen, score, victory)
        pygame.display.flip()


def draw_end_text(screen, game_time, victory):
    if victory:
        font = pygame.font.SysFont("Arial", WIDTH//8, True)
        caption = font.render(f"Victory!", True, (10, 10, 255))
        screen.blit(caption, (WIDTH//2 - WIDTH//5, HEIGHT//5))
        font = pygame.font.SysFont("Arial", WIDTH//20)
        font_color = (10, 10, 255)
        caption = font.render(f"Time: {game_time}", True, font_color)
    else:
        font = pygame.font.SysFont("Arial", WIDTH//8, True)
        caption = font.render(f"Game over!", True, (255, 0, 0))
        screen.blit(caption, (WIDTH//2 - WIDTH//3, HEIGHT//5))
        font = pygame.font.SysFont("Arial", WIDTH//20)
        font_color = (255, 0, 0)
        caption = font.render(f"Score: {game_time}", True, font_color)
    screen.blit(caption, (WIDTH//2 - 90, HEIGHT//2 + 200))
    caption = font.render(f"Click mouse button to play again", True, font_color)
    screen.blit(caption, (WIDTH//6, HEIGHT//2 + 100))


if __name__ == "__main__":
    main()
