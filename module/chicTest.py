import pygame
from pygame.locals import *
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

    def drawcell(self, surface):
        color2 = pygame.Color(255, 255, 255)
        pygame.draw.line(surface, color2, (self.positionX, self.positionY), (self.rangeX, self.positionY), 5)
        pygame.draw.line(surface, color2, (self.positionX, self.positionY), (self.positionX, self.rangeY), 5)
        pygame.draw.line(surface, color2, (self.rangeX, self.positionY), (self.rangeX, self.rangeY), 5)
        pygame.draw.line(surface, color2, (self.positionX, self.rangeY), (self.rangeX, self.rangeY), 5)

    def addpic(self,picname, surface, index, team):
        # create new image on input position
        # parameter (a tuple of (x,y) pixel position of where you want new image to be, tuple contain (width, and height) of one cell)
        x, y = index
        catImg = picname
        catImg = pygame.transform.scale(catImg, (math.floor(self.dimensionX -4.5), math.floor(self.dimensionY -4.5)))
        if team == 1:
            sc = pygame.Surface((math.floor(self.rect.width-4.5), math.floor(self.rect.height-4.5)))
            sc.fill((255, 0, 0))
            surface.blit(sc, (self.positionX+3, self.positionY+3))
        else:
            sc = pygame.Surface((math.floor(self.rect.width-4.5), math.floor(self.rect.height-4.5)))
            sc.fill((0, 0, 255))
            surface.blit(sc, (self.positionX+3, self.positionY+3))
        surface.blit(catImg, (self.positionX+3, self.positionY+3))
        return (x, y)

    def movepic(self, position, cellsize, last_position, surface):
        # create new image on input position and create black layer over last image
        # parameter (a tuple of (x,y) pixel position of where you want new image to be, tuple contain (width, and height) of one cell-
        # -, the tuple of pixel position of last image)
        x, y = position
        x1, y1 = last_position
        sizeX, sizeY = cellsize
        black = pygame.image.load('../pic/black.jpg')
        black = pygame.transform.scale(black, (math.floor(sizeX-4.5), math.floor(sizeY-4.5)))
        # print(last_position)
        surface.blit(black, (x1+3, y1+3))
        catImg = pygame.image.load('../pic/pop-cat.png')
        catImg = pygame.transform.scale(catImg, (math.floor(sizeX-4.5), math.floor(sizeY-4.5)))
        surface.blit(catImg, (x+3, y+3))
        return (x+3, y+3)

    # def check_pressed(self, mousex, mousey):
    #     # check if the mouse is pressed
    #     # parameter (2D array of grid class objects, 2D array of rect objects, tuple contain (width, and height) of one cell in table-
    #     # -, the tuple of pixel position of last image)
    #     # mousex, mousey = pygame.mouse.get_pos()
    #     # click = pygame.mouse.get_pressed()
    #     #
    #     # if click != (0, 0, 0):
    #     if self.rect.collidepoint(mousex, mousey):
    #         return (self.indexX, self.indexY)
# def makeract(table, cellsize):
#     # create rectangle object to use as hitbox for table
#     # parameter (2D array of grid class objects, tuple contain (width, and height) of one cell in table)
#     lenX, lenY = cellsize
#     for i in range(len(table)):
#         for l in range(len(table[i])):
#             box = pygame.Rect(table[i][l].positionX, table[i][l].positionY, lenX, lenY)
#             table[i][l].addrect(box)

def charsetup(charlist, surface, table):
    for i in range(len(charlist)):
        y, x = charlist[i].Position
        table[x][y].resident = charlist[i]
        table[x][y].addpic(charlist[i].Icon, surface, (x, y), charlist[i].Team)

def queuesetup(queue, surface, queuetable):
    for i in range(len(queue)):
        queuetable[i][0].addpic(queue[i].Icon, surface, (i, 0), queue[i].Team)

