import random

class Enemy:
    def __init__(self,name,maxhealth,attack_pwr,defense,goldgain):
        self.name = name
        self.maxhealth = maxhealth
        self.health = self.maxhealth
        self.attack_pwr = attack_pwr
        self.defense = defense
        self.goldgain = goldgain

    def attack(self, target):
        damage = self.attack_pwr - target.defense
        chance =random.randint(1,5)
        if chance ==5:
            print(f"Attaque Manquée par le {self.name} !")
        else:
            target.health -= damage
            print(f"Le {self.name} a attaqué {target.name} pour ({damage}HP) dégâts")