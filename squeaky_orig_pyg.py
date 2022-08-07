import pygame
import random
import time
from pygame import mixer

# island initialising
island_size = 1000
start_pos = 500


# the island is almost 2/3 of the height of console window
island_rel_height = 1 / 3
island_img = pygame.image.load("island.jpeg")


# Initialising the game
pygame.init()
speed = 100


# Background sound
mixer.music.load('rock_around_the_clock.mp3')
mixer.music.play(-1)    # putting -1 to run the music on loop


# The console window
scale = 1.5

width = 626 * scale
height = 250 * scale

island_img = pygame.transform.scale(island_img, (width, height))

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Random Walk on a Lonely Island")  # window title
pygame.display.set_icon(pygame.image.load('plaksha.png'))  # setting the window title


# the possible grid points
grid = [(width / 6) + (width * (2 / 3) / island_size) * i for i in range(0, island_size + 1)]


# character (Squeaky) properties
cur_pos = start_pos
squirrel_img = pygame.image.load('squirrel.png')  # initialy facing left
squirrel_size = 10 * width / island_size
squirrel_img = pygame.transform.scale(squirrel_img, (squirrel_size, squirrel_size))

squ_flip_img = pygame.transform.flip(squirrel_img, True, False)

squirrel_pos = (grid[cur_pos], height * island_rel_height)
updated_img = squirrel_img

bool_died = False


def player():

    global squirrel_pos, cur_pos, bool_running, bool_died, updated_img

    x = start_pos

    while 0 <= x <= island_size:

        screen.blit(island_img, (0, 0))

        rand_jump = 2 * random.random() - 1

        if rand_jump < 0:
            cur_pos = cur_pos - 1

            if cur_pos <= 0:

                bool_running = False
                bool_died = True
                mixer.music.pause()
                mixer.music.load('dying_music.mp3')
                mixer.music.play()
                return

            # original image facing left
            updated_img = squirrel_img

        else:
            cur_pos = cur_pos + 1

            if cur_pos >= island_size:

                bool_running = False
                bool_died = True
                mixer.music.pause()
                mixer.music.load('dying_music.mp3')
                mixer.music.play()
                return

            # flipped image
            updated_img = squ_flip_img

        squirrel_pos = (grid[cur_pos], height * island_rel_height - squirrel_size / island_size)
        screen.blit(updated_img, squirrel_pos)
        pygame.display.update()  # first updating the display
        time.sleep(10 / speed)  # then sleeping the game to account for frame speed


# Game Loop, running infinitely until bool_running is false
bool_running = True
started = False  # user has not started the game

screen.fill((000, 120, 120))
screen.blit(island_img, (0, 0))

while bool_running:

    # fetching all events
    for event in pygame.event.get():

        # if quit button is pressed
        if event.type == pygame.QUIT:

            # setting bool_running to False
            bool_running = False

        if event.type == pygame.KEYDOWN:
            player()
            bool_running = False

    pygame.display.update()


while bool_died:

    # fetching all events
    for event in pygame.event.get():

        # if quit button is pressed
        if event.type == pygame.QUIT:
            # setting bool_running to False
            bool_died = False

    screen.blit(updated_img, squirrel_pos)
    pygame.display.update()


print("Thanks for Playing the game.")
