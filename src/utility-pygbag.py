# This file contains global functions, classes
from __future__ import annotations

import os
import math
import random

import pygame
import pygame_gui

class Window(object):
    asp_ratio = 2880 / 1442  # w:h, longer height to fit GUI Interactives

    width = 1600  # in px
    height = width * asp_ratio**-1  # in px

    size = (width, height)

    background = (0, 120, 120)  # default background, RGB Plaksha Colour

    title = "Random Walk on a Lonely Island"
    small_title = "Squeaky's Demise"

    start_message = "Welcome! Press spacebar to start."
    end_message = "Press spacebar to play again!"

    probslider_size = (200, 30)
    probslider_pos = (width / 2 - probslider_size[0] / 2, height / 2 + 55)
    probslider_message = "Set probability of jump direction"

    initposslider_size = (200, 30)
    initposslider_pos = (width / 2 - initposslider_size[0] / 2, height / 2 + 140)
    initposslider_message = "Set initial position       "

    icon = pygame.image.load(
        os.path.join(os.path.dirname(__file__), "../assets/image/plaksha.png")
    )
    rel_padding = 0.13
    hor_padding = rel_padding * width

    """
    main_music = os.path.join(
        os.path.dirname(__file__), "../assets/music/rock_around.ogg"
    )
    """
    main_music = os.path.join(
        os.path.dirname(__file__), "../assets/music/aao_twist_karein.ogg"
    )
    death_music = os.path.join(
        os.path.dirname(__file__), "../assets/music/pacman_die.ogg"
    )

    fontpath = os.path.join(os.path.dirname(__file__), "../assets/fonts/courier.ttf")
    font_size = 30
    # font = pygame.font.Font(fontpath, int(font_size / 2))
    # ui_manager = pygame_gui.UIManager(size)


# Island globals
class Island(object):
    img = pygame.image.load(
        os.path.join(os.path.dirname(__file__), "../assets/image/island-final.png")
    )

    asp_ratio = 2880 / 1442  # w:h

    width = Window.width  # in px
    height = width * asp_ratio**-1  # in px

    size = (width, height)

    img = pygame.transform.scale(img, size)  # rescaling to fit width

    length = 36  # default size of island


# Squirrel globals
class Squirrel(object):
    asp_ratio = 1 / 1  # w:h
    # * (math.e ** (-Island.length / 1000))
    # !! this makes it very necessary to define island properties before squirel
    height = Island.height * (1 / 10)
    width = height * asp_ratio  # in px

    size = (width, height)

    cur_pos = 18  # default starting position of squirel
    init_pos = cur_pos

    rel_height = 0.67  # squirel stands 2 / 3 of island image height, from top

    img = pygame.image.load(
        os.path.join(os.path.dirname(__file__), "../assets/image/squirrel.png")
    )
    img = pygame.transform.scale(img, size)
    # reversed image to save time
    rev_img = pygame.transform.flip(img, True, False)

    splash_img = pygame.image.load(
        os.path.join(os.path.dirname(__file__), "../assets/image/splash.png")
    )
    splash_img = pygame.transform.scale(splash_img, size)  # reversed image to save time

    # set colorkeys
    img.set_colorkey((0, 0, 0))
    rev_img.set_colorkey((0, 0, 0))
    splash_img.set_colorkey((0, 0, 0))

    rel_grid_pos = [
        Window.rel_padding + i * (1 - 2 * Window.rel_padding) / Island.length
        for i in range(0, Island.length + 1)
    ]

    rel_death_y = 5 / 6
    death_y = rel_death_y * Island.height
    squirrel_y = rel_height * Island.height

    num_hops = 0

    # probability of jumping right (and consequently left)
    p_right = 0.5

    # left and right step sizes (why not)
    left_stepsize = 1
    right_stepsize = 1


# Coin globals
class Coin(object):  # Coin_Window actually
    asp_ratio = 1 / 1  # w:h

    height = Island.height * (1 / 4)
    width = height * asp_ratio

    size = (width, height)  # The window size

    rel_pos = (1 - 1.79 / 3, 1.03 / 2)
    abs_pos = (rel_pos[0] * Island.width, rel_pos[1] * Island.height)

    heads_img = pygame.image.load(
        os.path.join(os.path.dirname(__file__), "../assets/image/heads.png")
    )
    tails_img = pygame.image.load(
        os.path.join(os.path.dirname(__file__), "../assets/image/tails.png")
    )

    coin_size = (size[0] / (2.5), size[1] / 2.5)
    heads_img = pygame.transform.scale(heads_img, coin_size)
    tails_img = pygame.transform.scale(tails_img, coin_size)


