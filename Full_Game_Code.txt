import pygame
import sys
import sqlite3
import pygame.mixer
import time

# Initialize Pygame
pygame.init()
pygame.mixer.init()

#Load the sound for the bullet
bullet_sound = pygame.mixer.Sound(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\ESM_Designed_Game_Futuristic_Gun_Shot_183_Gun_Military_Pistol_Shot_Machine_Rifle_Sci_Fi_Mechanism_Alien_Space.mp3')

# Define font
font = pygame.font.Font(None, 36)

# Define variables
player_name = ""
input_active = False
input_text = ""
score = 0
play_time = 0
leaderboard_data = []
displayed_entries = []  # Track displayed entries
displayed_entry_index = 0
displayed_entries_count = 0
entries_to_display = 10

# Initialize SQLite database
conn = sqlite3.connect('leaderboard.db')
cursor = conn.cursor()

# Create leaderboard table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY,
        player_name TEXT,
        score INTEGER,
        play_time INTEGER
    )
''')

###cursor.execute('DELETE FROM scores')###

# Runs the SQL code
conn.commit()

# Constants for screen size
SCREEN_WIDTH = 1215
SCREEN_HEIGHT = 727

# Load images
walkRight = pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Char_Item\MC_Right2.png')
walkLeft = [pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Char_Item\MC_Left2.png')]
bg = [pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Used_BG\Main_Menu.png'),
      pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Used_BG\Instructions.png'),
      pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Used_BG\HUD_Cavern2.png'),
      pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Used_BG\HUD_CavCom.png'),
      pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Used_BG\HUD_2_TP.png'),
      pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Used_BG\HUD_2_TPC1.png'),
      pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Used_BG\HUD_2_TPC2.png'),
      pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Used_BG\HUD_Processing_Plant.png'),
      pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Used_BG\HUD_ProcCom.png'),
      pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Used_BG\HUD_FactoryGates.png'),
      pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Used_BG\HUD_FG_Com.png'),
      pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Used_BG\HUD_Power_Generator.png'),
      pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Used_BG\HUD_ControlRoom.png'),
      pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Used_BG\HUD_CR_Com.png'),
      pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Used_BG\HUD_ColdRoom.png'),
      pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Used_BG\HUD_ColdRoom_Com.png'),
      pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Used_BG\HUD_TheExit.png'),
      pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Used_BG\HUD_TheExit - Com1.png'),
      pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Used_BG\HUD_TheExit - Com2.png'),
      pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Used_BG\Player_Name.png'),
      pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Used_BG\LeaderBoard.png')]
char = pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Char_Item\MC_Right2.png')

#making the target class
class Target(object):
    def __init__(self, x, y, width, height):
        #target variables
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.visible = True

    def hit(self):
        #define what happens when the player hits the targets
        global z, wall_obj1
        z += 1
        if z < len(bg):
            win.blit(bg[z], (0, 0))
        self.visible = False

class wall(object):
    def __init__(self,x,y,width,height):
        # define wall variables
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.visible = True
        self.update_hitbox()

    def update_hitbox(self):
        # refreshes the hitbox if the players location has changed
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def hit(self, player_obj):
        # Code to define the collision detection between the player and the wall
        player_rect = pygame.Rect(player_obj.x, player_obj.y, player_obj.width, player_obj.height)

        if player_rect.colliderect(self.hitbox):
            # Adjusts player's horizontal position if they touch the left or right of the wall
            if player_rect.right > self.hitbox.left and player_rect.left < self.hitbox.left:
                player_obj.x = self.hitbox.left - player_obj.width
            elif player_rect.left < self.hitbox.right and player_rect.right > self.hitbox.right:
                player_obj.x = self.hitbox.right

            if player_obj.isJump:  # If player is jumping, stops the jump
                player_obj.isJump = False
                player_obj.jumpCount = player_obj.initial_jump_height
            player_rect = pygame.Rect(player_obj.x, player_obj.y, player_obj.width, player_obj.height)

            # Adjust player's vertical position if they touch the top or bottom of the wall
            if player_rect.colliderect(self.hitbox.move(0, -player_obj.vel)):
                player_obj.y = self.hitbox.bottom
            elif player_rect.colliderect(self.hitbox.move(0, player_obj.vel)):
                player_obj.y = self.hitbox.top - player_obj.height

class exit(object):
    def __init__(self,x,y,width,height):
        # define exit variables
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def hit(self):
        # Code showing waht happens when the player hits the exit
        global player,z, Start_x, Start_y
        z = z+1
        self.visible = False
        if z == 4:
            player_obj.x = 425
            Start_x = player_obj.x
            player_obj.y = 390
            Start_y = player_obj.y
        if z==7:
            player_obj.x = 567
            Start_x = player_obj.x
            player_obj.y = 101
            Start_y = player_obj.y  
        if z==9:
            player_obj.x = 80
            Start_x = player_obj.x
            player_obj.y = 420
            Start_y = player_obj.y   
        if z==11:
            player_obj.x = 1115
            Start_x = player_obj.x
            player_obj.y = 109
            Start_y = player_obj.y 
        if z==12:
            player_obj.x = 670
            Start_x = player_obj.x
            player_obj.y = 110
            Start_y = player_obj.y        
        if z==14:
            player_obj.x = 63
            Start_x = player_obj.x
            player_obj.y = 426
            Start_y = player_obj.y   
        if z==16 or z ==17:
            player_obj.x = 74
            Start_x = player_obj.x
            player_obj.y = 410
            Start_y = player_obj.y
        if z==19:
            player_obj.x = 0
            Start_x = player_obj.x
            player_obj.y = 0
            Start_y = player_obj.y            

class key(object):
    # loads key image
    key = pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Char_Item\Key2.png')
    def __init__(self,x,y,width,height):
        # defines the key's variable
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x,self.y,42,22)
        self.visible = True
        self.collected = False

    def draw(self,win):
        # Only shows the key if it is stated as visible
        if self.visible:
            win.blit(self.key, (self.x, self.y))

    def hit(self):
        # Code showing what happens when the player hits the key
        global player,z
        self.collected = True
        if key_obj1.collected:
            z = z+1
        if key_obj2.collected and key_obj3.collected and key_obj4.collected:
            z = z+1
        if key_obj5.collected and key_obj6.collected and key_obj7.collected and key_obj8.collected and key_obj9.collected:
            z = z+1
        if key_obj10.collected and key_obj11.collected:
            z = z+1
        win.blit(bg[z],(0,0))
        self.visible = False

        
class Player(object):
    def __init__(self, x, y, width, height):
        # player variables
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 8
        self.isJump = False
        self.jumpCount = 9.5
        self.initial_jump_height = self.jumpCount 
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = pygame.Rect(self.x, self.y, 34, 65)

    def draw(self, win):
        # When the player is drawn, it checks if its against the wall and resets its walk count if it is, not allowing it to move
        if self.walkCount >=len(walkLeft):
            self.walkCount = 0

        if not(self.standing):
            # Checks if the character is in the idle standing sprite and blits the character to face left or right depending on its direction
            if self.left:
                win.blit(walkLeft[self.walkCount//3],(self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight,(self.x,self.y))
                self.walkCount += 1
                #Loops through walking animation, if there is one which in this case there isn't
        else:
            win.blit(char, (self.x, self.y))
            #Blits the players walk so they dont leave a trail
        self.hitbox = pygame.Rect(self.x, self.y, 34, 65)
        # draws the hitbox around the player
        pass

    def update_hitbox(self):
        #
        self.hitbox = pygame.Rect(self.x, self.y, 34, 65)



class Platform(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, win):
        pygame.draw.rect(win, (0, 255, 0), self.rect)

class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 12*facing
        self.hitbox = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2,self.radius*2)
        #Projectile variables

    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x, self.y),self.radius)
        self.hitbox = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2,self.radius*2)
        #Draws an circle in front of the player

    def hit(self, enemies):
        for Enemy in enemies:
            if self.hitbox.colliderect(Enemy.hitbox):
                return True
                score += 100
        return False

class Enemy(object):
    moveRight = [pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Char_Item\Enemy_Right2.png')]
    moveLeft = [pygame.image.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Char_Item\Enemy_Left2.png')]
    #Loads Enemy images 
 
    def __init__(self,x,y,width,height,end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x, self.y,15,20)
        self.visible = True
        #Enemy variables

    def draw(self,win,bullets=None):
        if self.visible:
            if bullets is not None and self.hit(bullets):
                self.visible = False
                bullets.remove(bullet)
            
            self.move()

            if self.walkCount + 1 >= 3:
                self.walkCount = 0 

            if self.vel > 0:
                win.blit(self.moveRight[self.walkCount//3],(self.x,self.y))
                self.walkCount += 1
            else:
                win.blit(self.moveLeft[self.walkCount//3],(self.x,self.y))
                self.walkCount += 1
            #The Enemy animation loop

            if self.visible:
                self.hitbox = (self.x, self.y,31,42)
            #The enemies hitbox
        else:
            self.hitbox = (self.x, self.y,15,20)

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
                #The calculations for the automatic walking of the Enemy. Moves right a certain amount and then back a certain amount.
    def hit(self):
        global player,z
        if z == 2 or z == 3 or z==7 or z==8 or z==9 or z==10 or z==11 or z==12 or z==14 or z==16 or z==17: 
            player_obj.x = Start_x
            player_obj.y = Start_y  

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Manic Mania")

player_obj = Player(200, 398, 64, 64)
Start_x = 200
Start_y = 398
Enemy1 = Enemy(300,245,64,64,600)

Enemy2 = Enemy(446,420,64,64,1098)
Enemy3 = Enemy(927,165,64,64,1083)

Enemy4 = Enemy(515,315,64,64,1142)
Enemy5 = Enemy(84,204,64,64,875)
Enemy6 = Enemy(355,93,64,64,570)
Enemy7 = Enemy(708,93,64,64,990)

Enemy8 = Enemy(53,426,64,64,213)
Enemy9 = Enemy(227,426,64,64,400)
Enemy10 = Enemy(517,426,64,64,632)
Enemy11 = Enemy(691,426,64,64,890)
Enemy12 = Enemy(910,426,64,64,1027)
Enemy13 = Enemy(47,426,64,64,1167)

Enemy14 = Enemy(454,413,64,64,1057)
Enemy15 = Enemy(49,65,64,64,663)
Enemy16 = Enemy(226,229,64,64,371)

Enemy17 = Enemy(232,395,64,64,732)
Enemy18 = Enemy(429,163,64,64,979)
Enemy19 = Enemy(58,179,64,64,144)

Enemy20 = Enemy(232,395,64,64,732)
Enemy21 = Enemy(429,163,64,64,979)
Enemy22 = Enemy(58,179,64,64,144)

enemies =[]
enemy_check_1 = False
enemy_check_2 = False
enemy_check_3 = False
enemy_check_4 = False

platform1 = [Platform(0,0,0,0)] # Floor platform
platform2 = [Platform(0,0,0,0)]  
platform3 = [Platform(0,0,0,0)]
platform4 = [Platform(0,0,0,0)]
platform5= [Platform(0,0,0,0)]
platform6 = [Platform(0,0,0,0)]
platform7 = [Platform(0,0,0,0)]
platform8 = [Platform(0,0,0,0)]
platform9 = [Platform(0,0,0,0)]
platform10 = [Platform(0,0,0,0)]
platform11 = [Platform(0,0,0,0)]
platform12 = [Platform(0,0,0,0)]
key_obj1 = key(0,0,0,0)
key_obj1.visible=False
key_obj1.collected=False
key_obj2 = key(0,0,0,0)
key_obj2.visible=False
key_obj2.collected=False
key_obj3 = key(0,0,0,0)
key_obj3.visible=False
key_obj3.collected=False
key_obj4 = key(0,0,0,0)
key_obj4.visible=False
key_obj4.collected=False
key_obj5 = key(0,0,0,0)
key_obj5.visible=False
key_obj5.collected=False
key_obj6 = key(0,0,0,0)
key_obj6.visible=False
key_obj6.collected=False
key_obj7 = key(0,0,0,0)
key_obj7.visible=False
key_obj7.collected=False
key_obj8 = key(0,0,0,0)
key_obj8.visible=False
key_obj8.collected=False
key_obj9 = key(0,0,0,0)
key_obj9.visible=False
key_obj9.collected=False
key_obj10 = key(0,0,0,0)
key_obj10visible=False
key_obj10.collected=False
key_obj11 = key(0,0,0,0)
key_obj11.visible=False
key_obj11.collected=False
exit_obj = exit(1081,373,64,64)
wall_objects = [[],[],[wall(942,374,84,64)],[],[wall(587,305,33,151),wall(694,0,33,110),wall(510,0,33,308),wall(664,108,32,199),wall(491,296,155,10)],
                [wall(734,0,33,110),wall(510,0,33,308),wall(664,108,32,199),wall(491,296,155,10)],[wall(510,0,33,308),wall(664,108,32,199),wall(491,296,195,10)],
                [wall(1084,0,34,73),wall(1083,88,101,12)],[],[wall(479,375,33,98)],[],[],[wall(615,373,34,138), wall(488,377,51,131)],
                [],[wall(841,126,28,266),wall(943,122,46,271),wall(1080,372,85,7),wall(1079,380,28,76)],[wall(841,126,28,266),wall(943,122,46,271)],
                [wall(15,46,488,15), wall(474,46,172,81),wall(630,47,552,65),wall(890,308,35,154)],[wall(15,46,488,15), wall(474,46,172,81),wall(630,47,552,65)],
                [wall(15,46,488,15),wall(630,47,552,65)],[],[]]
Level_Check_0 = False
Level_Check_1 = False
Level_Check_2 = False
Level_Check_3 = False
Level_Check_4 = False
Level_Check_5 = False
Level_Check_6 = False
Level_Check_7 = False
Level_Check_8 = False
Level_Check_9 = False
Level_Check_10 = False
Level_Check_11 = False
Music_Check = False
Check = False
shootLoop = 0
bullets = []
jump_delay = 500  # 2000 milliseconds (2 seconds)
last_jump_time = 0

target_obj = [Target(0,0,0,0), Target(0,0,0,0), Target(0,0,0,0), Target(0,0,0,0), Target(0,0,0,0)]

z = 0  # Initialize the background index
start_time = None  # Variable to store the start time of the timer
timer_font = pygame.font.Font(None, 36)  # Font for displaying the timer

score = 0
score_font = pygame.font.Font(None,36)
number = 1

enter_pressed = False
# Variable to track the time when the leaderboard is displayed
enter_pressed_time = pygame.time.get_ticks()
auto_reset_duration = 3000

font = pygame.font.Font(None, 36)
display_leaderboard = False

run = True
clock = pygame.time.Clock()

current_platform = None
can_jump = False  # Flag to control jumping
initial_jump_height = None  # Initial jump height for maintaining consistent jump magnitude
has_jumped = False  # Flag to track whether the player has initiated a jump
pygame.mixer.music.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Finlays game music - title.mp3')
pygame.mixer.music.play(-1) 
while run:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and z==0 or z==1:
                z = min(z + 1, len(bg) - 1)
                if z==1:
                    start_time = pygame.time.get_ticks()
                win.fill((0,0,0))
            if event.key == pygame.K_RETURN and z == 20 and not enter_pressed:
                z = 1
                input_active = False
                score = 0
                Check = False
                Level_Check_0 = False
                Level_Check_1 = False
                Level_Check_2 = False
                Level_Check_3 = False
                Level_Check_4 = False
                Level_Check_5 = False
                Level_Check_6 = False
                Level_Check_7 = False
                Level_Check_8 = False
                Level_Check_9 = False
                Level_Check_10 = False
                Level_Check_11 = False
                key_obj1 = key(0,0,0,0)
                key_obj1.visible=False
                key_obj1.collected=False
                key_obj2 = key(0,0,0,0)
                key_obj2.visible=False
                key_obj2.collected=False
                key_obj3 = key(0,0,0,0)
                key_obj3.visible=False
                key_obj3.collected=False
                key_obj4 = key(0,0,0,0)
                key_obj4.visible=False
                key_obj4.collected=False
                key_obj5 = key(0,0,0,0)
                key_obj5.visible=False
                key_obj5.collected=False
                key_obj6 = key(0,0,0,0)
                key_obj6.visible=False
                key_obj6.collected=False
                key_obj7 = key(0,0,0,0)
                key_obj7.visible=False
                key_obj7.collected=False
                key_obj8 = key(0,0,0,0)
                key_obj8.visible=False
                key_obj8.collected=False
                key_obj9 = key(0,0,0,0)
                key_obj9.visible=False
                key_obj9.collected=False
                key_obj10 = key(0,0,0,0)
                key_obj10visible=False
                key_obj10.collected=False
                key_obj11 = key(0,0,0,0)
                key_obj11.visible=False
                key_obj11.collected=False
                exit_obj = exit(1081,373,64,64)                
                enter_pressed = True
                enter_pressed_time = pygame.time.get_ticks()  # Record the time
                enemy_check_1 = False
                enemy_check_2 = False
                enemy_check_3 = False
                enemy_check_4 = False
                displayed_entries = [] 
                number = 1
            if input_active:
                if event.key == pygame.K_RETURN:
                    if not enter_pressed:
                        input_active = False
                        player_name = input_text
                        cursor.execute('INSERT INTO scores (player_name, score, play_time) VALUES (?, ?, ?)', (player_name, score, play_time))
                        conn.commit()
                        input_text = ""
                        z = z+1
                        enter_pressed = True
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
        if z==19 and not input_active:
            input_active = True
        if z==20 and not Check:
            win.blit(bg[z],(0,0))
            Check = True
        if z==20:
            if not displayed_entries:
                cursor.execute('SELECT player_name, score, play_time FROM scores ORDER BY play_time')
                leaderboard_data = cursor.fetchall()
                print("Fetched data from the database:", leaderboard_data) 
                leaderboard_display_time = pygame.time.get_ticks()

            # Display leaderboard entries
            y = 160
            displayed_count = 0
            for entry in leaderboard_data:
                name, score, time = entry
                if entry not in displayed_entries and displayed_count<=10:
                    leaderboard_text = f"{number}. {name}"
                    leaderboard_surface = font.render(leaderboard_text, True, (255, 255, 255))
                    win.blit(leaderboard_surface, (180, y))
                    number += 1
                    leaderboard_text = f"{score}"
                    leaderboard_surface = font.render(leaderboard_text, True, (255, 255, 255))
                    win.blit(leaderboard_surface, (550, y))
                    leaderboard_text = f"{time}"
                    leaderboard_surface = font.render(leaderboard_text, True, (255, 255, 255))
                    win.blit(leaderboard_surface, (920, y))
                    y += 40
                    displayed_entries.append(entry)
                    displayed_count += 1
            while displayed_count < 10:
                y += 40
                displayed_count += 1
        pygame.display.update()  # Update the screen to display the leaderboard

    if enter_pressed and pygame.time.get_ticks() - enter_pressed_time >= auto_reset_duration:
        enter_pressed = False
                
    if z==1:
        pygame.mixer.music.stop()
    if z==1:
        if not pygame.mixer.get_busy():
            pygame.mixer.music.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Finlays game music - main.mp3')
            pygame.mixer.music.play(-1)
    if z ==19 and not Music_Check:
        if pygame.mixer.get_busy():
            pygame.mixer.music.stop()
        Music_Check = True
    if z==19:
        pygame.mixer.music.load(r'c:\Users\gfbro\OneDrive\Documents\ComputerScience\NEA\Finlays game music - title.mp3')
        pygame.mixer.music.play(-1)     
    if shootLoop > 0:
        shootLoop +=1
    if shootLoop>3:
        shootLoop =0
        #Used to stop a glitch with the bullets where multiple would be shot accidently

    for bullet in bullets:
        for Enemy in enemies:  # List of enemies
            if bullet.hitbox.colliderect(Enemy.hitbox):
                Enemy.visible = False                   # Set the Enemy's visibility to False
                bullets.remove(bullet)  # Remove the bullet
                score +=100
                if z==2:
                    enemies.remove(Enemy1)
                if z==7 and bullet.hitbox.colliderect(Enemy2.hitbox):
                    enemies.remove(Enemy2)
                if z==7 and bullet.hitbox.colliderect(Enemy3.hitbox):
                    enemies.remove(Enemy3)
                if z==9 and bullet.hitbox.colliderect(Enemy4.hitbox):
                    enemies.remove(Enemy4)
                if z==9 and bullet.hitbox.colliderect(Enemy5.hitbox):
                    enemies.remove(Enemy5)
                if z==9 and bullet.hitbox.colliderect(Enemy6.hitbox):
                    enemies.remove(Enemy6)
                if z==9 and bullet.hitbox.colliderect(Enemy7.hitbox):
                    enemies.remove(Enemy7)
                if z==11 and bullet.hitbox.colliderect(Enemy8.hitbox):
                    enemies.remove(Enemy8)
                if z==11 and bullet.hitbox.colliderect(Enemy9.hitbox):
                    enemies.remove(Enemy9)
                if z==11 and bullet.hitbox.colliderect(Enemy10.hitbox):
                    enemies.remove(Enemy10)
                if z==11 and bullet.hitbox.colliderect(Enemy11.hitbox):
                    enemies.remove(Enemy11)
                if z==11 and bullet.hitbox.colliderect(Enemy12.hitbox):
                    enemies.remove(Enemy12)
                if z==11 and bullet.hitbox.colliderect(Enemy13.hitbox):
                    enemies.remove(Enemy13)
                if z==14 and bullet.hitbox.colliderect(Enemy14.hitbox):
                    enemies.remove(Enemy14)
                if z==14 and bullet.hitbox.colliderect(Enemy15.hitbox):
                    enemies.remove(Enemy15)
                if z==14 and bullet.hitbox.colliderect(Enemy16.hitbox):
                    enemies.remove(Enemy16)
                if z==16 and bullet.hitbox.colliderect(Enemy17.hitbox):
                    enemies.remove(Enemy17)
                if z==16 and bullet.hitbox.colliderect(Enemy18.hitbox):
                    enemies.remove(Enemy18)
                if z==16 and bullet.hitbox.colliderect(Enemy19.hitbox):
                    enemies.remove(Enemy19)
                if z==17 and bullet.hitbox.colliderect(Enemy20.hitbox):
                    enemies.remove(Enemy20)
                if z==17 and bullet.hitbox.colliderect(Enemy21.hitbox):
                    enemies.remove(Enemy21)
                if z==17 and bullet.hitbox.colliderect(Enemy22.hitbox):
                    enemies.remove(Enemy22)

                break  # Exit the loop once a hit is detected

        if bullet.x < target.x + target.width and bullet.x > target.x:
            if bullet.y < target.y + target.height and bullet.y > target.y:
                target.hit()
                bullets.pop(bullets.index(bullet))
                break

        if bullet.x < 1175 and bullet.x>45:
            bullet.x += bullet.vel
        else:
            bullets.remove(bullet)
            continue
            #Removes bullets when they go off screen

        bullet.draw(win)
        for target in target_obj:
            if (bullet.x < target.x + target.width and bullet.x > target.x and bullet.y < target.y + target.height and bullet.y > target.y):
                    target.hit()
                    bullets.remove(bullet)
                    break

    for target in target_obj:
        if player_obj.hitbox[1] < target.hitbox[1] + target.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > target.hitbox[1]:
            if player_obj.hitbox[0] + player_obj.hitbox[2] > target.hitbox[0] and player_obj.hitbox[0] < target.hitbox[0] + target.hitbox[2]:
                target.hit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        if player_obj.left:
            facing = -1
        else:
            facing = 1
        if len(bullets)<5:
            bullets.append(projectile(round(player_obj.x + (player_obj.width//5)), round(player_obj.y + (player_obj.height//5)),4,(255,0,0),facing))
            if z>0:
                bullet_sound.play()
        
        shootLoop = 1
    #Controls the bullets, making sure they shoot the correct side and are the correct size and location
    #(man.x + (man.width//5)), round(man.y + (man.height//5)) controls the location bullets are shot from
    #4 controls the size of the bullets
    #(255,0,0) controls the colour of the bullets

    if (keys[pygame.K_LEFT] or keys[pygame.K_a])and player_obj.x > player_obj.vel+35:
        player_obj.x -= player_obj.vel
        player_obj.left = True
        player_obj.right = False
        player_obj.standing = False
    elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_obj.x < 1215 -player_obj.width -player_obj.vel:
        player_obj.x += player_obj.vel
        player_obj.left = False
        player_obj.right = True
        player_obj.standing = False

    # Check if the player is on platform1
    on_platform1 = False
    for platform in platform1:
        if player_obj.y + player_obj.height >= platform.y and player_obj.y <= platform.y + platform.height:
            if player_obj.x + player_obj.width >= platform.x and player_obj.x <= platform.x + platform.width:
                on_platform1 = True
                current_platform = platform1
                player_obj.y = platform.y - player_obj.height
                player_obj.isJump = False
                player_obj.jumpCount = 9.5
                can_jump = True
                initial_jump_height = player_obj.y
                break

    # Check if the player is on platform2
    on_platform2 = False
    for platform in platform2:
        if player_obj.y + player_obj.height >= platform.y and player_obj.y <= platform.y + platform.height:
            if player_obj.x + player_obj.width >= platform.x and player_obj.x <= platform.x + platform.width:
                on_platform2 = True
                current_platform = platform2
                player_obj.y = platform.y - player_obj.height
                player_obj.isJump = False
                player_obj.jumpCount = 9.5
                can_jump = True
                initial_jump_height = player_obj.y
                break

    # Check if the player is on platform3
    on_platform3 = False
    for platform in platform3:
        if player_obj.y + player_obj.height >= platform.y and player_obj.y <= platform.y + platform.height:
            if player_obj.x + player_obj.width >= platform.x and player_obj.x <= platform.x + platform.width:
                on_platform3 = True
                current_platform = platform3
                player_obj.y = platform.y - player_obj.height
                player_obj.isJump = False
                player_obj.jumpCount = 9.5
                can_jump = True
                initial_jump_height = player_obj.y
            break

    if not (on_platform2):
        player_obj.y += player_obj.vel

    # Check if the player is on platform4
    on_platform4 = False
    for platform in platform4:
        if player_obj.y + player_obj.height >= platform.y and player_obj.y <= platform.y + platform.height:
            if player_obj.x + player_obj.width >= platform.x and player_obj.x <= platform.x + platform.width:
                on_platform4 = True
                current_platform = platform4
                player_obj.y = platform.y - player_obj.height
                player_obj.isJump = False
                player_obj.jumpCount = 9.5
                can_jump = True
                initial_jump_height = player_obj.y
                break

    on_platform5 = False
    for platform in platform5:
        if player_obj.y + player_obj.height >= platform.y and player_obj.y <= platform.y + platform.height:
            if player_obj.x + player_obj.width >= platform.x and player_obj.x <= platform.x + platform.width:
                on_platform5 = True
                current_platform = platform5
                player_obj.y = platform.y - player_obj.height
                player_obj.isJump = False
                player_obj.jumpCount = 9.5
                can_jump = True
                initial_jump_height = player_obj.y
                break

    on_platform6 = False
    for platform in platform6:
        if player_obj.y + player_obj.height >= platform.y and player_obj.y <= platform.y + platform.height:
            if player_obj.x + player_obj.width >= platform.x and player_obj.x <= platform.x + platform.width:
                on_platform6 = True
                current_platform = platform6
                player_obj.y = platform.y - player_obj.height
                player_obj.isJump = False
                player_obj.jumpCount = 9.5
                can_jump = True
                initial_jump_height = player_obj.y
                break

    on_platform7 = False
    for platform in platform7:
        if player_obj.y + player_obj.height >= platform.y and player_obj.y <= platform.y + platform.height:
            if player_obj.x + player_obj.width >= platform.x and player_obj.x <= platform.x + platform.width:
                on_platform7 = True
                current_platform = platform6
                player_obj.y = platform.y - player_obj.height
                player_obj.isJump = False
                player_obj.jumpCount = 9.5
                can_jump = True
                initial_jump_height = player_obj.y
                break

    on_platform8 = False
    for platform in platform8:
        if player_obj.y + player_obj.height >= platform.y and player_obj.y <= platform.y + platform.height:
            if player_obj.x + player_obj.width >= platform.x and player_obj.x <= platform.x + platform.width:
                on_platform8 = True
                current_platform = platform6
                player_obj.y = platform.y - player_obj.height
                player_obj.isJump = False
                player_obj.jumpCount = 9.5
                can_jump = True
                initial_jump_height = player_obj.y
                break

    on_platform9 = False
    for platform in platform9:
        if player_obj.y + player_obj.height >= platform.y and player_obj.y <= platform.y + platform.height:
            if player_obj.x + player_obj.width >= platform.x and player_obj.x <= platform.x + platform.width:
                on_platform9 = True
                current_platform = platform6
                player_obj.y = platform.y - player_obj.height
                player_obj.isJump = False
                player_obj.jumpCount = 9.5
                can_jump = True
                initial_jump_height = player_obj.y
                break

    on_platform10 = False
    for platform in platform10:
        if player_obj.y + player_obj.height >= platform.y and player_obj.y <= platform.y + platform.height:
            if player_obj.x + player_obj.width >= platform.x and player_obj.x <= platform.x + platform.width:
                on_platform10 = True
                current_platform = platform6
                player_obj.y = platform.y - player_obj.height
                player_obj.isJump = False
                player_obj.jumpCount = 9.5
                can_jump = True
                initial_jump_height = player_obj.y
                break

    on_platform11 = False
    for platform in platform11:
        if player_obj.y + player_obj.height >= platform.y and player_obj.y <= platform.y + platform.height:
            if player_obj.x + player_obj.width >= platform.x and player_obj.x <= platform.x + platform.width:
                on_platform11 = True
                current_platform = platform6
                player_obj.y = platform.y - player_obj.height
                player_obj.isJump = False
                player_obj.jumpCount = 9.5
                can_jump = True
                initial_jump_height = player_obj.y
                break

    on_platform12 = False
    for platform in platform12:
        if player_obj.y + player_obj.height >= platform.y and player_obj.y <= platform.y + platform.height:
            if player_obj.x + player_obj.width >= platform.x and player_obj.x <= platform.x + platform.width:
                on_platform12 = True
                current_platform = platform6
                player_obj.y = platform.y - player_obj.height
                player_obj.isJump = False
                player_obj.jumpCount = 9.5
                can_jump = True
                initial_jump_height = player_obj.y
                break

    if not (on_platform1 or on_platform2 or on_platform2 or on_platform4 or on_platform5 or on_platform6 or on_platform7 or on_platform8 or on_platform9 or on_platform10 or on_platform11 or on_platform12):
        current_platform = None
        can_jump = False
        has_jumped = False  # Reset the has_jumped flag

    if not player_obj.isJump and (on_platform1 or on_platform2 or on_platform3 or on_platform4 or on_platform5 or on_platform6 or on_platform7 or on_platform8 or on_platform9 or on_platform10 or on_platform11 or on_platform12):
        can_jump = True
        has_jumped = False  # Reset the has_jumped flag

    if not has_jumped and (on_platform1 or on_platform2 or on_platform3 or on_platform4 or on_platform5 or on_platform6 or on_platform7 or on_platform8 or on_platform9 or on_platform10 or on_platform11 or on_platform12) and (keys[pygame.K_UP] or keys[pygame.K_w]) and can_jump:
        current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
        if current_time - last_jump_time >= jump_delay:
            player_obj.isJump = True
            can_jump = False
            initial_jump_height = player_obj.y
            has_jumped = True  # Set the has_jumped flag to True
            last_jump_time = current_time  # Update the last jump time

    if player_obj.isJump:
        if player_obj.jumpCount >= -9.25:
            neg = 1
            if player_obj.jumpCount < 0:
                neg = -1
            player_obj.y -= (player_obj.jumpCount ** 2) * 0.5 * neg
            player_obj.jumpCount -= 1
        else:
            player_obj.isJump = False
            player_obj.jumpCount = 9.5

    if not (on_platform1 or on_platform2 or on_platform3 or on_platform4 or on_platform5 or on_platform6 or on_platform7 or on_platform8 or on_platform9 or on_platform10 or on_platform11 or on_platform12):
        player_obj.y += player_obj.vel  # Adjust the value to control the fall speed

    if player_obj.hitbox[1] < exit_obj.hitbox[1] + exit_obj.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > exit_obj.hitbox[1]:
        if player_obj.hitbox[0] + player_obj.hitbox[2] > exit_obj.hitbox[0] and player_obj.hitbox[0] < exit_obj.hitbox[0] + exit_obj.hitbox[2]:
            exit_obj.hit()

    if z>=0 and z<len(wall_objects):
        current_level_walls = wall_objects[z]
        for wall_obj in current_level_walls:
            if wall_obj is not None:
                wall_obj.update_hitbox()
                wall_obj.hit(player_obj)

    if (z==2) and not Level_Check_0:
        player_obj = Player(200, 398, 64, 64)
        platform1 = [Platform(75,463,1108,46)] # Floor platform
        platform2 = [Platform(775,351,409,22)]  
        platform3 = [Platform(335,292,315,22)]
        platform4 = [Platform(206,234,82,28)]
        platform5= [Platform(88,169,63,25)]
        platform6 = [Platform(237,79,944,25)]
        platform7 = [Platform(0,0,0,0)]
        platform8 = [Platform(0,0,0,0)]
        platform9 = [Platform(0,0,0,0)]
        platform10 = [Platform(0,0,0,0)]
        platform11 = [Platform(0,0,0,0)]
        platform12 = [Platform(0,0,0,0)] 
        exit_obj = exit(1081,373,64,64)
        start_time = pygame.time.get_ticks()
        enemies.append(Enemy1)
        Enemy1.visible=True
        key_obj1 = key(1134, 47, 64, 64)
        key_obj1.visible=True
        Level_Check_0=True
        enter_pressed = False
    elif z==2:
        if player_obj.hitbox[1] < key_obj1.hitbox[1] + key_obj1.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > key_obj1.hitbox[1]:
            if player_obj.hitbox[0] + player_obj.hitbox[2] > key_obj1.hitbox[0] and player_obj.hitbox[0] < key_obj1.hitbox[0] + key_obj1.hitbox[2]:
                if not key_obj1.collected:
                    key_obj1.hit()
        if Enemy1.visible:
            if player_obj.hitbox[1] < Enemy1.hitbox[1] + Enemy1.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > Enemy1.hitbox[1]:
                if player_obj.hitbox[0] + player_obj.hitbox[2] > Enemy1.hitbox[0] and player_obj.hitbox[0] < Enemy1.hitbox[0] + Enemy1.hitbox[2]:
                    Enemy1.hit()
    elif z==3 and not enemy_check_1:
        if Enemy1.visible:
            enemies.remove(Enemy1)
        enemy_check_1 = True
    if (z == 4) and not Level_Check_1:
        platform1[0] = Platform(38,445,1144,66)
        platform2[0] = Platform(228,376,95,21)
        platform3[0] = Platform(78,290,87,15)
        platform4[0] = Platform(317,240,74,23)
        platform5[0] = Platform(187,171,31,18)
        platform6[0] = Platform(355,118,60,23)
        platform7[0] = Platform(940,363,64,23)
        platform8[0] = Platform(816,285,62,18)
        platform9[0] = Platform(1068,226,77,25)
        platform10[0] = Platform(878,156,103,26)
        platform11[0] = Platform(1112,92,72,18)
        platform12[0] = Platform(754,108,73,20)     
        exit_obj = exit(513,174,173,14)
        target_obj = [Target(429,30,60,71),Target(1130,25,53,62), Target(0,0,0,0), Target(0,0,0,0)]
        Level_Check_1 = True
    elif (z==5)and not Level_Check_2:
        target_obj = [Target(0,0,0,0),Target(1130,25,53,62), Target(0,0,0,0),Target(0,0,0,0)]  
        Level_Check_2 = True
    elif (z==6)and not Level_Check_3:
        target_obj = [Target(0,0,0,0), Target(0,0,0,0), Target(0,0,0,0),Target(0,0,0,0)]
        Level_Check_3 = True
    elif (z==7) and not Level_Check_4:
        platform1[0] = Platform(38,463,1144,46)
        platform2[0] = Platform(172,386,65,20)
        platform3[0] = Platform(323,273,519,21)
        platform4[0] = Platform(68,234,76,23)
        platform5[0] = Platform(540,127,90,23)
        platform6[0] = Platform(763,132,119,25)
        platform7[0] = Platform(944,211,148,23)
        platform8[0] = Platform(1020,73,83,21)
        platform9[0] = Platform(0,0,0,0)
        platform10[0] = Platform(0,0,0,0)
        platform11[0] = Platform(0,0,0,0)
        platform12[0] = Platform(0,0,0,0)     
        exit_obj = exit(1114,1,69,74)
        enemies.append(Enemy2)
        Enemy2.visible=True
        enemies.append(Enemy3)
        Enemy3.visible=True
        key_obj1.collected = False
        key_obj2 = key(597,251,64,64)
        key_obj2.visible=True
        key_obj2.collected=False
        key_obj3 = key(62,294,64,64)
        key_obj3.visible=True
        key_obj3.collected=False 
        key_obj4 = key(1130,442,64,64)
        key_obj4.visible=True
        key_obj4.collected=False   
        Level_Check_4 = True 
    elif z==7:

        if player_obj.hitbox[1] < key_obj2.hitbox[1] + key_obj2.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > key_obj2.hitbox[1]:
            if player_obj.hitbox[0] + player_obj.hitbox[2] > key_obj2.hitbox[0] and player_obj.hitbox[0] < key_obj2.hitbox[0] + key_obj2.hitbox[2]:
                if not key_obj2.collected:
                    key_obj2.hit()

        if player_obj.hitbox[1] < key_obj3.hitbox[1] + key_obj3.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > key_obj3.hitbox[1]:
            if player_obj.hitbox[0] + player_obj.hitbox[2] > key_obj3.hitbox[0] and player_obj.hitbox[0] < key_obj3.hitbox[0] + key_obj3.hitbox[2]:
                if not key_obj3.collected:
                    key_obj3.hit()

        if player_obj.hitbox[1] < key_obj4.hitbox[1] + key_obj4.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > key_obj4.hitbox[1]:
            if player_obj.hitbox[0] + player_obj.hitbox[2] > key_obj4.hitbox[0] and player_obj.hitbox[0] < key_obj4.hitbox[0] + key_obj4.hitbox[2]:
                if not key_obj4.collected:
                    key_obj4.hit()
        if Enemy2.visible:
            if player_obj.hitbox[1] < Enemy2.hitbox[1] + Enemy2.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > Enemy2.hitbox[1]:
                if player_obj.hitbox[0] + player_obj.hitbox[2] > Enemy2.hitbox[0] and player_obj.hitbox[0] < Enemy2.hitbox[0] + Enemy2.hitbox[2]:
                    Enemy2.hit()
        if Enemy3.visible:
            if player_obj.hitbox[1] < Enemy3.hitbox[1] + Enemy3.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > Enemy3.hitbox[1]:
                if player_obj.hitbox[0] + player_obj.hitbox[2] > Enemy3.hitbox[0] and player_obj.hitbox[0] < Enemy3.hitbox[0] + Enemy3.hitbox[2]:
                    Enemy3.hit() 
    elif z==8 and not enemy_check_2:
        if Enemy2.visible:
            enemies.remove(Enemy2)
        if Enemy3.visible:
            enemies.remove(Enemy3)
        enemy_check_2 = True
    elif (z==9) and not Level_Check_5:
        platform1[0] = Platform(38,470,1143,42)
        platform2[0] = Platform(338,360,845,21)
        platform3[0] = Platform(39,247,862,30)
        platform4[0] = Platform(363,133,819,24)
        platform5[0] = Platform(0,0,0,0)
        platform6[0] = Platform(0,0,0,0)
        platform7[0] = Platform(0,0,0,0)
        platform8[0] = Platform(0,0,0,0)
        platform9[0] = Platform(0,0,0,0)
        platform10[0] = Platform(0,0,0,0)
        platform11[0] = Platform(0,0,0,0)
        platform12[0] = Platform(0,0,0,0)     
        exit_obj = exit(1092,383,15,86)
        Enemy4.visible=True
        enemies.append(Enemy4)
        Enemy5.visible=True
        enemies.append(Enemy5)
        Enemy6.visisble=True
        enemies.append(Enemy6)
        Enemy7.visible=True
        enemies.append(Enemy7)
        Level_Check_5 = True 
        target_obj = [Target(0,0,0,0), Target(0,0,0,0), Target(1096,45,88,80)]
    elif z==9:
        Enemy4.draw(win)
        Enemy5.draw(win)
        Enemy6.draw(win)
        Enemy7.draw(win)
        if Enemy4.visible:
            if player_obj.hitbox[1] < Enemy4.hitbox[1] + Enemy4.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > Enemy4.hitbox[1]:
                if player_obj.hitbox[0] + player_obj.hitbox[2] > Enemy4.hitbox[0] and player_obj.hitbox[0] < Enemy4.hitbox[0] + Enemy4.hitbox[2]:
                    Enemy4.hit()
        if Enemy5.visible:
            if player_obj.hitbox[1] < Enemy5.hitbox[1] + Enemy5.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > Enemy5.hitbox[1]:
                if player_obj.hitbox[0] + player_obj.hitbox[2] > Enemy5.hitbox[0] and player_obj.hitbox[0] < Enemy5.hitbox[0] + Enemy5.hitbox[2]:
                    Enemy5.hit()
        if Enemy6.visible:
            if player_obj.hitbox[1] < Enemy6.hitbox[1] + Enemy6.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > Enemy6.hitbox[1]:
                if player_obj.hitbox[0] + player_obj.hitbox[2] > Enemy6.hitbox[0] and player_obj.hitbox[0] < Enemy6.hitbox[0] + Enemy6.hitbox[2]:
                    Enemy6.hit()
        if Enemy7.visible:
            if player_obj.hitbox[1] < Enemy7.hitbox[1] + Enemy7.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > Enemy7.hitbox[1]:
                if player_obj.hitbox[0] + player_obj.hitbox[2] > Enemy7.hitbox[0] and player_obj.hitbox[0] < Enemy7.hitbox[0] + Enemy7.hitbox[2]:
                    Enemy7.hit()
    elif z==10:
        target_obj = [Target(0,0,0,0), Target(0,0,0,0), Target(0,0,0,0)]
    elif (z==11) and not Level_Check_6:
        platform1[0] = Platform(37,465,1146,40)
        platform2[0] = Platform(345,127,64,23)
        platform3[0] = Platform(545,163,42,14)
        platform4[0] = Platform(716,179,186,41)
        platform5[0] = Platform(1070,147,118,43)
        platform6[0] = Platform(0,0,0,0)
        platform7[0] = Platform(0,0,0,0)
        platform8[0] = Platform(0,0,0,0)
        platform9[0] = Platform(0,0,0,0)
        platform10[0] = Platform(0,0,0,0)
        platform11[0] = Platform(0,0,0,0)
        platform12[0] = Platform(0,0,0,0)     
        exit_obj = exit(36,268,65,75)
        Enemy8.visible=True
        enemies.append(Enemy8)
        Enemy9.visible=True
        enemies.append(Enemy9)
        Enemy10.visisble=True
        enemies.append(Enemy10)
        Enemy11.visible=True
        enemies.append(Enemy11)
        Enemy12.visible=True
        enemies.append(Enemy12)
        Enemy13.visible=True
        enemies.append(Enemy13)
        if Enemy4.visible:
            enemies.remove(Enemy4)
        if Enemy5.visible:
            enemies.remove(Enemy5)
        if Enemy6.visible:
            enemies.remove(Enemy6)
        if Enemy7.visible:
            enemies.remove(Enemy7)
        Level_Check_6 = True 
    elif z==11:
        Enemy8.draw(win)
        Enemy9.draw(win)
        Enemy10.draw(win)
        Enemy11.draw(win)
        Enemy12.draw(win)
        Enemy13.draw(win)
        if Enemy8.visible:
            if player_obj.hitbox[1] < Enemy8.hitbox[1] + Enemy8.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > Enemy8.hitbox[1]:
                if player_obj.hitbox[0] + player_obj.hitbox[2] > Enemy8.hitbox[0] and player_obj.hitbox[0] < Enemy8.hitbox[0] + Enemy8.hitbox[2]:
                    Enemy8.hit()
        if Enemy9.visible:
            if player_obj.hitbox[1] < Enemy9.hitbox[1] + Enemy9.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > Enemy9.hitbox[1]:
                if player_obj.hitbox[0] + player_obj.hitbox[2] > Enemy9.hitbox[0] and player_obj.hitbox[0] < Enemy9.hitbox[0] + Enemy9.hitbox[2]:
                    Enemy9.hit()
        if Enemy10.visible:
            if player_obj.hitbox[1] < Enemy10.hitbox[1] + Enemy10.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > Enemy10.hitbox[1]:
                if player_obj.hitbox[0] + player_obj.hitbox[2] > Enemy10.hitbox[0] and player_obj.hitbox[0] < Enemy10.hitbox[0] + Enemy10.hitbox[2]:
                    Enemy10.hit()
        if Enemy11.visible:
            if player_obj.hitbox[1] < Enemy11.hitbox[1] + Enemy11.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > Enemy11.hitbox[1]:
                if player_obj.hitbox[0] + player_obj.hitbox[2] > Enemy11.hitbox[0] and player_obj.hitbox[0] < Enemy11.hitbox[0] + Enemy11.hitbox[2]:
                    Enemy11.hit()
        if Enemy12.visible:
            if player_obj.hitbox[1] < Enemy12.hitbox[1] + Enemy12.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > Enemy12.hitbox[1]:
                if player_obj.hitbox[0] + player_obj.hitbox[2] > Enemy12.hitbox[0] and player_obj.hitbox[0] < Enemy12.hitbox[0] + Enemy12.hitbox[2]:
                    Enemy12.hit()
        if Enemy13.visible:
            if player_obj.hitbox[1] < Enemy13.hitbox[1] + Enemy13.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > Enemy13.hitbox[1]:
                if player_obj.hitbox[0] + player_obj.hitbox[2] > Enemy13.hitbox[0] and player_obj.hitbox[0] < Enemy13.hitbox[0] + Enemy13.hitbox[2]:
                    Enemy13.hit()
    elif (z==12) and not Level_Check_7:
        platform1[0] = Platform(548,353,104,23)
        platform2[0] = Platform(290,336,90,23)
        platform3[0] = Platform(440,226,98,21)
        platform4[0] = Platform(220,133,95,20)
        platform5[0] = Platform(610,133,143,19)
        platform6[0] = Platform(800,236,131,20)
        platform7[0] = Platform(965,382,81,19)
        platform8[0] = Platform(1085,284,102,23)
        platform9[0] = Platform(39,503,1145,5)
        platform10[0] = Platform(0,0,0,0)
        platform11[0] = Platform(0,0,0,0)
        platform12[0] = Platform(0,0,0,0)     
        exit_obj = exit(540,378,92,133)
        if Enemy8.visible:
            enemies.remove(Enemy8)
        if Enemy9.visible:
            enemies.remove(Enemy9)
        if Enemy10.visible:
            enemies.remove(Enemy10)
        if Enemy11.visible:
            enemies.remove(Enemy11)
        if Enemy12.visible:
            enemies.remove(Enemy12)
        if Enemy13.visible:
            enemies.remove(Enemy13)
        Level_Check_7 = True 
        target_obj = [Target(0,0,0,0), Target(0,0,0,0), Target(0,0,0,0),Target(1059,372,105,125)]
    elif (z==13):
        target_obj = [Target(0,0,0,0), Target(0,0,0,0), Target(0,0,0,0),Target(0,0,0,0)]
    elif (z==14) and not Level_Check_8:
        platform1[0] = Platform(36,457,1149,52)
        platform2[0] = Platform(330,394,77,17)
        platform3[0] = Platform(490,351,81,14)
        platform4[0] = Platform(685,312,78,13)
        platform5[0] = Platform(765,157,76,19)
        platform6[0] = Platform(240,270,144,20)
        platform7[0] = Platform(60,232,117,11)
        platform8[0] = Platform(56,108,633,24)
        platform9[0] = Platform(0,0,0,0)
        platform10[0] = Platform(0,0,0,0)
        platform11[0] = Platform(0,0,0,0)
        platform12[0] = Platform(0,0,0,0)     
        exit_obj = exit(1093,392,93,66)
        enemies.append(Enemy14)
        Enemy14.visible=True
        enemies.append(Enemy15)
        Enemy15.visible=True
        enemies.append(Enemy16)
        Enemy16.visible=True
        key_obj4.collected = False
        key_obj5 = key(897,250,64,64)
        key_obj5.visible=True
        key_obj5.collected=False
        key_obj6 = key(55,76,64,64)
        key_obj6.visible=True
        key_obj6.collected=False 
        key_obj7 = key(50,217,64,64)
        key_obj7.visible=True
        key_obj7.collected=False  
        key_obj8 = key(308,375,64,64)
        key_obj8.visible=True
        key_obj8.collected=False  
        key_obj9 = key(786,127,64,64)
        key_obj9.visible=True
        key_obj9.collected=False   
        Level_Check_8 = True 
    elif z==14:
        Enemy14.draw(win)
        Enemy15.draw(win)
        Enemy16.draw(win)
        if player_obj.hitbox[1] < key_obj5.hitbox[1] + key_obj5.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > key_obj5.hitbox[1]:
            if player_obj.hitbox[0] + player_obj.hitbox[2] > key_obj5.hitbox[0] and player_obj.hitbox[0] < key_obj5.hitbox[0] + key_obj5.hitbox[2]:
                if not key_obj5.collected:
                    key_obj5.hit()

        if player_obj.hitbox[1] < key_obj6.hitbox[1] + key_obj6.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > key_obj6.hitbox[1]:
            if player_obj.hitbox[0] + player_obj.hitbox[2] > key_obj6.hitbox[0] and player_obj.hitbox[0] < key_obj6.hitbox[0] + key_obj6.hitbox[2]:
                if not key_obj6.collected:
                    key_obj6.hit()

        if player_obj.hitbox[1] < key_obj7.hitbox[1] + key_obj7.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > key_obj7.hitbox[1]:
            if player_obj.hitbox[0] + player_obj.hitbox[2] > key_obj7.hitbox[0] and player_obj.hitbox[0] < key_obj7.hitbox[0] + key_obj7.hitbox[2]:
                if not key_obj7.collected:
                    key_obj7.hit()

        if player_obj.hitbox[1] < key_obj8.hitbox[1] + key_obj8.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > key_obj8.hitbox[1]:
            if player_obj.hitbox[0] + player_obj.hitbox[2] > key_obj8.hitbox[0] and player_obj.hitbox[0] < key_obj8.hitbox[0] + key_obj8.hitbox[2]:
                if not key_obj8.collected:
                    key_obj8.hit()

        if player_obj.hitbox[1] < key_obj9.hitbox[1] + key_obj9.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > key_obj9.hitbox[1]:
            if player_obj.hitbox[0] + player_obj.hitbox[2] > key_obj9.hitbox[0] and player_obj.hitbox[0] < key_obj9.hitbox[0] + key_obj9.hitbox[2]:
                if not key_obj9.collected:
                    key_obj9.hit()

        if Enemy14.visible:
            if player_obj.hitbox[1] < Enemy14.hitbox[1] + Enemy14.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > Enemy14.hitbox[1]:
                if player_obj.hitbox[0] + player_obj.hitbox[2] > Enemy14.hitbox[0] and player_obj.hitbox[0] < Enemy14.hitbox[0] + Enemy14.hitbox[2]:
                    Enemy14.hit()
        if Enemy15.visible:
            if player_obj.hitbox[1] < Enemy15.hitbox[1] + Enemy15.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > Enemy15.hitbox[1]:
                if player_obj.hitbox[0] + player_obj.hitbox[2] > Enemy15.hitbox[0] and player_obj.hitbox[0] < Enemy15.hitbox[0] + Enemy15.hitbox[2]:
                    Enemy15.hit()
        if Enemy16.visible:
            if player_obj.hitbox[1] < Enemy16.hitbox[1] + Enemy16.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > Enemy16.hitbox[1]:
                if player_obj.hitbox[0] + player_obj.hitbox[2] > Enemy16.hitbox[0] and player_obj.hitbox[0] < Enemy16.hitbox[0] + Enemy16.hitbox[2]:
                    Enemy16.hit()
    elif z==15 and not enemy_check_3:
        if Enemy14.visible:
            enemies.remove(Enemy14)
        if Enemy15.visible:
            enemies.remove(Enemy15)
        if Enemy16.visible:
            enemies.remove(Enemy16)
        enemy_check_3 = True
    elif z==16 and not Level_Check_9:
        platform1[0] = Platform(40,448,1144,63)
        platform2[0] = Platform(830,397,62,22)
        platform3[0] = Platform(990,345,65,52)
        platform4[0] = Platform(1133,286,48,39)
        platform5[0] = Platform(590,344,76,15)
        platform6[0] = Platform(331,319,48,13)
        platform7[0] = Platform(208,286,102,15)
        platform8[0] = Platform(70,217,88,16)
        platform9[0] = Platform(454,198,553,26)
        platform10[0] = Platform(0,0,0,0)
        platform11[0] = Platform(0,0,0,0)
        platform12[0] = Platform(0,0,0,0)     
        exit_obj = exit(527,47,98,67)
        enemies.append(Enemy17)
        Enemy17.visible=True
        enemies.append(Enemy18)
        Enemy18.visible=True
        enemies.append(Enemy19)
        Enemy19.visible=True
        Level_Check_9=True
        target_obj = [Target(0,0,0,0), Target(0,0,0,0), Target(0,0,0,0),Target(0,0,0,0),Target(438,267,58,79)]
    elif z==17 and not Level_Check_10:
        exit_obj = exit(527,47,98,67)
        key_obj9.collected = False
        key_obj10 = key(897,250,64,64)
        key_obj10.visible=True
        key_obj10.collected=False
        key_obj11 = key(55,76,64,64)
        key_obj11.visible=True
        key_obj11.collected=False
        target_obj = [Target(0,0,0,0), Target(0,0,0,0), Target(0,0,0,0),Target(0,0,0,0),Target(0,0,0,0)]
        enemies.append(Enemy20)
        Enemy20.visible=True
        enemies.append(Enemy21)
        Enemy21.visible=True
        enemies.append(Enemy22)
        Enemy22.visible=True
        if Enemy17.visible:
            enemies.remove(Enemy17)
        if Enemy18.visible:
            enemies.remove(Enemy18)
        if Enemy19.visible:
            enemies.remove(Enemy19)
        Level_Check_10=True
    elif z==16:
        Enemy17.draw(win)
        Enemy18.draw(win)
        Enemy19.draw(win)
        if Enemy17.visible:
            if player_obj.hitbox[1] < Enemy17.hitbox[1] + Enemy17.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > Enemy17.hitbox[1]:
                if player_obj.hitbox[0] + player_obj.hitbox[2] > Enemy17.hitbox[0] and player_obj.hitbox[0] < Enemy17.hitbox[0] + Enemy17.hitbox[2]:
                    Enemy17.hit()
        if Enemy18.visible:
            if player_obj.hitbox[1] < Enemy18.hitbox[1] + Enemy18.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > Enemy18.hitbox[1]:
                if player_obj.hitbox[0] + player_obj.hitbox[2] > Enemy18.hitbox[0] and player_obj.hitbox[0] < Enemy18.hitbox[0] + Enemy18.hitbox[2]:
                    Enemy18.hit()
        if Enemy19.visible:
            if player_obj.hitbox[1] < Enemy19.hitbox[1] + Enemy19.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > Enemy19.hitbox[1]:
                if player_obj.hitbox[0] + player_obj.hitbox[2] > Enemy19.hitbox[0] and player_obj.hitbox[0] < Enemy19.hitbox[0] + Enemy19.hitbox[2]:
                    Enemy19.hit()
    elif z==17:
        Enemy20.draw(win)
        Enemy21.draw(win)
        Enemy22.draw(win)

        if player_obj.hitbox[1] < key_obj10.hitbox[1] + key_obj10.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > key_obj10.hitbox[1]:
            if player_obj.hitbox[0] + player_obj.hitbox[2] > key_obj10.hitbox[0] and player_obj.hitbox[0] < key_obj10.hitbox[0] + key_obj10.hitbox[2]:
                if not key_obj10.collected:
                    key_obj10.hit()

        if player_obj.hitbox[1] < key_obj11.hitbox[1] + key_obj11.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > key_obj11.hitbox[1]:
            if player_obj.hitbox[0] + player_obj.hitbox[2] > key_obj11.hitbox[0] and player_obj.hitbox[0] < key_obj11.hitbox[0] + key_obj11.hitbox[2]:
                if not key_obj11.collected:
                    key_obj11.hit()

        if Enemy20.visible:
            if player_obj.hitbox[1] < Enemy20.hitbox[1] + Enemy20.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > Enemy20.hitbox[1]:
                if player_obj.hitbox[0] + player_obj.hitbox[2] > Enemy20.hitbox[0] and player_obj.hitbox[0] < Enemy20.hitbox[0] + Enemy20.hitbox[2]:
                    Enemy20.hit()
        if Enemy21.visible:
            if player_obj.hitbox[1] < Enemy21.hitbox[1] + Enemy21.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > Enemy21.hitbox[1]:
                if player_obj.hitbox[0] + player_obj.hitbox[2] > Enemy21.hitbox[0] and player_obj.hitbox[0] < Enemy21.hitbox[0] + Enemy21.hitbox[2]:
                    Enemy21.hit()
        if Enemy22.visible:
            if player_obj.hitbox[1] < Enemy22.hitbox[1] + Enemy22.hitbox[3] and player_obj.hitbox[1] + player_obj.hitbox[3] > Enemy22.hitbox[1]:
                if player_obj.hitbox[0] + player_obj.hitbox[2] > Enemy22.hitbox[0] and player_obj.hitbox[0] < Enemy22.hitbox[0] + Enemy22.hitbox[2]:
                    Enemy22.hit()
    elif z ==18 and not enemy_check_4:
        if Enemy20.visible:
            enemies.remove(Enemy20)
        if Enemy21.visible:
            enemies.remove(Enemy21)
        if Enemy22.visible:
            enemies.remove(Enemy22)     
        enemy_check_4 = True 
    
    if input_active:
        play_time = elapsed_time
        win.blit(bg[z], (0, 0))
        input_surface = font.render("Enter Your Name: " + input_text, True, (255, 255, 255))
        input_rect = input_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        win.blit(input_surface, input_rect)
    elif z==19:
        exit_obj = exit(1200,0,0,0)
    elif z==20:
        pygame.display.update()

    else:
        win.blit(bg[z], (0, 0))

        if z >= 2 and z <= 18 and start_time is not None:
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
            timer_text = timer_font.render(f" {elapsed_time} s", True, (255, 201, 14))
            win.blit(timer_text, (784, 628))

        if z >= 2 and z <= 18:
            score_text = score_font.render(f"{score}", True, (255, 201, 14))
            win.blit(score_text, (230, 634))

        if z > 1 and z < 19:
            player_obj.draw(win)

    if z==2:
        Enemy1.draw(win)
        key_obj1.draw(win)
    if z==7:
        Enemy2.draw(win)
        Enemy3.draw(win)
        key_obj2.draw(win)
        key_obj3.draw(win)
        key_obj4.draw(win)
    if z==9:
        Enemy4.draw(win)
        Enemy5.draw(win)
        Enemy6.draw(win)
        Enemy7.draw(win)
    if z==11:
        Enemy8.draw(win)
        Enemy9.draw(win)
        Enemy10.draw(win)
        Enemy11.draw(win)
        Enemy12.draw(win)
        Enemy13.draw(win)
    if z==14:
        Enemy14.draw(win)
        Enemy15.draw(win)
        Enemy16.draw(win)
        key_obj5.draw(win)
        key_obj6.draw(win)
        key_obj7.draw(win)
        key_obj8.draw(win)
        key_obj9.draw(win)
    if z==16:
        Enemy17.draw(win)
        Enemy18.draw(win)
        Enemy19.draw(win)
    if z==17:
        Enemy20.draw(win)
        Enemy21.draw(win)
        Enemy22.draw(win)        
        key_obj10.draw(win)
        key_obj11.draw(win) 

    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()
conn.close()
pygame.quit()
sys.exit()