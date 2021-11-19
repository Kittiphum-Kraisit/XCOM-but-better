import pygame
from pygame.locals import *
from module.function import Bomb
import sys
import math


class Grid:
    # create grid class object
    def __init__(self, position, dimension, index):
        indX, indY = index
        posx, posy = position
        diX, diY = dimension
        self.positionX = math.floor(posx)
        self.positionY = math.floor(posy)
        self.dimensionX = math.floor(diX)
        self.dimensionY = math.floor(diY)
        self.rangeX = math.floor(posx + diX)
        self.rangeY = math.floor(posy + diY)
        self.indexX = indX
        self.indexY = indY
        self.rect = pygame.Rect(self.positionX, self.positionY, diX, diY)
        self.resident = None
        self.checked = None
        self.obstacle = False
        self.trap = None

    def drawcell(self, surface, color=(222, 255, 195)):
        # draw a cell on surface
        color_2 = pygame.Color(0, 0, 0)
        pygame.draw.line(surface, color_2, (self.positionX, self.positionY), (self.rangeX, self.positionY), 1)
        pygame.draw.line(surface, color_2, (self.positionX, self.positionY), (self.positionX, self.rangeY), 1)
        pygame.draw.line(surface, color_2, (self.rangeX, self.positionY), (self.rangeX, self.rangeY), 1)
        pygame.draw.line(surface, color_2, (self.positionX, self.rangeY), (self.rangeX, self.rangeY), 1)
        self.highlight(surface, color)

    def addpic(self, picname, surface, index, team):
        # create new image on input position parameter (a tuple of (x,y) pixel position of where you want new image
        # to be, tuple contain (width, and height) of one cell)
        x, y = index
        catImg = picname
        catImg = pygame.transform.scale(catImg, (math.floor(self.dimensionX - 4.5), math.floor(self.dimensionY - 4.5)))
        if team == 1:
            sc = pygame.Surface((math.floor(self.rect.width - 4.5), math.floor(self.rect.height - 4.5)))
            sc.fill((255, 0, 0))
            surface.blit(sc, (self.positionX + 3, self.positionY + 3))
        if team == 2:
            sc = pygame.Surface((math.floor(self.rect.width - 4.5), math.floor(self.rect.height - 4.5)))
            sc.fill((0, 0, 255))
            surface.blit(sc, (self.positionX + 3, self.positionY + 3))
        surface.blit(catImg, (self.positionX + 3, self.positionY + 3))
        return x, y

    def movepic(self, position, cell_size, last_position, surface):
        # create new image on input position and create black layer over last image parameter (a tuple of (x,
        # y) pixel position of where you want new image to be, tuple contain (width, and height) of one cell-
        x, y = position
        x1, y1 = last_position
        sizeX, sizeY = cell_size
        black = pygame.image.load('../pic/black.jpg')
        black = pygame.transform.scale(black, (math.floor(sizeX - 4.5), math.floor(sizeY - 4.5)))
        surface.blit(black, (x1 + 3, y1 + 3))
        catImg = pygame.image.load('../pic/pop-cat.png')
        catImg = pygame.transform.scale(catImg, (math.floor(sizeX - 4.5), math.floor(sizeY - 4.5)))
        surface.blit(catImg, (x + 3, y + 3))
        return x + 3, y + 3

    def highlight(self, surface, color):
        sc = pygame.Surface((math.floor(self.rect.width - 4.5), math.floor(self.rect.height - 4.5)))
        sc.fill(color)
        surface.blit(sc, (self.positionX + 3, self.positionY + 3))