class Tree(object):
    asp_ratio = 1 / 1  # w:h

    height = Island.height * (1 / 4)
    width = height * asp_ratio * 1.25

    size = (width, height)  # The window size

    rel_pos = (1.79 / 3, 0.9 / 2)
    abs_pos = (rel_pos[0] * Island.width, rel_pos[1] * Island.height)

    rel_padding = 1 / 10

    # has 1 where the node is
    nodes = [[0 for _ in range(0, Island.length + 1)]]
    edges = [[None for _ in range(0, Island.length + 1)]]
    choices = [[None for _ in range(0, Island.length + 1)]]

    nodes[Squirrel.num_hops][Squirrel.cur_pos] = 1

    white = (150, 150, 150)
    red = (250, 0, 0)
    black = (0, 0, 0)
    yellow = (255, 255, 0)
    cyan = (153, 255, 255)
    grey = (150, 150, 150)
    pink = (255, 192, 203)
    fluoro_green = (0, 250, 0)
    path_color = fluoro_green
    grid_color = grey
    background_color = (250, 250, 250, 0)

    tree_message = "Probability Path"


# Game globals
class Game(object):
    fps = 30  # fps
    clock = pygame.time.Clock()

    border_width_limit = int(5 * Island.size[0] * Window.rel_padding)
    border_width = int(abs(Squirrel.cur_pos) * border_width_limit / Island.length)


def init_game():
    global screen_surf
    global ui_manager

    pygame.init()
    # font = pygame.font.Font(Window.fontpath, int(Window.font_size / 2))
    ui_manager = pygame_gui.UIManager(Window.size)

    # before set_mode line, as advised in Doc
    pygame.display.set_icon(Window.icon)

    screen_surf = pygame.display.set_mode(
        size=Window.size,
        # flags=pygame.RESIZABLE,
        display=0,
    )
    # [display window should be sizeable](https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode)
    print("hi, this is malhar here")

    pygame.display.set_caption(Window.title, Window.small_title)


def text_on_screen(
    message: str,
    coordinates: tuple | pygame.Rect,
    color: tuple,
    ref_surf: pygame.Surface = None,
    font_size: int = None,
) -> tuple[pygame.Surface, pygame.Rect]:
    """
    message: the message string
    coordinates: coordinates relative to the surface that the text goes on
    """

    if font_size == None:
        font = pygame.font.Font(Window.fontpath, int(Window.font_size / 1))

    else:
        font = pygame.font.Font(Window.fontpath, int(font_size))

    text = font.render(message, True, color)  # True for anti-aliasing

    if ref_surf is None:
        text_pos = accurate_draw(text, coordinates)
    else:
        text_pos = accurate_draw(ref_surf, coordinates)

    return text, text_pos


