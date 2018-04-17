import pygame
import random
try:
    from gamelib import data, const, state
except:
    import data
    import state
from math import sqrt

class Picture():
    def __init__(self, width, height, screen_width, screen_hight, name, img_name,
                                                                        screen):
        self.name = name
        self.image = pygame.transform.scale(pygame.image.load(data.filepath(
                              "Level", img_name)), (width, height))
        self.button = screen.blit(self.image, (screen_width, screen_hight))

    def start_game(self, level):
        state.State(level, self.name).run_state()

class Door():
    def __init__(self, image, screen):
        self.image = image
        self.button = screen.blit(image,(280,200))

    def start_game(self, level):
        print(level)
        result = state.State(level, 'door').run_state()
        if result:
            return
