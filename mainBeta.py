import math

import pygame
import random
from pygame import mixer
from module.button import Button, draw_text, draw_bg, draw_img
from module.Character import choose_char, obj_char_create
from module.Scene import choose_character_in_pygame, blit_rotate
from module.function import *
from module.chicTest import *

# Init pygame
pygame.init()
pygame.mixer.init()
# Type 1
# bg_music = pygame.mixer.Sound("audio/rex.mp3")
# bg_music.set_volume(0.7)
# bg_music.play()
# Type 2
# mixer.music.load("audio/rex.mp3")
mixer.music.set_volume(0.7)
mixer.Channel(0).play(pygame.mixer.Sound("audio/MainMenuSound.mp3"))
clock = pygame.time.Clock()
fps = 60
test = True

# Screen setting
screen_width = 800 #1280 #800
screen_height = 700 #1080 #700
bottom_panel = screen_height * 220/1080 #150

screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption('Game')

# UI
font = pygame.font.SysFont('Times New Roman', 14)
bigger_font = pygame.font.SysFont('Times New Roman', 24)
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Images
background_img = pygame.image.load('pic/black.jpg').convert_alpha()


# pygame object
class char_card:
    def __init__(self, x, y, id, scale):
        self.id = id
        self.scale = scale
        self.info = obj_char_create(str(self.id), 0)
        img = pygame.image.load(f'pic/Full/{self.info.Name}.png').convert_alpha()
        self.image = pygame.transform.scale(img,
                                            (math.floor(img.get_width() * scale * 0.6/800), math.floor(img.get_height() * scale * 0.6/800))
                                            )
        self.x = x
        self.y = y
        self.available = True
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw_image(self):
        screen.blit(self.image, self.rect)

    def draw_info(self):
        draw_text(screen, self.info.Name, font, black, self.x - 50, self.y + self.image.get_height()/2)
        draw_text(screen, f'HP: {str(self.info.HP)}', font, black, self.x - 50, self.y + self.image.get_height()/2*1.25)
        draw_text(screen, f'Mana: {str(self.info.Mana)}', font, black, self.x - 50, self.y + self.image.get_height()/2*1.5)
        draw_text(screen, f'Skill: {self.info.Skill_name}', font, black, self.x - 50, self.y + self.image.get_height()/2*1.75)
        draw_text(screen, f'AtkDmg: {str(self.info.Atk_damage)}', font, black, self.x - 50, self.y + self.image.get_height()/2*2)


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
    c.append(char_card((screen_width*150/800)*2/3 + (screen_width*150/800 * i), (screen_height-bottom_panel) * 150/700, i, screen_height))