def death_player(
    screen_surf, background_surf, coin_surf, tree_surf, squirrel_surf, bg_size
):
    # Stop Music

    pygame.mixer.music.stop()
    pygame.mixer.music.load(Window.death_music, namehint="mp3")
    pygame.mixer.music.play(loops=1, start=0.0, fade_ms=1)

    last_squirrel_surf = squirrel_surf
    death_y = Squirrel.squirrel_y
    smoothness = 20
    while death_y < Squirrel.death_y:
        death_y += (Squirrel.death_y - Squirrel.squirrel_y) / smoothness

        background_surf.blit(Island.img.convert(), (0, 0))
        background_surf.blit(
            last_squirrel_surf,
            accurate_draw(last_squirrel_surf, (squirrel_location(), death_y)),
        )

        screen_surf.blit(pygame.transform.scale(background_surf, bg_size), (0, 0))
        pygame.display.flip()  # flips the blit on to the next frame, updates the frame

    last_squirrel_surf.blit(Squirrel.splash_img.convert_alpha(), (0, 0))
    # Text on screen
    text, text_pos = text_on_screen(
        Window.end_message,
        # background.get_rect().center,
        [sum(x) for x in zip(background_surf.get_rect().center, (0, -60))],
        (255, 255, 255, 1),
        font_size=Window.font_size * 2,
    )
    text_s1, text_pos_s1 = text_on_screen(
        Window.probslider_message,
        [sum(x) for x in zip(background_surf.get_rect().center, (0, 20))],
        (255, 255, 255, 1),
        font_size=Window.font_size / 1,
    )
    text_s2, text_pos_s2 = text_on_screen(
        Window.initposslider_message,
        [sum(x) for x in zip(background_surf.get_rect().center, (0, 120))],
        (255, 255, 255, 1),
        font_size=Window.font_size / 1,
    )
    font = pygame.font.Font(Window.fontpath, int(Window.font_size / 2))
    # live p values
    xpos1 = screen_surf.get_rect().center[0] + 120
    xpos2 = screen_surf.get_rect().center[0] - 270
    yposp = screen_surf.get_rect().center[1] + 65
    text_surface_probr = font.render(
        f"Prob(right) = {round(Squirrel.p_right, 2)}", True, (255, 255, 255)
    )
    text_surface_probl = font.render(
        f"Prob(left) = {round(1-Squirrel.p_right, 2)}", True, (255, 255, 255)
    )
    # live initpos values
    font1 = pygame.font.Font(Window.fontpath, int(Window.font_size / 1.5))
    xpos = screen_surf.get_rect().center[0] + 130
    ypos = screen_surf.get_rect().center[1] + 110
    text_surface_initpos = font1.render(
        f"{Squirrel.init_pos}", True, (255, 255, 255)
    )

    background_surf.blit(text, text_pos)
    background_surf.blit(
        last_squirrel_surf,
        accurate_draw(last_squirrel_surf, (squirrel_location(), death_y)),
    )
    background_surf.blit(text_s1, text_pos_s1)
    background_surf.blit(text_s2, text_pos_s2)

    screen_surf.blit(pygame.transform.scale(background_surf, bg_size), (0, 0))
    screen_surf.fill((0, 0, 0), (xpos1, yposp, 165, 13))
    screen_surf.fill((0, 0, 0), (xpos2, yposp, 155, 13))
    screen_surf.blit(text_surface_probr, (xpos1, yposp))
    screen_surf.blit(text_surface_probl, (xpos2, yposp))
    screen_surf.fill((0, 0, 0), (xpos, ypos, 20, 12))
    screen_surf.blit(text_surface_initpos, (xpos, ypos))
    Game.clock.tick(Game.fps)  # I am not sure what this does
    pygame.display.flip()  # flips the blit on to the next frame, updates the frame


def player(
    screen_surf, background_surf, coin_surf, tree_surf, squirrel_surf, bg_size
) -> tuple[bool, bool, bool]:
    death = False
    started = True
    success = False

    if Squirrel.cur_pos == 0 or Squirrel.cur_pos == Island.length:
        death = True
        started = False
        success = False

        death_player(
            screen_surf, background_surf, coin_surf, tree_surf, squirrel_surf, bg_size
        )

        Squirrel.cur_pos = Squirrel.init_pos
        Squirrel.num_hops = 0

        Tree.nodes = [[0 for _ in range(0, Island.length + 1)]]
        Tree.edges = [[None for _ in range(0, Island.length + 1)]]
        Tree.choices = [[None for _ in range(0, Island.length + 1)]]

        Tree.nodes[Squirrel.num_hops][Squirrel.cur_pos] = 1

    else:
        jump = random.choices(
            [-1 * Squirrel.left_stepsize, 1 * Squirrel.right_stepsize],
            weights=[1 - Squirrel.p_right, Squirrel.p_right],
            k=1,
        )[0]

        Squirrel.num_hops += 1
        Squirrel.cur_pos += jump

        Tree.choices.append([None for _ in range(0, Island.length + 1)])

        if jump == -1 * Squirrel.left_stepsize:
            # Tails or Left Jump
            coin_toss(screen_surf, background_surf, coin_surf, bg_size, -1)
            # I am not sure what this does
            Game.clock.tick(Game.fps)

            squirrel_surf = squirrel_draw(squirrel_surf, -1)
            coin_surf = coin_window(coin_surf, "TAILS", -1)
            Tree.choices[Squirrel.num_hops][Squirrel.cur_pos] = [
                False,
                True,
                "Red",
            ]

        elif jump == 1 * Squirrel.right_stepsize:
            # Heads or Right Jump
            coin_toss(screen_surf, background_surf, coin_surf, bg_size, 1)
            # I am not sure what this does
            Game.clock.tick(Game.fps)

            squirrel_surf = squirrel_draw(squirrel_surf, 1)
            coin_surf = coin_window(coin_surf, "HEADS", 1)
            Tree.choices[Squirrel.num_hops][Squirrel.cur_pos] = [
                True,
                False,
                "Red",
            ]

        else:
            raise "Error with Random Choice from list [-1, 1]"

        Tree.nodes.append([])
        Tree.nodes[Squirrel.num_hops] = next_row(Squirrel.num_hops)

        Tree.edges.append([])
        Tree.edges[Squirrel.num_hops] = next_edge(Squirrel.num_hops)

        tree_surf.fill((250, 250, 250, 0))

        tree_pos = accurate_draw(tree_surf, Tree.abs_pos)
        tree_text, tree_pos = text_on_screen(
            message=Tree.tree_message,
            coordinates=tree_pos.center,
            color=(250, 250, 250),
            ref_surf=tree_surf,
            font_size=Window.font_size / 1.5,
        )

        tree_surf.blit(
            tree_text,
            accurate_draw(
                tree_text, (Tree.width / 2, Tree.height * 9 / 10)
            ),
        )

        draw_lines(tree_surf, Tree.edges)
        draw_choices(tree_surf, Tree.choices)
        draw_nodes(tree_surf, Tree.nodes)

        # Squirrel.cur_pos += 1
        update_background(
            screen_surf, background_surf, coin_surf, tree_surf, squirrel_surf, bg_size
        )
        # I am not sure what this does
        Game.clock.tick(Game.fps)

        success = True

    return success, death, started


