import math
import pygame
import random
import inspect
from pygame import mixer
from module.button import Button, draw_text, draw_bg, draw_img
from module.Character import choose_char, obj_char_create, Character
from module.Scene import choose_character_in_pygame, blit_rotate, choose_equipment
from module.function import *
from module.chicTest import *
from module.Equipment import *

# Init pygame
pygame.init()
pygame.mixer.init()
mixer.music.set_volume(0.7)
mixer.Channel(0).play(pygame.mixer.Sound("audio/MainMenuSound.mp3"))
clock = pygame.time.Clock()
fps = 60

# Screen setting
screen_width = 800  # 1280 # 800
screen_height = 700  # 1080 # 700
bottom_panel = screen_height * 220/1080  # 150

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Game')

# UI
font = pygame.font.SysFont('sfcartoonisthand', 18)
bigger_font = pygame.font.SysFont('sfcartoonisthand', 28)
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Images
background_img = pygame.image.load('pic/black.jpg').convert_alpha()
bomb1 = pygame.image.load('pic/Trap_team1.png')
bomb2 = pygame.image.load('pic/Trap_team2.png')


# pygame object
class CharCard:
    def __init__(self, pos_x, pos_y, char_id, scale):
        self.id = char_id
        self.scale = scale
        self.info = obj_char_create(str(self.id), 0)
        char_card_image = pygame.image.load(f'pic/Full/{self.info.Name}.png').convert_alpha()
        self.image = pygame.transform.scale(char_card_image, (math.floor(char_card_image.get_width() * scale * 0.6/800),
                                                              math.floor(char_card_image.get_height() * scale * 0.6/800)
                                                              ))
        self.x = pos_x
        self.y = pos_y
        self.available = True
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)

    def draw_image(self):
        screen.blit(self.image, self.rect)

    def draw_info(self):
        draw_text(screen, self.info.Name, font, black, self.x - 50, self.y + self.image.get_height()/2)
        draw_text(screen, f'HP: {str(self.info.HP)}', font, black, self.x - 50, self.y + self.image.get_height()/2*1.25)
        draw_text(screen, f'Mana: {str(self.info.Mana)}', font, black, self.x - 50, self.y + self.image.get_height()/2 *
                  1.5)
        draw_text(screen, f'Skill: {self.info.Skill_name}', font, black, self.x - 50, self.y + self.image.get_height() /
                  2 * 1.75)
        draw_text(screen, f'AtkDmg: {str(self.info.Atk_damage)}', font, black, self.x - 50, self.y +
                  self.image.get_height()/2*2)


# Game parameters
init1, init2 = [], []  # initial speed team 1,2
start1, start2 = [], []  # start point team 1,2
queue = []

bomb_list = []

c = []  # all character cards
cc_team1, cc_team2 = [], []  # character cards team 1,2
equipments = []  # all equipments
count = 0
control = 0

# set character cards
for i in range(0, 5):
    c.append(CharCard((screen_width * 150 / 800) * 2 / 3 + (screen_width * 150 / 800 * i),
                      (screen_height - bottom_panel) * 200 / 700, i, screen_height))
for i in range(5, 10):
    c.append(CharCard((screen_width * 150 / 800) * 2 / 3 + (screen_width * 150 / 800 * (i - 5)),
                      (screen_height - bottom_panel) * 475 / 700, i, screen_height))
# set equipment cards
for i in range(0, 4):
    equipments.append(init_equipment(i))
    equipments[i].rect.center = ((screen_width*150/800) * 1.25 + (screen_width*150/800 * i),
                                 (screen_height-bottom_panel) - 250)
for i in range(4, 8):
    equipments.append(init_equipment(i))
    equipments[i].rect.center = (((screen_width*150/800) * 1.25 + (screen_width*150/800 * (i - 4))),
                                 (screen_height-bottom_panel) - 100)

run = True
scene = 1
executed = False
attacked = False
casted = False
old_clicked = False
once = False
initial_position1, initial_position2 = [], []
status = "None"
table_arr = []



