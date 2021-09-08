import pygame
from pygame.locals import *
import sys
import math

class grid():
    def __init__(self, position, dimension, index):
        indX, indY = index
        posx, posy = position
        diX, diY = dimension
        self.positionX = posx
        self.positionY = posy
        self.dimensionX = diX
        self.dimensionY = diY
        self.rangeX = posx + diX
        self.rangeY = posy + diY
        self.indexX = indX
        self.indexY = indY

def drawtable(table, top_left, bottom_right):
    big_table = []
    row = []
    tl_x, tl_y = top_left
    br_x, br_y = bottom_right
    for i in range(table+1):
        pygame.draw.line(DISPLAYSURF, color2, (tl_x, tl_y + (i * (abs(tl_y-br_y)/table))), (br_x, tl_y + (i * (abs(tl_y-br_y)/table))), 5)
        pygame.draw.line(DISPLAYSURF, color2, (tl_x + (i * (abs(tl_x-br_x)/table)), tl_y), (tl_x + (i * (abs(tl_x-br_x)/table)), br_y), 5)
    for i in range(table):
        for l in range(table):
            row.append([tl_x + (l * (abs(tl_x-br_x)/table)), tl_y + (i * (abs(tl_y-br_y)/table))])
        big_table.append(row)
        row = []
    return big_table, (abs(tl_x-br_x)/table, abs(tl_y-br_y)/table)

def addpic(position, cellsize):
    x, y = position
    sizeX, sizeY = cellsize
    catImg = pygame.image.load('pic/pop-cat.png')
    catImg = pygame.transform.scale(catImg, (math.floor(sizeX), math.floor(sizeY)))
    DISPLAYSURF.blit(catImg, (x, y))

def check_pressed():
    mousex, mousey = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if click != (0, 0, 0):
        print(mousex)
        print(mousey)

def makeclass(positions, cellsize):
    obj = []
    obj.append(grid())

pygame.init()
DISPLAYSURF = pygame.display.set_mode((720, 720))
color2 = pygame.Color(255, 255, 255)   # White

while True:
    pygame.display.update()
    x = 1
    y = 4
    a, cellsize = drawtable(10, (120, 50), (620, 505))
    addpic(a[x][y], cellsize)
    check_pressed()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
