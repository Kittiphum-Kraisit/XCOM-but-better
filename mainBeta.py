import math

import pygame
import random
from module.button import Button, draw_text, draw_bg, draw_img
from module.Character import choose_char, obj_char_create
from module.Scene import choose_character_in_pygame, blit_rotate
from module.function import *
from module.chicTest import *


pygame.init()
clock = pygame.time.Clock()
fps = 60
test = True
# screen setting
bottom_panel = 150
screen_width = 800
screen_height = 550 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Game')

# UI
font = pygame.font.SysFont('Times New Roman', 14)
bigger_font = pygame.font.SysFont('Times New Roman', 24)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


# images
background_img = pygame.image.load('pic/black.jpg').convert_alpha()


# pygame object
class char_card:
    def __init__(self, x, y, id):
        self.id = id
        self.info = obj_char_create(str(self.id), 0)
        img = pygame.image.load(f'pic/Full/{self.info.Name}.png').convert_alpha()
        #img = pygame.image.load(f'pic/Full/Grunt.png')
        self.image = pygame.transform.scale(img, (math.floor(img.get_width()*0.75), math.floor(img.get_height()*0.75)))
        self.x = x
        self.y = y
        self.available = True
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw_image(self):
        screen.blit(self.image, self.rect)

    def draw_info(self):
        draw_text(screen, self.info.Name, font, white, self.x - 50, self.y + 100)
        draw_text(screen, f'HP: {str(self.info.HP)}', font, white, self.x - 50, self.y + 120)
        draw_text(screen, f'Mana: {str(self.info.Mana)}', font, white, self.x - 50, self.y + 140)
        draw_text(screen, f'Skill: {self.info.Skill_name}', font, white, self.x - 50, self.y + 160)
        draw_text(screen, f'AtkDmg: {str(self.info.Atk_damage)}', font, white, self.x - 50, self.y + 180)


# game parameters
t1, t2 = [], []
init1, init2 = [], []
start1, start2 = [], []
queue = []

c = []
cc_team1 = []
cc_team2 = []
count = 0

for i in range(0, 5):
    c.append(char_card(90 + (150*i), 150, i))
for i in range(5, 10):
    c.append(char_card(90 + (150*(i-5)), 450, i))

run = True
scene = 1
executed = False
attacked = False
casted = False
old_clicked = False
initposition1 = []
initposition2 = []
status = "None"
table_arr = []
start_point = None

