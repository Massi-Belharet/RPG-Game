import sys
import os
import random
import time
import pickle

from Player import Player
from Enemy import Enemy


###### MAP   #######

    #     x = 0     x = 1   x = 2      x = 3          x = 4         x = 5       x = 6
map = [["accueil",  "opr",  "opr",  "pharmacie",  "laboratoire",  "terasse",  "urgences"], # y = 0
       ["laboratoire",  "laboratoire",  "laboratoire",  "laboratoire",  "laboratoire",   "consultation",  "terasse"], # y = 1
       ["laboratoire",   "bureau",   "cafeteria",   "opr",    "chambre",  "laboratoire",    "consultation"], # y = 2
       ["opr",   "pharmacie",   "opr",   "chambre",   "opr",   "consultation",  "terasse"], # y = 3
       ["opr",  "consultation",   "bureau",   "opr",   "consultation", "terasse",  "terasse"]] # y = 4

y_len = len(map)-1
x_len = len(map[0])-1

zone = {
    "opr": {
        "zone_name": "SALLE D'OPERATION",
        "e": True},
    "laboratoire": {
        "zone_name": "LABORATOIRE",
        "e": True},
    "terasse": {
        "zone_name": "TERASSE",
        "e": True},
    "consultation": {
        "zone_name": "SALLE DE CONSULTATION",
        "e": True},
    "urgences": {
        "zone_name": "LES URGENCES",
        "e": False},
    "chambre": {
        "zone_name": "CHAMBRE",
        "e": False},
    "bureau": {
        "zone_name": "BUREAU DE MEDECIN",
        "e": False},
    "cafeteria": {
        "zone_name": "CAFETERIA",
        "e": True},
    "pharmacie": {
        "zone_name": "PHARMACIE",
        "e": False},
    "accueil": {
        "zone_name": "ACCUEIL",
        "e": False,
    }
}



#### Afficher la localisation ####

def print_location():
    clear()
    draw()
    print("LOCATION: " + zone[map[player_1.y][player_1.x]]["zone_name"])
    print("CORD: (" + str(player_1.x) + "," + str(player_1.y) + ")")
    draw()

#### Soin ####

def heal(hp):
    global ready,object_func
    if player_1.health + hp < player_1.maxhealth:
        player_1.health += hp
    else:
        player_1.health = player_1.maxhealth
    print("la santé de "+ str(player_1.name) + "est rechargée à "+ str(player_1.health) + "!")
    input(">")
    if battle:
        fight()
    else:
        object_func=False
        ready = False
        play()

#### Magasin ####

def store():
    global ready,object_func
    clear()
    draw()
    print("Bienvenue au Magasin !")
    draw()
    print("GOLD: " + str(player_1.gold))
    print("PANSEMENTS: " + str(player_1.pots))
    print("ARME: "+ str(player_1.curweap))
    draw()
    print("1 - ACHETER DES PANSEMENTS (30HP) - 10 GOLD")
    print("2 - ACHETER NOKIA 3310 - 20 GOLD")
    print("3 - ACHETER UN FUSIL À POMPE - 30 GOLD")
    print("4 - SORTIR")
    draw()

    choice = input(">")
    if choice == "1":
        if player_1.gold >= 10:
            player_1.pots +=1
            player_1.gold -=10
            print("Vous avez acheté un Pansement!")
        else:
            print("Gold est insuffisant!")
        input("> ")
        store()
    elif choice=="2":
        if player_1.gold >=20:
            player_1.gold -=20
            player_1.weap.append("NOKIA 3310")
            print("Vous avez acheté un NOKIA 3310")
        else:
            print("Gold est insuffisant!")
        input("> ")
        store()
    elif choice=="3":
        if player_1.gold >=30:
            player_1.gold -=30
            player_1.weap.append("FUSIL À POMPE")
            print("Vous avez acheté un FUSIL À POMPE")
        else:
            print("Gold est insuffisant!")
        input("> ")
        store()
    elif choice=="4":
        object_func=False
        ready = False
        play()
    else:
        store()

#### Inventaire ####

def inventory():
    global ready,object_func
    i=1
    arm_numbers={}
    clear()
    draw()
    print("INVENTORY")
    draw()
    for weapon in player_1.weap:
        print(str(i)+" -",weapon)
        arm_numbers[weapon]=i
        i+=1
    print(str(i)+" - SORTIR")
    draw()
    choice= input(">")
    for key, value in arm_numbers.items():
        if choice == str(value):
            if player_1.curweap == key:
                print("Vous avez déjà équipé l'arme")
                input(">")
                inventory()
            else:
                player_1.curweap = key
                player_1.atck_upg()
                print("Vous avez équipé un " +str(player_1.curweap))
                input(">")
                inventory()
    if choice == str(i):
        if battle:
            fight()
        else:
            object_func = False
            ready = False
            play()
    else:
        inventory()

