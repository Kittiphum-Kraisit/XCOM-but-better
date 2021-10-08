import random
from module.Character import choose_char
from module.function import *
from module.chicTest import *

# start pygame
pygame.init()
DISPLAYSURF = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
fps = 60

Select_characters = '\nCharacter List: \n\n\
    1 : Battlemage \n\
    2 : Granadier \n\
    3 : Marksman\n\
    4 : Dancer\n\
    5 : Sheriff\n\
    6 : Flagellants\n\
    7 : Grunt\n\
    8 : Trapper\n\
    9 : Infiltrator\n\
    10 : Hospitallier\n'
    
t1, t2 = [], []
init1, init2 = [], []
queue = []

board = [['' for i in range(10)] for j in range(10)]

# Select characters
# team 1
print(Select_characters)
print('Team1 choose characters: ')

for i in range(0,5):
    t1.append(int(input())-1)

# team 2
print(Select_characters)
print('Team2 choose characters: ')

for i in range(0,5):
    t2.append(int(input())-1)

char_info1 = choose_char(t1,1)
char_info2 = choose_char(t2,2)

# preview
print('\nTeam 1: ', end ='')
for i in range(0,5):
    print(char_info1[i].Name, end =' ')
print('\nTeam 2: ', end ='')
for i in range(0,5):
    print(char_info2[i].Name, end =' ')

# set start position
print('\nSet position team1\n')
for i in range(0,5):
    print(char_info1[i].Name)
    start_point = int(input('start point: '))
    char_info1[i].set_position([start_point,0])
    board[start_point][0] = char_info1[i]

print('\nSet position team2\n')
for i in range(0,5):
    print(char_info2[i].Name)
    start_point = int(input('start point: '))
    char_info2[i].set_position([start_point,9])
    board[start_point][9] = char_info2[i]

# pygame display

color2 = pygame.Color(255, 255, 255)  # White
a, cellsize = drawtable(10, (120, 50), (620, 505), DISPLAYSURF)
table_obj = makeclass(a, cellsize)
ract_obj = makeract(table_obj, cellsize)
pygame.display.update()

for i in char_info1:
    # print(type(i.Position))
    # print(i.Position)
    position = (i.Position[0], i.Position[1])
    print(position)
    charsetup(i, position, cellsize, DISPLAYSURF, table_obj)
    pygame.display.update()

for i in char_info2:
    # print(i.Position)
    position = (i.Position[0], i.Position[1])
    print(position)
    charsetup(i, position, cellsize, DISPLAYSURF, table_obj)
    pygame.display.update()


