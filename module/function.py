import math
import random


def attack_range_check(char_atk, char_def_list):
    char_enemy = []
    for enemy in char_def_list:
        check = range_check(char_atk, enemy)
        if check <= char_atk.Atk_range and enemy.Invisible == 0:
            char_enemy.append(enemy)
    return char_enemy
# obstacle: obstacle + allies as positions in tuple
def los(char_atk, char_list, table):
    enemies = []
    obstacles = []
    for unit in char_list:
        check = range_check(char_atk, unit)
        if check <= char_atk.Atk_range and unit.Invisible == 0 and unit.Team != char_atk.Team:
            enemies.append(unit)
            obstacles.append((unit.Position[1], unit.Position[0]))
        elif check <= char_atk.Atk_range and unit.Team == char_atk.Team and unit.Name != char_atk.Name:
            obstacles.append((unit.Position[1], unit.Position[0]))
    for y in range(len(table)):
        for x in range(len(table[y])):
            ran = abs(char_atk.Position[0] - table[y][x].indexX) + abs(char_atk.Position[1] - table[y][x].indexY)
            if ran <= char_atk.Atk_range and table[y][x].obstacle == True:
                obstacles.append((y, x))
    print("1st", obstacles)
    for i in enemies:
        print("2nd", i)
    return line_of_sight(char_atk, enemies, obstacles)

def line_of_sight(char, enemies, obstacles):
    # y = (y1-y0/(x1-x0))*(x-x0) + y0
    y0, x0 = char.Position
    attackable = enemies.copy()
    print("3rd", obstacles)
    varx = 0
    for enemy in enemies:
        print("rounds",varx)
        varx += 1
        y1, x1 = enemy.Position
        for x in range(x0, x1):
            y = round(((y1-y0)/(x1-x0))*(x-x0) + y0)
            if (x, y) in obstacles:
                print("removed", x, y)
                attackable.remove(enemy)
                break
        continue
    for i in attackable:
        print(i.Name)
    return attackable






def skill_range_check(caster,char_list):
    char_inrange = []
    for char in char_list:
        check = range_check(char, caster)
        if check <= caster.Skill_range:
            char_inrange.append(char)
    return char_inrange


def attack(char_atk, char_def):
    check = range_check(char_atk, char_def)
    if check <= char_atk.Atk_range:
        if check_shield(char_def):
            char_def.Shield -= char_atk.Atk_damage
            if char_def.Shield < 0:
                char_def.HP += char_def.Shield
                char_def.Shield = 0
        elif char_def.Name == 'Dancer':
          if nimble(char_def) == False:
            char_def.HP -= char_atk.Atk_damage
        else:
            char_def.HP -= char_atk.Atk_damage
        return True
    else:
        return False


def charmove(char, new_index, old_index, table, surface):
    check = pos_check(char, new_index)
    if check <= char.Stamina:
        x, y = new_index
        x1, y1 = old_index
        char.position = (x, y)
        table[x1][y1].resident = None
        table[x][y].resident = char
        table[x][y].addpic(char.Icon, surface, (x, y), char.Team)

def move(char, destination, board):
    check = pos_check(char, destination)
    if check <= char.Stamina:
        char.Stamina -= check
        # if board[destination[0]][destination[1]] == '':
        #     char.Stamina -= check
        #     return True
        # if board[destination[0]][destination[1]] == 't':
        #     char.HP -= 50
        #     char.Stamina -= check
        #     return True

        return True
    return False


def check_death(char):
    if char.HP <= 0:
        return True
    elif char.HP > 0:
        return False


def range_check(char1, char2):
    ran = abs(char1.Position[0] - char2.Position[0]) + abs(char1.Position[1] - char2.Position[1])
    return ran


def pos_check(char, destination):
    ran = abs(char.Position[0] - destination[0]) + abs(char.Position[1] - destination[1])
    return ran


def mana_check(char):
    if char.Mana >= char.Cost:
        return True
    else:
        print("Not enought mana!")
        return False
        
        
def mana_reduce(char):
    char.Mana -= char.Cost

#skills


# Battlemage
def warp_to_tile(char, destination):
    check = pos_check(char, destination)
    if check <= char.Skill_range:
        char.Position = destination
        mana_reduce(char)
    else:
        return False


# Granadier
def under_barrel(char_atk, char_def):
    check = range_check(char_atk, char_def)
    if check <= char_atk.Skill_range:
        if shield_skill(char_atk, char_def):
            char_def.HP -= char_atk.Skill_damage
        elif char_def.Name == 'Dancer':
          if nimble(char_def) == False:
            char_def.HP -= char_atk.Skill_damage
        mana_reduce(char_atk)
    else:
        return False


# Marksman
def critical_shot(char_atk, char_def):
    check = range_check(char_atk, char_def)
    if check <= char_atk.Skill_range:
        if shield_skill(char_atk, char_def):
            char_def.HP -= char_atk.Skill_damage
        elif char_def.Name == 'Dancer':
          if nimble(char_def) == False:
            char_def.HP -= char_atk.Skill_damage
        mana_reduce(char_atk)
    else:
        return False


def nimble(char):
  chance = random.randint(0, 100)
  if chance > char.Skill_damage:
    return False
  else:
    return True


# Sheriff
def high_noon(char_atk, char_def_list):
    print('random 6 targets')
    for i in range(6):
        target = char_def_list[random.randint(0, len(char_def_list)-1)]
        if shield_skill(char_atk, target):
            target.HP -= char_atk.Skill_damage
        elif target.Name == 'Dancer':
          if nimble(target) == False:
            target.HP -= char_atk.Skill_damage
        print(target.HP)
    mana_reduce(char_atk)


# Flagellants
def salvation(char_atk, char_def, current_ally):
    death = 5 - current_ally
    check = range_check(char_atk, char_def)
    if check <= char_atk.Skill_range:
        damage = (char_atk.Skill_damage) + (10 * death)
        if shield_skill(char_atk, char_def, damage):
            char_def.HP -= (char_atk.Skill_damage) + (10 * death)
        elif char_def.Name == 'Dancer':
          if nimble(char_def) == False:
            char_def.HP -= damage
        mana_reduce(char_atk)
    else:
        return False


# Hospitalier
def heal(healer, patient):
    patient.HP += healer.Skill_damage
    mana_reduce(healer)
    return True


# Reset every turn
def reset_stamina(chars):
  for character in chars:
    character.Stamina = character.Movement


# Shield
def shield(char):
  char.Shield = char.Skill_damage
  mana_reduce(char)


def check_shield(char):
    if char.Shield > 0:
        return True
    return False


def shield_skill(char_atk, char_def, dmg = 0):
    if check_shield(char_def):
        if dmg != 0:
            char_def.Shield -= dmg
        else:
            char_def.Shield -= char_atk.Skill_damage
        if char_def.Shield < 0:
            char_def.HP += char_def.Shield
            char_def.Shield = 0
        return False
    return True


 # Trapper
def trap(char, place):
    check = pos_check(char, place)
    if check <= char.Skill_range:
        mana_reduce(char)
        print("Trapped")
        return True 
    else:
        return False
