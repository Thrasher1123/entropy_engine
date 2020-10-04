import typing
import pygame as py
import pygame as keys  # so you can access the keys from entropy_engine
import global_data
import curser
import renderer
import fail_system
import unit_tests
import time
import time_controller
import utilities
import colour
import scene_controller

# ================================================================================================
# |-------------------------------------={ Joseph Coppin }=-------------------------------------|
# ================================================================================================
#
#                                  Project Name : Entropy Engine
#
#                                     File Name : entropy_engine.py
#
# ------------------------------------------------------------------------------------------------
#
#      Controls the game engine. This is the file that the user accesses to use the engine.
#
# ------------------------------------------------------------------------------------------------
#
#   init - initialises the screen and game engine
#   __tick - ticks the game engine forward one tick
#   run_game - called at the end of the user file, runs the game
#   end - prematurely ends the game, eg if they click a quit button
#   create_sprite - returns and created a empty Sprite.
#   create_ui_element - returns and creates a empty ui element
#   get_screen_size - returns the dimensions of the screen in pixels by pixels
#   force_screen_update - forces the screen to refresh mid-tick
#   get_center - returns the coordinates of the center of the screen
#
# ================================================================================================


def init(screen_size):
    new_size = utilities.check_vector2(screen_size, int, 'entropy_engine.init(screen_size)')
    if new_size is not False:
        renderer.init_screen(new_size)

        unit_tests.Tests().run_all_tests()


def __tick():
    # for finding the current fps
    start_time = time.time()

    # checks if the window should close, because you have pressed the close button
    for event in py.event.get():
        if event.type == py.QUIT:
            end()

    # controls the processing of sprites and ui elements
    current_scene = scene_controller.scene_manager.scenes[scene_controller.scene_manager.active_scene]
    current_scene.ui_controller.run_ui()
    current_scene.sprite_controller.update_sprites()

    # controls rendering of UI and sprites (keep this order)
    renderer.render_background()
    renderer.render_sprites()
    renderer.render_ui()
    renderer.render_cursor()
    renderer.tick_window()

    if global_data.typing_sticky_keys > 0:
        global_data.typing_sticky_keys -= 1

    curser.update_mouse_clicked()

    time_controller.update_fps(start_time)
    time_controller.tick += 1


def run_game():
    current_scene = scene_controller.scene_manager.scenes[scene_controller.scene_manager.active_scene]
    current_scene.sprite_controller.init_sprites()
    current_scene.ui_controller.init_ui()

    while global_data.go:
        __tick()

    py.quit()
    quit()


def end():
    global_data.go = False


def get_screen_size():
    return renderer.mid[0] * 2, renderer.mid[1] * 2


def force_screen_update():
    py.display.update()


def get_center():
    return renderer.mid


def chaos():
    return typing.chaos_14x16


def retro():
    return typing.retro_8x10


def keypress(key):
    try:
        if py.key.get_pressed()[key]:
            return True
        return False
    except IndexError:
        fail_system.error(str(key) + ' is not a valid key input.', 'entropy_engine.keypress(key)')


def get_mouse_position():
    return py.mouse.get_pos()


def get_mouse_down():
    return py.mouse.get_pressed()


def set_window_title(message):
    new_message = utilities.check_input(message, str, (
        'Window title must be set to type str, not ' + str(type(message)) +
        '.', 'entropy_engine.set_window_title(message)'))
    if new_message is not False:
        global_data.window_title = new_message


def file_to_image(file_name):
    new_file_name = utilities.check_input(file_name, str, (
        'File name cannot be ' + str(file_name) + '. Must be of type str.',
        'entropy_engine.file_to_image(file_name)'))
    if new_file_name is not False:
        try:
            return py.image.load(str(new_file_name))
        except:
            fail_system.error("File '" + str(new_file_name) + "' could not be found",
                              'entropy_engine.file_to_image()')


def get_current_fps():
    return time_controller.current_fps


def get_target_fps():
    return renderer.run_FPS


def set_target_fps(fps):
    new_fps = utilities.check_input(fps, int, (
        'target FPS cannot be get to type ' + str(type(fps)) + '. Must be of type int.',
        'entropy_engine.set_target_fps(fps)'))
    if new_fps is not False:
        try:
            new_fps = int(new_fps)
            if 0 < new_fps < 10000:
                renderer.run_FPS = new_fps
            else:
                fail_system.error('FPS cannot be set to ' + str(new_fps),
                                  'entropy_engine.set_target_fps() (6)')
        except:
            fail_system.error('FPS cannot be set to ' + str(new_fps),
                              'entropy_engine.set_target_fps() (8)')


def get_current_tick():
    return time_controller.tick


def new_colour(_colour):
    new_colour = utilities.check_vector(_colour, int, 'entropy_engine.new_colour(colour)')
    if new_colour is not False:
        if len(new_colour) == 3:
            good = True
            for i in range(3):
                if 0 > new_colour[i] > 255:
                    good = False

            if good:
                return colour.Colour(new_colour)

    fail_system.error(
        f'Cannot create colour {new_colour}. Make sure there are three elements between 0 and 255.',
        'entropy_engine.new_colour(_colour)')
    return False


def scene_manager():
    return scene_controller.scene_manager


def create_sprite(name):
    return scene_controller.scene_manager.current_scene().create_sprite(name)


def create_ui_element(name):
    return scene_controller.scene_manager.current_scene().create_ui_element(name)
