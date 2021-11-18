import pygame
from pygame.locals import *
from module.function import bomb
import sys
import math


class grid():
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
        color2 = pygame.Color(0, 0, 0)
        pygame.draw.line(surface, color2, (self.positionX, self.positionY), (self.rangeX, self.positionY), 1)
        pygame.draw.line(surface, color2, (self.positionX, self.positionY), (self.positionX, self.rangeY), 1)
        pygame.draw.line(surface, color2, (self.rangeX, self.positionY), (self.rangeX, self.rangeY), 1)
        pygame.draw.line(surface, color2, (self.positionX, self.rangeY), (self.rangeX, self.rangeY), 1)
        self.highlight(surface, color)

    def addpic(self, picname, surface, index, team):
        # create new image on input position
        # parameter (a tuple of (x,y) pixel position of where you want new image to be, tuple contain (width, and height) of one cell)
        x, y = index
        catImg = picname
        catImg = pygame.transform.scale(catImg, (math.floor(self.dimensionX -4.5), math.floor(self.dimensionY -4.5)))
        if team == 1:
            sc = pygame.Surface((math.floor(self.rect.width-4.5), math.floor(self.rect.height-4.5)))
            sc.fill((255, 0, 0))
            surface.blit(sc, (self.positionX+3, self.positionY+3))
        if team == 2:
            sc = pygame.Surface((math.floor(self.rect.width-4.5), math.floor(self.rect.height-4.5)))
            sc.fill((0, 0, 255))
            surface.blit(sc, (self.positionX+3, self.positionY+3))
        surface.blit(catImg, (self.positionX+3, self.positionY+3))
        return (x, y)

    def movepic(self, position, cellsize, last_position, surface):
        # create new image on input position and create black layer over last image
        # parameter (a tuple of (x,y) pixel position of where you want new image to be, tuple contain (width, and height) of one cell-
        x, y = position
        x1, y1 = last_position
        sizeX, sizeY = cellsize
        black = pygame.image.load('../pic/black.jpg')
        black = pygame.transform.scale(black, (math.floor(sizeX-4.5), math.floor(sizeY-4.5)))
        surface.blit(black, (x1+3, y1+3))
        catImg = pygame.image.load('../pic/pop-cat.png')
        catImg = pygame.transform.scale(catImg, (math.floor(sizeX-4.5), math.floor(sizeY-4.5)))
        surface.blit(catImg, (x+3, y+3))
        return (x+3, y+3)

    def highlight(self, surface, color):
        sc = pygame.Surface((math.floor(self.rect.width - 4.5), math.floor(self.rect.height - 4.5)))
        sc.fill(color)
        surface.blit(sc, (self.positionX + 3, self.positionY + 3))


def fillflush(x, y, range, table, surface, arr):
    # x, y = position
    if (table[y][x].resident == None) or (isinstance(table[y][x].resident, bomb)):
        table[y][x].highlight(surface, (0, 204, 0, 50))
        arr.append((y, x))
        
    if range <= 0:
        return y, x
    # if x + 1 < len(table) and y + 1 < len(table[0]) and x - 1 > 0 and y - 1 > 0:
    if (y + 1 < len(table) and table[y+1][x].resident is None) or (y + 1 < len(table) and isinstance(table[y][x].resident, bomb)):
        fillflush(x, y+1, range-1, table, surface, arr)
    if (x + 1 < len(table[0]) and table[y][x+1].resident is None) or (x + 1 < len(table[0]) and isinstance(table[y][x].resident, bomb)):
        fillflush(x+1, y, range-1, table, surface, arr)
    if (y - 1 >= 0 and table[y-1][x].resident is None) or (y - 1 >= 0 and isinstance(table[y][x].resident, bomb)):
        fillflush(x, y-1, range-1, table, surface, arr)
    if (x - 1 >= 0 and table[y][x-1].resident is None) or (x - 1 >= 0 and isinstance(table[y][x].resident, bomb)):
        fillflush(x-1, y, range-1, table, surface, arr)
    return arr


