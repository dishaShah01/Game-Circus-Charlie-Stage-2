import pygame
import random
import math
from pygame import mixer

#initialize the pygame
pygame.init()

#create screen
screen=pygame.display.set_mode((800,600))

#background
background=pygame.image.load('backgroundimage.png')
pygame.display.set_caption("Circus Charlie")
bx=-2

#background when game is won
bg=pygame.image.load('winner.png')

#background music
mixer.music.load('circus.mp3')
mixer.music.play(-1,2.5)

#game over text
font = pygame.font.SysFont('Comic Sans', 32, False,False)
over_font= pygame.font.SysFont('Comic Sans', 72, False,False)

#clownimages
walk=[pygame.image.load('clownsprite2.png'),pygame.image.load('clownsprite1.png'),pygame.image.load('clownsprite3.png')]
jumping=pygame.image.load('clownjump.png')
dead=pygame.image.load('gameover.png')   
x=0
y=234

def create_background():
    global bx
    #background colour(r,g,b)
    screen.fill((128,128,128))
    #background
    screen.blit(background,(bx,0))    
    name=font.render("Circus Charlie",True,(255,255,255))
    screen.blit(name,(330,20))

clock=pygame.time.Clock()

width=64
height = 64
vel = 7
gameover=False
iswon=False
isJump = False
jumpCount = 10
run=True
leftright=False
walkcount=0
monkeywalkcount=0

#function to be called when game is over or if the player has won
def gameovert(iswon,gameover):
    global run    
    run=False#stop running the game loop    
    create_background()    
    
    if iswon and gameover==False:        
        pygame.mixer.music.stop()
        screen.blit(bg,(0,-5))#displaying the background when game is won
        over=font.render("You Won!",True,(255,255,255))
        screen.blit(over,(340,200))        
        claps=pygame.mixer.Sound('claps.wav')
        claps.play()
        pygame.display.update()
        
    elif gameover and iswon==False:        
        screen.blit(dead,(x,500))    
        over=font.render("Game over!",True,(255,255,255))
        screen.blit(over,(340,200))        
        pygame.display.update()
    
#monkey
monkeywalk=[pygame.image.load('monkeysprite3.png'),pygame.image.load('monkeysprite2.png'),pygame.image.load('monkeysprite1.png')]
monkeyimg=[]
mx=[800]
my=[]
mx_change=[]
my_change=[]
n=50#number of monkeys
mx_lowerlimit=800
mx_upperlimit=801

for i in range(n):
    monkeyimg.append(monkeywalk)
    mx.append(random.randint(mx_lowerlimit,mx_upperlimit))#to place monkeys at different positions
    mx_lowerlimit+=300
    mx_upperlimit=mx_lowerlimit+random.randint(1,200)
    my.append(235)
    mx_change.append(3)

print(mx)
#display clown images
def clown(x,y):    
    global walkcount#for clown's leg movement
    if walkcount+1>=9:
        walkcount=0
            
    if leftright and y==234:
        screen.blit(walk[walkcount//3],(x,y))
        walkcount+=1       
            
    elif y!=234 and leftright:
        screen.blit(jumping,(x,y))
    else:
        screen.blit(walk[1],(x,y))
        
#display monkey images     
def monkey(x,y,i):
    global monkeywalkcount
    if monkeywalkcount+1>=9:
        monkeywalkcount=0
    
    screen.blit(monkeyimg[i][monkeywalkcount//3],(x,y))
    
#check the distance between monkey and clown for possible collision and game over
def collision(mx,my,x,y):
    dist=math.sqrt(((mx-x)**2)+((my-y)**2))
    if dist<64:
        return True
    else:
        return False   
    
#game loop  
while run:
    
    clock.tick(9)
    create_background()
    
    #setting condition to win game   
    for i in range(n):
        
        if bx>-700:
            break
        
        else:
            
            for j in range(2000):
                y+=0.8
                clown(x,y)
            
            iswon=True
            gameover=False
            gameovert(iswon,gameover)
            break
        
    #when player wants to quit the running game
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
            
    #for player actions
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > vel: 
        x -= vel
        bx+= 9#to move the background image
        leftright=True
    elif keys[pygame.K_RIGHT]:  
        x += vel
        bx-=9
        leftright=True
    else:
        leftright=False
        walkcount=0
        
    if not(isJump): 
        
        if keys[pygame.K_SPACE]:#use spacebar to jump
            jum=pygame.mixer.Sound('jump.wav')
            jum.play()
            isJump = True
    else:
        
        if jumpCount >= -10:
            y -= (jumpCount * abs(jumpCount)) * 0.5
            jumpCount -= 1
        else: 
            jumpCount = 10
            isJump = False
            
                    
    #monkey movement      
    for i in range(n):
        
        mx_change[i]=-10
        mx[i]+=mx_change[i]
        monkeywalkcount+=1#for monkey's leg movement
            
        #collision
        c=collision(mx[i],my[i],x,y)
        if c:
            pygame.mixer.music.stop()
            out=pygame.mixer.Sound('out.wav')
            out.play()
            
            for j in range(300):
                y+=0.8
                clown(x,y) 
                
            gameover=True            
            break
        
        monkey(int(mx[i]),my[i],i)
         
    if gameover==False:
        clown(x,y)
    if gameover==True:
        iswon=False
        gameovert(iswon,gameover)
        
        
    pygame.display.update()
    
#quit game
while True:
    for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()
