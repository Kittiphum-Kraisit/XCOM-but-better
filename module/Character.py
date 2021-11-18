import json
import pygame

# get data from JSON file
f = open('module/characters.json', )
data = json.load(f)

# a class for Characters
class Character:
    def __init__(self, name, HP, Mana, Sta, Atk_dam, Atk_ran, Skl_name, Skl_dam, Skl_ran, Cost, Spd, team):
        self.Name = name
        self.HP = HP
        self.Max_HP = HP
        self.Mana = Mana
        self.Max_Mana = Mana
        self.Movement = Sta
        self.Stamina = Sta
        self.Atk_damage = Atk_dam
        self.Atk_range = Atk_ran
        self.Skill_name = Skl_name
        self.Skill_damage = Skl_dam
        self.Skill_range = Skl_ran
        self.Cost = Cost
        self.Speed = Spd
        self.Team = team
        self.Invisible = 0
        self.Shield = 0
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