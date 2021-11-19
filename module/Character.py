import json
import pygame

# get data from JSON file
f = open('module/characters.json', )
data = json.load(f)


# a class for Characters
class Character:
    def __init__(self, name, hp, mana, sta, atk_dam, atk_ran, skl_name, skl_dam, skl_ran, cost, spd, team):
        self.Name = name
        self.HP = hp
        self.Max_HP = hp
        self.Mana = mana
        self.Max_Mana = mana
        self.Movement = sta
        self.Stamina = sta
        self.Atk_damage = atk_dam
        self.Atk_range = atk_ran
        self.Skill_name = skl_name
        self.Skill_damage = skl_dam
        self.Skill_range = skl_ran
        self.Cost = cost
        self.Speed = spd
        self.Team = team
        self.Invisible = 0
        self.Shield = 0
        self.CurrSpeed = 0
        self.Position = 0
        path = f"pic/Icon/{name}.png"
        self.Icon = pygame.image.load(path)
        self.equip = None

    def set_currspeed(self, initvalue):
        self.CurrSpeed = self.Speed + initvalue
    
    def set_team(self, team):
        self.Team = team
    
    def set_position(self, array):
        self.Position = array

    def __str__(self):
        return str(self.Team)


# create an instance of Character
def obj_char_create(n, team):
    return Character(data[n]['name'], data[n]['health'], data[n]['mana'],
                     data[n]['stamina'], data[n]['atk_damage'],
                     data[n]['atk_range'], data[n]['skill_name'],
                     data[n]['skill_damage'], data[n]['skill_range'],
                     data[n]['mana_cost'], data[n]['speed'], team)


# Create 5 characters and assign them to a team
def choose_char(a, team):
    ret = []
    for i in range(len(a)):
        ret.append(obj_char_create(str(a[i]), team))
    return ret
