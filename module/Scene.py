import random
import pygame
import math
from module.button import draw_bg, draw_text, Button, draw_img
from module.function import *
# colors and fonts

# a function to choose characters for each player
def choose_character_in_pygame(all_character_list, screen, list_of_team, scene_number):
    font = pygame.font.SysFont('Times New Roman', 14)
    bigger_font = pygame.font.SysFont('Times New Roman', 24)
    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    black = (0, 0, 0)
    if scene_number == 2:
        color = red
    else:
        color = blue
    w,h = pygame.display.get_surface().get_size()
    Next_butt = Button(screen, w - w/10, h - h/10, 80, 30,(196,196,196))
    draw_text(screen, "Player " + str(scene_number-1) + " Select character", font, black, 370, 0)
    for i in range(10):
        if all_character_list[i].available:
            all_character_list[i].draw_image()
        elif not all_character_list[i].available:
            # pygame.draw.rect(screen, color, all_character_list[i].rect, 2)
            draw_img(screen, pygame.image.load("pic/Character_Select.png"),all_character_list[i].rect)
            all_character_list[i].draw_image()
        all_character_list[i].draw_info()
    if len(list_of_team) == 5:
        # Draw button next

        if Next_butt.draw():
            for i in range(10):
                all_character_list[i].available = True
            print("Succ")
            return scene_number + 1

        draw_text(screen, "Next ->", bigger_font, red, w - w/10, h - h/10)

    return scene_number

# a function to rotate an image in place (for the dice)
def blit_rotate(surf, image, topleft, scale, angle):
    resized_img = pygame.transform.scale(image, (math.floor(image.get_width() * scale),
                                                   math.floor(image.get_height() * scale)))
    rotated_image = pygame.transform.rotate(resized_img, angle)
    new_rect = rotated_image.get_rect(center=resized_img.get_rect(topleft=topleft).center)
    surf.blit(rotated_image, new_rect.topleft)