while run:
    screen.fill(0)
    if scene == 1:
        draw_text(screen, "Welcome", font, white, 350, 200)
        draw_text(screen, "Click to start", font, white, 350, 250)
    elif scene == 2:
        scene = choose_character_in_pygame(c, screen, cc_team1, 2)
    elif scene == 3:
        scene = choose_character_in_pygame(c, screen, cc_team2, 3)

    elif scene == 4:
        # Char select scene with UI for team 1 ################################################################
        draw_text(screen, "Team 1 set position: ", font, white, 400, 0)
        if len(start1) < 5:
            draw_text(screen, f"{char_info1[len(start1)].Name}", font, white, 520, 0)
        table_arr = drawtable(10, 10, (120, 80), (620, 535), screen)
        pygame.draw.rect(screen, red, pygame.Rect((120, 80), (50, 455)), 2)
        if len(initposition1) != 0:
            for ele in range(len(initposition1)):
                initposition1[ele].addpic(char_info1[ele].Icon, screen, (0, 0), 1)

        if len(initposition2) != 0:
            for ele in range(len(initposition2)):
                initposition2[ele].addpic(char_info2[ele].Icon, screen, (0, 0), 2)
        #######################################################################################################
        # print('\nTeam 1: ', end='')
        # for i in range(0, 5):
        #     print(char_info1[i].Name, end=' ')
        # print('\nTeam 2: ', end='')
        # for i in range(0, 5):
        #     print(char_info2[i].Name, end=' ')
        if len(start1) == 5:
            scene = 5

    elif scene == 5:
        # Char select scene with UI for team 2 ################################################################
        draw_text(screen, "Team 2 set position: ", font, white, 400, 0)
        table_arr = drawtable(10, 10, (120, 80), (620, 535), screen)
        if len(start2) < 5:
            draw_text(screen, f"{char_info2[len(start2)].Name}", font, white, 520, 0)
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect((570, 80), (50, 455)), 2)

        if len(initposition1) != 0:
            for ele in range(len(initposition1)):
                initposition1[ele].addpic(char_info1[ele].Icon, screen, (0, 0), 1)

        if len(initposition2) != 0:
            for ele in range(len(initposition2)):
                initposition2[ele].addpic(char_info2[ele].Icon, screen, (0, 0), 2)
        #######################################################################################################
        if len(start2) == 5:
            scene = 6
        start_time = pygame.time.get_ticks()
        angle = 0

    elif scene == 6:
        elapsed = pygame.time.get_ticks() - start_time
        screen.fill(0)
        draw_text(screen, "Rolling Characters speed", bigger_font, white, ((screen_width // 2)-100), 150)
        blit_rotate(screen, pygame.image.load("pic/dice.png"), (((screen_width // 2)-225), (screen_height//4)), angle)
        angle += 1
        pygame.display.flip()
        if elapsed >= 3000:
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
            fixed_queue = queue.copy()
            reset_stamina(queue)
            print(queue)
            turn = 0
            scene = 7

    elif scene == 7:

        table_arr = drawtable(10, 10, (120, 80), (620, 535), screen)
        queue_table = drawtable(10, 1, (120, 10), (620, 60), screen)
        charsetup(char_info1, screen, table_arr)
        charsetup(char_info2, screen, table_arr)
        queuesetup(queue, screen, queue_table)

        if old_clicked is not False:
            draw_text(screen, old_clicked.Name, font, white, 150, screen_height - 140)
            draw_text(screen, "HP: " + str(old_clicked.HP), font, red, 150, screen_height - 120)
            draw_text(screen, "MP: " + str(old_clicked.Mana), font, blue, 150, screen_height - 100)
            draw_text(screen, "Stamina: " + str(old_clicked.Stamina), font, white, 150, screen_height - 80)
            draw_text(screen, "Movement: " + str(old_clicked.Movement), font, white, 150, screen_height - 60)
            # Dynamic ver.
            draw_img(screen, pygame.image.load(f"pic/Full/{old_clicked.Name}.png"), (0, screen_height - 250))
            # test ver.
            # draw_img(screen, pygame.image.load("pic/Full/Grunt.png"), (0, screen_height - 250))
            draw_text(screen, "Attack damage: " + str(old_clicked.Atk_damage), font, white, 300, screen_height - 140)
            draw_text(screen, "Attack range: " + str(old_clicked.Atk_range), font, white, 300, screen_height - 120)
            draw_text(screen, "Skill: " + str(old_clicked.Skill_name), font, white, 300, screen_height - 100)

            if old_clicked.Shield > 0:
                draw_text(screen, "Shield: " + str(old_clicked.Shield), font, white, 300, screen_height - 100)

        Atk_button = Button(screen, 500, 550, 100, 50, (156, 246, 255))
        Move_button = Button(screen, 500, 620, 100, 50, (156, 246, 255))
        Skill_button = Button(screen, 620, 550, 100, 50, (156, 246, 255))
        End_button = Button(screen, 620, 620, 100, 50, (156, 246, 255))
        End_button.draw()

        char = fixed_queue[turn]
        if char.Team == 1:
            draw_text(screen, f'Team {char.Team}', font, red, screen_width - 100, 0)
        else:
            draw_text(screen, f'Team {char.Team}', font, blue, screen_width - 100, 0)
        draw_text(screen, f'{char.Name}\'s turn', font, white, screen_width - 100, 30)
        if char.HP <= 0:
            turn += 1
            if turn >= len(fixed_queue):
                scene = 6
                attacked = False
                casted = False
                start_time = pygame.time.get_ticks()
                angle = 0

        if Atk_button.draw() and not attacked:
            if int(char.Team) == 1:
                # targets = attack_range_check(char, char_info2)
                targets = los(char, fixed_queue, table_arr)
                check = char_info2
            else:
                targets = los(char, fixed_queue, table_arr)
                # targets = attack_range_check(char, char_info1)
                check = char_info1

            if len(targets) != 0:
                status = "attack"
                print('choose target')
                # for i in range(0, len(targets)):
                #     print(str(i) + ':' + str(targets[i].Name))
                # attack(char, target)
                # attacked = True
                #
                # check = check_death(target, check)
                # print(target.HP)
            else:
                print('No target in range')
            print("ATK")

        if Move_button.draw():
            status = "move"
            print('Current position: ' + str(char.Position))
            print('Movement: ' + str(char.Stamina))
            # setrange(char, table_arr, screen, "move")
            print("Move")

        if Skill_button.draw() and not casted:
            if mana_check(char):
                if char.Name == "Infiltrator":
                    print('Activated Invisibility')
                    char.Invisible = 2
                    casted = True

                elif char.Name == "Grunt":
                    print('Activated Shield')
                    char.Shield = 30
                    casted = True

                else:
                    status = "skill"
            print("Skill")
            # setrange(char, table_arr, screen, "skill")
        if status is not None:
            if status == "move":
                moveable = fillflush(char.Position[0], char.Position[1], char.Stamina, table_arr, screen, [])
                moveable = list(dict.fromkeys(moveable))
                moveable.sort()
                if test:
                    print(moveable)
                    test = False
            else:
                setrange(char, table_arr, screen, status)
        draw_text(screen, "Attack", font, red, Atk_button.rect.centerx - 20, Atk_button.rect.centery - 10)
        draw_text(screen, "Move", font, red, Move_button.rect.centerx - 20, Move_button.rect.centery - 10)
        draw_text(screen, "Skill", font, red, Skill_button.rect.centerx - 20, Skill_button.rect.centery - 10)
        draw_text(screen, "End", font, red, End_button.rect.centerx - 20, End_button.rect.centery - 10)

        if len(char_info1) == 0 or len(char_info2) == 0:
            scene = 8
            print('Win scene')

    elif scene == 8:
        lp = pygame.image.load("pic/left-popper.png")
        rp = pygame.image.load("pic/right-popper.png")
        if len(char_info1) == 0:
            draw_text(screen, "Player 2 Win!", pygame.font.SysFont('Times New Roman', 48), (255, 255, 224),
                      (screen.get_width() // 2)-125, (screen_height // 2)-50)
        # player 1 won
        else:
            draw_text(screen, "Player 1 Win!", pygame.font.SysFont('Times New Roman', 48), (255, 255, 224),
                      (screen.get_width() // 2)-125, (screen_height // 2)-50)
        draw_img(screen, pygame.transform.scale(lp, (lp.get_width() // 2, lp.get_height() // 2)), (50, 400))
        draw_img(screen, pygame.transform.scale(rp, (rp.get_width() // 2, rp.get_height() // 2)), (500, 400))


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

            if scene == 4:
                pos = pygame.mouse.get_pos()
                for i in range(len(table_arr)):
                    if table_arr[0][i].rect.collidepoint(pos):
                        clicked = table_arr[0][i]
                        start_point = clicked.indexY

                if start_point != None and (start_point, 0) not in start1:
                    initposition1.append(clicked)
                    char_info1[count].set_position([start_point, 0])
                    clicked.resident = char_info1[count]
                    print(clicked.resident)
                    start1.append((start_point, 0))
                    count += 1
                    start_point = None
                    # clicked.addpic(char_info1[len(start1)-1].Icon, screen, (0, 0), 1)

            if scene == 5:
                pos = pygame.mouse.get_pos()
                for i in range(len(table_arr)):
                    if table_arr[9][i].rect.collidepoint(pos):
                        clicked = table_arr[9][i]
                        start_point = clicked.indexY

                if start_point != None and (start_point, 9) not in start2:
                    initposition2.append(clicked)
                    char_info2[count-5].set_position([start_point, 9])
                    clicked.resident = char_info2[count-5]
                    print(clicked.resident)
                    start2.append((start_point, 9))
                    count += 1
                    start_point = None
                    # clicked.addpic(char_info2[len(start2)-1].Icon, screen, (0, 0), 2)



            if scene == 7:
                pos = pygame.mouse.get_pos()


                for i in range(len(table_arr)):
                    for j in range(len(table_arr[i])):
                        if table_arr[i][j].rect.collidepoint(pos):
                            clicked = table_arr[i][j]
                            print(clicked.indexX, clicked.indexY)
                            # edge = findedge(char, table_arr)
                            # print(edge)
                            if clicked.resident != None:
                                old_clicked = clicked.resident
                                if status == "attack":
                                    # setrange(char, table_arr, screen, "attack")
                                    for i in range(0, len(targets)):
                                        print(str(i) + ':' + str(targets[i].Name))
                                    if clicked.resident in targets:
                                        attack(char, clicked.resident)
                                        attacked = True
                                        status = None
                                        if check_death(clicked.resident):
                                            check.remove(clicked.resident)
                                            if clicked.resident in queue:
                                                queue.remove(clicked.resident)
                                    print(clicked.resident.HP)

                                elif status == "skill":
                                    x = clicked.indexX
                                    y = clicked.indexY
                                    if char.Name == "Hospitallier":
                                        if (int(char.Team) == 1):
                                            allies = skill_range_check(char, char_info1)
                                        else:
                                            allies = skill_range_check(char, char_info2)

                                        if len(allies) != 0:
                                            print('choose allies')
                                            for i in range(0, len(allies)):
                                                print(str(i) + ':' + str(allies[i].Name))
                                            if clicked.resident in allies:
                                                eval(char.Skill_name + '(' + 'char, clicked.resident' + ')')
                                            casted = True
                                            status = None
                                            print(clicked.resident.HP)
                                        else:
                                            print('No ally in range')

                                    else:
                                        if (int(char.Team) == 1):
                                            targets = skill_range_check(char, char_info2)
                                            check = char_info2
                                        else:
                                            targets = skill_range_check(char, char_info1)
                                            check = char_info1

                                        if len(targets) != 0:

                                            if char.Name == "Sheriff":
                                                eval(char.Skill_name + '(' + 'char, targets' + ')')
                                                for target in targets:
                                                    if check_death(target):
                                                        check.remove(target)
                                                        if target in queue:
                                                            queue.remove(target)
                                                casted = True
                                                status = None

                                            elif char.Name == "Flagellants":
                                                if clicked.resident in targets:
                                                    eval(char.Skill_name + '(' + 'char, clicked.resident, len(char_info' + str(char.Team) + '))')
                                                    casted = True
                                                    status = None

                                                    if check_death(clicked.resident):
                                                        check.remove(clicked.resident)
                                                        if clicked.resident in queue:
                                                            queue.remove(clicked.resident)
                                            else:
                                                print('choose target')
                                                for i in range(0, len(targets)):
                                                    print(str(i) + ':' + str(targets[i].Name))
                                                if clicked.resident in targets:
                                                    eval(char.Skill_name + '(' + 'char, clicked.resident' + ')')
                                                    casted = True
                                                    status = None
                                                    if check_death(clicked.resident):
                                                        check.remove(clicked.resident)
                                                        if clicked.resident in queue:
                                                            queue.remove(clicked.resident)
                                                    print(clicked.resident.HP)
                            elif status == "move":
                                x = clicked.indexX
                                y = clicked.indexY
                                if (x,y) in moveable:
                                    if move(char, (y, x), table_arr):
                                        if int(char.Team) == 1:
                                            check = char_info1
                                        else:
                                            check = char_info2

                                        table_arr[char.Position[1]][char.Position[0]].resident = None

                                        # if char.HP <= 0:
                                        #     check = check_death(char, check)
                                        #     print('you are dead')
                                        #     executed = True
                                        table_arr[y][x].resident = char
                                        char.Position = [y, x]
                                        print('you can move')
                                        status = None
                                    else:
                                        print('cannot move')
                            if char.Name == "Battlemage" and status == "skill" and clicked.resident == None:
                                x = clicked.indexX
                                y = clicked.indexY
                                eval(char.Skill_name + '(' + 'char, [y,x]' + ')')
                                casted = True
                                status = None

                if End_button.draw():
                    turn += 1
                    attacked = False
                    casted = False
                    status = None
                    test = True
                    queue.remove(char)
                    if turn >= len(fixed_queue):
                        scene = 6
                        start_time = pygame.time.get_ticks()
                        angle = 0
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()

