import pygame
import random
import math

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


#title and icon
pygame.display.set_caption("space invaders")

icon = pygame.image.load('logo_3.png')
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change=0


#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 6 


for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,60))
    enemyX_change.append(4)
    enemyY_change.append(40)


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

text_X = 10
text_Y = 10


#game over text
over_font = pygame.font.Font('fonty.ttf',64)



def show_score(x,y):
    score = font.render("score : " + str(score_value),True, (255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER",True, (255,255,255))
    screen.blit(over_text,(200,250))



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
            game_over_text()
            break



        enemyX[i] += enemyX_change[i]
        if enemyX[i]<=0:
            enemyX_change[i] = 1.2
            enemyY[i] += enemyY_change[i]        
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1.2
            enemyY[i] += enemyY_change[i]

            #collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value+=1
            print(score_value)
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
    
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



