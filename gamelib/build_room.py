import pygame
from gamelib import data
from gamelib.objects import Door

def build(screen, width, height, door_image, wall_image, floor_image):

    door_image = pygame.transform.scale(door_image, (150, 300))
    floor_image = pygame.transform.scale(floor_image, (width, height))

    height = height * 2

    for x in range(int(width/wall_image.get_width())+2):
            for y in range(int(height/wall_image.get_height())+2):
                screen.blit(wall_image,(x*100,y*100))

    screen.blit(floor_image,(0,500))
    door = Door(door_image, screen)
    return door, door.button



def choice_wall():
    wall_img = []
    for i in range(10):
        wall_img += [pygame.transform.scale(pygame.image.load(data.filepath("Room",
                                            "wall" + str(i) + ".png")), (100, 100))]
    return wall_img