while run:
    screen.fill((220, 254, 254))
    if scene == 1:
        # Welcome screen
        main_menu = pygame.image.load("pic/main menu.png")
        screen.blit(main_menu, main_menu.get_rect())
    elif scene == 2:
        # Character selection team1
        scene = choose_character_in_pygame(c, screen, cc_team1, 2)
    elif scene == 3:
        # Character selection team2
        scene = choose_character_in_pygame(c, screen, cc_team2, 3)
        # if scene == 4:
        #    scene = 9
    elif scene == 4:
        # choose equipment for team 1
        if control < 5:
            control = choose_equipment(char_info1, equipments, screen, control)
        if control == 5:
            control = 0
            for i in char_info1:
                if i.equip.type == "once":
                    method_to_call = getattr(Equipment, i.equip.ability)
                    result = method_to_call(i.equip, i)
            scene = 5
    elif scene == 5:
        # choose equipment for team 2
        if control < 5:
            control = choose_equipment(char_info2, equipments, screen, control)
        if control == 5:
            control = 0
            for i in char_info2:
                if i.equip.type == "once":
                    method_to_call = getattr(Equipment, i.equip.ability)
                    result = method_to_call(i.equip, i)
            scene = 6
    elif scene == 6:
        # Char select start position with UI for team 1
        draw_text(screen, "Team 1 set position: ", pygame.font.SysFont('sfcartoonisthand', 30), black, 180, 15)
        if len(start1) < 5:
            draw_text(screen, f"{char_info1[len(start1)].Name}", pygame.font.SysFont('sfcartoonisthand', 30), black,
                      385, 15)
        table_arr = drawtable(10, 10, (screen_width*120/800, screen_height*80/700), (screen_width*620/800, screen_height
                                                                                     * 535/700), screen)
        pygame.draw.rect(screen, red, pygame.Rect((screen_width*120/800, screen_height*80/700),
                                                  (screen_width*500/800/10, screen_height*455/700)), 2)

        # Render characters icons inside grids
        if len(initial_position1) != 0:
            for ele in range(len(initial_position1)):
                initial_position1[ele].addpic(char_info1[ele].Icon, screen, (0, 0), 1)
        if len(initial_position2) != 0:
            for ele in range(len(initial_position2)):
                initial_position2[ele].addpic(char_info2[ele].Icon, screen, (0, 0), 2)

        # End scene
        if len(start1) == 5:
            scene = 7

    elif scene == 7:
        # Char select start position with UI for team 2
        draw_text(screen, "Team 2 set position: ", pygame.font.SysFont('sfcartoonisthand', 30), black, 180, 15)
        table_arr = drawtable(10, 10, (screen_width*120/800, screen_height*80/700), (screen_width*620/800,
                                                                                     screen_height * 535/700), screen)
        if len(start2) < 5:
            draw_text(screen, f"{char_info2[len(start2)].Name}", pygame.font.SysFont('sfcartoonisthand', 30), black,
                      385, 15)
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect((screen_width*570/800, screen_height*80/700),
                                                          (screen_width * 500/800/10, screen_height*455/700)), 2)

        # Render characters icons inside grids
        if len(initial_position1) != 0:
            for ele in range(len(initial_position1)):
                initial_position1[ele].addpic(char_info1[ele].Icon, screen, (0, 0), 1)
        if len(initial_position2) != 0:
            for ele in range(len(initial_position2)):
                initial_position2[ele].addpic(char_info2[ele].Icon, screen, (0, 0), 2)

        # Initial dice rolling
        start_time = pygame.time.get_ticks()
        angle = 0

        daBox = pygame.image.load("pic/box.png")

        map1 = [(8, 2), (7, 2), (6, 2), (0, 3), (3, 4), (4, 4), (5, 4), (6, 4), (8, 6), (9, 6), (1, 7), (2, 7), (3, 7)]
        map2 = [(0, 5), (1, 2), (1, 5), (2, 2), (2, 7), (3, 7), (4, 1), (4, 3), (4, 5), (4, 7), (5, 2), (5, 4), (5, 6),
                (5, 8), (6, 4), (7, 4), (7, 6), (8, 2), (8, 6), (9, 2)]
        map3 = [(2, 2), (2, 4), (2, 5), (2, 6), (2, 7), (3, 2), (4, 2), (4, 4), (4, 7), (5, 2), (5, 5), (5, 7), (6, 7),
                (7, 2), (7, 3), (7, 4), (7, 5), (7, 7)]

        haha = random.randint(1, 3)
        if haha == 1:
            selected = map1
        elif haha == 2:
            selected = map2
        elif haha == 3:
            selected = map3
        # End scene
        if len(start2) == 5:
            scene = 8

    elif scene == 8:
        # Roll initiative
        elapsed = pygame.time.get_ticks() - start_time
        # screen.fill(0)
        draw_img(screen, pygame.image.load("pic/Roll_Bg.png"), (0, 0))
        # draw_text(screen, "Rolling Characters speed", bigger_font, black, ((screen_width // 2) - 100), 150)
        blit_rotate(screen, pygame.image.load("pic/new_Dice.png"), (((screen_width // 2) - 100), (screen_height // 4)
                                                                    + 130), 3, angle)
        angle += 1
        pygame.display.flip()
        if elapsed >= 3000:
            init1.clear()
            init2.clear()
            queue.clear()
            for i in range(0, len(char_info1)):
                init1.append(random.randint(0, 100))

            for i in range(0, len(char_info2)):
                init2.append(random.randint(0, 100))

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
            queue.sort(key=lambda cha: cha.CurrSpeed, reverse=True)
            fixed_queue = queue.copy()
            reset_stamina(queue)
            turn = 0
            scene = 9

    elif scene == 9:
        # Gameplay
        mixer.Channel(0).stop()
        if mixer.Channel(1).get_busy() == 0:
            mixer.Channel(1).play(pygame.mixer.Sound("audio/qilins.mp3"))
        table_arr = drawtable(10, 10, (screen_width*120/800, screen_height*80/700), (screen_width*620/800,
                                                                                     screen_height*535/700), screen)
        set_map(table_arr, selected, screen, daBox)
        queue_table = drawtable(10, 1, (screen_width*150/800, screen_height*10/700),
                                (screen_width*620/800, screen_height*60/700), screen, 'queue')
        charsetup(char_info1, screen, table_arr)
        charsetup(char_info2, screen, table_arr)
        bombsetup(bomb_list, screen, table_arr)
        queuesetup(queue, screen, queue_table)
        arrow_img = pygame.image.load("pic/queue/arrow.png")
        arrow_img = pygame.transform.scale(arrow_img, (math.floor(arrow_img.get_width() * 0.5),
                                                       math.floor(arrow_img.get_height() * 0.5)))
        draw_img(screen, arrow_img, (130, -15))
        if old_clicked is not False and isinstance(old_clicked, Character):
            draw_text(screen, old_clicked.Name, font, black, screen_width * 100/800, screen_height-bottom_panel)
            draw_text(screen, "HP: " + str(old_clicked.HP), font, red, screen_width * 100/800,
                      screen_height-bottom_panel + bottom_panel/5)
            draw_text(screen, "MP: " + str(old_clicked.Mana), font, blue, screen_width * 100/800,
                      screen_height-bottom_panel + bottom_panel*2/5)
            draw_text(screen, "Stamina: " + str(old_clicked.Stamina), font, black, screen_width * 100/800,
                      screen_height-bottom_panel + bottom_panel*3/5)
            draw_text(screen, "Movement: " + str(old_clicked.Movement), font, black, screen_width * 100/800,
                      screen_height-bottom_panel + bottom_panel*4/5)
            img = pygame.image.load(f"pic/Full/{old_clicked.Name}.png").convert_alpha()
            draw_img(screen, pygame.transform.scale(img, (math.floor(img.get_width() * screen_height * 0.6/800),
                                                          math.floor(img.get_height() * screen_height * 0.6/800))),
                     (0, screen_height-bottom_panel))
            draw_text(screen, "Attack damage: " + str(old_clicked.Atk_damage), font, black, screen_width * 200/800,
                      screen_height-bottom_panel + bottom_panel/5)
            draw_text(screen, "Attack range: " + str(old_clicked.Atk_range), font, black, screen_width * 200/800,
                      screen_height-bottom_panel + bottom_panel*2/5)
            draw_text(screen, "Skill: " + str(old_clicked.Skill_name), font, black, screen_width * 200/800,
                      screen_height-bottom_panel + bottom_panel*3/5)

            if old_clicked.Shield > 0:
                draw_text(screen, "Shield: " + str(old_clicked.Shield), font, black, screen_width * 200/800,
                          screen_height-bottom_panel + bottom_panel*4/5)
                img = pygame.image.load("pic/Shield.png").convert_alpha()
                draw_img(screen, img, (screen_width * 350/800, screen_height-bottom_panel + bottom_panel/5))
            elif old_clicked.Invisible > 0:
                img = pygame.image.load("pic/Invisible.png").convert_alpha()
                draw_img(screen, img, (screen_width * 350 / 800, screen_height - bottom_panel + bottom_panel / 5))
            elif old_clicked.Name == "Dancer":
                img = pygame.image.load("pic/Nimble.png").convert_alpha()
                draw_img(screen, img, (screen_width * 350 / 800, screen_height - bottom_panel + bottom_panel / 5))
        # Running queue
        char = fixed_queue[turn]

        # Set character display color
        if char.Team == 1:
            draw_text(screen, f'Team {char.Team}', pygame.font.SysFont('sfcartoonisthand', 20), black, 15, 15)
        else:
            draw_text(screen, f'Team {char.Team}', pygame.font.SysFont('sfcartoonisthand', 20), black, 15, 15)
        draw_text(screen, f'{char.Name}\'s turn', pygame.font.SysFont('sfcartoonisthand', 20), black, 15, 35)

        # if death then skip turn
        if char.HP <= 0:
            turn += 1
            if turn >= len(fixed_queue):
                scene = 8
                attacked = False
                casted = False
                start_time = pygame.time.get_ticks()
                angle = 0

        # Action Buttons setting
        Atk_button = Button(screen, screen_width*500/800, screen_height*550/700, 100, 50)
        if not attacked:
            draw_img(screen, pygame.image.load('pic/Buttons/Attack.png'), (screen_width*500/800, screen_height*550/700))
        else:
            draw_img(screen, pygame.image.load('pic/Buttons/Attack_pressed.png'), (screen_width*500/800,
                                                                                   screen_height*550/700))

        Move_button = Button(screen, screen_width*500/800, screen_height*620/700, 100, 50)
        if char.Stamina > 0:
            draw_img(screen, pygame.image.load('pic/Buttons/Move.png'), (screen_width*500/800, screen_height*620/700))
        else:
            draw_img(screen, pygame.image.load('pic/Buttons/Move_pressed.png'), (screen_width*500/800,
                                                                                 screen_height*620/700))
        Skill_button = Button(screen, screen_width*620/800, screen_height*550/700, 100, 50)
        if not casted:
            draw_img(screen, pygame.image.load('pic/Buttons/Skill.png'), (screen_width*620/800, screen_height*550/700))
        else:
            draw_img(screen, pygame.image.load('pic/Buttons/Skill_pressed.png'), (screen_width*620/800,
                                                                                  screen_height*550/700))
        End_button = Button(screen, screen_width*620/800, screen_height*620/700, 100, 50)
        draw_img(screen, pygame.image.load('pic/Buttons/End.png'), (screen_width*620/800, screen_height*620/700))
        End_button.draw()

        # if Attack button is pressed
        if Atk_button.draw() and not attacked:
            if int(char.Team) == 1:
                targets = los(char, fixed_queue, table_arr)
                check = char_info2
            else:
                targets = los(char, fixed_queue, table_arr)
                check = char_info1

            if len(targets) != 0:
                status = "attack"

        # if Move button is pressed
        if Move_button.draw():
            status = "move"
        # if skill button is pressed
        if Skill_button.draw() and not casted:
            if mana_check(char):
                if char.Name == "Infiltrator":
                    char.Invisible = 2
                    casted = True

                elif char.Name == "Grunt":
                    char.Shield = 30
                    casted = True

                else:
                    status = "skill"

        # check whether player takes an action yet
        if status is not None:
            # if player is moving, highlight the available grid space
            if status == "move":
                moveable = fillflush(char.Position[0], char.Position[1], char.Stamina, table_arr, screen, [])
                moveable = list(dict.fromkeys(moveable))
                moveable.sort()

            else:
                # highlight attack/skill range
                setrange(char, table_arr, screen, status)

        # Change to scene 8 when one of the team lost
        if len(char_info1) == 0 or len(char_info2) == 0:
            scene = 10

    elif scene == 10:
        mixer.Channel(1).stop()
        if not once:
            mixer.Channel(0).play(pygame.mixer.Sound("audio/WinSound.mp3"))
            once = True
        # Display who winner scene
        player1_win = pygame.image.load("pic/Victory1.png")
        player2_win = pygame.image.load("pic/Victory2.png")

        # Player 2 won
        if len(char_info1) == 0:
            draw_img(screen, player2_win, (0, 0))

        # Player 1 won
        else:
            draw_img(screen, player1_win, (0, 0))

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
                            mixer.Channel(3).play(pygame.mixer.Sound("audio/CharSelect.mp3"))
                            cc_team1.append(c[i].id)
                            c[i].available = not c[i].available
                        elif not c[i].available and c[i].id in cc_team1:
                            cc_team1.remove(c[i].id)
                            c[i].available = not c[i].available
                        char_info1 = choose_char(cc_team1, 1)

            # Character selection team2
            if scene == 3:
                pos = pygame.mouse.get_pos()

                # Detect collision with character cards
                for i in range(0, 10):
                    if c[i].rect.collidepoint(pos):
                        if c[i].available and (len(cc_team2) < 5):
                            mixer.Channel(3).play(pygame.mixer.Sound("audio/CharSelect.mp3"))
                            cc_team2.append(c[i].id)
                            c[i].available = not c[i].available
                        elif not c[i].available and c[i].id in cc_team2:
                            cc_team2.remove(c[i].id)
                            c[i].available = not c[i].available
                        char_info2 = choose_char(cc_team2, 2)

            if scene == 4:
                pos = pygame.mouse.get_pos()
                # Detect collision with equipment image
                for i in range(0, 8):
                    if equipments[i].rect.collidepoint(pos):
                        if char_info1[control].equip is None:
                            equipments[i].clicked = True
                            char_info1[control].equip = equipments[i]
                        else:
                            equipments[i].clicked = True
                            char_info1[control].equip = equipments[i]
                            for j in range(8):
                                if equipments[j].name != char_info1[control].equip.name:
                                    equipments[j].clicked = False

            if scene == 5:
                pos = pygame.mouse.get_pos()
                # Detect collision with equipment image
                for i in range(0, 8):
                    if equipments[i].rect.collidepoint(pos):
                        if char_info2[control].equip is None:
                            equipments[i].clicked = True
                            char_info2[control].equip = equipments[i]
                        else:
                            equipments[i].clicked = True
                            char_info2[control].equip = equipments[i]
                            for j in range(8):
                                if equipments[j].name != char_info2[control].equip.name:
                                    equipments[j].clicked = False

            # Select start position team1
            if scene == 6:
                # detect collision with the left-most side of the grid
                pos = pygame.mouse.get_pos()
                for i in range(len(table_arr)):
                    if table_arr[0][i].rect.collidepoint(pos):
                        clicked = table_arr[0][i]
                        # if detect collision is within the left side of the grid, add character on screen
                        if (clicked.indexY, 0) not in start1:
                            initial_position1.append(clicked)
                            char_info1[count].set_position([clicked.indexY, 0])
                            clicked.resident = char_info1[count]
                            start1.append((clicked.indexY, 0))
                            count += 1

            # Select start position team1
            if scene == 7:

                # detect collision with the right-most side of the grid
                pos = pygame.mouse.get_pos()
                for i in range(len(table_arr)):
                    if table_arr[9][i].rect.collidepoint(pos):
                        clicked = table_arr[9][i]
                        # if detect collision is within the right side of the grid, add character on screen
                        if (clicked.indexY, 9) not in start2:
                            initial_position2.append(clicked)
                            char_info2[count - 5].set_position([clicked.indexY, 9])
                            clicked.resident = char_info2[count - 5]
                            start2.append((clicked.indexY, 9))
                            count += 1

            # Gameplay scene
            if scene == 9:
                pos = pygame.mouse.get_pos()

                # Detect collision with the grid
                for i in range(len(table_arr)):
                    for j in range(len(table_arr[i])):
                        if table_arr[i][j].rect.collidepoint(pos):
                            clicked = table_arr[i][j]
                            x = clicked.indexX
                            y = clicked.indexY

                            # storing to display selected character info.
                            if clicked.resident is not None and status != "move":
                                old_clicked = clicked.resident

                                if status == "attack":
                                    # check whether target is attackable
                                    if clicked.resident in targets:
                                        attack(char, clicked.resident)
                                        attacked = True
                                        status = None
                                        if check_death(clicked.resident):
                                            print(check)
                                            check.remove(clicked.resident)
                                            if clicked.resident in queue:
                                                queue.remove(clicked.resident)

                                elif status == "skill":
                                    if char.Name == "Hospitallier":

                                        # gather target that's allies and is in range of the skill
                                        if int(char.Team) == 1:
                                            allies = skill_range_check(char, char_info1)
                                        else:
                                            allies = skill_range_check(char, char_info2)

                                        # if there are allies in range
                                        if len(allies) != 0:
                                            for i3 in range(0, len(allies)):
                                                print(str(i3) + ':' + str(allies[i3].Name))

                                            # if clicked characters is a valid target, activate the skill
                                            if clicked.resident in allies:
                                                eval(char.Skill_name + '(' + 'char, clicked.resident' + ')')
                                                casted = True
                                                status = None


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
                                                        char.Skill_name + '(' + 'char, clicked.resident, len(char_info'
                                                        + str(char.Team) + '))')
                                                    casted = True
                                                    status = None

                                                    if check_death(clicked.resident):
                                                        check.remove(clicked.resident)
                                                        if clicked.resident in queue:
                                                            queue.remove(clicked.resident)
                                            else:
                                                print('choose target')
                                                for i1 in range(0, len(targets)):
                                                    print(str(i1) + ':' + str(targets[i1].Name))
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
                                if (x, y) in moveable:
                                    if move(char, (y, x), table_arr, bomb_list):
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
                                eval(char.Skill_name + '(' + 'char, [y,x]' + ')')
                                casted = True
                                status = None

                            elif char.Name == "Trapper" and status == "skill":
                                if clicked.resident is None:
                                    if char.Team == 1:
                                        if trap(char, (x, y), table_arr, bomb1, screen, bomb_list):
                                            casted = True
                                            status = None
                                    elif char.Team == 2:
                                        if trap(char, (x, y), table_arr, bomb2, screen, bomb_list):
                                            casted = True
                                            status = None

                # end current character's turn
                if End_button.draw():
                    turn += 1
                    attacked = False
                    casted = False
                    status = None

                    if char.equip.type == "utility":
                        method_to_call = getattr(Equipment, char.equip.ability)
                        method_to_call(char.equip, char)
                    queue.remove(char)

                    # if the turn is equal/greater than current queue -> go back to roll initial speed scene
                    if turn >= len(fixed_queue):
                        scene = 8
                        start_time = pygame.time.get_ticks()
                        angle = 0

        # if click on close button, exit the game
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()
