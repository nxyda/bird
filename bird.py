import pygame
import sys
import random

pygame.init()
clock = pygame.time.Clock()

bird_move = 0
score = 0  # Inicjalizacja licznika punktów

screen = pygame.display.set_mode((512, 800))

bird = pygame.image.load("bird.png").convert()
bird_rect = bird.get_rect(center=(100, 512))
background = pygame.image.load("background.png").convert()
background = pygame.transform.scale2x(background)

gravity = 0.7

game_true = True

floor_base = pygame.image.load("floor.png").convert()
floor_base = pygame.transform.scale2x(floor_base)
floor_x = 0

pipe_bottom = pygame.image.load("pipe.png")
pipe_list = []
pipe_height = 450

pipe_render = pygame.USEREVENT
pygame.time.set_timer(pipe_render, 1200)

# Font dla punktów
font = pygame.font.Font(None, 36)

def game_floor():
    screen.blit(floor_base, (floor_x, 700))
    screen.blit(floor_base, (floor_x + 500, 900))

def check_collision():
    if bird_rect.top <= -100 or bird_rect.bottom >= 700:
        return False
    return True

def game_over():
    screen.fill((0, 0, 0))
    text = font.render("GAME OVER", True, (255, 255, 255))
    text_rect = text.get_rect(center=(512/2, 800/2))
    screen.blit(text, text_rect)
    pygame.display.flip()

def create_pipe():
    random_pipe_pos = random.randint(300, 600)
    bottom_pipe = pipe_bottom.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_bottom.get_rect(midbottom=(700, random_pipe_pos - 250))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe[0].centerx -= 5
        pipe[1].centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        screen.blit(pipe_bottom, pipe[0])
        screen.blit(pygame.transform.flip(pipe_bottom, False, True), pipe[1])

def update_score(score):
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_true == True:
                bird_move = 0
                bird_move -= 12
            if event.key == pygame.K_SPACE and game_true == False:
                bird_rect.center = (100, 400)
                bird_move = 0
                game_true = True
                pipe_list.clear()  # Wyczyść listę rur
                score = 0  # Zresetuj licznik punktów

        if event.type == pipe_render and game_true == True:
            pipe_list.append(create_pipe())

    screen.blit(background, (0, 0))

    if game_true == True:
        bird_move += gravity
        bird_rect.centery += bird_move
        screen.blit(bird, bird_rect)
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Sprawdzenie, czy ptak przeszedł rurę i zwiększenie punktów
        for pipe in pipe_list:
            if bird_rect.centerx == pipe[0].centerx:
                score += 1

        update_score(score)  # Aktualizuj punkty
        game_true = check_collision()
    else:
        game_over()

    floor_x -= 1
    game_floor()
    if floor_x <= -512:
        floor_x = 0

    pygame.display.update()
    clock.tick(60)
