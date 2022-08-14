# Deep Shah
# July 11th, 2022
# Snake Game created with the pyGame module in Python as a beginner project 

# Importing the pyGame module and the Vector2 and randint functions from the pyGame.math and random module
import pygame 
import sys
from pygame.math import Vector2 
from random import randint 
pygame.init() # This line imports all functions of the pyGame module

class Fruit: # This class has functions to draw the fruit and randomize where it is placed on the next turn

    # Calls the randomize function when this class is called
    def __init__(self): 
        self.randomize()

    # To draw the fruit, the rectangle coordinates are stored in fruitRect and draws them onto the screen using the 2nd line 
    def drawFruit(self): 
        fruitRect = pygame.Rect(int(self.position.x * cellSize), int(self.position.y * cellSize), cellSize, cellSize)
        screen.blit(apple, fruitRect)

    # To randomize the fruit location, a random x and y number is chosen from 0 to 39, and its location (vector) is stored in self.position
    def randomize(self): 
        self.x = randint(0, cellNumber - 1)
        self.y = randint(0, cellNumber - 1)
        self.position = Vector2(self.x, self.y)
        
class Snake: # This class has functions to draw the snake, update the head and tail graphics, move the snake, add a block, play a sound, and reset the game

    def __init__(self):

        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)] # Initializing starting position of snake
        self.direction = Vector2(0, 0) # Direction of snake when game resets
        self.newBlock = False 

        # Importing all the possible snake positions for the head, tail, and body depending on direction
        self.head_up = pygame.image.load('Images/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Images/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Images/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Images/head_left.png').convert_alpha()
		
        self.tail_up = pygame.image.load('Images/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Images/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Images/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Images/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Images/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Images/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Images/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Images/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Images/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Images/body_bl.png').convert_alpha()

        self.crunchSound = pygame.mixer.Sound('Sound/Sound_crunch.wav') # Importing sound for when snake eats the apple

    # To draw the snake, multiple steps have to be taken 
    def drawSnake(self):

        # Calling the update head and tail graphics functions 
        self.updateHeadGraphics() 
        self.updateTailGraphics()

        for index, block in enumerate(self.body): # Enumerate allows there to be an index for each block
                                                  # Loops through the snake body

            # Initializing the x and y position, and the rectangle coordinates for the block 
            xPosition = int(block.x * cellSize) 
            yPosition = int(block.y * cellSize)
            blockRect = pygame.Rect(xPosition, yPosition, cellSize, cellSize)

            if index == 0: screen.blit(self.head, blockRect) # Index 0 refers to the head of the snake
            elif index == len(self.body) - 1: screen.blit(self.tail, blockRect) # The last index refers to the tail of the snake
            else: # If the index is anything other than the first or last index, more steps will be taken

                # Initializing the previous and next block 
                previousBlock = self.body[index + 1] - block
                nextBlock = self.body[index - 1] - block

                if previousBlock.x == nextBlock.x: screen.blit(self.body_vertical, blockRect) # If the x value of the previous and next block are equal, then the snake is in a vertical position
                elif previousBlock.y == nextBlock.y: screen.blit(self.body_horizontal, blockRect) # If the y value of the previous and next block are equal, then the snake is in a horizontal position
                else: # If they are not equal, this means that the snake is turning so the block will have to be curved 
                    if previousBlock.x == -1 and nextBlock.y == -1 or previousBlock.y == -1 and nextBlock.x == -1: screen.blit(self.body_tl, blockRect)
                    elif previousBlock.x == -1 and nextBlock.y == 1 or previousBlock.y == 1 and nextBlock.x == -1: screen.blit(self.body_bl,blockRect)
                    elif previousBlock.x == 1 and nextBlock.y == -1 or previousBlock.y == -1 and nextBlock.x == 1: screen.blit(self.body_tr,blockRect)
                    elif previousBlock.x == 1 and nextBlock.y == 1 or previousBlock.y == 1 and nextBlock.x == 1: screen.blit(self.body_br,blockRect)
                    
    def updateHeadGraphics(self): 

        headRelation = self.body[1] - self.body[0] # Finds the head position 

        # Depending on the head position, the head will either be pointing left, right, up, or down 
        if headRelation == Vector2(1, 0): self.head = self.head_left
        elif headRelation == Vector2(-1, 0): self.head = self.head_right
        elif headRelation == Vector2(0, 1): self.head = self.head_up
        elif headRelation == Vector2(0, -1): self.head = self.head_down

    def updateTailGraphics(self): 

        tailRelation = self.body[-2] - self.body[-1] # Finds the tail position 

        # Depending on the tail position, the tail will either be pointing left, right, up, or down
        if tailRelation == Vector2(1, 0): self.tail = self.tail_left
        elif tailRelation == Vector2(-1, 0): self.tail = self.tail_right
        elif tailRelation == Vector2(0, 1): self.tail = self.tail_up
        elif tailRelation == Vector2(0, -1): self.tail = self.tail_down

    def moveSnake(self): 

        # If the new block is true, the snake should move using these commands 
        if self.newBlock == True: 
            bodyCopy = self.body[:]
            bodyCopy.insert(0, bodyCopy[0] + self.direction)
            self.body = bodyCopy[:]
            self.newBlock = False # Once the body has been copied, new block is set to False so it does not continously add a block
        else: 
            bodyCopy = self.body[:-1]
            bodyCopy.insert(0, bodyCopy[0] + self.direction)
            self.body = bodyCopy[:]

    def addBlock(self):
        self.newBlock = True

    def playCrunchSound(self):
        self.crunchSound.play()

    def reset(self): # Resets the snake position instead of closing the pyGame window entirely 
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)

