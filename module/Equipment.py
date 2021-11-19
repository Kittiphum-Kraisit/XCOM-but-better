import json

import pygame.image
import math

data = open('module/Equipment.json', )
equipment_data = json.load(data)


class Equipment:
    def __init__(self, name, description, e_type, image, ability):
        self.name = name
        self.description = description
        self.type = e_type
        self.img = pygame.image.load(f"pic/equipment/{image}")
        self.rect = self.img.get_rect()
        self.rect.center = (0, 0)
        self.clicked = False
        self.ability = ability

    def vampire_knife(self, owner):
        owner.HP += math.ceil((30/100)*owner.Atk_damage)

    def unstoppable_sword(self, owner):
        owner.Atk_damage += 10

    def immovable_armor(self, damage):
        return damage - 10

    def stim(self, owner):
        owner.HP += 10

    def battery(self, owner):
        owner.Mana += 5

    def shoes(self, owner):
        owner.Stamina += 2

    def scope(self, owner):
        owner.Atk_range += 1

    def visor(self, owner):
        owner.Speed += 10


def init_equipment(n):
    return Equipment(equipment_data[str(n)]['name'], equipment_data[str(n)]['description'],
                     equipment_data[str(n)]['type'], equipment_data[str(n)]['image'], equipment_data[str(n)]['ability'])