def squirrel_draw(squirrel_surf, mode):
    squirrel_surf.fill((0, 0, 0, 0))
    if mode == -1:
        squirrel_surf.blit(Squirrel.img.convert(), (0, 0))
    elif mode == 1:
        squirrel_surf.blit(Squirrel.rev_img.convert(), (0, 0))

    return squirrel_surf


def coin_toss(screen_surf, background, coin_surf, bg_size, mode):
    smoothness = math.pi * (1 - math.exp(-Game.fps / 300)) / 2
    angle = 0 + smoothness

    if mode == -1:
        img = Coin.tails_img.convert_alpha()
    else:
        img = Coin.heads_img.convert_alpha()
    empty = pygame.Color(0, 0, 0, 0)
    while angle < math.pi / 2 + smoothness:
        # pygame.draw.circle(coin_surf, (250, 250, 250, 1),
        #                    coin_surf.get_rect().center, Coin.size[0] / 2)  # HARD CODING SOME STUFF
        coin_surf.fill(empty)
        angle += smoothness

        x_width = Coin.coin_size[0] * math.sin(angle)

        temp_img = pygame.transform.scale(img, (x_width, Coin.coin_size[1]))
        coin_surf.blit(
            temp_img,
            accurate_draw(
                temp_img,
                (coin_surf.get_rect().centerx, coin_surf.get_rect().centery * 2 / 3),
            ),
        )

        background.blit(coin_surf, accurate_draw(coin_surf, Coin.abs_pos))
        screen_surf.blit(pygame.transform.scale(background, bg_size), (0, 0))
        Game.clock.tick()
        pygame.display.flip()  # flips the blit on to the next frame, updates the frame


def coin_window(coin_surf, message, mode):
    coin_surf.fill((0, 0, 0, 0))
    # pygame.draw.circle(coin_surf, (250, 250, 250, 0),
    #                    coin_surf.get_rect().center, Coin.size[0] / 2)  # HARD CODING SOME STUFF

    if mode == -1:
        coin_surf.blit(
            Coin.tails_img.convert_alpha(),
            (
                accurate_draw(
                    Coin.tails_img,
                    (
                        coin_surf.get_rect().centerx,
                        coin_surf.get_rect().centery * 2 / 3,
                    ),
                )
            ),
        )
    elif mode == 1:
        coin_surf.blit(
            Coin.heads_img.convert_alpha(),
            (
                accurate_draw(
                    Coin.tails_img,
                    (
                        coin_surf.get_rect().centerx,
                        coin_surf.get_rect().centery * 2 / 3,
                    ),
                )
            ),
        )

    coin_text, _ = text_on_screen(
        message=message,
        coordinates=coin_surf.get_rect().center,
        color=(250, 250, 250, 1),
        ref_surf=coin_surf,
    )
    coin_surf.blit(
        coin_text,
        accurate_draw(coin_text, (Coin.width / 2, Coin.height * 4 / 6)),
    )

    return coin_surf


