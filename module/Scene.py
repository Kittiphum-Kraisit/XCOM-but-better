import random
import pygame
from module.button import draw_bg, draw_text, Button
from module.function import *
# colors and fonts


def rot_center(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)
    return rotated_image, new_rect


def choose_character_in_pygame(all_character_list, screen, list_of_team, scene_number):
    #draw_bg(screen)
    font = pygame.font.SysFont('Times New Roman', 14)
    bigger_font = pygame.font.SysFont('Times New Roman', 24)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    Next_butt = Button(screen, 700, 475, 80, 30)
    draw_text(screen, "Player " + str(scene_number-1) + " Select character", font, white, 370, 0)
    for i in range(10):
        if all_character_list[i].available:
            all_character_list[i].draw_image()
        elif not all_character_list[i].available:
            pygame.draw.rect(screen, (196, 196, 196, 25), all_character_list[i].rect)
            all_character_list[i].draw_image()
        all_character_list[i].draw_info()
    if len(list_of_team) == 5:
        # Draw button next

        if Next_butt.draw():
            for i in range(10):
                all_character_list[i].available = True
            print("Succ")
            return scene_number + 1

        draw_text(screen, "Next ->", bigger_font, red, 700, 475)

    return scene_number

# draw_bg()
# draw_text("Player 1 Select character", font, white, 370, 0)
# for i in range(10):
#     if c[i].available:
#         c[i].draw_image()
#     elif not c[i].available:
#         pygame.draw.rect(screen, (196, 196, 196, 25), c[i].rect)
#         c[i].draw_image()
#     c[i].draw_info()
# if len(cc_team1) == 5:
#     #Draw button next
#     draw_text("Next ->", bigger_font, red, 700, 475)
#     if Next_butt.draw():
#         for i in range(10):
#             c[i].available = True
#         print("Succ")
#         scene = 3

# draw_bg(screen, background_img)
# draw_text(screen, "Player 2 Select character", font, white, 370, 0)
# for i in range(10):
#     if c[i].available:
#         c[i].draw_image()
#     elif not c[i].available:
#         pygame.draw.rect(screen, (196, 196, 196, 25), c[i].rect)
#         c[i].draw_image()
#     c[i].draw_info()
#     if len(cc_team2) == 5:
#     # Draw button next
#         draw_text(screen, "Next ->", bigger_font, red, 700, 475)
#         if Next_butt.draw():
#             print("Succ")
#             scene = 4