#### Combat ####

def fight():
    global ready,battle,object_func
    if map[player_1.y][player_1.x] == "urgences":
        enemy=boss
    else:
        enemy=zombie
    while battle:
        while player_1.health > 0 and enemy.health > 0:
            clear()
            draw()
            print("    Vaincre le "+ enemy.name + "!")
            draw()
            print(enemy.name + "'s HP: " + str(enemy.health) + "/" + str(enemy.maxhealth))
            print(player_1.name + "'s HP: " + str(player_1.health) + "/" + str(player_1.maxhealth))
            print("PANSEMENTS: "+str(player_1.pots))
            print("ARME: "+str(player_1.curweap))
            draw()
            print("1 - ATTAQUER")
            if player_1.pots > 0:
                print("2 - UTILISER LE PANCEMENT (20HP)")
            print("3 - INVENTAIRE")


            choice=input(">")
            if choice=="1":
                player_1.attack(enemy)
                if enemy.health > 0:
                    enemy.attack(player_1)
                input(">")
                fight()
            elif choice == "2":
                if player_1.pots > 0:
                    player_1.pots -= 1
                    heal(20)
                else:
                    print("Vous avez pas des pancements !")
                input(">")
                fight()
            elif choice =="3":
                inventory()
        if player_1.health <= 0:
            print("le "+str(enemy.name)+" vous a battu !")
            draw()
            print("GAME OVER")
            input(">")
            clear()
            main()
        if enemy.health <= 0:
            print(str(player_1.name)+" a battu le "+str(enemy.name)+"!")
            draw()
            player_1.lvl +=1
            player_1.gold +=enemy.goldgain
            print("Vous avez trouvé " + str(enemy.goldgain) + " gold!")
            if enemy == boss:
                draw()
                print("Félicitations, vous avez terminé le jeu!")

            input(">")
            object_func=False
            ready = False
            battle=False
            clear()
            if enemy ==boss:
                menu()
            else:
                play()

#### Medecin ####

def medecin():
    global ready,object_func
    clear()
    draw()
    print("Medecin: Salut "+str(player_1.name)+"!")
    if player_1.lvl < 5:
        speech1="Medecin: Vous n'êtes pas encore assez fort pour affronter le boss! Continuez à combattre les zombies et Revenez plus tard pour avoir la clé des urgences!.\n"
        speech2="Medecin: Il faut atteindre le niveau 5 ou plus.\n"
        for character in speech1:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(0.05)
        for character in speech2:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(0.05)
        player_1.boss_fight = False
    else:
        speech3="Medecin: Tenez la clé.\n"
        speech4="Medecin: C'est le temps pour affronter le boss!.\n"
        for character in speech3:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(0.05)
        for character in speech4:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(0.05)
        player_1.boss_fight = True
    draw()
    print("1 - SORTIR")
    draw()
    choice = input(">")
    if choice == "1":
        ready = False
        object_func = False
        play()
    else:
        medecin()

#### Le Boss ###

def bossfight():
    global battle,ready,object_func
    clear()
    if player_1.lvl >= 5 and player_1.boss_fight==True:
        speech1="Le Boss: Tu n'auras jamais le vaccin !!!\n"
        for character in speech1:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(0.05)
        input(">")
        battle = True
        fight()
    elif player_1.lvl >= 5 and player_1.boss_fight==False:
        print("Allez voir le medecin pour ramener la clé\n")
        print("1 - SORTIR")
        choice = input(">")
        if choice == "1":
            ready = False
            object_func = False
            play()
        else:
            bossfight()
    elif player_1.lvl < 5:
        print("Vous n'êtes pas encore prêt pour affronter le boss.\n")
        print("1 - SORTIR")
        choice = input(">")
        if choice == "1":
            ready = False
            object_func = False
            play()
        else:
            bossfight()


def find_object():
    if random.randint(1,2)==1:
        player_1.pots += 1
        print("Vous avez Trouvé un Pansement!")
    else:
        g=random.randint(1,5)
        player_1.gold+=g
        print("Vous avez trouvé " + str(g) + " gold!")


#### Clear Page ####

def clear():
    os.system('cls||clear')


#### Enregistrement ####

def save():
    global player_1
    clear()
    with open("savefile", "wb") as f:
        pickle.dump(player_1, f)
        print("Game has been saved")
    input(">")
    clear()
    main()


#### Quitter le jeu ####

def exit():
    sys.exit()

#### Main Page ####

def main():
    print("############################")
    print("          RPG GAME !        ")
    print("############################")
    menu()

#### Menu ####