def accurate_draw(surface, coordinates):
    # centers the blit-ing to the origin of Surface
    surface_rect = surface.get_rect()
    surface_rect.center = coordinates

    return surface_rect


def squirrel_location():
    return Squirrel.rel_grid_pos[Squirrel.cur_pos] * Island.width


def return_surface(
    size: tuple, init_color: tuple | None, mode: str = None, shape: str = None
) -> pygame.Surface:
    # a pygame object, to be modified with pygame methods
    surface = pygame.Surface(size)

    if mode == "convert":
        # converting to single pixel format to drastically speed up rendering times.
        surface = surface.convert()

    elif mode == "convert_alpha":
        surface = surface.convert_alpha()

    if init_color is not None:
        if shape is None:
            surface.fill(init_color)
        else:
            if shape == "circle":
                # print("A circle")
                pygame.draw.circle(
                    surface, init_color, surface.get_rect().center, size[0] / 2
                )

    return surface


# def game_loop():
#     # utility globals
#     # init_pos = Squirrel.cur_pos
#     bg_size = screen_surf.get_size()

#     (
#         background,
#         coin_surf,
#         tree_surf,
#         squirrel_surf,
#         prob_slider,
#         initpos_slider,
#     ) = background_load(screen_surf)

#     started = False
#     dead = False
#     bool_running = True
#     while bool_running:
#         # This is important for programs that want to share the system with other applications.
#         # pygame.event.pump()  # to allow pygame to handle internal actions, calls the event queue
#         # current_event = pygame.event.wait()  # fetches one event

#         time_delta = Game.clock.tick(60) / 1000.0

#         for current_event in pygame.event.get():
#             if current_event.type == pygame.QUIT:
#                 # checking for quit
#                 bool_running = False
#                 return
#             elif started and current_event.type == pygame.KEYDOWN:
#                 if current_event.key == pygame.K_ESCAPE:
#                     print("ESCAPE")
#                     started = False
#                     dead = True
#                     pygame.mixer.music.stop()
#                     Squirrel.num_hops = 0
#                     Tree.nodes = [[0 for _ in range(0, Island.length + 1)]]
#                     Tree.edges = [
#                         [None for _ in range(0, Island.length + 1)]
#                     ]
#                     Tree.choices = [
#                         [None for _ in range(0, Island.length + 1)]
#                     ]
#                     Tree.nodes[Squirrel.num_hops][
#                         Squirrel.cur_pos
#                     ] = 1

#                     # return to initial screen

#                     # screen_surf.blit(pygame.transform.scale(background, bg_size), (0, 0))
#                     # background.blit(Island.img.convert(), (0, 0))
#                     prob_slider.kill()  # Assuming prob_slider is a pygame_gui element, remove it from the UI
#                     initpos_slider.kill()  # Remove other GUI elements similarly

#                     (
#                         background,
#                         coin_surf,
#                         tree_surf,
#                         squirrel_surf,
#                         prob_slider,
#                         initpos_slider,
#                     ) = background_load(screen_surf)

#                     # bool_running = False
#                     # return

#             elif not started and current_event.type == pygame.KEYDOWN:
#                 if current_event.key == pygame.K_SPACE:
#                     # If space-bar pressed
#                     started = True
#                     dead = False

#                     pygame.mixer.music.load(Window.main_music, namehint="mp3")
#                     # fades into 100 volume in 5ms
#                     # pygame.mixer.music.play(loops=-1, start=3.3, fade_ms=5)
#                     pygame.mixer.music.play(loops=-1, start=20, fade_ms=5)

#             elif current_event.type == pygame.VIDEORESIZE:
#                 # in the running frame it is updated later on:
#                 bg_size = current_event.dict["size"]
#             if current_event.type == pygame.USEREVENT:
#                 if current_event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
#                     # Update parameter values when a slider is moved
#                     font = pygame.font.Font(
#                         Window.fontpath, int(Window.font_size / 2)
#                     )

#                     if current_event.ui_element == prob_slider:
#                         value = current_event.ui_element.get_current_value()
#                         print(f"Probability Slider moved to {value}")
#                         Squirrel.p_right = value