def setrange(char, table, surface, type):
    if type == "move":
        for y in range(len(table)):
            for x in range(len(table[y])):
                ran = abs(char.Position[0] - table[y][x].indexX) + abs(char.Position[1] - table[y][x].indexY)
                if ran <= char.Stamina and table[x][y].resident == None:
                    table[x][y].highlight(surface, (165, 250, 162))  # prev. (128, 0, 0, 50)

    elif type == "attack":
        for y in range(len(table)):
            for x in range(len(table[y])):
                ran = abs(char.Position[0] - table[y][x].indexX) + abs(char.Position[1] - table[y][x].indexY)
                if ran <= char.Atk_range and table[x][y].resident == None:
                    table[x][y].highlight(surface, (255, 173, 173))  # prev. (255, 192, 203, 50)
    elif type == "skill":
        for y in range(len(table)):
            for x in range(len(table[y])):
                ran = abs(char.Position[0] - table[y][x].indexX) + abs(char.Position[1] - table[y][x].indexY)
                if ran <= char.Skill_range and table[x][y].resident == None:
                    table[x][y].highlight(surface, (162, 250, 240))  # prev. (153, 204, 255, 50)


def charsetup(charlist, surface, table):
    for i in range(len(charlist)):
        y, x = charlist[i].Position
        table[x][y].resident = charlist[i]
        table[x][y].addpic(charlist[i].Icon, surface, (x, y), charlist[i].Team)

def bombsetup(bomblist, surface, table):
        for i in range(len(bomblist)):
            y, x = bomblist[i].position
            table[x][y].resident = bomb(x,y)
            table[x][y].addpic(pygame.image.load('pic/Trap.png'), surface, (x, y), 0)



def queuesetup(queue, surface, queuetable):
    for i in range(len(queue)):
        queuetable[i][0].addpic(queue[i].Icon, surface, (i, 0), queue[i].Team)


def drawtable(tableX, tableY, top_left, bottom_right, surface, table_type='table'):
    # draw the table on the display surface
    # parameter (the number of cell you want in each direction, pixel position of top_left of table, pixel position of bottom_right of table)
    big_table = []
    row = []
    tl_x, tl_y = top_left
    br_x, br_y = bottom_right
    for i in range(tableX):
        for l in range(tableY):
            row.append(grid((tl_x + (i * (abs(tl_x-br_x)/tableX)), tl_y + (l * (abs(tl_y-br_y)/tableY))), (abs(tl_x-br_x)/tableX, abs(tl_y-br_y)/tableY), (i, l)))
        big_table.append(row)
        row = []
    for i in range(len(big_table)):
        for l in range(len(big_table[i])):
            if table_type != 'table':
                if i + l == 0:
                    big_table[i][l].drawcell(surface, (255, 248, 64))
                else:
                    big_table[i][l].drawcell(surface, (255, 227, 183))
            else:
                big_table[i][l].drawcell(surface)
    return big_table


def setMap(table, obsPos, surface, obsPic):
    for i in range(len(obsPos)):
        x, y = obsPos[i]
        table[y][x].resident = "obstacle"
        table[y][x].obstacle = True
        table[y][x].addpic(obsPic, surface, (x, y), 1)


if __name__ == "__main__":
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((720, 720))
    color2 = pygame.Color(255, 255, 255)  # White
    x = 1
    y = 4
    a = drawtable(10, (120, 50), (620, 505), DISPLAYSURF)
    for i in range(len(a)):
        for l in range(len(a[i])):
            a[i][l].drawcell(DISPLAYSURF)

    while True:
        pygame.display.update()
        new_pos = None
        click = pygame.mouse.get_pressed()
        if click != (0, 0, 0):
            mousex, mousey = pygame.mouse.get_pos()
            for i in range(len(a)):
                for l in range(len(a[i])):
                    a[i][l].check_pressed(mousex, mousey)
        if new_pos is not None:
            print(new_pos)
            oldposition = new_pos
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
