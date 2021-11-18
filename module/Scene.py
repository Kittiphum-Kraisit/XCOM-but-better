import random
import pygame
import math
from module.button import draw_bg, draw_text, Button, draw_img
from module.function import *
# colors and fonts

# a function to choose characters for each player
def choose_character_in_pygame(all_character_list, screen, list_of_team, scene_number):
    font = pygame.font.SysFont('sfcartoonisthand', 18)
    bigger_font = pygame.font.SysFont('sfcartoonisthand', 28)
    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    black = (0, 0, 0)
    if scene_number == 2:
        color = red
    else:
        color = blue
    w, h = pygame.display.get_surface().get_size()
    Next_butt = Button(screen, w - w/10, h - h/10, 80, 30, white)
    whiteBox = pygame.Rect((0, 0), (w, h*7/10))
    scr = pygame.Surface((whiteBox.width, whiteBox.height))
    scr.fill(white)
    screen.blit(scr, (0, int(h/9)))


    draw_text(screen, "Team " + str(scene_number-1) + " Select Characters", pygame.font.SysFont('sfcartoonisthand', 32), black, 250, 10)
    for i in range(10):
        if all_character_list[i].available:
            all_character_list[i].draw_image()
        elif not all_character_list[i].available:
            # pygame.draw.rect(screen, color, all_character_list[i].rect, 2)
            box = pygame.image.load("pic/light.png")
            box = pygame.transform.scale(box, (all_character_list[i].rect.width + 20, all_character_list[i].rect.height + 20))
            draw_img(screen, box, (all_character_list[i].rect.x - 10, all_character_list[i].rect.y - 10))
            all_character_list[i].draw_image()
        all_character_list[i].draw_info()
    if len(list_of_team) == 5:
        # Draw button next

        if Next_butt.draw():
            for i in range(10):
                all_character_list[i].available = True
            print("Succ")
            return scene_number + 1

        draw_text(screen, "Next?", bigger_font, black, w - w/10, h - h/10)

    return scene_number


def choose_equipment(char_list, equipment_list, screen, control):
    font = pygame.font.SysFont('sfcartoonisthand', 18)
    bigger_font = pygame.font.SysFont('sfcartoonisthand', 28)
    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    black = (0, 0, 0)
    w, h = pygame.display.get_surface().get_size()
    Next_butt = Button(screen, w - w / 10, h - h / 10, 80, 30, (196, 196, 196))
    white_box = pygame.Rect((0, 0), (w, h * 4 / 10))
    scr = pygame.Surface((white_box.width, white_box.height))
    scr.fill(white)
    screen.blit(scr, (0, int(h / 2.8)))
    draw_text(screen, f"Team {char_list[control].Team}: Select equipment for {char_list[control].Name}", pygame.font.SysFont('sfcartoonisthand', 34), black, (w/2)-185, 10)
    im = pygame.image.load(f"pic/Full/{char_list[control].Name}.png")
    im = pygame.transform.scale(im, (math.floor(im.get_width() * 0.8),
                                math.floor(im.get_height() * 0.8)))
    screen.blit(im, ((w/2) - 200, (h/2) - 300))
    draw_text(screen, "Character stats:", bigger_font, black, (w / 2) - 80, (h / 2) - 300)
    draw_text(screen, f"HP: {char_list[control].Max_HP}", bigger_font, black, (w/2) - 80, (h/2) - 250)
    draw_text(screen, f"Mana: {char_list[control].Mana}", bigger_font, black, (w / 2) + 30, (h / 2) - 250)
    draw_text(screen, f"Attack: {char_list[control].Atk_damage}", bigger_font, black, (w / 2) - 80, (h / 2) - 200)
    draw_text(screen, f"Range: {char_list[control].Atk_range}", bigger_font, black, (w / 2) + 30, (h / 2) - 200)
    draw_text(screen, f"Stamina: {char_list[control].Stamina}", bigger_font, black, (w / 2) - 80, (h / 2) - 150)
    for i in range(8):
        if not equipment_list[i].clicked:
            screen.blit(equipment_list[i].img, (equipment_list[i].rect.x, equipment_list[i].rect.y))
        else:
            screen.blit(equipment_list[i].img, (equipment_list[i].rect.x, equipment_list[i].rect.y))
            # pygame.draw.rect(screen, red, equipment_list[i].rect, 2)
            # pygame.image.load("pic/equip_select.png")
            screen.blit(pygame.image.load("pic/equip_select.png"), (equipment_list[i].rect.x - 20, equipment_list[i].rect.y - 15))
            draw_text(screen, f"Weapon: {equipment_list[i].name}", bigger_font, black, (w/2) - 300, (h/2) + 200)
            draw_text(screen, f"Effect: {equipment_list[i].description}", bigger_font, black, (w / 2) - 300, (h / 2) + 230)
    if char_list[control].equip is not None:
        if Next_butt.draw():
            for j in range(8):
                equipment_list[j].clicked = False
            return control + 1
        draw_text(screen, "Next ->", bigger_font, red, w - w / 10, h - h / 10)
    return control



# a function to rotate an image in place (for the dice)
def blit_rotate(surf, image, topleft, scale, angle):
    resized_img = pygame.transform.scale(image, (math.floor(image.get_width() * scale),
                                                   math.floor(image.get_height() * scale)))
    rotated_image = pygame.transform.rotate(resized_img, angle)
    new_rect = rotated_image.get_rect(center=resized_img.get_rect(topleft=topleft).center)
    surf.blit(rotated_image, new_rect.topleft)
