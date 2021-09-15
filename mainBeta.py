import random
import pygame
from module.button import Button
from module.Character import choose_char, obj_char_create
from module.function import *


pygame.init()
clock = pygame.time.Clock()
fps = 60

#screen setting
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Game')

#UI
font = pygame.font.SysFont('Times New Roman', 14)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

#images
background_img = pygame.image.load('pic/black.jpg').convert_alpha()

#pygame object
class char_card:
    def __init__(self, x, y, id):
        self.id = id;
        img = pygame.image.load('pic/cat.png')
        self.image = pygame.transform.scale(img, (img.get_width()//3, img.get_height()//3))
        self.x = x
        self.y = y
        self.available = True
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.image, self.rect)
        info = obj_char_create(str(self.id),0)
        draw_text(info.Name, font, white, self.x - 50, self.y+40)
        draw_text(f'HP: {str(info.HP)}', font, white, self.x - 50, self.y + 60)
        draw_text(f'Mana: {str(info.Mana)}', font, white, self.x - 50, self.y + 80)
        draw_text(f'Skill: {info.Skill_name}', font, white, self.x - 50, self.y + 100)
        draw_text(f'AtkDmg{str(info.Atk_damage)}', font, white, self.x - 50, self.y + 120)



#pygame functions
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col, (0,0,0))
    screen.blit(img, (x, y))

def draw_bg():
    screen.blit(background_img, (0, 0))

c = []
for i in range (0,5):
     c.append(char_card(90 + (150*i), 100, i))

for i in range (5,10):
     c.append(char_card(90 + (150*(i-5)), 300, i))


run = True
scene = 1
while run:
    screen.fill(0)

    if scene == 1:
        draw_bg()
        draw_text("Welcome", font, white, 350, 200)
        draw_text("Click to start", font, white, 350, 250)
    elif scene == 2:
        draw_bg()
        for i in range(10):
            c[i].draw()
        draw_text("Select character", font, white, 370, 0)


    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            scene = 2
        if event.type == pygame.QUIT:
            run = False


    pygame.display.update()

pygame.quit()

