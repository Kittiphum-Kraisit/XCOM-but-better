import math

import pygame
import random
from module.button import Button, draw_text, draw_bg, draw_img
from module.Character import choose_char, obj_char_create
from module.Scene import choose_character_in_pygame, blit_rotate
from module.function import *
from module.chicTest import *

# Init pygame
pygame.init()
clock = pygame.time.Clock()
fps = 60
test = True

# Screen setting
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

# Images
background_img = pygame.image.load('pic/black.jpg').convert_alpha()


# pygame object
class char_card:
    def __init__(self, x, y, id):
        self.id = id
        self.info = obj_char_create(str(self.id), 0)
        img = pygame.image.load(f'pic/Full/{self.info.Name}.png').convert_alpha()
        self.image = pygame.transform.scale(img,
                                            (math.floor(img.get_width() * 0.75), math.floor(img.get_height() * 0.75))
                                            )
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


# Game parameters
t1, t2 = [], []
init1, init2 = [], []
start1, start2 = [], []
queue = []

c = []
cc_team1 = []
cc_team2 = []
count = 0

for i in range(0, 5):
    c.append(char_card(90 + (150 * i), 150, i))
for i in range(5, 10):
    c.append(char_card(90 + (150 * (i - 5)), 450, i))

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
        # Welcome screen
        draw_text(screen, "Welcome", font, white, 350, 200)
        draw_text(screen, "Click to start", font, white, 350, 250)
    elif scene == 2:
        # Character selection team1
        scene = choose_character_in_pygame(c, screen, cc_team1, 2)
    elif scene == 3:
        # Character selection team2
        scene = choose_character_in_pygame(c, screen, cc_team2, 3)

    elif scene == 4:
        # Char select start position with UI for team 1
        draw_text(screen, "Team 1 set position: ", font, white, 400, 0)
        if len(start1) < 5:
            draw_text(screen, f"{char_info1[len(start1)].Name}", font, white, 520, 0)
        table_arr = drawtable(10, 10, (120, 80), (620, 535), screen)
        pygame.draw.rect(screen, red, pygame.Rect((120, 80), (50, 455)), 2)

        # Render characters icons inside grids
        if len(initposition1) != 0:
            for ele in range(len(initposition1)):
                initposition1[ele].addpic(char_info1[ele].Icon, screen, (0, 0), 1)
        if len(initposition2) != 0:
            for ele in range(len(initposition2)):
                initposition2[ele].addpic(char_info2[ele].Icon, screen, (0, 0), 2)

        # End scene
        if len(start1) == 5:
            scene = 5

    elif scene == 5:
        # Char select start position with UI for team 2
        draw_text(screen, "Team 2 set position: ", font, white, 400, 0)
        table_arr = drawtable(10, 10, (120, 80), (620, 535), screen)
        if len(start2) < 5:
            draw_text(screen, f"{char_info2[len(start2)].Name}", font, white, 520, 0)
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect((570, 80), (50, 455)), 2)

        # Render characters icons inside grids
        if len(initposition1) != 0:
            for ele in range(len(initposition1)):
                initposition1[ele].addpic(char_info1[ele].Icon, screen, (0, 0), 1)
        if len(initposition2) != 0:
            for ele in range(len(initposition2)):
                initposition2[ele].addpic(char_info2[ele].Icon, screen, (0, 0), 2)

        # Initial dice rolling
        start_time = pygame.time.get_ticks()
        angle = 0

        # End scene
        if len(start2) == 5:
            scene = 6

    elif scene == 6:
        # Roll initiative
        elapsed = pygame.time.get_ticks() - start_time
        screen.fill(0)
        draw_text(screen, "Rolling Characters speed", bigger_font, white, ((screen_width // 2) - 100), 150)
        blit_rotate(screen, pygame.image.load("pic/dice.png"), (((screen_width // 2) - 225), (screen_height // 4)),
                    angle)
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

            # Sort characters queue
            queue.sort(key=lambda x: x.CurrSpeed, reverse=True)
            fixed_queue = queue.copy()
            reset_stamina(queue)
            print(queue)
            turn = 0
            scene = 7

    elif scene == 7:
        # Gameplay

        # Draw table, queue
        table_arr = drawtable(10, 10, (120, 80), (620, 535), screen)
        queue_table = drawtable(10, 1, (120, 10), (620, 60), screen)
        charsetup(char_info1, screen, table_arr)
        charsetup(char_info2, screen, table_arr)
        queuesetup(queue, screen, queue_table)

        # Display character info. when selected
        if old_clicked is not False:
            draw_text(screen, old_clicked.Name, font, white, 150, screen_height - 140)
            draw_text(screen, "HP: " + str(old_clicked.HP), font, red, 150, screen_height - 120)
            draw_text(screen, "MP: " + str(old_clicked.Mana), font, blue, 150, screen_height - 100)
            draw_text(screen, "Stamina: " + str(old_clicked.Stamina), font, white, 150, screen_height - 80)
            draw_text(screen, "Movement: " + str(old_clicked.Movement), font, white, 150, screen_height - 60)
            draw_img(screen, pygame.image.load(f"pic/Full/{old_clicked.Name}.png"), (0, screen_height - 250))
            draw_text(screen, "Attack damage: " + str(old_clicked.Atk_damage), font, white, 300, screen_height - 140)
            draw_text(screen, "Attack range: " + str(old_clicked.Atk_range), font, white, 300, screen_height - 120)
            draw_text(screen, "Skill: " + str(old_clicked.Skill_name), font, white, 300, screen_height - 100)

            if old_clicked.Shield > 0:
                draw_text(screen, "Shield: " + str(old_clicked.Shield), font, white, 300, screen_height - 100)



        # Running queue
        char = fixed_queue[turn]

        # Set character display color
        if char.Team == 1:
            draw_text(screen, f'Team {char.Team}', font, red, screen_width - 100, 0)
        else:
            draw_text(screen, f'Team {char.Team}', font, blue, screen_width - 100, 0)
        draw_text(screen, f'{char.Name}\'s turn', font, white, screen_width - 100, 30)

        # if death then skip turn
        if char.HP <= 0:
            turn += 1
            if turn >= len(fixed_queue):
                scene = 6
                attacked = False
                casted = False
                start_time = pygame.time.get_ticks()
                angle = 0


        # Action Buttons setting
        Atk_button = Button(screen, 500, 550, 100, 50, (156, 246, 255))
        Move_button = Button(screen, 500, 620, 100, 50, (156, 246, 255))
        Skill_button = Button(screen, 620, 550, 100, 50, (156, 246, 255))
        End_button = Button(screen, 620, 620, 100, 50, (156, 246, 255))
        End_button.draw()

        # if Attack button is pressed
        if Atk_button.draw() and not attacked:
            if int(char.Team) == 1:
                targets = LoS(char, fixed_queue, table_arr)
                check = char_info2
            else:
                targets = LoS(char, fixed_queue, table_arr)
                check = char_info1

            if len(targets) != 0:
                status = "attack"
                print('choose target')

            else:
                print('No target in range')
            print("ATK")

        # if Move button is pressed
        if Move_button.draw():
            status = "move"
            print('Current position: ' + str(char.Position))
            print('Movement: ' + str(char.Stamina))
            print("Move")

        # if skill button is pressed
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

        # check whether player takes an action yet
        if status is not None:

            # if player is moving, highlight the available grid space
            if status == "move":
                moveable = fillflush(char.Position[0], char.Position[1], char.Stamina, table_arr, screen, [])
                moveable = list(dict.fromkeys(moveable))
                moveable.sort()
                if test:
                    print(moveable)
                    test = False

            else:
                # highlight attack/skill range
                setrange(char, table_arr, screen, status)

        # Draw text on buttons
        draw_text(screen, "Attack", font, red, Atk_button.rect.centerx - 20, Atk_button.rect.centery - 10)
        draw_text(screen, "Move", font, red, Move_button.rect.centerx - 20, Move_button.rect.centery - 10)
        draw_text(screen, "Skill", font, red, Skill_button.rect.centerx - 20, Skill_button.rect.centery - 10)
        draw_text(screen, "End", font, red, End_button.rect.centerx - 20, End_button.rect.centery - 10)

        # Change to scene 8 when one of the team lost
        if len(char_info1) == 0 or len(char_info2) == 0:
            scene = 8
            print('Win scene')

    elif scene == 8:

        # Display who winner scene
        lp = pygame.image.load("pic/left-popper.png")
        rp = pygame.image.load("pic/right-popper.png")

        # Player 2 won
        if len(char_info1) == 0:
            draw_text(screen, "Player 2 Win!", pygame.font.SysFont('Times New Roman', 48), (255, 255, 224),
                      (screen.get_width() // 2) - 125, (screen_height // 2) - 50)

        # Player 1 won
        else:
            draw_text(screen, "Player 1 Win!", pygame.font.SysFont('Times New Roman', 48), (255, 255, 224),
                      (screen.get_width() // 2) - 125, (screen_height // 2) - 50)
        draw_img(screen, pygame.transform.scale(lp, (lp.get_width() // 2, lp.get_height() // 2)), (50, 400))
        draw_img(screen, pygame.transform.scale(rp, (rp.get_width() // 2, rp.get_height() // 2)), (500, 400))

    # Events in games
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Welcome screen
            if scene == 1:
                # Click to scene2
                scene = 2

            # Character selection team1
            if scene == 2:
                pos = pygame.mouse.get_pos()

                # Detect collision with character cards
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

            # Character selection team1
            if scene == 3:
                pos = pygame.mouse.get_pos()

                # Detect collision with character cards
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

            # Select start position team1
            if scene == 4:

                # detect collision with the left-most side of the grid
                pos = pygame.mouse.get_pos()
                for i in range(len(table_arr)):
                    if table_arr[0][i].rect.collidepoint(pos):
                        clicked = table_arr[0][i]
                        start_point = clicked.indexY

                # if detect collision is within the left side of the grid, add character on screen
                if start_point is not None and (start_point, 0) not in start1:
                    initposition1.append(clicked)
                    char_info1[count].set_position([start_point, 0])
                    clicked.resident = char_info1[count]
                    print(clicked.resident)
                    start1.append((start_point, 0))
                    count += 1
                    start_point = None

            # Select start position team1
            if scene == 5:

                # detect collision with the right-most side of the grid
                pos = pygame.mouse.get_pos()
                for i in range(len(table_arr)):
                    if table_arr[9][i].rect.collidepoint(pos):
                        clicked = table_arr[9][i]
                        start_point = clicked.indexY

                # if detect collision is within the right side of the grid, add character on screen
                if start_point is not None and (start_point, 9) not in start2:
                    initposition2.append(clicked)
                    char_info2[count - 5].set_position([start_point, 9])
                    clicked.resident = char_info2[count - 5]
                    print(clicked.resident)
                    start2.append((start_point, 9))
                    count += 1
                    start_point = None

            # Gameplay scene
            if scene == 7:
                pos = pygame.mouse.get_pos()

                # Detect collision with the grid
                for i in range(len(table_arr)):
                    for j in range(len(table_arr[i])):
                        if table_arr[i][j].rect.collidepoint(pos):
                            clicked = table_arr[i][j]
                            print(clicked.indexX, clicked.indexY)

                            # storing to display selected character info.
                            if clicked.resident is not None:
                                old_clicked = clicked.resident

                                if status == "attack":
                                    for i in range(0, len(targets)):
                                        print(str(i) + ':' + str(targets[i].Name))

                                    # check whether target is attackable
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

                                        # gather target that's allies and is in range of the skill
                                        if int(char.Team) == 1:
                                            allies = skill_range_check(char, char_info1)
                                        else:
                                            allies = skill_range_check(char, char_info2)

                                        # if there are allies in range
                                        if len(allies) != 0:
                                            print('choose allies')
                                            for i in range(0, len(allies)):
                                                print(str(i) + ':' + str(allies[i].Name))

                                            # if clicked characters is a valid target, activate the skill
                                            if clicked.resident in allies:
                                                eval(char.Skill_name + '(' + 'char, clicked.resident' + ')')
                                                casted = True
                                                status = None
                                                print(clicked.resident.HP)
                                        else:
                                            print('No ally in range')

                                    # Damaging skills
                                    else:
                                        if int(char.Team) == 1:
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
                                                    eval(
                                                        char.Skill_name + '(' + 'char, clicked.resident, len(char_info' + str(
                                                            char.Team) + '))')
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

                            # No character insides the clicked grid
                            elif status == "move":
                                x = clicked.indexX
                                y = clicked.indexY
                                if (x, y) in moveable:
                                    if move(char, (y, x), table_arr):
                                        if int(char.Team) == 1:
                                            check = char_info1
                                        else:
                                            check = char_info2

                                        # Move character to the destination
                                        table_arr[char.Position[1]][char.Position[0]].resident = None
                                        table_arr[y][x].resident = char
                                        char.Position = [y, x]
                                        print('you can move')
                                        status = None
                                    else:
                                        print('cannot move')

                            elif char.Name == "Battlemage" and status == "skill":
                                x = clicked.indexX
                                y = clicked.indexY
                                eval(char.Skill_name + '(' + 'char, [y,x]' + ')')
                                casted = True
                                status = None

                # end current character's turn
                if End_button.draw():
                    turn += 1
                    attacked = False
                    casted = False
                    status = None
                    test = True
                    queue.remove(char)
                    # if the turn is equal/greater than current queue -> go back to roll initial speed scene
                    if turn >= len(fixed_queue):
                        scene = 6
                        start_time = pygame.time.get_ticks()
                        angle = 0

        # if click on close button, exit the game
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()
