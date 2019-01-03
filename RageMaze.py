# The RAGE MAZE
# Calvin Tran
# January 25, 2017

import os
import random
import pygame
import time

# A class for the player, which has functions for its movements.

class Player(object):

    def __init__(self,x,y):
        # Create the player at a given spot.
        self.rect = pygame.Rect(x+3, y+3, 10, 10)

    def move(self, dx, dy):
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.moveSingleAxis(dx, 0)
        if dy != 0:
            self.moveSingleAxis(0, dy)
    
    def moveSingleAxis(self, dx, dy):
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # Colliding with a wall will prevent the player from moving depending on the wall the player hits.
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: 
                    self.rect.right = wall.rect.left
                if dx < 0: 
                    self.rect.left = wall.rect.right
                if dy > 0: 
                    self.rect.bottom = wall.rect.top
                if dy < 0:
                    self.rect.top = wall.rect.bottom

    # A respawn function that recreates the player at the given location.

    def respawn(self,x,y):
        self.rect = pygame.Rect(x+3,y+3,10,10)

# A class to hold each wall 'block', which adds it to the list: walls[].

class Wall(object):
    
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

# A class for obstacles, which has functions that control its movement.
    
class Obstacles(object):

    def __init__(self,x,y,width,height):
        self.rect = pygame.Rect(x,y,width,height)

    # Moves the obstacle in the given direction

    def moveVerticallyDown(self,speed):
        self.rect.y += speed

    def moveVerticallyUp(self,speed):
        self.rect.y -= speed

    def moveHorizontallyRight(self,speed):
        self.rect.x += speed

    def moveHorizontallyLeft(self,speed):
        self.rect.x -= speed

# A class for checkpoints, which can be used for several things, such as to replace respawn coordinates, or to trigger traps

class Checkpoint(object):

    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,16,16)

# A small function that is called upon when the "X" button is clicked, which exits the game

def quitGame():
    pygame.quit()
    quit()

# A function that displays the number of deaths during each level

def deathCount(count):
    text = smallFont.render("Deaths: "+str(count),True,white)
    screen.blit(text,(370,1))

# Prints text and gets the rectangle that the text is contained within; Used for the button function.
        
