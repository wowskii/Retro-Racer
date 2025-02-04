import pyxel
import random
import pygame
# taille de la fenêtre 128x128 pixels et titre

pyxel.init(64, 64, title = "Retro Racer")


started = False

# position initiale du vaisseau
# (origine des positions : coin haut gauche)
vaisseau_x = 28
vaisseau_y = 32

# initialisation des tirs
tirs_liste = []

# initialisation des ennemis
ennemis_liste = []

# vies
vies = 3

score_value = 0

# initialisation des explosions
explosions_liste = []


bulldozer_powerup_liste = []

coeur_liste = []

bulldozer = False
bulldozer_warning = False

ult = False
ult_lvl = 0


premier_fait = False
coeur_premier_fait = False

display_50 = False

stringscore = ""

# defilement
scroll_y = 0

speed = 16
tempspeed = speed
n = 0
btimer = 0
utimer = 0
ecount = 0
score_give_count = 0
compteur_display_50 = 0

# chargement des images
pyxel.load("jeu_voitures.pyxres")


#musique
pygame.init()
music = pygame.mixer.Sound("musique.mp3")
music.set_volume(0.1)
music.play(-1)

#pyxel. playm(0, 0, True)
#def init():
    


def voiture_deplacement(x, y):
    """déplacement avec les touches de directions"""
    global ult, ult_lvl, bulldozer
    
    if pyxel.btn(pyxel.KEY_D) and (x < 45) and bulldozer == True:        
            x = x + 1
    if pyxel.btn(pyxel.KEY_D) and (x < 49) and bulldozer == False:        
            x = x + 1
    if pyxel.btn(pyxel.KEY_A) and (x > 11):        
            x = x - 1
    if pyxel.btn(pyxel.KEY_S) and (y < 56): 
            y = y + 1
    if pyxel.btn(pyxel.KEY_W) and (y > 0):
            y = y - 1
            
    if pyxel.btn(pyxel.KEY_RIGHT) and (x < 45) and bulldozer == True:        
            x = x + 1
    if pyxel.btn(pyxel.KEY_RIGHT) and (x < 49) and bulldozer == False:        
            x = x + 1
    if pyxel.btn(pyxel.KEY_LEFT) and (x > 11):        
            x = x - 1
    if pyxel.btn(pyxel.KEY_DOWN) and (y < 56): 
            y = y + 1
    if pyxel.btn(pyxel.KEY_UP) and (y > 0):
            y = y - 1
            
    if pyxel.btn(pyxel.KEY_SPACE) and ult == False and ult_lvl >= 15000:
        ult = True
        ult_lvl = 0
        print(ult)
        
    return x, y

def scroll(scroll_y):
    """defilement du décor"""
    if scroll_y > 64:
        scroll_y -= speed/10
    else :
        scroll_y = 192
    return scroll_y

def score():
    global score_value, score_give_count
    score_give_count += 1
    if score_give_count == 5:
        score_value += 1
        score_give_count = 0
    #print(score_value)
        
    return score_value

def afficher_score(score_value):
    stringscore = str(score_value)
    for i in range(4-len(stringscore)):
        stringscore = "0"+stringscore
        #print("fait")
    #print(stringscore)
    return stringscore

def explosions_creation(x, y):
    """explosions aux points de collision entre deux objets"""
    explosions_liste.append([x, y, 0])
    pyxel.play(3, 32, 0, False)


def explosions_animation():
    """animation des explosions"""
    for explosion in explosions_liste:
        explosion[2] +=1
        if explosion[2] == 12:
            explosions_liste.remove(explosion)




def bulldozer_powerup_creation():
    """création de powerups"""
    global premier_fait, bulldozer
    if (pyxel.frame_count % 400 == 0) and premier_fait == False:
        premier_fait = True
    
    if (pyxel.frame_count % 400 == 0) and premier_fait == True and bulldozer == False:
        rand = random.randint(0,1)
        if rand == 0:
            bulldozer_powerup_liste.append([random.randint(12, 46), 0])
        
def bulldozer_powerup_deplacement():
    """déplacement des ennemis vers le haut et suppression s'ils sortent du cadre"""

    for bpowerup in bulldozer_powerup_liste:
        bpowerup[1] += 0.8*(speed/10)
        if  bpowerup[1] > 128:
            bulldozer_powerup_liste.remove(bpowerup)
            
def coeur_creation():
    """création de powerups"""
    global coeur_premier_fait
    if (pyxel.frame_count % 500 == 0) and coeur_premier_fait == False:
        coeur_premier_fait = True
    
    if (pyxel.frame_count % 500 == 0) and coeur_premier_fait == True:
        rand = random.randint(0,1)
        if rand == 0:
            coeur_liste.append([random.randint(12, 46), 0])
            

def coeur_deplacement():
    """déplacement des ennemis vers le haut et suppression s'ils sortent du cadre"""

    for coeur in coeur_liste:
        coeur[1] += 0.8*(speed/10)
        if  coeur[1] > 128:
            coeur_liste.remove(coeur)