for i in range(5, 10):
    c.append(char_card((screen_width*150/800)*2/3 + (screen_width*150/800 * (i - 5)), (screen_height-bottom_panel) * 425/700, i, screen_height))

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
    screen.fill((220, 254, 254))
    if scene == 1:
        # Welcome screen
        # draw_text(screen, "Welcome", font, black, 350, 200)
        # draw_text(screen, "Click to start", font, black, 350, 250)
        # Image ver.
        main_menu = pygame.image.load("pic/main menu.png")
        screen.blit(main_menu, main_menu.get_rect())
    elif scene == 2:
        # Character selection team1
        scene = choose_character_in_pygame(c, screen, cc_team1, 2)
    elif scene == 3:
        # Character selection team2
        scene = choose_character_in_pygame(c, screen, cc_team2, 3)

    elif scene == 4:
        # Char select start position with UI for team 1
        draw_text(screen, "Team 1 set position: ", font, black, screen_width/2, screen_height/1000)
        if len(start1) < 5:
            draw_text(screen, f"{char_info1[len(start1)].Name}", font, black, screen_width/1000, screen_height/1000)
        table_arr = drawtable(10, 10, (screen_width*120/800, screen_height*80/700), (screen_width*620/800, screen_height*535/700), screen)
        pygame.draw.rect(screen, red, pygame.Rect((screen_width*120/800, screen_height*80/700), (screen_width*500/800/10, screen_height*455/700)), 2)

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
        draw_text(screen, "Team 2 set position: ", font, black, 400, 0)
        table_arr = drawtable(10, 10, (screen_width*120/800, screen_height*80/700), (screen_width*620/800, screen_height*535/700), screen)
        if len(start2) < 5:
            draw_text(screen, f"{char_info2[len(start2)].Name}", font, black, 520, 0)
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect((screen_width*570/800, screen_height*80/700), (screen_width*500/800/10, screen_height*455/700)), 2)

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
        # screen.fill(0)
        draw_text(screen, "Rolling Characters speed", bigger_font, black, ((screen_width // 2) - 100), 150)
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
        mixer.Channel(0).stop()
        if mixer.Channel(1).get_busy() == False:
            mixer.Channel(1).play(pygame.mixer.Sound("audio/FightMusic.mp3"))
        # Draw table, queue
        table_arr = drawtable(10, 10, (screen_width*120/800, screen_height*80/700), (screen_width*620/800, screen_height*535/700), screen)
        queue_table = drawtable(10, 1, (screen_width*120/800, screen_height*10/700), (screen_width*620/800, screen_height*60/700), screen)
        charsetup(char_info1, screen, table_arr)
        charsetup(char_info2, screen, table_arr)
        queuesetup(queue, screen, queue_table)

        # Display character info. when selected
        if old_clicked is not False:
            draw_text(screen, old_clicked.Name, font, black, screen_width * 150/800, screen_height-bottom_panel)
            draw_text(screen, "HP: " + str(old_clicked.HP), font, red, screen_width * 150/800, screen_height-bottom_panel + bottom_panel/5)
            draw_text(screen, "MP: " + str(old_clicked.Mana), font, blue, screen_width * 150/800, screen_height-bottom_panel + bottom_panel*2/5)
            draw_text(screen, "Stamina: " + str(old_clicked.Stamina), font, black, screen_width * 150/800, screen_height-bottom_panel + bottom_panel*3/5)
            draw_text(screen, "Movement: " + str(old_clicked.Movement), font, black, screen_width * 150/800, screen_height-bottom_panel + bottom_panel*4/5)
            img = pygame.image.load(f"pic/Full/{old_clicked.Name}.png").convert_alpha()
            draw_img(screen, pygame.transform.scale(img, (math.floor(img.get_width() * screen_height * 0.6/800), math.floor(img.get_height() * screen_height * 0.6/800))), (0, screen_height-bottom_panel))
            draw_text(screen, "Attack damage: " + str(old_clicked.Atk_damage), font, black, screen_width * 300/800, screen_height-bottom_panel + bottom_panel/5)
            draw_text(screen, "Attack range: " + str(old_clicked.Atk_range), font, black, screen_width * 300/800, screen_height-bottom_panel + bottom_panel*2/5)
            draw_text(screen, "Skill: " + str(old_clicked.Skill_name), font, black, screen_width * 300/800, screen_height-bottom_panel + bottom_panel*3/5)

            if old_clicked.Shield > 0:
                draw_text(screen, "Shield: " + str(old_clicked.Shield), font, black, screen_width * 300/800, screen_height-bottom_panel + bottom_panel*4/5)



        # Running queue
        char = fixed_queue[turn]

        # Set character display color
        if char.Team == 1:
            draw_text(screen, f'Team {char.Team}', font, red, screen_width - 100, 0)
        else:
            draw_text(screen, f'Team {char.Team}', font, blue, screen_width - 100, 0)
        draw_text(screen, f'{char.Name}\'s turn', font, black, screen_width - 100, 30)

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
        Atk_button = Button(screen, screen_width*500/800, screen_height*550/700, 100, 50)
        if not attacked:
            draw_img(screen, pygame.image.load('pic/Buttons/Attack.png'), (screen_width*500/800, screen_height*550/700))
        else:
            draw_img(screen, pygame.image.load('pic/Buttons/Attack_pressed.png'), (screen_width*500/800, screen_height*550/700))
        Move_button = Button(screen, screen_width*500/800, screen_height*620/700, 100, 50)
        if char.Stamina > 0:
            draw_img(screen, pygame.image.load('pic/Buttons/Move.png'), (screen_width*500/800, screen_height*620/700))
        else:
            draw_img(screen, pygame.image.load('pic/Buttons/Move_pressed.png'), (screen_width*500/800, screen_height*620/700))
        Skill_button = Button(screen, screen_width*620/800, screen_height*550/700, 100, 50)
        if not casted:
            draw_img(screen, pygame.image.load('pic/Buttons/Skill.png'), (screen_width*620/800, screen_height*550/700))
        else:
            draw_img(screen, pygame.image.load('pic/Buttons/Skill_pressed.png'), (screen_width*620/800, screen_height*550/700))
        End_button = Button(screen, screen_width*620/800, screen_height*620/700, 100, 50)
        draw_img(screen, pygame.image.load('pic/Buttons/End.png'), (screen_width*620/800, screen_height*620/700))
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
        # draw_text(screen, "Attack", font, red, Atk_button.rect.centerx - 20, Atk_button.rect.centery - 10)
        # draw_text(screen, "Move", font, red, Move_button.rect.centerx - 20, Move_button.rect.centery - 10)
        # draw_text(screen, "Skill", font, red, Skill_button.rect.centerx - 20, Skill_button.rect.centery - 10)
        # draw_text(screen, "End", font, red, End_button.rect.centerx - 20, End_button.rect.centery - 10)

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
                            mixer.Channel(3).play(pygame.mixer.Sound("audio/CharSelect.mp3"))
                            cc_team1.append(c[i].id)
                            c[i].available = not c[i].available
                        elif not c[i].available and c[i].id in cc_team1:
                            cc_team1.remove(c[i].id)
                            c[i].available = not c[i].available
                        char_info1 = choose_char(cc_team1, 1)
                        print(char_info1)

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
