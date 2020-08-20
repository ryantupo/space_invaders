import pygame
import random
import math
from datetime import datetime
import time
import threading


#plan

#make it so space invaders die - done
#i want there to be a specific amount of enemies for level 1
# they move like the old space invaders - done
#make the other types of space invaders == different points

#make a flash spirite when you kill an invader

#enemy details
enemyImg, enemyX, enemyY, enemyX_change, enemyY_change = [],[],[],[],[]

from pygame import mixer
# this inmitializes the pygame
pygame.init()


#create the screen
screen = pygame.display.set_mode((800,600))

#background
backgroundImg = pygame.image.load('space.png')


#background sound
#mixer.music.load('background.wav')
#mixer.music.play(-1)

#moving background
backgorundY_change=5
backgroundX=0
backgroundY=-9000

win_count = 0

#title and icon
pygame.display.set_caption("space invaders")

#icon = pygame.image.load('logo_3.png')
#pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change=0

number_of_enemies = 0
def add_enemies(number_of_ens,speed):
    #enemy
    global enemyImg, enemyX, enemyY, enemyX_change, enemyY_change,number_of_enemies
    number_of_enemies = number_of_ens
    x=0
    for i in range(number_of_ens):
        enemyImg.append(pygame.image.load('enemy.png'))
        
        if i <=8:
            enemyX.append((i+1)*64)
            enemyY.append(50)
        elif i>=9 and i<=16:
            x+=1
            enemyX.append((x)*64)
            enemyY.append(125)
        elif i==16:
            x=0
        elif i>=17 and i<=24:
            x+=1
            enemyX.append((x)*64)
            enemyY.append(200)
        enemyX_change.append(speed)
        enemyY_change.append(40)

def level_enemies_generator(level):
    if level == 0:
        add_enemies(8,7)
    #level 1 6 * 2 12 - speed 8 
    elif level == 1:
        add_enemies(12,8)
    #level 2 8 * 2 16 - speed 9
    elif level == 2:
        add_enemies(16,9) 
    #level 3 6 * 3 18 - speed 10
    elif level == 3:
        add_enemies(18,10)
    #level 4 8 * 3 24 - speed 11
    elif level == 4:
        add_enemies(24,11)
    #level 5 10 * 3 30 - speed 12
    elif level == 5:
        add_enemies(30,11)
    

#ready state means you cant see the bullet
# fire means the bullet is currently moving
#bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change=0
bulletY_change=10
bullet_state = "ready"

#score

score_value = 0
font = pygame.font.Font('fonty.ttf',32)

#what level?
level = 1

text_X = 10
text_Y = 10

fuck = False
#game over text
over_font = pygame.font.Font('fonty.ttf',64)
won_font = pygame.font.Font('fonty.ttf',64)
level_font = pygame.font.Font('fonty.ttf',64)

show_text =False

#text varibles
over_text = over_font.render("GAME OVER",True, (255,255,255))
won_text = won_font.render("YOU WON",True, (255,255,255))
level_text = level_font.render(f"Level {level}",True, (255,255,255))

def show_score(x,y):
    score = font.render("score : " + str(score_value),True, (255,255,255))
    screen.blit(score,(x,y))

def win_check():
    global fuck, win_count, time_counter, level, number_of_enemies
    dead_counter=0
    for i in enemyY:
        if i <=0:
            dead_counter+=1
    if dead_counter == (number_of_enemies):
        win_count+=1
        fuck = True
        level+=1
        time_counter = time.time()

def you_won_text():
    while True:
        global won_text
        global level
        while True:
            screen.blit(won_text,(200,250))
        level+=1
        return level

def game_over_text():
    x=0
    global show_text
    global over_text
    start_time = int(float(str(datetime.now()).split(":")[-1]))
    while x==0:
        screen.blit(over_text,(200,250))
        if int(float(str(datetime.now()).split(":")[-1])) - start_time >3:
            x+=1
            print(int(float(str(datetime.now()).split(":")[-1])))
            return x
    over_text = over_font.render("",True, (255,255,255))

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def background(x,y):
    screen.blit(backgroundImg,(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = (math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2))))
    if distance < 27:
        return True
    else:
        return False

def move_right():
    for i in range(len(enemyImg)):
        enemyY[i]+=enemyY_change[i]
        enemyX_change[i] = 1.2

def move_left():
    for i in range(len(enemyImg)):
        enemyY[i]+=enemyY_change[i]
        enemyX_change[i] = -1.2

#def game_reset():

            

            
won_thread = threading.Thread(target=you_won_text)
level_enemies_generator(level)

#infinate loop so the game keeps running 
running = True
while running:

    #rgb for background
    screen.fill((0,0,0))
    
    #background image
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #if keystroke is pressed check wether is right or left
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change-=0.15
        if event.key == pygame.K_RIGHT:
            playerX_change+=0.15

        if event.key == pygame.K_SPACE:
            if bullet_state is "ready":
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                #gets currenht x coordinate of spaceship[]
                bulletX=playerX
                fire_bullet(bulletX , bulletY)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerX_change = 0

    playerX += playerX_change
    enemyX += enemyX_change
    backgroundY += backgorundY_change

    background(backgroundX,backgroundY)
    player(playerX,playerY)
    show_score(text_X,text_Y)
    
    if fuck == False:
        win_check()
    elif time.time() - time_counter < 3:
        screen.blit(won_text,(200,250))
    elif (time.time() - time_counter > 3.5) and (time.time() - time_counter < 6):
        screen.blit(level_text,(200,250))
    else:
        level_enemies_generator(level)
        fuck = False


    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736

        #enemy movement

    for i in range(number_of_enemies):
        #game over
        if enemyY[i] > 440:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            game_over_timer = 0
            game_over_text()
        
            



        enemyX[i] += enemyX_change[i]
        if enemyX[i]<=0:
            move_right()      
        elif enemyX[i] >= 736:
            move_left()   

            #collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            #explosion_sound = mixer.Sound('explosion.wav')
            #explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value+=1
            print(score_value)
            enemyY[i]= -2000
#            enemyImg.pop(i)
#            enemyX.pop(i)
#            enemyY.pop(i)
#            enemyX_change.pop(i)
#            enemyY_change.pop(i)            


    
        enemy(enemyX[i], enemyY[i], i)

    #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change
        
    if backgroundY>=0:
        backgroundY=-9000

    #updates the screen
    pygame.display.update()