def coeur_activation(vies):
    """Activation et disparition des bpowerup si contact"""
    
    for coeur in coeur_liste:
        if coeur[0] <= vaisseau_x + 3 and coeur[1] <= vaisseau_y + 8 and coeur[0] + 8 >= vaisseau_x and coeur[1] + 7 >= vaisseau_y:
            coeur_liste.remove(coeur)
            vies += 1
            pyxel.play(3, 33, 0, False)
            print("+ 1")
    return vies


def ennemis_creation():
    """création aléatoire des ennemis"""
    global speed
    # un ennemi par seconde
    if (pyxel.frame_count % 20 == 0):
        ennemis_liste.append([random.randint(12, 48), -10])
    if (pyxel.frame_count % 15 == 0):
        if speed >= 20:
            ennemis_liste.append([random.randint(12, 48), -10])
    
        
def ennemis_deplacement():
    """déplacement des ennemis vers le haut et suppression s'ils sortent du cadre"""

    for ennemi in ennemis_liste:
        ennemi[1] += 0.8*(speed/10)
        if  ennemi[1] > 128:
            ennemis_liste.remove(ennemi)
            
            
'''def ennemis_selection():
    i = 0
    j = 0
    for i in range(len(ennemis_liste)):
        for j in range(0, i-1):
            if ennemis_liste[i][0] <= ennemis_liste[j][0] + 7 and ennemis_liste[i][1] <= ennemis_liste[j][1] + 8 and ennemis_liste[i][0] + 3 >= ennemis_liste[j][0] and ennemis_liste[i][1] + 8 >= ennemis_liste[j][1]:
                ennemis_liste.remove(ennemis_liste[j])'''

def speed_change(speed):
    global n, ult, tempspeed
    """increase the speed with time"""
    if ult == False:
        if speed<30:
            if n >= 500:
                speed += 2
                n = 0
                tempspeed = speed
                print("speed =",speed)
            else:
                n += 1
                #print("n =",n)
    return speed
    
    

def vaisseau_suppression(vies):
    """disparition du vaisseau et d'un ennemi si contact"""
    global score_value, display_50
    if bulldozer == False:
        for ennemi in ennemis_liste:
            if ennemi[0] <= vaisseau_x + 3 and ennemi[1] <= vaisseau_y + 8 and ennemi[0] + 3 >= vaisseau_x and ennemi[1] + 8 >= vaisseau_y:
                vies = vies -1
                ennemis_liste.remove(ennemi)
                pyxel.play(3, 34, 0, False)
                # on ajoute l'explosion
                #explosions_creation(vaisseau_x, vaisseau_y)
    else:
        for ennemi in ennemis_liste:
            if ennemi[0] <= vaisseau_x + 7 and ennemi[1] <= vaisseau_y + 8 and ennemi[0] + 3 >= vaisseau_x and ennemi[1] + 8 >= vaisseau_y:
                explosions_creation(ennemi[0] - 2, ennemi[1] - 2)
                ennemis_liste.remove(ennemi)
                score_value += 50
                display_50 = True
                # on ajoute l'explosion
                #explosions_creation(vaisseau_x, vaisseau_y)

    return vies


def bpowerup_activation(bulldozer):
    """Activation et disparition des bpowerup si contact"""
    
    for bpowerup in bulldozer_powerup_liste:
        if bpowerup[0] <= vaisseau_x + 3 and bpowerup[1] <= vaisseau_y + 4 and bpowerup[0] + 3 >= vaisseau_x and bpowerup[1] + 4 >= vaisseau_y:
            bulldozer_powerup_liste.remove(bpowerup)
            bulldozer = True
            
    return bulldozer

def bulldozer_timer():
    global bulldozer, btimer, bulldozer_warning
    btimer+=1
    if btimer > 500:
        bulldozer = False
        btimer = 0

    
        
def ult_timer():
    global ult, utimer, speed, tempspeed
    utimer+=1
    speed = 2
    if utimer > 300:
        ult = False
        utimer = 0
        print(ult)
        speed = tempspeed
        print(tempspeed)

def ult_lvl_change(ult_lvl):
    if ult_lvl < 15000:
        ult_lvl += 10
        #print(ult_lvl)
    return ult_lvl