#                         xpos1 = background.get_rect().center[0] + 120
#                         xpos2 = background.get_rect().center[0] - 270
#                         ypos = background.get_rect().center[1] + 65
#                         screen_surf.fill((0, 0, 0), (xpos1, ypos, 165, 13))
#                         screen_surf.fill((0, 0, 0), (xpos2, ypos, 155, 13))
#                         text_surface_probr = font.render(
#                             f"Prob(right) = {round(value, 2)}", True, (255, 255, 255)
#                         )
#                         text_surface_probl = font.render(
#                             f"Prob(left) = {round(1-value, 2)}", True, (255, 255, 255)
#                         )
#                         screen_surf.blit(text_surface_probr, (xpos1, ypos))
#                         screen_surf.blit(text_surface_probl, (xpos2, ypos))

#                     if current_event.ui_element == initpos_slider:
#                         value = current_event.ui_element.get_current_value()
#                         print(f"InitPos Slider moved to {value}")
#                         Squirrel.init_pos = value
#                         Tree.nodes[Squirrel.num_hops][
#                             Squirrel.cur_pos
#                         ] = 0
#                         Squirrel.cur_pos = value
#                         Tree.nodes[Squirrel.num_hops][
#                             Squirrel.cur_pos
#                         ] = 1

#                         font1 = pygame.font.Font(
#                             Window.fontpath, int(Window.font_size / 1.5)
#                         )
#                         xpos = background.get_rect().center[0] + 130
#                         ypos = background.get_rect().center[1] + 110
#                         screen_surf.fill((0, 0, 0), (xpos, ypos, 25, 15))
#                         text_surface_initpos = font1.render(
#                             f"{Squirrel.cur_pos}", True, (255, 255, 255)
#                         )
#                         screen_surf.blit(text_surface_initpos, (xpos, ypos))

#             ui_manager.process_events(current_event)

#         if not dead and started:
#             # if game already started
#             success, dead, started = player(
#                 screen_surf, background, coin_surf, tree_surf, squirrel_surf, bg_size
#             )
#             if success:
#                 # if everything inside player went OK
#                 update_background(
#                     screen_surf,
#                     background,
#                     coin_surf,
#                     tree_surf,
#                     squirrel_surf,
#                     bg_size,
#                 )

#         # for UI elements => sliders buttons etc
#         ui_manager.update(time_delta)
#         if dead or not started:
#             ui_manager.draw_ui(screen_surf)
#         Game.clock.tick(Game.fps)  # I am not sure what this does
#         pygame.display.flip()  # updating the frame


