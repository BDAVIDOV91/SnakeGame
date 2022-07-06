import pygame
import sys
import time
import random

#Set up diffculty - 10, 25, 40, 60, 120
difficulty = 10

#Setup windows size
frameSize_x = 720
frameSize_y = 480

#Chekc for errors
checkErrors = pygame.init()

if checkErrors[1] > 0:
    print(f'[!] Had {checkErrors[1]} errors when initialising game, exiting...')
    sys.exit(-1)

else:
    print('[+] Game successfully initialised')

#Initialise game window
pygame.display.set_caption('Snake Eater')
gameWindow = pygame.display.set_mode((frameSize_x, frameSize_y))

#Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# fps controller 
fpsController = pygame.time.Clock()

#veriables

snakePos = [100, 50]
snakeBody = [[100,50], [100-10, 50], [100-(2*10), 50]]

foodPos = [random.randrange(1, (frameSize_x//10)) * 10, random.randrange(1, (frameSize_y//10) * 10)]
foodSpawn = True

direction = 'RIGHT'
changeTo = direction

score = 0

# game over section

def gameOver():
    myFont = pygame.font.SysFont('JEEZ', 90)
    gameOverSurface = myFont.render('You Died', True, red)
    gameOverRect = gameOverSurface.get_rect()
    gameOverRect.midtop = (frameSize_x/2, frameSize_y/4)
    gameWindow.fill(black)
    gameWindow.blit(gameOverSurface, gameOverRect)
    #show_score def later
    showScore(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit

# score

def showScore(choice, color, font, size):
    scoreFont = pygame.font.SysFont(font, size)
    scoreSurface = scoreFont.render('Score : ' + str(score), True, color)
    scoreRect = scoreSurface.get_rect()
    if choice == 1:
        scoreRect.midtop = (frameSize_x/10 , 15)
    else:
        scoreRect.midtop = (frameSize_x/2 , frameSize_y/1.25)
    gameWindow.blit(scoreSurface, scoreRect)

# logic 

while True:
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            pygame.quit()
            sys.exit

        elif event.type == pygame.KEYDOWN:
            # w - up  s - down a - left d - right
            if event.key == pygame.K_UP or event.key == ord('w'):
                changeTo = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                changeTo = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                changeTo = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                changeTo = 'RIGHT'

            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))


    if changeTo == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if changeTo == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if changeTo == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if changeTo == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT' 


    # moving the snake
    if direction == 'UP':
        snakePos[1] -= 10
    if direction == 'DOWN':
        snakePos[1] += 10
    if direction == 'LEFT':
        snakePos[0] -= 10
    if direction == 'RIGHT':
        snakePos[0] += 10


    #snake growing
    snakeBody.insert(0 , list(snakePos))
    if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
        score += 1
        foodSpawn = False
    else:
        snakeBody.pop()

    #food on screen
    if not foodSpawn:
        foodPos = [random.randrange(1, (frameSize_x//10)) * 10, random.randrange(1, (frameSize_y//10)) * 10]
    foodSpawn = True

    gameWindow.fill(black)
    for pos in snakeBody:
        pygame.draw.rect(gameWindow, green, pygame.Rect(pos[0], pos[1], 10, 10))

    #snake food
    pygame.draw.rect(gameWindow, white, pygame,pygame.Rect(foodPos[0], foodPos[1], 10, 10))


    #game over condition
    if snakePos[0] < 0 or snakePos[0] > frameSize_x-10:
        gameOver()
    if snakePos[1] <0 or snakePos[1] > frameSize_y-10:
        gameOver()

    for block in snakeBody[1:]:
        if snakePos[0] == block[0] and snakePos[1] == block[1]:
            gameOver()


    showScore(1, white, 'consola', 20)
    pygame.display.update()
    fpsController.tick(difficulty)