def fillflush(x, y, ranges, table, surface, arr):
    # x, y = position
    if table[y][x].resident is None:
        table[y][x].highlight(surface, (0, 204, 0, 50))
        arr.append((y, x))

    if isinstance(table[y][x].resident, Bomb):
        table[y][x].highlight(surface, (128, 0, 128, 50))
        arr.append((y, x))
        return y, x

    if ranges <= 0:
        return y, x

    # if x + 1 < len(table) and y + 1 < len(table[0]) and x - 1 > 0 and y - 1 > 0:
    if (y + 1 < len(table)) and (table[y + 1][x].resident is None or isinstance(table[y + 1][x].resident, Bomb)):
        fillflush(x, y + 1, ranges - 1, table, surface, arr)
    if (x + 1 < len(table[0])) and (table[y][x + 1].resident is None or isinstance(table[y][x + 1].resident, Bomb)):
        fillflush(x + 1, y, ranges - 1, table, surface, arr)
    if (y - 1 >= 0) and (table[y - 1][x].resident is None or isinstance(table[y - 1][x].resident, Bomb)):
        fillflush(x, y - 1, ranges - 1, table, surface, arr)
    if (x - 1 >= 0) and (table[y][x - 1].resident is None or isinstance(table[y][x - 1].resident, Bomb)):
        fillflush(x - 1, y, ranges - 1, table, surface, arr)
    return arr


def setrange(char, table, surface, action_type):
    if action_type == "move":
        for y in range(len(table)):
            for x in range(len(table[y])):
                ran = abs(char.Position[0] - table[y][x].indexX) + abs(char.Position[1] - table[y][x].indexY)
                if ran <= char.Stamina and table[x][y].resident is None:
                    table[x][y].highlight(surface, (165, 250, 162))  # prev. (128, 0, 0, 50)

    elif action_type == "attack":
        for y in range(len(table)):
            for x in range(len(table[y])):
                ran = abs(char.Position[0] - table[y][x].indexX) + abs(char.Position[1] - table[y][x].indexY)
                if ran <= char.Atk_range and table[x][y].resident is None:
                    table[x][y].highlight(surface, (255, 173, 173))  # prev. (255, 192, 203, 50)
    elif action_type == "skill":
        for y in range(len(table)):
            for x in range(len(table[y])):
                ran = abs(char.Position[0] - table[y][x].indexX) + abs(char.Position[1] - table[y][x].indexY)
                if ran <= char.Skill_range and table[x][y].resident is None:
                    table[x][y].highlight(surface, (162, 250, 240))  # prev. (153, 204, 255, 50)


def charsetup(charlist, surface, table):
    for i in range(len(charlist)):
        y, x = charlist[i].Position
        table[x][y].resident = charlist[i]
        table[x][y].addpic(charlist[i].Icon, surface, (x, y), charlist[i].Team)


def bombsetup(bomblist, surface, table):
    for i in range(len(bomblist)):
        y, x = bomblist[i].position
        table[x][y].resident = Bomb(x, y)
        table[x][y].addpic(pygame.image.load('pic/Trap.png'), surface, (x, y), 0)


def queuesetup(queue, surface, queuetable):
    for i in range(len(queue)):
        queuetable[i][0].addpic(queue[i].Icon, surface, (i, 0), queue[i].Team)


def drawtable(table_x, table_y, top_left, bottom_right, surface, table_type='table'):
    # draw the table on the display surface
    # parameter (the number of cell you want in each direction,
    # pixel position of top_left of table, pixel position of bottom_right of table)
    big_table = []
    row = []
    tl_x, tl_y = top_left
    br_x, br_y = bottom_right
    for i in range(table_x):
        for j in range(table_y):
            row.append(Grid((tl_x + (i * (abs(tl_x - br_x) / table_x)), tl_y + (j * (abs(tl_y - br_y) / table_y))),
                            (abs(tl_x - br_x) / table_x, abs(tl_y - br_y) / table_y), (i, j)))
        big_table.append(row)
        row = []
    for i in range(len(big_table)):
        for j in range(len(big_table[i])):
            if table_type != 'table':
                if i + j == 0:
                    big_table[i][j].drawcell(surface, (255, 248, 64))
                else:
                    big_table[i][j].drawcell(surface, (255, 227, 183))
            else:
                big_table[i][j].drawcell(surface)
    return big_table


def set_map(table, obs_pos, surface, obs_pic):
    for i in range(len(obs_pos)):
        x, y = obs_pos[i]
        table[y][x].resident = "obstacle"
        table[y][x].obstacle = True
        table[y][x].addpic(obs_pic, surface, (x, y), 1)