class Main: # This class updates the game, draws the elements, checks for collision, checks for barriers, resets the game, and draws the grass and score

    # The following 3 functions just calls other functions
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.moveSnake()
        self.checkCollision()
        self.checkFail()

    def drawElements(self):
        self.drawGrass()
        self.fruit.drawFruit()
        self.snake.drawSnake()
        self.drawScore()

    # Checks for collision between the snake and the apple
    def checkCollision(self):
        
        # If the head of the snake is at the same position as the fruit, the fruit is randomized, a block is added to the snake, and the crunch sound is played
        if self.fruit.position == self.snake.body[0]: 
            self.fruit.randomize()
            self.snake.addBlock()
            self.snake.playCrunchSound()

        # If the fruit spawns at the snake's body somewhere, instead of reseting the game, the fruit is randomized as the fruit should not be spawning there
        for block in self.snake.body[1:]:
            if block == self.fruit.position: self.fruit.randomize()

    # Checks if the snake hits any of the barriers 
    def checkFail(self):

        # Ensures that the snake's head is between 0 and 39 in both the x and y direction, and if it is not, the game is over 
        if not 0 <= self.snake.body[0].x < cellNumber or not 0 <= self.snake.body[0].y < cellNumber:
            self.gameOver()

        # If the snake hits itself, the game is also over
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.gameOver()

    def gameOver(self): # Reseting the game using reset function in Snake class
        self.snake.reset()
        
    # Following 2 functions are additional details to the game (grass and score)
    def drawGrass(self): 

        grassColor = (167, 209, 61) 

        # Depending on column, row, odd, and even, this entire loop sets the grid colors appropriately 
        for row in range(cellNumber):
            if row % 2 == 0: # Even
                for column in range(cellNumber):
                    if column % 2 == 0: # Even
                        grassRect = pygame.Rect(column * cellSize, row * cellSize, cellSize, cellSize)
                        pygame.draw.rect(screen, grassColor, grassRect)
            else:
                for column in range(cellNumber):
                    if column % 2 != 0: # Odd
                        grassRect = pygame.Rect(column * cellSize, row * cellSize, cellSize, cellSize)
                        pygame.draw.rect(screen, grassColor, grassRect)

    def drawScore(self):

        scoreText = str(len(self.snake.body) - 3) # The score is always 3 less than the snake's body length 
        scoreSurface = gameFont.render(scoreText, True, (56, 74, 12)) # Setting the text to render on the screen

        # Setting the x and y position of the score location and creating where the score text and apple iamge will be 
        scoreX = int(cellSize * cellNumber - 60) 
        scoreY = int(cellSize * cellNumber - 40)
        scoreRect = scoreSurface.get_rect(center = (scoreX, scoreY))
        appleRect = apple.get_rect(midright = (scoreRect.left, scoreRect.centery))

        # Creating and drawing the border around the score  
        bgRect = pygame.Rect(appleRect.left, appleRect.top, appleRect.width + scoreRect.width + 8, appleRect.height) 
        pygame.draw.rect(screen, (167, 209, 61), bgRect)

        # Displaying everything on the screen
        screen.blit(scoreSurface, scoreRect)
        screen.blit(apple, appleRect)
        pygame.draw.rect(screen, (56, 74, 12), bgRect, 2)

cellSize = 40
cellNumber = 20
screen = pygame.display.set_mode((cellSize * cellNumber, cellSize * cellNumber)) # Setting up the pygame window display

clock = pygame.time.Clock() # Clock for animation look
apple = pygame.image.load('Images/apple.png').convert_alpha() # Importing apple image
gameFont = pygame.font.Font(None, 25) # Font used for score

screenUpdate = pygame.USEREVENT 
pygame.time.set_timer(screenUpdate, 150) # Event signal sent out every 150 ms

mainGame = Main() 

while True: # infinite loop needed to update elements constantly

    for event in pygame.event.get(): # loop runs for each event that occurs

        if event.type == pygame.QUIT: # if the event is closing the pygame window then the window closes and the code stops running
            pygame.quit()
            sys.exit()

        if event.type == screenUpdate: 
            mainGame.update()

        # Depending on the key clicked (up, down, right, or left), the direction of the snake changes (4 different vectors)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if mainGame.snake.direction.y != 1:
                    mainGame.snake.direction = Vector2(0, -1)

            if event.key == pygame.K_DOWN:
                if mainGame.snake.direction.y != -1:
                    mainGame.snake.direction = Vector2(0, 1)

            if event.key == pygame.K_RIGHT:
                if mainGame.snake.direction.x != -1:
                    mainGame.snake.direction = Vector2(1, 0)

            if event.key == pygame.K_LEFT:
                if mainGame.snake.direction.x != 1:
                    mainGame.snake.direction = Vector2(-1, 0)

    screen.fill((175, 215, 70)) # Filling the screen with color
    mainGame.drawElements()
    pygame.display.update() # Draw all elements
    clock.tick(60) # The game will never run at more than 60 fps