def background_load(
    screen_surf,
) -> tuple[pygame.Surface, pygame.Surface, pygame.Surface, pygame.Surface]:
    # Called only once, at the beginning of game_loop()
    bg_size = screen_surf.get_size()
    # The background object
    background = return_surface(
        size=bg_size, init_color=Window.background, mode="convert"
    )

    # Text object on screen
    text, text_pos = text_on_screen(
        Window.start_message,
        # background.get_rect().center,
        [sum(x) for x in zip(background.get_rect().center, (0, -100))],
        (255, 255, 255, 1),
        font_size=Window.font_size * 2,
    )

    # Text for probability slider
    text_s1, text_pos_s1 = text_on_screen(
        Window.probslider_message,
        [sum(x) for x in zip(background.get_rect().center, (0, 20))],
        (255, 255, 255, 1),
        font_size=Window.font_size / 1,
    )

    # Text for initpos slider
    text_s2, text_pos_s2 = text_on_screen(
        Window.initposslider_message,
        [sum(x) for x in zip(background.get_rect().center, (0, 120))],
        (255, 255, 255, 1),
        font_size=Window.font_size / 1,
    )

    # live p values
    font = pygame.font.Font(Window.fontpath, int(Window.font_size / 2))
    xpos1 = background.get_rect().center[0] + 120
    xpos2 = background.get_rect().center[0] - 270
    yposp = background.get_rect().center[1] + 65
    text_surface_probr = font.render(
        f"Prob(right) = {round(Squirrel.p_right, 2)}", True, (255, 255, 255)
    )
    text_surface_probl = font.render(
        f"Prob(left) = {round(1-Squirrel.p_right, 2)}", True, (255, 255, 255)
    )

    # live initpos values
    font1 = pygame.font.Font(Window.fontpath, int(Window.font_size / 1.5))
    xpos = background.get_rect().center[0] + 130
    ypos = background.get_rect().center[1] + 110
    text_surface_initpos = font1.render(
        f"{Squirrel.cur_pos}", True, (255, 255, 255)
    )

    # Squirrel Surface
    squirrel_surf = return_surface(
        size=Squirrel.size, init_color=(0, 0, 0, 0), mode="convert_alpha"
    )
    squirrel_surf.blit(Squirrel.img.convert_alpha(), (0, 0))

    # Coin Window Surface
    coin_surf = return_surface(
        size=Coin.size, init_color=(0, 0, 0), mode="convert_alpha", shape="circle"
    )
    coin_surf.blit(
        Coin.heads_img.convert_alpha(),
        accurate_draw(Coin.heads_img, coin_surf.get_rect().center),
    )

    pygame.draw.rect(coin_surf, (250, 250, 250, 0.5), coin_surf.get_rect(), width=3)
    coin_pos = accurate_draw(coin_surf, Coin.abs_pos)
    # Coin Text on screen
    coin_text, coin_pos = text_on_screen(
        message="-----",
        coordinates=coin_pos.center,
        color=(250, 250, 250, 1),
        ref_surf=coin_surf,
    )
    coin_surf.blit(
        coin_text,
        accurate_draw(coin_text, (Coin.width / 2, Coin.height * 3 / 6)),
    )

    # Tree Window Surface
    tree_surf = return_surface(
        size=Tree.size,
        init_color=Tree.background_color,
        mode="convert_alpha",
    )
    pygame.draw.rect(tree_surf, (250, 250, 250, 0.5), tree_surf.get_rect(), width=3)
    tree_pos = accurate_draw(tree_surf, Tree.abs_pos)
    tree_text, tree_pos = text_on_screen(
        message=Tree.tree_message,
        coordinates=tree_pos.center,
        color=(250, 250, 250),
        ref_surf=tree_surf,
        font_size=Window.font_size / 1.5,
    )
    tree_surf.fill(Tree.background_color)
    tree_surf.blit(
        tree_text,
        accurate_draw(tree_text, (Tree.width / 2, Tree.height * 9 / 10)),
    )

    prob_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect(
            Window.probslider_pos, Window.probslider_size
        ),
        start_value=Squirrel.p_right,
        value_range=(0.0, 1.0),
        manager=ui_manager,
    )
    initpos_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect(
            Window.initposslider_pos, Window.initposslider_size
        ),
        start_value=Squirrel.cur_pos,
        value_range=(0, Island.length),
        manager=ui_manager,
    )

    # ------------
    background.blit(text, text_pos)
    background.blit(text_s1, text_pos_s1)
    background.blit(text_s2, text_pos_s2)
    # background.blit(text_surface_probr, text_pos_surface_probr)
    # background.blit(text_surface_probl, text_pos_surface_probl)
    screen_surf.blit(pygame.transform.scale(background, bg_size), (0, 0))

    screen_surf.fill((0, 0, 0), (xpos1, yposp, 165, 13))
    screen_surf.fill((0, 0, 0), (xpos2, yposp, 155, 13))
    screen_surf.blit(text_surface_probr, (xpos1, yposp))
    screen_surf.blit(text_surface_probl, (xpos2, yposp))
    screen_surf.fill((0, 0, 0), (xpos, ypos, 25, 15))
    screen_surf.blit(text_surface_initpos, (xpos, ypos))

    Game.clock.tick(Game.fps)  # I am not sure what this does
    pygame.display.flip()  # updating the frame

    return (
        background,
        coin_surf,
        tree_surf,
        squirrel_surf,
        prob_slider,
        initpos_slider,
    )


def update_background(
    screen_surf,
    background: pygame.Surface,
    coin_surf,
    tree_surf,
    squirrel_surf,
    bg_size,
):
    # updates the background object
    background.blit(Island.img.convert(), (0, 0))
    # pygame.draw.rect(background, (0, 0, 0, 1), background.get_rect(), width=int(1 + abs(
    #    Squirrel.cur_pos - Island.length / 2) * 0.2 * Game.border_width_limit / Island.length))

    background.blit(coin_surf, accurate_draw(coin_surf, Coin.abs_pos))
    background.blit(tree_surf, accurate_draw(tree_surf, Tree.abs_pos))
    background.blit(
        squirrel_surf,
        accurate_draw(squirrel_surf, (squirrel_location(), Squirrel.squirrel_y)),
    )

    # Blit-ing everything to the screen
    screen_surf.blit(pygame.transform.scale(background, bg_size), (0, 0))
    Game.clock.tick(Game.fps)  # I am not sure what this does
    pygame.display.flip()  # flips the blit on to the next frame, updates the frame
    # blit-ing, which is where you copy the pixels belonging to said object onto the destination object