def menu():
    global player_1
    print("MAIN MENU:")
    print("1-Create New Game")
    print("2-Load Saved Game")
    print("3-About")
    print("4-Exit\n")
    print("Note: For best experience, use the console.")
    choix = input(">")
    if choix == "1":
        startgame()
    elif choix == "2":
        clear()
        if os.path.exists("savefile") == True:
            with open("savefile", "rb") as f:
                player_1 = pickle.load(f)
            print("Welcome back "+str(player_1.name)+" !")
            input(">")
            clear()
            play()
        else:
            print("You have no save file")
            input(">")
            clear()
            main()

    elif choix== "3":
        clear()
        about()
    elif choix == "4":
        exit()
    else:
        clear()
        main()


def about():
    print("******** PROJET FAIT PAR ********")
    print("--BELHARET MASSINISSA--")
    print("--OZCELIK MELIH--")
    print("--BAH MAMADOU ATIGOU--")
    print("--AKIL MOURAD--")
    print("--BEN KHALED NADHIR--")
    print("*********************************")
    input(">")
    clear()
    main()

#### Lancement de jeu ####
def startgame():
    global object_func
    global sound_btn
    clear()
    print("Donnez votre nom:")
    nom = input(">")
    global player_1
    player_1 = Player(nom)
    global boss
    boss = Enemy("Boss",150,20,8,20)
    clear()
    story()
    input(">")
    object_func=False
    play()

#### Histoire de jeu ####

def story():
    clear()
    speech1="Il y’a un virus contagieux qui a atteint la ville et ce virus transforme les gens en un truc de zombie !!!\n"
    speech2="Il y’a un vaccin qui se trouve à l'hôpital et qui peut guérir tout le monde.\n"
    speech3=f"C'est à vous {player_1.name} de trouver le vaccin.\n"


    for character in speech1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)

    for character in speech2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)

    for character in speech3:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)


def draw():
    print("}≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈{")

#### Informations sur le joueur ####

def player_stats():
    print("NOM:", player_1.name," LVL "+str(player_1.lvl))
    print("HP:" + str(player_1.health) + "/" + str(player_1.maxhealth))
    print("GOLD:" + str(player_1.gold))
    print("PANSEMENTS:" + str(player_1.pots))
    print("ARME: " + str(player_1.curweap))
    draw()

ready = False    #être prêt pour le combat
battle = False

#### Jeu ####

def play():
    global battle,ready,object_func
    if ready:
        if zone[map[player_1.y][player_1.x]]["e"]:
            if random.randint(0,100)<30:
                hp=random.randrange(30,80,10)
                atk=random.randint(6,10)
                df=random.randint(4,8)
                Gg= random.randint(5,10)
                global zombie
                zombie=Enemy("Zombie",hp,atk,df,Gg)
                battle=True
                fight()

    print_location()
    player_stats()
    print("0 - SAVE AND QUIT")
    if player_1.y > 0:
        print("1 - NORD")
    if player_1.x < x_len:
        print("2 - EST")
    if player_1.y < y_len:
        print("3 - SUD")
    if player_1.x > 0:
        print("4 - OUEST")
    if player_1.pots > 0:
        print("5 - UTILISER LE PANCEMENT (30HP)")
    print("6 - INVENTORY")
    if map[player_1.y][player_1.x] == "pharmacie" or map[player_1.y][player_1.x] == "bureau" or map[player_1.y][player_1.x] == "urgences":
        print("7 - ENTRER")
    draw()
    chance = random.randint(1,100)
    if object_func:
        if map[player_1.y][player_1.x] != "pharmacie" and chance < 40:
            find_object()

    choice =input(">")

    if choice == "0":
        save()
    if choice == "1":
        if player_1.y > 0:
            player_1.y -=1
            object_func = True
            ready=True
            play()
        else:
            play()
    elif choice == "2":
        if player_1.x <x_len:
            player_1.x +=1
            object_func = True
            ready = True
            play()
        else:
            play()
    elif choice == "3":
        if player_1.y < y_len:
            player_1.y += 1
            ready = True
            object_func = True
            play()
        else:
            play()
    elif choice == "4":
        if player_1.x > 0:
            player_1.x -=1
            ready = True
            object_func = True
            play()
        else:
            play()
    elif choice == "5":
        if player_1.pots > 0:
            player_1.pots -= 1
            heal(30)
        else:
            print("Vous avez pas des pancements !")
        input(">")
        ready = False
        play()
    elif choice == "6":
        ready = False
        inventory()
    elif choice == "7":
        if map[player_1.y][player_1.x] == "pharmacie":
            store()
        elif map[player_1.y][player_1.x] == "bureau":
            medecin()
        elif map[player_1.y][player_1.x] == "urgences":
            bossfight()
        else:
            play()
    else:
        object_func=False
        ready=False
        play()
