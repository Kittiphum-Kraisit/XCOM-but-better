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
    catImg = pygame.transform.scale(catImg, (math.floor(sizeX -4.5), math.floor(sizeY -4.5)))
    DISPLAYSURF.blit(catImg, (x+3, y+3))
    return (x, y)

def movepic(position, cellsize, last_position):
    x, y = position
    x1, y1 = last_position
    sizeX, sizeY = cellsize
    black = pygame.image.load('pic/black.jpg')
    black = pygame.transform.scale(black, (math.floor(sizeX-4.5), math.floor(sizeY-4.5)))
    # print(last_position)
    DISPLAYSURF.blit(black, (x1+3, y1+3))
    catImg = pygame.image.load('pic/pop-cat.png')
    catImg = pygame.transform.scale(catImg, (math.floor(sizeX-4.5), math.floor(sizeY-4.5)))
    DISPLAYSURF.blit(catImg, (x+3, y+3))
    return (x+3, y+3)

def check_pressed(table , ract_obj, cellsize, old_position):
    mousex, mousey = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if click != (0, 0, 0):
        for i in range(len(ract_obj)):
            for l in range(len(ract_obj[i])):
                if ract_obj[i][l].collidepoint(mousex, mousey):
                    movepic((table[i][l].positionX, table[i][l].positionY), cellsize, old_position)
                    return (table[i][l].positionX, table[i][l].positionY)

def makeclass(positions, cellsize):
    obj = []
    for i in range(len(positions)):
        row = []
        for l in range(len(positions[i])):
            row.append(grid(positions[i][l], cellsize, (i, l)))
        obj.append(row)
    return obj

def makeract(table, cellsize):
    ractobj = []
    lenX, lenY = cellsize
    for i in range(len(table)):
        ractrow = []
        for l in range(len(table[i])):
            box = pygame.Rect(table[i][l].positionX, table[i][l].positionY, lenX, lenY)
            ractrow.append(box)
        ractobj.append(ractrow)
    return ractobj


if __name__ == "__main__":
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((720, 720))
    color2 = pygame.Color(255, 255, 255)  # White
    x = 1
    y = 4
    a, cellsize = drawtable(10, (120, 50), (620, 505))
    table_obj = makeclass(a, cellsize)
    ract_obj = makeract(table_obj, cellsize)
    oldposition = addpic(a[x][y], cellsize)

    while True:
        pygame.display.update()
        new_pos = check_pressed(table_obj, ract_obj, cellsize, oldposition)
        if new_pos != None:
            print(new_pos)
            oldposition = new_pos
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
