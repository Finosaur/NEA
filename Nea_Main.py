import pygame
pygame.init()
#Imports pygame allowing the code to work
win = pygame.display.set_mode((500,480))
#Sets display size
pygame.display.set_caption("Test_Game") # sets application name

walkRight = [pygame.image.load('MC_Right.png')]
walkLeft = [pygame.image.load('MC_Left.png')]
bg = pygame.image.load('BG.jpg')
char = pygame.image.load('MC_Right.png')
# loading in all images for the game

clock = pygame.time.Clock() #Sets up the clock for the refresh rate

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right =False
        self.walkCount = 0
        self.jumpCount = 5
        self.Standing = True
        self.hitbox = (self.x, self.y, 17, 20)
        # Variables for the player

    def draw(self,win):
        if self.walkCount +1 >=3:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3],(self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3],(self.x,self.y))
                self.walkCount += 1
                #Loops through walking animation, if there is one
        else:
            if self.right:
                win.blit(walkRight[0], (self.x,self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
            #Blits the players walk so they dont leave a trail
        self.hitbox = (self.x, self.y, 17, 20)
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        # draws the hitbox around the player

class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8*facing
        #Projectile variables

    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x, self.y),self.radius)
        #Draws an circle in front of the player

class enemy(object):
    walkRight = [pygame.image.load('Enemy_Right.png')]
    walkLeft = [pygame.image.load('Enemy_Left.png')]
    #Loads enemy images
 
    def __init__(self,x,y,width,height,end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x, self.y,15,20)
        #Enemy variables

    def draw(self,win):
        self.move()

        if self.walkCount + 1 >= 3:
            self.walkCount = 0 

        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount//3],(self.x,self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount//3],(self.x,self.y))
            self.walkCount += 1
        #The enemy animation loop
    
        self.hitbox = (self.x, self.y,15,20)
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        #The enemies hitbox

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1]+self.vel:
                self.x += self.vel
            else:
                self.vel=self.vel*-1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0]-self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel*-1
                self.x += self.vel
                self.walkCount=0
                #The calculations for the automatic walking of the enemy. Moves right a certain amount and then back a certain amount.
    def hit(self):
       print('hit')
    #Proves that the enemy is hit

man = player(200,410,64,64)
Enemy = enemy(100,410,64,64,300)
shootLoop = 0
run = True
bullets = []
#Setting variables and parameters using the defintions we already made
while run:
    clock.tick(30) #Controls the refresh rate

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #Controls when the game is stopped
    
    if shootLoop > 0:
        shootLoop +=1
    if shootLoop>3:
        shootLoop =0
        #Used to stop a glitch with the bullets where multiple would be shot accidently

    for bullet in bullets:
        if bullet.y -bullet.radius < Enemy.hitbox[1] + Enemy.hitbox[3] and bullet.y + bullet.radius > Enemy.hitbox[1]:
            if bullet.x + bullet.radius > Enemy.hitbox[0] and bullet.x - bullet.radius < Enemy.hitbox[0] + Enemy.hitbox[2]:
                Enemy.hit()
                bullets.pop(bullets.index(bullet))
        #Checks if enemy has been hit, and displays if it has

        if bullet.x < 500 and bullet.x>0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
            #Removes bullets when they go off screen

    keys = pygame.key.get_pressed()
    #Sets up for when the buttons are pressed
    if keys[pygame.K_SPACE] and shootLoop == 0:
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets)<5:
            bullets.append(projectile(round(man.x + (man.width//5)), round(man.y + (man.height//5)),4,(255,0,0),facing))
        
        shootLoop = 1
    #Controls the bullets, making sure they shoot the correct side and are the correct size and location
    #(man.x + (man.width//5)), round(man.y + (man.height//5)) controls the location bullets are shot from
    #4 controls the size of the bullets
    #(255,0,0) controls the colour of the bullets
    if keys[pygame.K_UP]:
        if man.left:
            facing = -1
        else:
            facing = 1
        
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 -man.width -man.vel:
        man.x += man.vel
        man.right = True
        man.left = False 
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
#Controls the mans walking, doing it based on the original starting position. If it exceeds this it stops as thats the border of the screen.
    if not(man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -5:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 5
#Controls the mans jumping, allowing it to go uo a certain height then come back down to level ground.
    win.fill((0,0,0))
    win.blit(bg,(0,0))
    man.draw(win)
    Enemy.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()
#Fill the background to black and load the characters back in, also drawing the enemies bullets in. This is then updated to the user using pygame.display.update()
pygame.quit()
#This exits the while code