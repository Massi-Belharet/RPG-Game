
import random

class Player:
    def __init__(self,name):
        self.name = name
        self.maxhealth = 100
        self.health = self.maxhealth
        self.attack_pwr = 10
        self.defense = 4
        self.gold = 0
        self.pots = 0
        self.weap = ["COUTEAU"]
        self.curweap = "COUTEAU"
        self.lvl=1
        self.boss_fight = False
        self.x = 0
        self.y = 0

    def attack(self,target):
        damage = self.attack_pwr - target.defense
        chance=random.randint(1,5)
        if chance == 5:
            print(f"Attaque Manquée par {self.name} !")
        else:
            target.health -= damage
            print(f"{self.name} a attaqué le {target.name} pour ({damage}HP) dégâts")

    def atck_upg(self):
        if self.curweap == "COUTEAU":
            self.attack_pwr = 10
        elif self.curweap == "NOKIA 3310":
            self.attack_pwr = 15
        elif self.curweap == "FUSIL À POMPE":
            self.attack_pwr = 30