import math
import random
from module.Equipment import Equipment


class bomb:
    def __init__(self, x, y):
        self.position = (x, y)
        # self.pic = bombpic
        self.Name = "bomb"


# check the attack range
def attack_range_check(char_atk, char_def_list):
    char_enemy = []
    for enemy in char_def_list:
        check = range_check(char_atk, enemy)
        if check <= char_atk.Atk_range and enemy.Invisible == 0:
            char_enemy.append(enemy)
    return char_enemy

# obstacle: obstacle + allies as positions in tuple


# get target in attack/skill range
def LoS(char_atk, char_list, table):
    enemies = []
    obstacles = []
    for unit in char_list:
        check = range_check(char_atk, unit)
        if check <= char_atk.Atk_range and unit.Invisible == 0 and unit.Team != char_atk.Team:
            enemies.append(unit)
            obstacles.append((unit.Position[1], unit.Position[0]))
        elif check <= char_atk.Atk_range and unit.Team == char_atk.Team and unit.Name != char_atk.Name:
            obstacles.append((unit.Position[1], unit.Position[0]))
    # for y in range(len(table)):
    #     for x in range(len(table[y])):
    for y in range(0, 10):
        for x in range(0, 10):
            ran = abs(char_atk.Position[0] - table[y][x].indexY) + abs(char_atk.Position[1] - table[y][x].indexX)
            if ran <= char_atk.Atk_range and table[y][x].obstacle == True:
                print(table[y][x].obstacle)
                obstacles.append((y, x))
    print("1st", obstacles)
    for i in enemies:
        print("2nd", i)
    return line_of_sight(char_atk, enemies, obstacles)


# check if the enemies in in the sight or not
def line_of_sight(char, enemies, obstacles):
    # Formula: y = (y1-y0/(x1-x0))*(x-x0) + y0
    y0, x0 = char.Position
    attackable = enemies.copy()
    print("3rd", obstacles)
    varx = 0
    for enemy in enemies:
        bug = []
        print("rounds", varx)
        varx += 1
        y1, x1 = enemy.Position
        print("x0,x1,y0,y1", x0, x1, y0, y1)

        xs = [x0 + x / 4 for x in range((x1 - x0) * 4)] if x1 > x0 \
            else [x1 + x / 4 for x in range((x0 - x1) * 4)]

        for x in xs:
            y = round(((y1 - y0) / (x1 - x0)) * (x - x0) + y0)
            bug.append((x, y))
            print((y, round(x)) != (y1, x1), (y, round(x)), enemy.Position)
            if (y, round(x)) != (y1, x1) and (x, round(y)) in obstacles:
                print("removed", round(x), y)
                print(enemy)
                attackable.remove(enemy)
                break
        if x1 == x0:
            ys = range(y0, y1) if y1 > y0 else range(y1, y0)
            for y in ys:
                print(y != y1, (y, round(x1)), enemy.Position)
                if y != y1 and (x1, y) in obstacles:
                    print(enemy)
                    attackable.remove(enemy)
                    break
        print(bug)
        continue
    for i in attackable:
        print(i.Name)
    return attackable


# check the skill range
def skill_range_check(caster, char_list):
    char_in_range = []
    for char in char_list:
        check = range_check(char, caster)
        if check <= caster.Skill_range:
            char_in_range.append(char)
    return char_in_range


# reduce shield or hp
def attack(char_atk, char_def):
    atk_power = char_atk.Atk_damage
    if char_atk.equip.type == "attack":
        method_to_call = getattr(Equipment, char_atk.equip.ability)
        method_to_call(char_atk.equip, char_atk)
    if char_def.equip.type == "defend":
        method_to_call = getattr(Equipment, char_def.equip.ability)
        atk_power = method_to_call(char_def.equip, atk_power)
    check = range_check(char_atk, char_def)
    if check <= char_atk.Atk_range:
        if check_shield(char_def):
            char_def.Shield -= atk_power
            if char_def.Shield < 0:
                char_def.HP += char_def.Shield
                char_def.Shield = 0
        elif char_def.Name == 'Dancer':
            if nimble(char_def) is False:
                char_def.HP -= atk_power
        else:
            char_def.HP -= atk_power
        return True
    else:
        return False


