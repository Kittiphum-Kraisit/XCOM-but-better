import pygame
import random
from module.button import Button, draw_text, draw_bg
from module.Character import choose_char, obj_char_create
from module.Scene import choose_character_in_pygame
from module.function import *


pygame.init()
clock = pygame.time.Clock()
fps = 60

# screen setting
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Game')

# UI
font = pygame.font.SysFont('Times New Roman', 14)
bigger_font = pygame.font.SysFont('Times New Roman', 24)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)


# images
background_img = pygame.image.load('pic/black.jpg').convert_alpha()


# pygame object
class char_card:
    def __init__(self, x, y, id):
        self.id = id
        img = pygame.image.load('pic/cat.png')
        self.image = pygame.transform.scale(img, (img.get_width()//3, img.get_height()//3))
        self.x = x
        self.y = y
        self.available = True
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw_image(self):
        screen.blit(self.image, self.rect)

    def draw_info(self):
        info = obj_char_create(str(self.id), 0)
        draw_text(screen, info.Name, font, white, self.x - 50, self.y + 40)
        draw_text(screen, f'HP: {str(info.HP)}', font, white, self.x - 50, self.y + 60)
        draw_text(screen, f'Mana: {str(info.Mana)}', font, white, self.x - 50, self.y + 80)
        draw_text(screen, f'Skill: {info.Skill_name}', font, white, self.x - 50, self.y + 100)
        draw_text(screen, f'AtkDmg: {str(info.Atk_damage)}', font, white, self.x - 50, self.y + 120)


# game parameters
t1, t2 = [], []
init1, init2 = [], []
queue = []
c = []
cc_team1 = []
cc_team2 = []

for i in range(0, 5):
    c.append(char_card(90 + (150*i), 100, i))
for i in range(5, 10):
    c.append(char_card(90 + (150*(i-5)), 300, i))

run = True
scene = 1
while run:
    screen.fill(0)
    if scene == 1:
        draw_bg(screen, background_img)
        draw_text(screen, "Welcome", font, white, 350, 200)
        draw_text(screen, "Click to start", font, white, 350, 250)
    elif scene == 2:
        scene = choose_character_in_pygame(c, screen, cc_team1, 2)
    elif scene == 3:
        scene = choose_character_in_pygame(c, screen, cc_team2, 3)

    elif scene == 4:
        print('\nTeam 1: ', end='')
        for i in range(0, 5):
            print(char_info1[i].Name, end=' ')
        print('\nTeam 2: ', end='')
        for i in range(0, 5):
            print(char_info2[i].Name, end=' ')
        scene = 5
    elif scene == 5:
        scene = 6
    elif scene == 6:
        init1.clear()
        init2.clear()
        queue.clear()
        for i in range(0, len(char_info1)):
            init1.append(random.randint(0, 100))
            print(char_info1[i].Name + ":" + str(init1[-1]))

        print('\nTeam2 roll')
        for i in range(0, len(char_info2)):
            init2.append(random.randint(0, 100))
            print(char_info2[i].Name + ":" + str(init2[-1]))

        for i in range(0, len(char_info1)):
            char_info1[i].Mana += 10

            if char_info1[i].Name == "Flagellants":
                char_info1[i].Speed = 30 + 10 * (5 - len(char_info1))

            if char_info1[i].Invisible != 0:
                char_info1[i].Invisible -= 1

            char_info1[i].set_currspeed(init1[i])
            queue.append(char_info1[i])

        for i in range(0, len(char_info2)):
            char_info2[i].Mana += 10

            if char_info2[i].Name == "Flagellants":
                char_info2[i].Speed = 30 + 10 * (5 - len(char_info2))

            if char_info2[i].Invisible != 0:
                char_info2[i].Invisible -= 1

            char_info2[i].set_currspeed(init2[i])
            queue.append(char_info2[i])

        # sort
        queue.sort(key=lambda x: x.CurrSpeed, reverse=True)
        reset_stamina(queue)
        print(queue)
        scene = 7

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if scene == 1:
                scene = 2
            if scene == 2:
                pos = pygame.mouse.get_pos()
                for i in range(0, 10):
                    if c[i].rect.collidepoint(pos):
                        if c[i].available and (len(cc_team1) < 5):
                            cc_team1.append(c[i].id)
                            c[i].available = not c[i].available
                        elif not c[i].available and c[i].id in cc_team1:
                            cc_team1.remove(c[i].id)
                            c[i].available = not c[i].available
                        char_info1 = choose_char(cc_team1, 1)
                        print(char_info1)

            if scene == 3:
                pos = pygame.mouse.get_pos()
                for i in range(0, 10):
                    if c[i].rect.collidepoint(pos):
                        if c[i].available and (len(cc_team2) < 5):
                            cc_team2.append(c[i].id)
                            c[i].available = not c[i].available
                        elif not c[i].available and c[i].id in cc_team2:
                            cc_team2.remove(c[i].id)
                            c[i].available = not c[i].available
                        char_info2 = choose_char(cc_team2, 2)
                        print(char_info2)
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()