def textObjects(text,font,color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

# Creates a button by checking if the mouse is within the boundaries of a rectangle. If it is, the button will change colour and
# if the mouse is clicked, will perform the function given. Text drawn in the button is automatically centered using the rectangle gained from
# the textObjects function

def button(msg,x,y,w,h,inactiveColor,activeColor,action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen,activeColor,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen,inactiveColor,(x,y,w,h))

    textSurf, textRect = textObjects(msg, mediumFont,black)
    textRect.center = ((x+(w/2),(y+h/2)))
    screen.blit(textSurf,textRect)
    # Adds a border to each button.
    pygame.draw.rect(screen,white,[x,y,w,h], 2)

# A function for the intro screen to the game.

def gameIntro():

    intro = True

    while intro:
        for event in pygame.event.get():
            # If the "X" button is clicked, the game will exit.
            if event.type == pygame.QUIT:
                quitGame()

        # Creates the introduction screen by displaying text and an image.
        
        titleText = largeRageFont.render("RAGE MAZE",True,white)
        screen.blit(titleText,(50,50))

        rageIcon = pygame.image.load('rage.png')
        rageIcon = pygame.transform.scale(rageIcon,(300,270))
        screen.blit(rageIcon,(450,220))

        # Creates a button that, when clicked, calls the instructions() function.
        button("PLAY",150,350,200,100,lightGrey,buttonGrey,instructions)

        # Update the display in order to show everything on the screen.
        pygame.display.update()

        # Make the FPS 10; FPS does not need to be very high during this screen.
        clock.tick(10)

# A function to display the instructions.

def instructions():

    global instruct
    global toLevelSelect

    instruct = True

    while instruct:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()

        # Fill the screen with black to cover the previous screen.
        screen.fill(black)

        # Load in different images. The text for this page must be put in as an image as it uses a font that is not a system font.
        titleText = mediumRageFont.render("INSTRUCTIONS",True,white)
        screen.blit(titleText,(220,50))

        instructionsText = pygame.image.load('instructionsText.png')
        instructionsText = pygame.transform.scale(instructionsText,(750,200))
        screen.blit(instructionsText,(30,160))

        # This will first make a button that leads to the level select page. After that, the only other time this function will be
        # called is during the pause screen, and thus, the continue button will then lead back to the paused screen, instead of
        # the level select page.
        if toLevelSelect:
            button("CONTINUE",250,495,300,80,lightGrey,buttonGrey,levelSelect)
        else:
            button("CONTINUE",250,495,300,80,lightGrey,buttonGrey,paused)
        
        pygame.display.update()
        clock.tick(10)

# A function to allow the player to select the level they want to play.

def levelSelect():

    global toLevelSelect
    # Sets toLevelSelect to False so that when the instructions function is called again, the "Continue" button will lead back to the paused
    # screen instead of the level select page.
    toLevelSelect = False
    
    select = True

    while select:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()

            # Fill the screen with black to clear the previous screen.

            screen.fill(black)

            # Import level select title and scale it.
            
            titleText = mediumRageFont.render("LEVEL SELECT", True, white)
            screen.blit(titleText,(210,40))

            # Create three buttons that calls each level function.

            button("LEVEL 1",20,150,240,440,lightGrey,buttonGrey,levelOne)
            button("LEVEL 2",280,150,240,440,lightGrey,buttonGrey,levelTwo)
            button("LEVEL 3",540,150,240,440,lightGrey,buttonGrey,levelThree)

            levelOneText = levelButtonFont.render("This is easy",True,white)
            screen.blit(levelOneText,(70,250))

            levelOneGoal = smallFont.render("5 deaths or less",True,white)
            screen.blit(levelOneGoal,(78,550))

            levelTwoText = levelButtonFont.render("How do I get in?",True,white)
            screen.blit(levelTwoText,(305,250))

            levelTwoGoal = smallFont.render("7 deaths or less",True,white)
            screen.blit(levelTwoGoal,(340,550))

            levelThreeText = levelButtonFont.render("Please don't quit",True,white)
            screen.blit(levelThreeText,(560,250))

            levelThreeGoal = smallFont.render("10 deaths or less",True,white)
            screen.blit(levelThreeGoal,(595,550))

            greyStarOne = pygame.image.load("star.png")
            greyStarOne = pygame.transform.scale(greyStarOne,(60,60))
            screen.blit(greyStarOne,(110,420))

            # Gives a star to the player if the corresponding variable is true.

            if lvlOneStar:

                yellowStarOne = pygame.image.load("yellowstar.png")
                yellowStarOne = pygame.transform.scale(yellowStarOne,(60,60))
                screen.blit(yellowStarOne,(110,420))

            greyStarTwo = pygame.image.load("star.png")
            greyStarTwo = pygame.transform.scale(greyStarTwo,(60,60))
            screen.blit(greyStarTwo,(370,420))

            if lvlTwoStar:

                yellowStarTwo = pygame.image.load("yellowstar.png")
                yellowStarTwo = pygame.transform.scale(yellowStarTwo,(60,60))
                screen.blit(yellowStarTwo,(370,420))

            greyStarThree = pygame.image.load("star.png")
            greyStarThree = pygame.transform.scale(greyStarThree,(60,60))
            screen.blit(greyStarTwo,(630,420))

            if lvlThreeStar:

                yellowStarThree = pygame.image.load("yellowstar.png")
                yellowStarThree = pygame.transform.scale(yellowStarThree,(60,60))
                screen.blit(yellowStarThree,(630,420))

            pygame.display.update()
            clock.tick(10)

# A function to unpause in the pause menu and return to the game.

def unpause():

    global instruct
    global pause
    pause = False

    # Sets instruct to False so that the instructions do not display again.
    instruct = False

# A function to change the frame rate in the pause menu. This updates the actual frame rate
# as well as the displayed number in the button.

def changeFrameRate():

    global frameRate
    global displayedNumber

    if frameRate == 30:
        frameRate = 60
        displayedNumber = "60"
    elif frameRate == 60:
        frameRate = 20
        displayedNumber = "20"
    elif frameRate == 20:
        frameRate = 30
        displayedNumber = "30"

def mute():

    global muted
    global displayMute

    if muted == True:
        muted = False
        displayMute = "ON"
        pygame.mixer.music.play(-1,0.0) 
    elif muted == False:
        muted = True
        displayMute = "OFF"
        pygame.mixer.music.stop()

# A function to create the pause menu.

def paused():

    global frameRate
    global displayedNumber
    global mute
    global displayMute

    displayedNumber = str(frameRate)
    if muted == True:
        displayMute = "OFF"
    elif muted == False:
        displayMute = "ON"

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
                
        screen.fill(black)
        pauseText = largeRageFont.render("PAUSED",True,white)
        screen.blit(pauseText,(240,50))
        
        rageFace = pygame.image.load('rage.png')
        rageFace = pygame.transform.scale(rageFace,(250,220))
        screen.blit(rageFace,(50,250))
        
        button("CONTINUE",390,200,300,70,lightGrey,buttonGrey,unpause)
        button("LEVEL SELECT",340,280,400,70,lightGrey,buttonGrey,levelSelect)
        button("FPS:" + displayedNumber,340,360,200,70,lightGrey,buttonGrey,changeFrameRate)
        button("?",550,360,190,70,lightGrey,buttonGrey,instructions)
        button("Music: " + displayMute,400,440,280,70,lightGrey,buttonGrey,mute)

        pygame.display.update()
        clock.tick(10)

# A function for level one.

def levelOne():

    global pause
    global frameRate
    global toLevelSelect

    # The list of walls is cleared so that the walls from the previous level played will not be drawn into this level. 

    while len(walls) > 0 :
            walls.pop()

    # Create constants for various parameters so they are easy to work with later.

    obstHeight = 30
    obstWidth = 30
    obstacleColour = blue

    xRespawn = 32
    yRespawn = 32
    
    xCheckpoint = 608
    yCheckpoint = 80
    
    # Create each obstacle and add each one to a list using a for loop.

    obstacles = []

    for i in range(10): 

        obstacles.append(Obstacles(random.randrange(0,displayWidth - obstWidth),0 - random.randrange(200,700),obstWidth,obstHeight))

    # Create four triggers for traps in four different spots in the map.
    
    trollTrigger = Checkpoint(208,16)
    trollTrigger1 = Checkpoint(304,544)
    trollTrigger2 = Checkpoint(464,224)
    trollTrigger3 = Checkpoint(480,192)

    troll = False
    troll1 = False
    troll2 = False

    # Create a variable for the checkpoint sound effect so that it will not continuously replay.

    checkpointSound = True

    # Set the number of deaths to 0.

    deathsOne = 0

    # Holds the level map in a list of strings.
    level = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W     W             W   W             W          W",
    "W S W WWWWWWW WWWWWWW W W W W WWWWWWW   WWWWWW W W",
    "W   W               W W W W W       WWWWW   WW W W",
    "W W W WWWWW WWWWWWW W W W W W W WWW W   W W    W W",
    "W W W W   W W     W W W W W W W W W W C W WWWWWW W",
    "W W W W W W W W W WWW WWW W W W W   W   W  W     W",
    "W W W W W W W W W           W W W WWWW WWW WWWWW W",
    "W W W   W W W W WWWWWWWWWWWWW W W W  W W W     W W",
    "W W WWWWW W W W               W W WW W W WWWWW W W",
    "W W             WWWWWWWWWWWWW   W    W W W   W W W",
    "W WWWWWWWWWW W WW WW W  WWW WWWWWWWWWW W W W W W W",
    "W          W W W   W WW W W W          W   W W W W",
    "WWWWWWWW WWW   W W W  W W   W WWWWWWW WWWWWW W W W",
    "W      W W W W W W W WW W W W W   W   W    W   W W",
    "W WWW  W W W W            W W W W W WWWWWW WWWWW W",
    "W W WW W W W WWWWWWWWWWWWWW W WWW W W W W    WW  W",
    "W W    W W                  W     W W W   WW     W",
    "W WWWWWW WWWWWWWWWWWWWWWWWWWWWW W W     WWWWWWWW W",
    "W              W  WW W        W W WWWWWWW        W",
    "W WWWWWW WWWWW W     WWW WWWW W W  W   WWWWWWWWWWW",
    "W W    W W   W W WWW   W W WW W W  W E           W",
    "W W WW W W W W   W W   W W    W W  W   WWWWWWWWW W",
    "W W W  W W W WWWWW WWW   WWWW W WWWWWWWW       W W",
    "W W WW     W         WWW    WWW W     WWWWWWWW W W",
    "W W WWWWWWWWWWW WWW WW W WW       WW           W W",
    "W               W W    W WWWWWW WWWWW WWWWWWWWWW W",
    "W WWW WWW WWWWWWW WWWW W      W     W W          W",
    "W W W W   W     W    W W WWWWWW WWW W W W W WWWWWW",
    "W W W W WWW WWW WWWW W W          W W W W W      W",
    "W W W W     W W    W W WWWWWWWW W WWW WWWWW WWWW W",
    "W W W WWWWWWW W WWWW W        W W WW   W W   W   W",
    "W W   W       W    W W WWWWWW W W  W W W W   W WWW",
    "W WWWWW W W W W WWWW W      W WWWW W W W W WWW   W",
    "W       W W W        WWWWWW W      W W W   W     W",
    "W WWWWWWW WWWWWWW W    WW W WWWWWWWW W WWWWWWWWW W",
    "W                 WW W    W          W           W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    ]

    # Parse the string above. "W" adds a wall to the list walls[], "E" creates the
    # end rectangle, "S" spawns in the player, "C" creates a checkpoint.
    
    x = y = 0
    for row in level:
        for col in row:
            if col == "W":
                Wall((x, y))
            if col == "E":
                endRect = Checkpoint(x,y)
            if col == "S":
                player = Player(x,y)
                start = Checkpoint(x,y)
            if col == "C":
                check = Checkpoint(x,y)
            x += 16
        y += 16
        x = 0

    running = True
    coin = False

    # Begin running the actual level.

    while running:
        
        clock.tick(frameRate)

        # Moves each obstacle at a speed based on frame rate. If the obstacle reaches the
        # bottom of the screen, it respawns at the top of the screen.

        for i in range(10): 
            obstacle = obstacles[i]
            obstacle.moveVerticallyDown(180/frameRate) 
            if obstacle.rect.y > displayHeight:
                obstacle.rect.y = 0 - random.randrange(200,700)
                obstacle.rect.x = random.randrange(0,displayWidth - obstWidth)      
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            # If the key "p" is pressed, the pause function will be called.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    paused()
            
        # Move the player at a speed based on frame rate if an arrow key is pressed.
        
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            player.move(-120/frameRate, 0)
        if key[pygame.K_RIGHT]:
            player.move(120/frameRate, 0)
        if key[pygame.K_UP]:
            player.move(0, -120/frameRate)
        if key[pygame.K_DOWN]:
            player.move(0, 120/frameRate)

        # Check for collisions 
            
        for i in range(10):
            
            # "Kills" if the player hits an obstacle AND isn't on the starting rectangle or the checkpoint.
            
            if player.rect.colliderect(obstacles[i]) and not player.rect.colliderect(start) and not player.rect.colliderect(check):
                #Plays a sound effect each time the player dies.
                death.play()
                player.respawn(xRespawn,yRespawn)
                deathsOne += 1
                
        # If the player touches the checkpoint, the end rectangle will appear and the game can be finished.
        
        if player.rect.colliderect(check):
            xRespawn = xCheckpoint
            yRespawn = yCheckpoint
            coin = True
            
        if coin:
            if checkpointSound:
                # Plays a sound effect when the player hits the checkpoint.
                checkpoint.play()
                # Makes the checkpointSound variable False so that the checkpointSound plays only once.
                checkpointSound = False
            if player.rect.colliderect(endRect):
                # Play a sound effect when the player finishes the level 
                finish.play()
                global lvlOneStar
                if deathsOne <= 5:
                    lvlOneStar = True
                levelSelect()

        if player.rect.colliderect(trollTrigger):
            troll = True

        if player.rect.colliderect(trollTrigger1):
            troll1 = True

        if player.rect.colliderect(trollTrigger2) or player.rect.colliderect(trollTrigger3):
            troll2 = True
        
        # Draw the various objects on the screen. Note: the trollTriggers do not need to be drawn as they are supposed to be
        # invisible.
        
        screen.fill(black)
        
        for wall in walls:
            pygame.draw.rect(screen, grey, wall.rect)
       
        if coin == True:
            pygame.draw.rect(screen, green, check.rect)
            pygame.draw.rect(screen, red, endRect.rect)
        else:
            pygame.draw.rect(screen, brightGreen, check.rect)

        pygame.draw.rect(screen, white, player.rect)

        for i in range(10):
            pygame.draw.rect(screen, obstacleColour, obstacles[i].rect)

        # Creates a stationary obstacle on the map, if the corresponding variable becomes True.
        
        if troll:
            obstacleTroll = Obstacles(208,48,16,16)
            pygame.draw.rect(screen, obstacleColour, obstacleTroll.rect)
            if player.rect.colliderect(obstacleTroll):
                death.play()
                player.respawn(xRespawn,yRespawn)
                deathsOne +=1
    
        if troll1:
            obstacleTroll1 = Obstacles(272,544,16,16)
            pygame.draw.rect(screen, obstacleColour, obstacleTroll1.rect)
            if player.rect.colliderect(obstacleTroll1):
                death.play()
                player.respawn(xRespawn,yRespawn)
                deathsOne +=1

        if troll2:
            obstacleTroll2 = Obstacles(464,192,16,16)
            pygame.draw.rect(screen, obstacleColour, obstacleTroll2.rect)
            if player.rect.colliderect(obstacleTroll2):
                death.play()
                player.respawn(xRespawn,yRespawn)
                deathsOne +=1
        
        deathCount(deathsOne)

        pygame.display.update()

# A function for level two.

def levelTwo():

    global pause
    global frameRate

    # The list of walls is cleared so that the walls from the previous level played will not be drawn into this level. 

    while len(walls) > 0 :
        walls.pop()

    # Create constants for various parameters so they are easy to work with later.

    obstHeight = 40
    obstWidth = 40
    obstacleColour = blue

    xRespawn = 352
    yRespawn = 303
    
    xCheckpoint = 448
    yCheckpoint = 304

    # Draw each obstacle and add it to a list.

    obstacles = []

    for i in range(7):
        obstacles.append(Obstacles(random.randrange(0,displayWidth - obstWidth),0 - random.randrange(200,700),obstWidth,obstHeight))

    # Create the triggers for various traps.

    startTrollTrigger = Checkpoint(384,304)
    startTrollTrigger1 = Checkpoint(384,288)
    startTrollTrigger2 = Checkpoint(384,320)

    startTroll = False

    endTrollTrigger = Checkpoint(368,512)
    endTrollTrigger1 = Checkpoint(368,528)
    endTrollTrigger2 = Checkpoint(368,544)

    endTroll = False

    trollTrigger = Checkpoint(16,368)
    trollTrigger1 = Checkpoint(320,496)
    trollTrigger2 = Checkpoint(480,496)
    trollTrigger3 = Checkpoint(480,528)

    # Create the trap obstacle for the first trollTrigger (the other traps don't require an obstacle to be created).

    trollObstacle = Obstacles(16,648,32,10)

    troll = False
    troll1 = False
    troll2 = False
    troll3 = False

    # Create a variable for the checkpoint sound effect so that it will not continuously replay.

    checkpointSound = True

    invisWall = Checkpoint(352,528)

    deathsTwo = 0    

    # Holds the level map in a list of strings.
    level = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W                             W                  W",
    "WW W W WWWWWWWWWWWWWW WWW W W W WWWWWWWWWWWWWWW WW",
    "W  W W     W   W    W W W W W W W   W         W  W",
    "W WW W   W   W   W  W W W W W W W W W WWWWWWW WW W",
    "W  W WWWWWWWWWWWWWW W W W     W W W W W     W W  W",
    "WW W    W   W     W W W W  WWWW W W W W W W W W WW",
    "W  W  W   W   W W W W W WWWW    W W W W W W W W  W",
    "W WW WWWWWWWWWW W W W W      WWWW W W W W W W WW W",
    "W W           W WWW W W WWWW W    W W W W W W W  W",
    "W WWWWWWWWW W W     W W W    W WWWWWW W W W   W WW",
    "W W       W W W WWWWW W WWWWWW W      W W WWWWW  W",
    "W W WWWWW W W W W              W WWWWWW W W      W",
    "W W W   W W W W W WWWW WWWWWWWWW W      W W WWWW W",
    "W W W W W W W W W W  W W         W WWWWWW W  W W W",
    "W W W W W W W W W W WW WWWWWWWWW W W      WW W W W",
    "W W W W W W W W W    W W         W W WWWWWW  W W W",
    "W W W W     W   W  WWW WWWWWWWWW W W W      WW W W",
    "W W W WWWWWWWWWWWWWW           WWW W W WWWWWW  W W",
    "W W W                 S     C      W W   W  W  W W",
    "W W WWWWWWWWWWWWWWWW           WWWWW W W   WWW W W",
    "W   W              WWW WWWWWWWWW     WWWWWWW W W W",
    "W WWWWWWWWWWWWWW W   W W         WWW         W   W",
    "W W              W W W WWWWWWWWWWW W WWWWWWWWW W W",
    "W WWWWWWWWWWWWWW W W W             W W         W W",
    "W W            W W W W WWWWWWWWWWWWW W WWW WWWWW W",
    "W WWWWWWWWWW W W W W W W W  W        W W W W  W  W",
    "W          W W     W        W WWWWWWWW W WWW     W",
    "W WWWWWWWW WWWWWWWWWWWWWWWWWW W        W   WW  W W",
    "W W   W                       W WWWWWWWWWW  WWWW W",
    "W   W   W W WWWWWWWWWWWWWWWWWWW W   W    WW      W",
    "W WWWWWWWWW           W     W     W   W   WWWWWW W",
    "W         WWWWWWWWWWWWW     WWWWWWWWWWWWW        W",
    "W WWWWWWWWW              E  W           WWWWWWWW W",
    "W             WWWWWWWWW     WWWWWWWWW            W",
    "W WWWWWWWWWWWWWW   W  W     W  W   WWWWWWWWWWWWW W",
    "W                W   WWWWWWWWW   W               W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    ]

    # Parse the string above. "W" adds a wall to the list walls[], "E" creates the
    # end rectangle, "S" spawns in the player, "C" creates a checkpoint.
    x = y = 0
    for row in level:
        for col in row:
            if col == "W":
                Wall((x, y))
            if col == "E":
                endRect = Checkpoint(x,y)
            if col == "S":
                player = Player(x,y)
                start = Checkpoint(x,y)
            if col == "C":
                check = Checkpoint(x,y)
            
            x += 16
        y += 16
        x = 0

    running = True
    coin = False

    # Begin running the actual level.

    while running:
        
        clock.tick(frameRate)

        # Move each obstacle at a speed based on frame rate. If the obstacle reaches the bottom of the screen, respawn the obstacle at
        # a random spot at the top.

        for i in range(7):
            obstacle = obstacles[i]

            obstacle.moveVerticallyDown(180/frameRate)

            if obstacle.rect.y > displayHeight:
                obstacle.rect.y = 0 - random.randrange(200,700)
                obstacle.rect.x = random.randrange(0,displayWidth - obstWidth)
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()

            # If "p" is pressed, call the pause menu function.

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    paused()
        
        # Move the player at a speed based on frame rate if an arrow key is pressed.
        
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            player.move(-120/frameRate, 0)
        if key[pygame.K_RIGHT]:
            player.move(120/frameRate, 0)
        if key[pygame.K_UP]:
            player.move(0, -120/frameRate)
        if key[pygame.K_DOWN]:
            player.move(0, 120/frameRate)
        
        # Check for collisions.

        for i in range(7):
            if player.rect.colliderect(obstacles[i]) and not player.rect.colliderect(start) and not player.rect.colliderect(check):
                death.play()
                player.respawn(xRespawn,yRespawn)
                deathsTwo += 1

        if player.rect.colliderect(trollObstacle):
            death.play()
            player.respawn(xRespawn,yRespawn)
            deathsTwo += 1

        if player.rect.colliderect(check):
            xRespawn = xCheckpoint
            yRespawn = yCheckpoint
            coin = True
            
        if coin:
            if checkpointSound:
                checkpoint.play()
                # Makes the checkpointSound variable False so that the checkpointSound plays only once.
                checkpointSound = False
            if player.rect.colliderect(endRect):
                finish.play()
                global lvlTwoStar
                if deathsTwo <= 7:
                    lvlTwoStar = True
                levelSelect()
             
        if player.rect.colliderect(startTrollTrigger) or player.rect.colliderect(startTrollTrigger1) or player.rect.colliderect(startTrollTrigger2):
            startTroll = True

        if player.rect.colliderect(endTrollTrigger) or player.rect.colliderect(endTrollTrigger1) or player.rect.colliderect(endTrollTrigger2):
            endTroll = True

        if player.rect.colliderect(trollTrigger):
            troll = True

        # Moves a troll obstacle up if troll becomes True, which occurs if the player hits trollTrigger.

        if troll:
            trollObstacle.moveVerticallyUp(420/frameRate)

        if player.rect.colliderect(trollTrigger1):
            troll1 = True

        if player.rect.colliderect(trollTrigger2):
            troll2 = True

        if player.rect.colliderect(trollTrigger3):
            troll3 = True

        # Draw everything onto the screen.
          
        screen.fill(black)
        
        for wall in walls:
            pygame.draw.rect(screen, grey, wall.rect)
        if coin == True:
            pygame.draw.rect(screen, green, check.rect)
            pygame.draw.rect(screen, red, endRect)
        else:
            pygame.draw.rect(screen, brightGreen, check.rect)

        # Draws stationary obstacles.

        if startTroll:
            startTrollObstacle = Obstacles(400,304,16,16)
            startTrollObstacle1 = Obstacles(400,288,16,16)
            startTrollObstacle2 = Obstacles(400,320,16,16)
            pygame.draw.rect(screen, obstacleColour, startTrollObstacle.rect)
            pygame.draw.rect(screen, obstacleColour, startTrollObstacle1.rect)
            pygame.draw.rect(screen, obstacleColour, startTrollObstacle2.rect)
            if player.rect.colliderect(startTrollObstacle) or player.rect.colliderect(startTrollObstacle1) or player.rect.colliderect(startTrollObstacle2):
                death.play()
                player.respawn(xRespawn,yRespawn)
                deathsTwo +=1

        if endTroll:
            endTrollObstacle = Obstacles(384,512,16,16)
            endTrollObstacle1 = Obstacles(384,528,16,16)
            endTrollObstacle2 = Obstacles(384,544,16,16)
            pygame.draw.rect(screen, obstacleColour, endTrollObstacle.rect)
            pygame.draw.rect(screen, obstacleColour, endTrollObstacle1.rect)
            pygame.draw.rect(screen, obstacleColour, endTrollObstacle2.rect)
            if player.rect.colliderect(endTrollObstacle) or player.rect.colliderect(endTrollObstacle1) or player.rect.colliderect(endTrollObstacle2):
                death.play()
                player.respawn(xRespawn,yRespawn)
                deathsTwo +=1

        if troll1:
            trollObstacle1 = Obstacles(336,496,16,16)
            pygame.draw.rect(screen, obstacleColour, trollObstacle1.rect)
            if player.rect.colliderect(trollObstacle1):
                death.play()
                player.respawn(xRespawn,yRespawn)
                deathsTwo +=1

        if troll2:
            trollObstacle2 = Obstacles(464,496,16,16)
            pygame.draw.rect(screen, obstacleColour, trollObstacle2.rect)
            if player.rect.colliderect(trollObstacle2):
                death.play()
                player.respawn(xRespawn,yRespawn)
                deathsTwo +=1

        if troll3:
            trollObstacle3 = Obstacles(464,528,16,16)
            pygame.draw.rect(screen, obstacleColour, trollObstacle3.rect)
            if player.rect.colliderect(trollObstacle3):
                death.play()
                player.respawn(xRespawn,yRespawn)
                deathsTwo +=1
                
        pygame.draw.rect(screen, grey, invisWall.rect)
        pygame.draw.rect(screen, white, player.rect)
        for i in range(7):
            pygame.draw.rect(screen, obstacleColour, obstacles[i].rect)
        pygame.draw.rect(screen, obstacleColour, trollObstacle.rect)
        
        deathCount(deathsTwo)
        
        pygame.display.update()

# A function for level three.

def levelThree():

    global pause
    global frameRate

    # The list of walls is cleared so that the walls from the previous level played will not be drawn into this level.

    while len(walls) > 0 :
        walls.pop()

    obstHeightLong = 80
    obstWidth = 16
    obstacleColour = blue

    xRespawn = 416
    yRespawn = 32
    
    xCheckpoint = 416
    yCheckpoint = 304
    
    # Create two sets of obstacles, one for obstacles going right and one for obstacles going left. 

    obstaclesRight = []
    obstaclesLeft = []

    for i in range(3):
        obstaclesRight.append(Obstacles(0 - random.randrange(200,700),random.randrange(0,displayHeight - obstHeightLong),obstWidth,obstHeightLong))
        obstaclesLeft.append(Obstacles(displayWidth + random.randrange(200,700),random.randrange(0,displayHeight - obstHeightLong),obstWidth,obstHeightLong))

    # Create the triggers for various traps.

    trollTrigger = Checkpoint(544,272)
    trollTrigger1 = Checkpoint(688,544)
    trollTrigger2 = Checkpoint(768,384)
    trollTrigger3 = Checkpoint(528,224)

    troll = False
    troll1 = False
    troll2 = False
    troll3 = False

    obstacleTroll = Obstacles(-64,144,64,192)
    obstacleTroll1 = Obstacles(900,544,48,48)
    obstacleTroll2 = Obstacles(736,656,48,48)

    # Create a variable for the checkpoint sound effect so that it will not continuously replay.

    checkpointSound = True
    
    deathsThree = 0

    # Holds the level map in a list of strings.
    level = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W                                                W",
    "W WWWWW WWWWWW WWWWWWWWWW S WWWWW WWWW WWWWWWWWW W",
    "W  W                W       W       W       W    W",
    "W WWW WWW W WW WW WWW WW WW WWWWWWW W WWWW WWW WWW",
    "W W W W W W W   W W   W  W  W     W W    W       W",
    "W W W W W W W WWW W W W WWW WWWWW W W WWWWWWWWWW W",
    "W W W W     W W W W WWW W         W W          W W",
    "W W W WW WW W W   W W   WWWWWWWWWWW WWWWW WWWWWW W",
    "W W W     WWW W W W WWW     W           W        W",
    "W W WWWWW     W W W W W WWW W WWWWWWWWW W WWWWWWWW",
    "W W     W W W W W W W W W W W         W W        W",
    "W WWW W W W           W W W WWWWWWW WWW WWWWWWWWWW",
    "W   W WWW WWWWWWWWWWWWW W W       W W W          W",
    "WWW W   W             W W WWWWWWW W W W WWWWWWWW W",
    "W W WWW WWWWWW WWWWWW W W   W   W W W W        W W",
    "W W     W      W      W     W W W WWW W WWWWWWWW W",
    "W W WWWWWWWWWW W WWWWWW WWWWW W       W        W W",
    "W W W          W W      W     W W W W W WWWWWWWW W",
    "W W W W WWWWWW W WWWWWWWW C W W W W W W W        W",
    "W W W W W               W   W W W W W W WW WWWWWWW",
    "W   W W W WWWWWWWWW WWWWWWWWW WWW W W W  W       W",
    "W W W W W         W W    W WWWW   W W W  WWWWWWW W",
    "W W W W WW WWWWWW W WWWW W    WWWWW W WW W       W",
    "W W W             W W    WWWW       W  W W WWW W W",
    "W W    WWWWWWW WWWW W WWWW    W WWWWWW W W   W W W",
    "W WWWW W W          W W  W WWWW    W W W W W W W W",
    "W      W WWWWWWWWW WW WW W W     W   W W W W W W W",
    "W WWWW W       W      W  W WWWWWWWWW W W W W W W W",
    "W    W WWWW WWWW WWWWWW WW             W WWWWW W W",
    "W WWWW    W    W W      WWWWWWWWWWWWWW W       W W",
    "W W  WWWW WWWW W W WWW  W            W W WWWWWWW W",
    "W WW W  W        W W W WW W W WWWWWW W W W       W",
    "W    W WW WWWWWWWW W    W   W W      W W W WWWWWWW",
    "W WWWW  W          WWWWWWWWWW W WWWWWW W W       W",
    "W W  WW W WWWWWWWWWW   W   W  W   W    W WWWWW E W",
    "W       W            W   W    W W   W  W     W   W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    ]

    # Parse the string above. "W" adds a wall to the list walls[], "E" creates the
    # end rectangle, "S" spawns in the player, "C" creates a checkpoint.
    
    x = y = 0
    for row in level:
        for col in row:
            if col == "W":
                Wall((x, y))
            if col == "E":
                endRect = Checkpoint(x,y)
            if col == "S":
                player = Player(x,y)
                start = Checkpoint(x,y)
            if col == "C":
                check = Checkpoint(x,y)
            x += 16
        y += 16
        x = 0

    running = True
    coin = False

    # Begin running the actual level.

    while running:
        
        clock.tick(frameRate)

        # Move each set of obstacles in the corresponding direction at a speed based on frame rate. If the obstacle reaches the
        # opposite side of the screen, respawn the obstacle at a random spot back on the other side of the screen.

        for i in range(3):
            obstacle = obstaclesRight[i]

            obstacle.moveHorizontallyRight(180/frameRate)
            
            if obstacle.rect.x > displayWidth:
                obstacle.rect.x = 0 - random.randrange(0,200)
                obstacle.rect.y = random.randrange(0,displayHeight-obstHeightLong)

            obstacle1 = obstaclesLeft[i]

            obstacle1.moveHorizontallyLeft(180/frameRate)

            if obstacle1.rect.x < 0:
                obstacle1.rect.x = 800 + random.randrange(0,200)
                obstacle1.rect.y = random.randrange(0,displayHeight-obstHeightLong) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()

            # Call the pause menu function if the key "p" is pressed.

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    paused()
            
        
        # Move the player at a speed based on the frame rate if an arrow key is pressed.
        
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            player.move(-120/frameRate, 0)
        if key[pygame.K_RIGHT]:
            player.move(120/frameRate, 0)
        if key[pygame.K_UP]:
            player.move(0, -120/frameRate)
        if key[pygame.K_DOWN]:
            player.move(0, 120/frameRate)
        
        # Check for collisions.

        for i in range(3):
            if player.rect.colliderect(obstaclesRight[i]) and not player.rect.colliderect(start) and not player.rect.colliderect(check):
                death.play()
                player.respawn(xRespawn,yRespawn)
                deathsThree +=1
            if player.rect.colliderect(obstaclesLeft[i]) and not player.rect.colliderect(start) and not player.rect.colliderect(check):
                death.play()
                player.respawn(xRespawn,yRespawn)
                deathsThree+=1

        if player.rect.colliderect(obstacleTroll) or player.rect.colliderect(obstacleTroll1) or player.rect.colliderect(obstacleTroll2):
            death.play()
            player.respawn(xRespawn,yRespawn)
            deathsThree += 1
            
        if player.rect.colliderect(check):
            xRespawn = xCheckpoint
            yRespawn = yCheckpoint
            
            coin = True
            
        if coin:
            if checkpointSound:
                checkpoint.play()
                # Makes the checkpointSound variable False so that the checkpointSound plays only once.
                checkpointSound = False
            if player.rect.colliderect(endRect):
                finish.play()
                global lvlThreeStar
                if deathsThree <= 10:
                    lvlThreeStar = True
                levelSelect()

        if player.rect.colliderect(trollTrigger):
            troll = True

        if player.rect.colliderect(trollTrigger1):
            troll1 = True

        if player.rect.colliderect(trollTrigger2):
            troll2 = True

        if player.rect.colliderect(trollTrigger3): 
            troll3 = True

        # Moves various obstacles if their corresponding triggers are hit.
        
        if troll:
            obstacleTroll.moveHorizontallyRight(480/frameRate)

        if troll1:
            obstacleTroll1.moveHorizontallyLeft(420/frameRate)
            
        if troll2:
            obstacleTroll2.moveVerticallyUp(360/frameRate)

# Draw each object onto the screen.

        screen.fill(black)
        
        for wall in walls:
            pygame.draw.rect(screen, grey, wall.rect)
            
        if coin == True:
            pygame.draw.rect(screen, green, check.rect)
            pygame.draw.rect(screen, red, endRect)
        else:
            pygame.draw.rect(screen, brightGreen, check.rect)
        
        pygame.draw.rect(screen, obstacleColour, obstacleTroll.rect)
        pygame.draw.rect(screen, obstacleColour, obstacleTroll1.rect)
        pygame.draw.rect(screen, obstacleColour, obstacleTroll2.rect)

        # Create a stationary obstacle if troll3 is True.

        if troll3:
            obstacleTroll3 = Obstacles(528,256,16,16)
            pygame.draw.rect(screen, obstacleColour, obstacleTroll3.rect)
            if player.rect.colliderect(obstacleTroll3):
                death.play()
                player.respawn(xRespawn,yRespawn)
                deathsThree +=1

        pygame.draw.rect(screen, white, player.rect)

        for i in range(3):
            pygame.draw.rect(screen, obstacleColour, obstaclesRight[i].rect)
            pygame.draw.rect(screen, obstacleColour, obstaclesLeft[i].rect)
                    
        deathCount(deathsThree)

        pygame.display.update()

# MAIN PROGRAM

# Initialise pygame and create the window in the centre of the screen.

os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Initialise the music player

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.init()

# Create a variable for width and height of display and define colours.

displayWidth = 800
displayHeight = 608

white = (255,255,255)
lightGrey = (80,80,80)
buttonGrey = (50,50,50)
grey = (40,40,40)
green = (47,150,25)
blue = (0,50,255)
black = (0,0,0)
red = (200,0,0)
brightRed = (255,0,0)
brightGreen = (0,255,0)

# Create variables that are used in some functions.

lvlOneStar = False
lvlTwoStar = False
lvlThreeStar = False

pause = False
muted = False

toLevelSelect = True

frameRate = 60

# Define music files and start background music.

music = pygame.mixer.music.load("gameMusic.mp3")
death = pygame.mixer.Sound("smack.ogg")
checkpoint = pygame.mixer.Sound("coin.ogg")
finish = pygame.mixer.Sound("finish.ogg")
pygame.mixer.music.play(-1,0.0)
pygame.mixer.music.set_volume(0.1)

# A list to hold the walls for each level.

walls = []

# Imports various fonts from system fonts and font files.

mediumFont = pygame.font.Font("neutronium.ttf",55)
smallFont = pygame.font.SysFont("courier",14)
levelButtonFont = pygame.font.SysFont("courier",20)

largeRageFont = pygame.font.Font("road_rage.otf",80)
mediumRageFont = pygame.font.Font("road_rage.otf",55)
                            
# Set up the display.

icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

pygame.display.set_caption("RAGE MAZE")
screen = pygame.display.set_mode((displayWidth, displayHeight))

clock = pygame.time.Clock()

# Call the gameIntro function to begin the game.

gameIntro()
