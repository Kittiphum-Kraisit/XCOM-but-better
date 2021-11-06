import pygame.image
import math


class Equipment:
    def __init__(self, name, description, image):
        self.name = name
        self.description = description
        self.img = pygame.image.load(f"pic/equipment/{image}")

    def vampire_knife(self, owner):
        owner.HP += math.floor((5/100)*owner.Atk_damage)

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

