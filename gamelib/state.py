import pygame
import time
from random import choice
import random
import numpy
import yaml

try:
    import const
    import data
except:
    from gamelib import const, data


class State:

    def __init__(self, level, state_name):
        self.level = level
        self.level_str = 'level_' + str(level.level_number)
        self.real_screen = level.real_screen
        self.state_name = state_name
        self.information = yaml.load(open(data.filepath("configs", "state.yaml")))
        self.screen = pygame.surface.Surface((2 * const.WIDTH, 2 * const.HEIGHT))
        self.exit_animation = False
        pygame.mixer.music.stop()
        pygame.mixer.music.load(data.filepath('Audio', 'mini_2.mp3'))
        pygame.mixer.music.set_volume(const.SOUND_VOLUME)
        pygame.mixer.music.play(-1)

    def run_win_loss(self, pass_fail):

        vic_image = pygame.image.load(open(data.filepath("Cover", pass_fail + '.png')))

        last_time = pygame.time.get_ticks()

        while 1:

            if pygame.time.get_ticks() > last_time + 1000:
                return
            else:
                pygame.display.flip()
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(vic_image, (200, 250))
                pygame.transform.scale(self.screen, (2 * const.WIDTH, 2 * const.HEIGHT),
                                       self.real_screen)
                pygame.display.flip()



    def animation(self, ent_exit, image_num):
        num_str = '{0:03}'.format(image_num)
        last_time = pygame.time.get_ticks()
        self.screen.blit(self.background, (0, 0))
        pygame.transform.scale(self.screen, (2 * const.WIDTH, 2 * const.HEIGHT),
                               self.real_screen)
        pygame.display.flip()

        while not self.exit_animation:


            if ent_exit == "enter":
                image_num += 1
            if ent_exit == "exit":
                image_num -= 1
            num_str = '{0:03}'.format(image_num)
            self.background = pygame.image.load(data.filepath(self.level.directory,
                                    self.level.bg_color + " map_00" + num_str + ".png"))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            if image_num == 71 or image_num == 0:
                self.exit_animation = True

            self.screen.blit(self.background, (0, 0))
            pygame.transform.scale(self.screen, (2 * const.WIDTH, 2 * const.HEIGHT),
                                   self.real_screen)
            pygame.display.flip()


    def run_state(self):

        return_value = None


        if self.state_name == 'door':
            self.level.result = self.try_out_room()
        if self.state_name in ['picture', 'picture_1', 'picture_2', 'picture_3']:
            self.run_picture_state()

        #self.animation("exit", 71)

        pygame.mixer.music.stop()
        pygame.mixer.music.load(data.filepath('Audio', 'theme.mp3'))
        pygame.mixer.music.set_volume(const.SOUND_VOLUME)
        pygame.mixer.music.play(-1)

        return return_value

    def run_picture_state(self):
        self.screen = pygame.surface.Surface(
            (2 * const.WIDTH, 2 * const.HEIGHT))
        self.screen.fill(0)
        img_info = self.information[self.level_str][self.state_name]
        img = pygame.transform.scale(pygame.image.load(data.filepath("State",
                    img_info['name'])), (img_info['width'], img_info['hight']))
        self.screen.blit(img, (img_info['screen_width'], img_info['screen_hight']))
        pygame.transform.scale(self.screen,
                               (2 * const.WIDTH, 2 * const.HEIGHT),
                               self.real_screen)

        while True:

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return True
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.fadeout(const.FADEOUT_TIME)
                        sys.exit()

    def try_out_room(self):
        self.screen =  pygame.surface.Surface(
            (2 * const.WIDTH, 2 * const.HEIGHT))
        door_image = {}
        pass_button = None
        fail_button = None
        turns = 0
        for num in range(0, 10):
            door_image[num] = pygame.transform.scale(pygame.image.load(
                data.filepath("Game", "num-" + str(num) +".png")), (90,50))
        img_info = self.information[self.level_str][self.state_name]
        door_lock_img = pygame.transform.scale(pygame.image.load(data.filepath(
                    "State", "door.png")), (img_info['width'], img_info['hight']))
        pass_img = pygame.transform.scale(pygame.image.load(data.filepath(
                    "State", "pass.png")), (100, 100))
        fail_img = pygame.transform.scale(pygame.image.load(data.filepath(
                    "State", "fail.png")), (100, 100))
        return_img = pygame.transform.scale(pygame.image.load(data.filepath(
                    "State", "return.png")), (300, 300))
        password_len = len(str(img_info['password']))
        button = {}
        correction = ''
        result = False

        while not result:
            self.screen.fill(0)
            self.screen.blit(door_lock_img, (img_info['screen_width'],
                                                        img_info['screen_hight']))
            return_button = self.screen.blit(return_img, (400, 500))
            button[0] = self.screen.blit(door_image[0], [300, 500])
            for num in range (0,3):
                for y in range (0,3):
                    button[y + 1 + num * 3] = self.screen.blit(door_image[y + 1 +  num * 3],
                                                              [y*100+200, num*100+200])

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if turns < password_len:
                        position = pygame.mouse.get_pos()
                        for key, butt in button.items():
                            if butt.collidepoint(position):
                                correction += str(key)
                                turns += 1

                    if return_button.collidepoint(pygame.mouse.get_pos()) and \
                                                        not pass_button:
                        return False

                    if fail_button:
                        turns = 0
                        correction = ''
                        fail_button = None

                    if pass_button:
                        turns = 0
                        correction = ''
                        pass_button = None
                        return True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.fadeout(const.FADEOUT_TIME)
                        sys.exit()


                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    exit(0)




            if turns >= password_len:
                if self.check_out(correction, img_info['password']):
                    pass_button = self.screen.blit(pass_img, (100, 100))
                else:
                    fail_button = self.screen.blit(fail_img, (100, 100))





            pygame.transform.scale(self.screen,
                                   (2 * const.WIDTH, 2 * const.HEIGHT),
                                   self.real_screen)
            pygame.display.flip()

    def check_out(self, correction, password):
        if str(correction) == str(password):
            return True
        else:
            return False
