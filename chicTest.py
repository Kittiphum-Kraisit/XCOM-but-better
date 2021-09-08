import pygame
from pygame.locals import *
import sys
import math

class grid():
    def __init__(self, position, dimension, index):
        indX, indY = index
        posx, posy = position
        diX, diY = dimension
        self.positionX = math.floor(posx)
        self.positionY = math.floor(posy)
        self.dimensionX = math.floor(diX) + math.floor(posx)
        self.dimensionY = math.floor(diY) + math.floor(posy)
        self.rangeX = math.floor(posx + diX)
        self.rangeY = math.floor(posy + diY)
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

def check_pressed(table):
    mousex, mousey = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if click != (0, 0, 0):
        # print(mousex)
        # print(mousey)
        # print(str(table[0][0].positionX) + " : " + str(table[0][0].dimensionX))
        # print(str(table[0][0].positionY) + " : " + str(table[0][0].dimensionY))
        for i in range(len(table)):
            for l in range(len(table[i])):
                if table[i][l].positionX < mousex < table[i][l].dimensionX:
                    if table[i][l].positionY < mousey < table[i][l].dimensionY:
                        print(table[i][l].indexX)
                        print(table[i][l].indexY)

def makeclass(positions, cellsize):
    obj = []
    for i in range(len(positions)):
        row = []
        for l in range(len(positions[i])):
            row.append(grid(positions[i][l], cellsize, (i, l)))
        obj.append(row)
    return obj

pygame.init()
DISPLAYSURF = pygame.display.set_mode((720, 720))
color2 = pygame.Color(255, 255, 255)   # White
x = 1
y = 4
a, cellsize = drawtable(10, (120, 50), (620, 505))
table_obj = makeclass(a, cellsize)

while True:
    pygame.display.update()
    addpic(a[x][y], cellsize)
    check_pressed(table_obj)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