def next_row(num_hop: int) -> list:
    row = [0 for _ in range(0, Island.length + 1)]

    for island_loc in range(0, Island.length + 1):
        if island_loc == 0:
            row[island_loc] += int(bool(Tree.nodes[num_hop - 1][island_loc + 1]))

        elif island_loc == Island.length:
            row[island_loc] += int(bool(Tree.nodes[num_hop - 1][island_loc - 1]))

        elif 0 < island_loc < Island.length:
            row[island_loc] += int(
                bool(
                    Tree.nodes[num_hop - 1][island_loc - 1]
                    + Tree.nodes[num_hop - 1][island_loc + 1]
                )
            )

    return row


def next_edge(num_hop: int) -> list:
    """returns a matrix with tuple at every island_loc, for previous set of lines, num_hops > 0"""
    edge = [0 for i in range(0, Island.length + 1)]

    for island_loc in range(0, Island.length + 1):
        if island_loc == 0:
            edge[island_loc] = [
                False,
                bool(Tree.nodes[num_hop - 1][island_loc + 1]),
            ]

        elif island_loc == Island.length:
            edge[island_loc] = [
                bool(Tree.nodes[num_hop - 1][island_loc - 1]),
                False,
            ]

        elif 0 < island_loc < Island.length:
            edge[island_loc] = [
                bool(Tree.nodes[num_hop - 1][island_loc - 1]),
                bool(Tree.nodes[num_hop - 1][island_loc + 1]),
            ]

    return edge


def get_cordinates(num_hop: int, island_loc: int) -> tuple[int, int]:
    padding_x = Tree.rel_padding * Tree.size[0]
    padding_y = Tree.rel_padding * Tree.size[1] * 1.75

    k = 3
    H_eff = Tree.size[1] - 2 * padding_y
    N = Squirrel.num_hops

    x = padding_x + island_loc * (
        (Tree.size[0] - 2 * padding_x) / Island.length
    )

    y = padding_y + H_eff * num_hop * (math.e ** (k * (num_hop / N - 1)) / N)

    return (x, y)


def draw_nodes(screen_surf: pygame.Surface, nodes: list) -> None:
    num_hops = len(nodes)
    for num_hop in range(0, num_hops):
        for island_loc in range(0, Island.length + 1):
            if nodes[num_hop][island_loc]:
                pygame.draw.circle(
                    screen_surf,
                    Tree.grid_color,
                    get_cordinates(num_hop, island_loc),
                    radius=1,
                )

    return


def draw_lines(screen_surf: pygame.Surface, nodes: list) -> None:
    num_hops = len(nodes)
    for num_hop in range(0, num_hops):
        for island_loc in range(0, Island.length + 1):
            line_info = Tree.edges[num_hop][island_loc]

            if line_info is not None:
                if line_info[0]:
                    # upper left node draws a line to current

                    # location of top left
                    start_pos = get_cordinates(num_hop - 1, island_loc - 1)

                    # location of top right
                    end_pos = get_cordinates(num_hop, island_loc)

                    pygame.draw.line(
                        screen_surf, Tree.grid_color, start_pos, end_pos, width=1
                    )

                if line_info[1]:
                    # upper right node draws a line to current location

                    # location of top right
                    start_pos = get_cordinates(num_hop - 1, island_loc + 1)

                    # location of top right
                    end_pos = get_cordinates(num_hop, island_loc)

                    pygame.draw.line(
                        screen_surf, Tree.grid_color, start_pos, end_pos, width=1
                    )

    return


def draw_choices(screen_surf: pygame.Surface, nodes: list) -> None:
    num_hops = len(nodes)
    for num_hop in range(0, num_hops):
        for island_loc in range(0, Island.length + 1):
            line_info = Tree.choices[num_hop][island_loc]

            if line_info is not None:
                if line_info[0]:
                    # upper left node draws a line to current

                    # location of top left
                    start_pos = get_cordinates(num_hop - 1, island_loc - 1)

                    # location of top right
                    end_pos = get_cordinates(num_hop, island_loc)

                    pygame.draw.line(
                        screen_surf, Tree.path_color, start_pos, end_pos, width=4
                    )

                if line_info[1]:
                    # upper right node draws a line to current location

                    # location of top right
                    start_pos = get_cordinates(num_hop - 1, island_loc + 1)

                    # location of top right
                    end_pos = get_cordinates(num_hop, island_loc)

                    pygame.draw.line(
                        screen_surf, Tree.path_color, start_pos, end_pos, width=4
                    )

    return