# game start
while len(char_info1) is not 0 and len(char_info2) is not 0:



    # pygame update
    pygame.display.update()
    clock.tick(fps)

    pygame.event.get()
    # roll initiative
    init1.clear()
    init2.clear()
    queue.clear()
    print('\nTeam1 roll')
    for i in range(0,len(char_info1)):
        # _ = input()
        init1.append(random.randint(0,100))
        print(char_info1[i].Name + ":" + str(init1[-1]))

    
    print('\nTeam2 roll')
    for i in range(0,len(char_info2)):
        # _ = input()
        init2.append(random.randint(0,100))
        print(char_info2[i].Name + ":" + str(init2[-1]))

        
    # plus 10 mana to all unit
    # plus init to character speed
    for i in range(0,len(char_info1)):
        char_info1[i].Mana += 10 
        
        if char_info1[i].Name == "Flagellants":
            char_info1[i].Speed = 30 + 10*(5-len(char_info1))

        if char_info1[i].Invisible != 0:
            char_info1[i].Invisible -=1

        char_info1[i].set_currspeed(init1[i])
        queue.append(char_info1[i])
        

    for i in range(0, len(char_info2)):
        char_info2[i].Mana += 10 

        if char_info2[i].Name == "Flagellants":
            char_info2[i].Speed = 30 + 10*(5-len(char_info2))
            
        if char_info2[i].Invisible != 0:
            char_info2[i].Invisible -=1
        
        char_info2[i].set_currspeed(init2[i])
        queue.append(char_info2[i])
    
    # sort
    queue.sort(key = lambda x : x.CurrSpeed, reverse = True)
    reset_stamina(queue)

    for char in queue:

        executed = False
        attacked = False
        casted = False

        while not executed:
            print(str(char.Team)+' '+ str(char.Name) + "\'s turn")
            actions = []
            actions.append('end turn')
            if not attacked :
                actions.append('attack')
            else:
                actions.append('')
            if not casted :
                actions.append('skill')
            else:
                actions.append('')
            actions.append('move')

            for i in range(0,len(actions)):
                if actions[i] == '':
                    continue
                print( str(i) + ' : ' + actions[i])
            
            action = int(input())

            if action == 0:
                # endturn
                executed = True
                break
    
            elif action == 1:
                # attack
                if(int(char.Team)==1):
                    targets = attack_range_check(char,char_info2)
                    check = char_info2
                else:
                    targets = attack_range_check(char,char_info1)
                    check = char_info1

                if len(targets)!=0 :
                    print('choose target')
                    for i in range(0,len(targets)):
                        print(str(i) + ':' + str(targets[i].Name))
                    target = targets[int(input())]
                    attack(char, target)
                    attacked = True

                    check = check_death(target, check)
                    print(target.HP)
                else:
                    print('No target in range')

            elif action == 2:
                # skill
                if mana_check(char):
                    if char.Name == "Hospitallier":

                        if(int(char.Team)==1):
                            allies = skill_range_check(char,char_info1)
                        else:
                            allies = skill_range_check(char,char_info2)

                        if len(allies)!=0 :
                            print('choose allies')
                            for i in range(0,len(allies)):
                                print(str(i) + ':' + str(allies[i].Name))
                            ally = allies[int(input())]
                            eval(char.Skill_name + '(' + 'char, ally'+ ')')
                            casted = True 
                            print(ally.HP)
                        else:
                            print('No ally in range')
                        
                    elif char.Name == "Infiltrator":
                        print('Activated Invisibility')
                        char.Invisible = 2
                        casted = True

                    elif char.Name == "Grunt":
                        print('Activated Shield')
                        char.Shield = 30
                        casted = True
                    
                    elif char.Name == "Battlemage":
                        x = int(input('Warp to x :'))
                        y = int(input('Warp to y :'))
                        eval(char.Skill_name + '(' + 'char, [x,y]'+ ')')
                        casted = True

                    elif char.Name == "Trapper":
                        print('Place trap')
                        x = int(input('x :'))
                        y = int(input('y :'))
                        if eval(char.Skill_name + '(' + 'char, [x,y]'+ ')'):
                            board[x][y]='t'
                            casted = True
                        
                    else:
                        if(int(char.Team)==1):
                            targets = skill_range_check(char,char_info2)
                            check = char_info2
                        else:
                            targets = skill_range_check(char,char_info1)
                            check = char_info1

                        if len(targets)!=0 :

                            if char.Name == "Sheriff":
                                eval(char.Skill_name + '(' + 'char, targets'+ ')')
                                casted = True
                            else:
                                print('choose target')
                                for i in range(0,len(targets)):
                                    print(str(i) + ':' + str(targets[i].Name))
                                target = targets[int(input())]
                                eval(char.Skill_name + '(' + 'char, target'+ ')')
                                casted = True
                                check = check_death(target, check)
                                print(target.HP)

                        else:
                            print('No target in range')

            elif action == 3:
                # move
                print('Current position: '+str(char.Position))
                print('Movement: ' + str(char.Stamina))
                x = int(input('x: '))
                y = int(input('y: '))
                if move(char, [x,y], board):
                    if(int(char.Team)==1):
                        check = char_info1
                    else:
                        check = char_info2
                    
                    board[char.Position[0]][char.Position[1]] = ''

                    if char.HP <= 0:
                        check = check_death(char, check)
                        print('you are dead')
                        executed = True
                    else:
                        board[x][y] = char
                        char.Position = [x,y]
                        print('you can move')
                else :
                    print('cannot move')

        print(len(char_info1)) 
        print(len(char_info2))           

            
    

    


    

    # queue

print('the end')