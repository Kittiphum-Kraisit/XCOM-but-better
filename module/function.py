import random as r


def attack_range_check(char_atk, char_def_list):
    char_enemy = []
    for enemy in char_def_list:
        check = range_check(char_atk, enemy)
        if check <= char_atk.Atk_range and enemy.Invisible == 0:
            char_enemy.append(enemy)
    return char_enemy


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
            if char_def.shield < 0:
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


def move(char, destination, board):
    check = pos_check(char, destination)
    if check <= char.Stamina:
        if board[destination[0]][destination[1]] == '':
            char.Stamina -= check
            return True
        if board[destination[0]][destination[1]] == 't':
            char.HP -= 50
            char.Stamina -= check
            return True
    return False


def check_death(char, team):
    if char.HP <= 0:
        return team.remove(char)
    elif char.HP > 0:
        return team


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
  chance = r.randint(0, 100)
  if chance > char.Skill_damage:
    return False
  else:
    return True


# Sheriff
def high_noon(char_atk, char_def_list):
    print('choose 6 targets')
    for i in range(6):
        for j in range(0,len(char_def_list)):
            print(str(j) + ':' + str(char_def_list[j].Name))
        if i+1 == 1:
            x = 'st'
        elif i+1 == 2:
            x = 'nd'
        elif i+1 == 3:
            x = 'rd'
        else:
            x = 'th'
        print('choose '+ str(i+1) + x + ' target')
        target = char_def_list[int(input())]
        if shield_skill(char_atk, target):
            target.HP -= char_atk.Skill_damage
        elif target.Name == 'Dancer':
          if nimble(target) == False:
            target.HP -= char_atk.Skill_damage
        print(target.HP)
        check_death(char_def_list[i], char_def_list)
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