def update():
    global vaisseau_x, vaisseau_y, speed, vies, bulldozer, score_value, stringscore, ult_lvl, tempspeed, started
    if started == True:
        #déplacement de la voiture
        vaisseau_x, vaisseau_y = voiture_deplacement(vaisseau_x, vaisseau_y)

        # creation des ennemis
        if ult == False:
            ennemis_creation()

        # mise a jour des positions des ennemis
        ennemis_deplacement()
        
        #ennemis_selection()
        
        #increasing speed
        speed = speed_change(speed)
        
        # suppression du vaisseau et ennemi si contact
        vies = vaisseau_suppression(vies)
        
        vies = coeur_activation(vies)
        #print(vies)
        
        # evolution de l'animation des explosions
        explosions_animation()
        
        #coeurs
        
        #création de coeurs
        coeur_creation()
        
        #déplacement des coeurs
        coeur_deplacement()
        
        #coeur_activation(vies)
        
        #bpowerups------------------------------------------------------------------------------------
        #création de bpowerups
        bulldozer_powerup_creation()
        
        #déplacement des powerups
        bulldozer_powerup_deplacement()
        
        #activation des bpowerup
        bulldozer = bpowerup_activation(bulldozer)
        
        if bulldozer == True:
            bulldozer_timer()
            
        
        if ult == True:
            ult_timer()
            
        else:
            ult_lvl = ult_lvl_change(ult_lvl)

                
        
        
            
        #score
        score_value = score()
        stringscore = afficher_score(score_value)
        

        if vies == 0:
            started = False
        
    else:
        pyxel.run(startscreen_update, startscreen_draw)

def draw():
    """création des objets (30 fois par seconde)"""
    global scroll_y, stringscore, display_50, compteur_display_50, ult_lvl, utimer, started, btimer
    if started == True:
        # vide la fenetre
        pyxel.cls(0)

        # si le vaisseau possede des vies le jeu continue
        if vies > 0:
            
            
            
            # affichage du décor
            pyxel.camera()
               
            pyxel.bltm(0, 0, 0, 192, (scroll_y // 4) % 128, 128, 128)
            pyxel.bltm(0, 0, 0, 0, scroll_y,  128, 128, 0)

            # vaisseau (carre 8x8)
            if bulldozer == True:
                if btimer < 470:
                    pyxel.blt(vaisseau_x, vaisseau_y, 0, 24, 0, 8, 8)
                else:
                    pyxel.blt(vaisseau_x, vaisseau_y, 0, 24, 8, 8, 8)
            else:
                pyxel.blt(vaisseau_x, vaisseau_y, 0, 2, 0, 4, 8)
            
            
            for ennemi in ennemis_liste:
                pyxel.blt(ennemi[0], ennemi[1], 0, 2, 8, 4, 8)
                
            for bpowerup in bulldozer_powerup_liste:
                pyxel.blt(bpowerup[0], bpowerup[1], 0, 58, 2, 4, 4)
            
            #coeurs
            for coeur in coeur_liste:
                pyxel.blt(coeur[0], coeur[1], 0, 40, 0, 8, 7)
            
            # explosions (cercles de plus en plus grands)
            for explosion in explosions_liste:
                pyxel.circb(explosion[0]+4, explosion[1]+4, 2*(explosion[2]//4), 8+explosion[2]%3)
                
            #afficher le score
            #cadre pour le score
            pyxel.blt(0, 0, 0, 0, 48, 17, 7)
            #score
            for scoreplace in range(0, 4):
                pyxel.blt(1+4*scoreplace, 1, 0, int(stringscore[scoreplace])*4, 40, 3, 5)

            
            #affichage des coeurs
            for viesplace in range(1, 8):
                if vies >= viesplace:
                    pyxel.blt(1, 10+5*viesplace, 0, 32, 0, 5, 4)


            
            
            if display_50 == True:
                if compteur_display_50 < 10:
                    compteur_display_50+=1
                    pyxel.blt(1, 9, 0, 0, 57, 11, 5)
                    #print("display")
                else:
                    display_50 = False
                    compteur_display_50=0
                    
                    
            #afficher la barre de ult
            pyxel.blt(61, 0, 0, 45, 56, 3, 32)
            
            for i in range(0, 15000, 500):
                if ult_lvl > i:
                    pyxel.blt(62, 30-(i/500), 0, 0, 24, 1, 1)
                    
            if ult == True:
                for u in range(0, 300, 10):
                    if utimer < u:
                        pyxel.blt(62, 1+(u/10), 0, 0, 24, 1, 1)

            
        scroll_y = scroll(scroll_y)
        


    
    
    
def startscreen_update():
    global started, vies, ult_lvl, speed, score_value, ennemis_liste
    if started == False:
        if pyxel.btn(pyxel.KEY_RETURN):
            started = True
            vies = 3
            ult_lvl = 0
            speed = 16
            score_value = 0
            ennemis_liste = []
        
    else:
        pyxel.run(update, draw)
            
    #print("working")
    
def startscreen_draw():
    global scroll_y, ecount
    if started == False:
        # affichage du décor
        pyxel.camera()
        
        pyxel.bltm(0, 0, 0, 192, (scroll_y // 4) % 128, 128, 128)
        pyxel.bltm(0, 0, 0, 0, scroll_y,  128, 128, 0)
        
        #enter
        if ecount < 15:
            pyxel.blt(18, 26, 0, 7, 87, 28, 7)
            ecount += 1
        elif ecount < 30:
            ecount += 1
        else:
            ecount = 0
        
        #tuto
        #pyxel.blt(32, 56, 0, 0, 104, 31, 7)
        #retro racer
        pyxel.blt(14, 5, 0, 0, 120, 36, 19)
        scroll_y = scroll(scroll_y)




pyxel.run(startscreen_update, startscreen_draw)

