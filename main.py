# -*- coding: utf-8 -*-

# This file calls variables defined in utility.py,
# and functions defined in utility.py
import sys, os, asyncio

import src.utility as utility

async def main():
    utility.init_game()
    
    # init_pos = utility.Squirrel.cur_pos
    bg_size = utility.screen_surf.get_size()

    (
        background,
        coin_surf,
        tree_surf,
        squirrel_surf,
        prob_slider,
        initpos_slider,
    ) = utility.background_load(utility.screen_surf)

    started = False
    dead = False
    bool_running = True
    while bool_running:
        # This is important for programs that want to share the system with other applications.
        # utility.pygame.event.pump()  # to allow utility.pygame to handle internal actions, calls the event queue
        # current_event = utility.pygame.event.wait()  # fetches one event

        time_delta = utility.Game.clock.tick(60) / 1000.0

        for current_event in utility.pygame.event.get():
            if current_event.type == utility.pygame.QUIT:
                # checking for quit
                bool_running = False
                return
            elif started and current_event.type == utility.pygame.KEYDOWN:
                if current_event.key == utility.pygame.K_ESCAPE:
                    print("ESCAPE")
                    started = False
                    dead = True
                    utility.pygame.mixer.music.stop()
                    utility.Squirrel.num_hops = 0
                    utility.Tree.nodes = [[0 for _ in range(0, utility.Island.length + 1)]]
                    utility.Tree.edges = [
                        [None for _ in range(0, utility.Island.length + 1)]
                    ]
                    utility.Tree.choices = [
                        [None for _ in range(0, utility.Island.length + 1)]
                    ]
                    utility.Tree.nodes[utility.Squirrel.num_hops][
                        utility.Squirrel.cur_pos
                    ] = 1

                    # return to initial screen

                    # utility.screen_surf.blit(utility.pygame.transform.scale(background, bg_size), (0, 0))
                    # background.blit(utility.Island.img.convert(), (0, 0))
                    prob_slider.kill()  # Assuming prob_slider is a utility.pygame_gui element, remove it from the UI
                    initpos_slider.kill()  # Remove other GUI elements similarly

                    (
                        background,
                        coin_surf,
                        tree_surf,
                        squirrel_surf,
                        prob_slider,
                        initpos_slider,
                    ) = utility.background_load(utility.screen_surf)

                    # bool_running = False
                    # return

            elif not started and current_event.type == utility.pygame.KEYDOWN:
                if current_event.key == utility.pygame.K_SPACE:
                    # If space-bar pressed
                    started = True
                    dead = False

                    utility.pygame.mixer.music.load(utility.Window.main_music, namehint="mp3")
                    # fades into 100 volume in 5ms
                    # utility.pygame.mixer.music.play(loops=-1, start=3.3, fade_ms=5)
                    utility.pygame.mixer.music.play(loops=-1, start=20, fade_ms=5)

            elif current_event.type == utility.pygame.VIDEORESIZE:
                # in the running frame it is updated later on:
                bg_size = current_event.dict["size"]
            if current_event.type == utility.pygame.USEREVENT:
                if current_event.user_type == utility.pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    # Update parameter values when a slider is moved
                    font = utility.pygame.font.Font(
                        utility.Window.fontpath, int(utility.Window.font_size / 2)
                    )

                    if current_event.ui_element == prob_slider:
                        value = current_event.ui_element.get_current_value()
                        print(f"Probability Slider moved to {value}")
                        utility.Squirrel.p_right = value

                        xpos1 = background.get_rect().center[0] + 120
                        xpos2 = background.get_rect().center[0] - 270
                        ypos = background.get_rect().center[1] + 65
                        utility.screen_surf.fill((0, 0, 0), (xpos1, ypos, 165, 13))
                        utility.screen_surf.fill((0, 0, 0), (xpos2, ypos, 155, 13))
                        text_surface_probr = font.render(
                            f"Prob(right) = {round(value, 2)}", True, (255, 255, 255)
                        )
                        text_surface_probl = font.render(
                            f"Prob(left) = {round(1-value, 2)}", True, (255, 255, 255)
                        )
                        utility.screen_surf.blit(text_surface_probr, (xpos1, ypos))
                        utility.screen_surf.blit(text_surface_probl, (xpos2, ypos))

                    if current_event.ui_element == initpos_slider:
                        value = current_event.ui_element.get_current_value()
                        print(f"InitPos Slider moved to {value}")
                        utility.Squirrel.init_pos = value
                        utility.Tree.nodes[utility.Squirrel.num_hops][
                            utility.Squirrel.cur_pos
                        ] = 0
                        utility.Squirrel.cur_pos = value
                        utility.Tree.nodes[utility.Squirrel.num_hops][
                            utility.Squirrel.cur_pos
                        ] = 1

                        font1 = utility.pygame.font.Font(
                            utility.Window.fontpath, int(utility.Window.font_size / 1.5)
                        )
                        xpos = background.get_rect().center[0] + 130
                        ypos = background.get_rect().center[1] + 110
                        utility.screen_surf.fill((0, 0, 0), (xpos, ypos, 25, 15))
                        text_surface_initpos = font1.render(
                            f"{utility.Squirrel.cur_pos}", True, (255, 255, 255)
                        )
                        utility.screen_surf.blit(text_surface_initpos, (xpos, ypos))

            utility.ui_manager.process_events(current_event)

        if not dead and started:
            # if game already started
            success, dead, started = utility.player(
                utility.screen_surf, background, coin_surf, tree_surf, squirrel_surf, bg_size
            )
            if success:
                # if everything inside player went OK
                utility.update_background(
                    utility.screen_surf,
                    background,
                    coin_surf,
                    tree_surf,
                    squirrel_surf,
                    bg_size,
                )

        # for UI elements => sliders buttons etc
        utility.ui_manager.update(time_delta)
        if dead or not started:
            utility.ui_manager.draw_ui(utility.screen_surf)
        utility.Game.clock.tick(utility.Game.fps)  # I am not sure what this does
        utility.pygame.display.flip()  # updating the frame
        
        await asyncio.sleep(0)


if __name__ == "__main__":

    sys.path.append(os.path.abspath("./src/"))

    # main()
    asyncio.run(main())
