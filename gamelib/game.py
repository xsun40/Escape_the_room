import pygame
import sys
import os
import random
import copy
import yaml
from os.path import join, dirname, realpath
from gamelib import const, data, build_room
from gamelib.objects import Picture

ClassType = {'picture': Picture, 'picture_1': Picture, 'picture_2': Picture,
                                                'picture_3': Picture}


class GameWindow(object):
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(45) / 300.0
        pygame.display.set_caption('Escape')
        self.real_screen = pygame.display.set_mode((2 * const.WIDTH, 2 * const.HEIGHT))

        try:
            pygame.mixer.init()
        except:
            pass
        self.intro()

    def intro(self):
        start = Intro(self).loop()
        if start:
            self.transition()

    def transition(self):
        move_on = Transition(self).loop("transition.wav", const.FADEOUT_TIME)
        if move_on:
            self.game()

    def game(self):
        Game(self).loop()


class Intro(object):
    def __init__(self, window):
        self.window = window
        self.real_screen = window.real_screen
        self.screen = pygame.surface.Surface((2 * const.WIDTH, 2 * const.HEIGHT))
        pygame.mixer.music.load(data.filepath('Audio', 'start.ogg'))
        pygame.mixer.music.set_volume(const.SOUND_VOLUME)
        pygame.mixer.music.play(-1)
        self.start = False

    def loop(self):

        wall_img = pygame.image.load(data.filepath("Cover", "wall.png"))
        door_img = pygame.image.load(data.filepath("Cover", "door.png"))
        floor_img = pygame.image.load(data.filepath("Cover", "floor.png"))
        startbar = pygame.transform.scale(pygame.image.load(data.filepath("Cover",
                                                    "startbutton.png")), (180, 90))
        name_img = pygame.transform.scale(pygame.image.load(data.filepath("Cover",
                                                    "name.png")), (800, 500))


        button = None


        pygame.transform.scale(self.screen, (2 * const.WIDTH, 2 * const.HEIGHT),
                               self.real_screen)
        pygame.display.update()

        while not self.start:

            build_room.build(self.screen, 2 * const.WIDTH, const.HEIGHT, door_img,
                                                                wall_img, floor_img)

            button = self.screen.blit(startbar, (265, 410))
            self.screen.blit(name_img, (-50, -100))


            pygame.transform.scale(self.screen, (2 * const.WIDTH, 2 * const.HEIGHT),
                                   self.real_screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if button:
                    self.on_start(event, button)

        return self.start

    def on_start(self, event, button):
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or \
           (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and \
            button.collidepoint(pygame.mouse.get_pos())):
                self.start = True
                startsound = pygame.mixer.Sound(data.filepath('Audio', 'start.ogg'))
                startsound.set_volume(const.SOUND_VOLUME / 3)
                startsound.play()
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            sys.exit()

class Transition(object):
    def __init__(self, window):
        self.window = window
        self.real_screen = window.real_screen
        self.screen = pygame.surface.Surface((2 * const.WIDTH, 2 * const.HEIGHT))
        self.move_on = False

    def loop(self, audio_file, fadeout):
        eye_img = pygame.transform.scale(pygame.image.load(data.filepath("Transitions",
                                                        'eye.png')), (300, 300))
        info_img = pygame.transform.scale(pygame.image.load(data.filepath("Transitions",
                                                        'info.png')), (550, 550))
        click = pygame.image.load(data.filepath("Transitions", "click.png"))


        self.screen.blit(eye_img, (200, 0))
        self.screen.blit(info_img, (100, 200))
        pygame.transform.scale(self.screen, (2 * const.WIDTH, 2 * const.HEIGHT),
                               self.real_screen)
        pygame.display.flip()

        pygame.mixer.music.fadeout(fadeout)
        pygame.mixer.music.load(data.filepath("Audio", audio_file))
        pygame.mixer.music.set_volume(const.SOUND_VOLUME / 8)
        pygame.mixer.music.play(-1)
        click_time = pygame.time.get_ticks()

        while not self.move_on:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

                    elif event.key == pygame.K_SPACE:
                        self.move_on = True

                elif event.type == pygame.QUIT:
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.move_on = True

            if self.move_on is True:
                pygame.mixer.music.stop()

            if pygame.time.get_ticks() >= click_time + const.FADEOUT_TIME:
                self.screen.blit(click, (340, 620))
            pygame.transform.scale(self.screen, (2 * const.WIDTH, 2 * const.HEIGHT),
                                   self.real_screen)
            pygame.display.flip()

        return self.move_on


class Game(object):
    def __init__(self, window):
        self.window = window
        self.real_screen = window.real_screen
        self.screen = pygame.surface.Surface((2 * const.WIDTH, 2 * const.HEIGHT))
        self.clock = window.clock
        self.dt = window.dt
        self.level_info =  yaml.load(open(data.filepath('Level', 'level_info.yaml')))
        self.len = len(self.level_info.keys())


    def loop(self):
        game_level = 1
        wall_list = build_room.choice_wall()

        while 1:



            if game_level <= self.len:
                pygame.mixer.music.load(data.filepath('Audio', 'theme.mp3'))
                pygame.mixer.music.set_volume(const.SOUND_VOLUME)
                pygame.mixer.music.play(-1)

                level_str = "level_" + str(game_level)
                level_info = self.level_info[level_str]
                wall_img = random.choice(wall_list)

                Level(self, level_info, game_level, wall_img).loop()

                game_level += 1

            elif game_level <= 0:
                pygame.mixer.music.load(data.filepath('Audio', 'lose.wav'))
                pygame.mixer.music.set_volume(const.SOUND_VOLUME / 2)
                pygame.mixer.music.play(-1)
                self.lose_game()

            elif game_level > self.len:
                pygame.mixer.music.load(data.filepath('Audio', 'win.wav'))
                pygame.mixer.music.set_volume(const.SOUND_VOLUME / 2)
                pygame.mixer.music.play(-1)
                self.win_game()

    def win_game(self):
        start_string = "YOU WON_00"
        directory = "End Sequence YOU WON"
        image_count = 215

        self.animate(start_string, directory, image_count)

        self.window.game()

    def lose_game(self):
        start_string = "YOU LOST_00"
        directory = "End Sequence YOU LOST"
        image_count = 215

        self.animate(start_string, directory, image_count)

        self.window.game()

    def animate(self, start_string, directory, image_count):
        restartbar = pygame.transform.scale(pygame.image.load(data.filepath("Cover",
                                                      "restart-01.png")), (118, 59))
        image_num = 0
        num_str = '{0:03}'.format(image_num)
        button = None
        image = pygame.image.load(data.filepath(directory,
                                            start_string + num_str + ".png"))

        pygame.transform.scale(self.screen, (2 * const.WIDTH, 2 * const.HEIGHT),
                               self.real_screen)
        pygame.display.update()

        last_time = pygame.time.get_ticks()
        restart = False
        while not restart:

            self.screen.blit(image, (0, 0))

            if image_num == image_count:
                button = self.screen.blit(restartbar, (500, 600))
            elif pygame.time.get_ticks() > last_time + 20:
                image_num += 1
                num_str = '{0:03}'.format(image_num)
                image = pygame.image.load(data.filepath(directory,
                                                start_string + num_str + ".png"))
                last_time = pygame.time.get_ticks()

            pygame.transform.scale(self.screen, (2 * const.WIDTH, 2 * const.HEIGHT),
                                   self.real_screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    exit(0)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.fadeout(const.FADEOUT_TIME)
                        sys.exit()

                if image_num == image_count and button:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            position = pygame.mouse.get_pos()
                            if button.collidepoint(position):
                                restart = True


class Level:
    def __init__(self, game, level_info, level_number, wall_img):
        self.level_number = level_number
        self.level_info = level_info
        self.wall_img = wall_img
        self.game = game
        self.window = game.window
        self.real_screen = game.real_screen
        self.screen = pygame.surface.Surface((2*const.WIDTH, 2*const.HEIGHT))
        self.dt = game.dt
        self.rect_dict = {}
        self.object_dict = {}
        self.result = False

    def room_setup(self):
        self.door_img = pygame.image.load(data.filepath("Room", "door.png"))
        floor_img = pygame.image.load(data.filepath("Room", "floor.png"))
        door, door_rect = build_room.build(self.screen, 2 * const.WIDTH, const.HEIGHT, self.door_img,
                                                        self.wall_img, floor_img)
        self.rect_dict['Door'] = door_rect
        self.object_dict['Door'] = door
        print(door)

    def object_setup(self):
        # add objects into the map_

        for thing in self.level_info.keys():
            img_name = self.level_info[thing]['name']
            width = self.level_info[thing]['width']
            height = self.level_info[thing]['height']
            screen_width = self.level_info[thing]['screen_width']
            screen_hight = self.level_info[thing]['screen_hight']
            trinket = ClassType[thing](width, height, screen_width, screen_hight,
                                                    thing, img_name, self.screen)
            self.rect_dict[thing] = trinket.button
            self.object_dict[thing] = trinket

    def loop(self):
        self.room_setup()
        self.object_setup()
        while 1:
            self.views()
            self.event_processor()
            if self.result:
                return self.result

    def views(self):
        if self.result:
            return
        pygame.transform.scale(self.screen,
                               (2 * const.WIDTH, 2 * const.HEIGHT),
                               self.real_screen)
        pygame.display.flip()

    def event_processor(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    sys.exit()

            for object in self.rect_dict.keys():
                if event.type == pygame.MOUSEBUTTONDOWN and \
                    self.rect_dict[object].collidepoint(pygame.mouse.get_pos()):
                    self.object_dict[object].start_game(self)