# move the characters
def charmove(char, new_index, old_index, table, surface, bomblist=None):
    check = pos_check(char, new_index)
    if check <= char.Stamina:
        x, y = new_index
        x1, y1 = old_index
        char.position = (x, y)
        if table[x][y].resident is not None and type(table[x][y].resident) != str and table[x][y].resident.name == "bomb":
            char.HP -= 50
            for i in range(len(bomblist)):
                if bomblist[i].position == (x, y):
                    bomblist.remove(bomblist[i])
        table[x1][y1].resident = None
        table[x][y].resident = char
        table[x][y].addpic(char.Icon, surface, (x, y), char.Team)


# check stamina
def move(char, destination, table, bomblist):
    x, y = destination
    check = pos_check(char, destination)
    if check <= char.Stamina:
        char.Stamina -= check
        lst = []
        print(lst)
        if table[y][x].resident is not None and type(table[y][x].resident) != str and table[y][x].resident.Name == "bomb":
            char.HP -= 50
            for i in range(len(bomblist)):
                if bomblist[i].position == (x, y):
                    bomblist.remove(bomblist[i])
        return True
    return False


# check death
def check_death(char):
    if char.HP <= 0:
        return True
    elif char.HP > 0:
        return False


# check range of the character to character
def range_check(char1, char2):
    ran = abs(char1.Position[0] - char2.Position[0]) + abs(char1.Position[1] - char2.Position[1])
    return ran


# check range of the character to destination
def pos_check(char, destination):
    ran = abs(char.Position[0] - destination[0]) + abs(char.Position[1] - destination[1])
    return ran


# check the mana
def mana_check(char):
    if char.Mana >= char.Cost:
        return True
    else:
        print("Not enought mana!")
        return False


# reduce mana
def mana_reduce(char):
    char.Mana -= char.Cost


# Skills
# Battlemage skill
def warp_to_tile(char, destination):
    check = pos_check(char, destination)
    if check <= char.Skill_range:
        char.Position = destination
        mana_reduce(char)
    else:
        return False


# Granadier skill
def under_barrel(char_atk, char_def):
    check = range_check(char_atk, char_def)
    if check <= char_atk.Skill_range:
        if shield_skill(char_atk, char_def):
            char_def.HP -= char_atk.Skill_damage
        elif char_def.Name == 'Dancer':
            if nimble(char_def) is False:
                char_def.HP -= char_atk.Skill_damage
        mana_reduce(char_atk)
    else:
        return False


# Marksman skill
def critical_shot(char_atk, char_def):
    check = range_check(char_atk, char_def)
    if check <= char_atk.Skill_range:
        if shield_skill(char_atk, char_def):
            char_def.HP -= char_atk.Skill_damage
        elif char_def.Name == 'Dancer':
            if nimble(char_def) is False:
                char_def.HP -= char_atk.Skill_damage
        mana_reduce(char_atk)
    else:
        return False


# Dancer skill
def nimble(char):
    chance = random.randint(0, 100)
    if chance > char.Skill_damage:
        return False
    else:
        return True


# Sheriff skill
def high_noon(char_atk, char_def_list):
    print('random 6 targets')
    for i in range(6):
        target = char_def_list[random.randint(0, len(char_def_list)-1)]
        if shield_skill(char_atk, target):
            target.HP -= char_atk.Skill_damage
        elif target.Name == 'Dancer':
            if nimble(target) is False:
                target.HP -= char_atk.Skill_damage
        print(target.HP)
    mana_reduce(char_atk)


# Flagellants skill
def salvation(char_atk, char_def, current_ally):
    death = 5 - current_ally
    check = range_check(char_atk, char_def)
    if check <= char_atk.Skill_range:
        damage = char_atk.Skill_damage + (10 * death)
        if shield_skill(char_atk, char_def, damage):
            char_def.HP -= char_atk.Skill_damage + (10 * death)
        elif char_def.Name == 'Dancer':
            if nimble(char_def) is False:
                char_def.HP -= damage
        mana_reduce(char_atk)
    else:
        return False


# Hospital skill
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


# check if there is a shield
def check_shield(char):
    if char.Shield > 0:
        return True
    return False


# Battle mage skill
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


# Trapper skill
def trap(char, place, table, trapPic, surface, bomblist):
    place2 = (place[1], place[0])
    check = pos_check(char, place2)
    print(0)
    print(check)
    print(char.Skill_range)
    if check <= char.Skill_range:
        print(1)
        mana_reduce(char)
        newBomb = bomb(place2[0], place2[1])
        table[place2[0]][place2[1]].resident = newBomb
        table[place2[0]][place2[1]].addpic(trapPic, surface, place2, 0)
        bomblist.append(newBomb)
        print("Trapped")
        return True 
    else:
        print(2)
        return False