# def makeclass(positions, cellsize):
#     # create grid class object to collect position, dimension, index in single object
#     # parameter (2D array of tuples contain pixel position (x,y) of each cell, tuple contain (width, and height) of one cell in table)
#     obj = []
#     for i in range(len(positions)):
#         row = []
#         for l in range(len(positions[i])):
#             row.append(grid(positions[i][l], cellsize, (i, l)))
#         obj.append(row)
#     return obj

def drawtable(tableX, tableY, top_left, bottom_right, surface):
    # draw the table on the display surface
    # parameter (the number of cell you want in each direction, pixel position of top_left of table, pixel position of bottom_right of table)
    # color2 = pygame.Color(255, 255, 255)
    big_table = []
    row = []
    tl_x, tl_y = top_left
    br_x, br_y = bottom_right
    # for i in range(table+1):
    #     pygame.draw.line(surface, color2, (tl_x, tl_y + (i * (abs(tl_y-br_y)/table))), (br_x, tl_y + (i * (abs(tl_y-br_y)/table))), 5)
    #     pygame.draw.line(surface, color2, (tl_x + (i * (abs(tl_x-br_x)/table)), tl_y), (tl_x + (i * (abs(tl_x-br_x)/table)), br_y), 5)
    for i in range(tableX):
        for l in range(tableY):
            # row.append([tl_x + (l * (abs(tl_x-br_x)/table)), tl_y + (i * (abs(tl_y-br_y)/table))])
            row.append(grid((tl_x + (i * (abs(tl_x-br_x)/tableX)), tl_y + (l * (abs(tl_y-br_y)/tableY))), (abs(tl_x-br_x)/tableX, abs(tl_y-br_y)/tableY), (i, l)))
        big_table.append(row)
        row = []
    for i in range(len(big_table)):
        for l in range(len(big_table[i])):
            big_table[i][l].drawcell(surface)
    return big_table

def drawqueue(table, top_left, bottom_right, surface):
    # draw the table on the display surface
    # parameter (the number of cell you want in each direction, pixel position of top_left of table, pixel position of bottom_right of table)
    # color2 = pygame.Color(255, 255, 255)
    row = []
    tl_x, tl_y = top_left
    br_x, br_y = bottom_right
    # for i in range(table+1):
    #     pygame.draw.line(surface, color2, (tl_x, tl_y + (i * (abs(tl_y-br_y)/table))), (br_x, tl_y + (i * (abs(tl_y-br_y)/table))), 5)
    #     pygame.draw.line(surface, color2, (tl_x + (i * (abs(tl_x-br_x)/table)), tl_y), (tl_x + (i * (abs(tl_x-br_x)/table)), br_y), 5)
    for i in range(table):
        row.append(grid((tl_x + (i * (abs(tl_x-br_x)/table)), tl_y), (abs(tl_x-br_x)/table, abs(br_y-tl_y)), (0, i)))
    for l in range(len(row)):
        row[l].drawcell(surface)
    return row



if __name__ == "__main__":
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((720, 720))
    color2 = pygame.Color(255, 255, 255)  # White
    x = 1
    y = 4
    # cell = grid((120, 50), (100, 25), (0, 0))
    # cell.drawcell(DISPLAYSURF)
    a = drawtable(10, (120, 50), (620, 505), DISPLAYSURF)
    for i in range(len(a)):
        for l in range(len(a[i])):
            a[i][l].drawcell(DISPLAYSURF)
    # makeract(table_obj, cellsize)
    # oldposition = grid.addpic(a[x][y], cellsize, "../pic/pop-cat.png", DISPLAYSURF)

    while True:
        pygame.display.update()
        new_pos = None
        click = pygame.mouse.get_pressed()
        if click != (0, 0, 0):
            mousex, mousey = pygame.mouse.get_pos()
            # print(mousex, mousey)
            for i in range(len(a)):
                for l in range(len(a[i])):
                    a[i][l].check_pressed(mousex, mousey)
        if new_pos != None:
            print(new_pos)
            oldposition = new_pos
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
