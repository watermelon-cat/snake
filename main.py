import pygame
import random
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((600, 440))
pygame.display.set_caption("SNEK")
clock = pygame.time.Clock()

#game variables
running = True
xpos = 0
ypos = 0
mousePos = (xpos, ypos)
press = False
ticker = 0
score = 0
try:
    pygame.mixer.music.load("crape.ogg")
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play(-1) #-1 means loop forever
except:
        ("sound didn't load")

#snake variables
snake = [
    [10, 8], #head
    [9, 8], #body segment 1
    [8, 8] #body segment 2
]

dx = 1 #speed going left/right
dy = 0 #speed going up/down
alive = True
Red = (158, 33, 44)
Blue = (54, 67, 201)
Green = (55, 122, 60)
Purple = (115, 55, 122)
White = (255, 255, 255)
Pink = (230, 124, 194)
colorInput = Green

try:
    bite = pygame.mixer.Sound("bite.wav")
    bite.set_volume(1)
    
except:
    bite = None
    print("sound didn't load")


#Function DEFs
def draw_gird():
    #draw vertical lines
    for x in range(0, 600, 20):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, 440))
    for y in range(0, 440, 20):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (600, y))
    
def draw_snake_head(x_cell, y_cell, color):
    pygame.draw.rect(screen, (color), (x_cell * 20, y_cell * 20, 20, 20))
    
def spawn_food(snake_list):
    #keep trying random cells untill we find one not on the snake
    while True:
        fx = random.randint(0, 29) #30 colums
        fy = random.randint(0, 21) #22 rows
        if [fx, fy] not in snake_list:
            return [fx, fy] #return statements exit the function

food = spawn_food(snake)

title = pygame.image.load("title.png")
title = pygame.transform.scale(title, (600, 440))
start_time = pygame.time.get_ticks()
while True:
    clock.tick(60)
    #if pygame.time.get_ticks() - start_time > 4000: #4 seconds
        #break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            mousePos = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            press = True
        if event.type == pygame.MOUSEBUTTONUP:
            press = False
    if mousePos[0] > 450 and mousePos[0] < 520 and mousePos[1] > 250 and mousePos[1] < 300 and press == True:
        colorInput = Red
        break
    elif mousePos[0] > 520 and mousePos[0] < 590 and mousePos[1] > 250 and mousePos[1] < 300 and press == True:
        colorInput = Blue
        break
    elif mousePos[0] > 450 and mousePos[0] < 520 and mousePos[1] > 300 and mousePos[1] < 350 and press == True:
        colorInput = Green
        break
    elif mousePos[0] > 520 and mousePos[0] < 590 and mousePos[1] > 300 and mousePos[1] < 350 and press == True:
        colorInput = Purple
        break
    elif mousePos[0] > 450 and mousePos[0] < 520 and mousePos[1] > 350 and mousePos[1] < 400 and press == True:
        colorInput = White
        break
    elif mousePos[0] > 520 and mousePos[0] < 590 and mousePos[1] > 350 and mousePos[1] < 400 and press == True:
        colorInput = Pink
        break
        
    screen.blit(title, (0, 0))
    pygame.draw.rect(screen, (158, 33, 44), (450, 250, 70, 50)) #red square
    pygame.draw.rect(screen, (54, 67, 201), (520, 250, 70, 50)) #blue square
    pygame.draw.rect(screen, (55, 122, 60), (450, 300, 70, 50)) #green square
    pygame.draw.rect(screen, (115, 55, 122), (520, 300, 70, 50)) #purple square
    pygame.draw.rect(screen, (255, 255, 255), (450, 350, 70, 50)) #big square
    pygame.draw.rect(screen, (230, 124, 194), (520, 350, 70, 50)) #big square
    pygame.display.flip()
    
    
while running:
    clock.tick(60)
        
    #input section----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if dx == 0:
                if event.key == pygame.K_RIGHT:
                    dx = 1
                    dy = 0
                elif event.key == pygame.K_LEFT:
                    dx = -1
                    dy = 0
            if dy == 0:
                if event.key == pygame.K_UP:
                    dx = 0
                    dy = -1
                elif event.key == pygame.K_DOWN:
                    dx = 0
                    dy = 1
    #physics section---------------
    ticker += 1
    if alive:
        if ticker % 4 == 0:
            ticker = 0
            head_x = snake[0][0]
            head_y = snake[0][1]
            
            #set a new head to be the cell in front of us
            new_head = [head_x + dx, head_y + dy]
            if new_head in snake[:-1]:
                alive = False
            
            #check if you've bonked a wall
            if new_head[0] < 0 or new_head[0] > 29 or new_head[1] < 0 or new_head[1] > 21:
                alive = False
            else: #no wall bonk means move to the next cell
                
                snake.insert(0, new_head)#insert new head at beginning of list
                
                #check if we have hit food
                if new_head[0] == food[0] and new_head[1] == food[1]:
                    bite.play()
                    food = spawn_food(snake)
                    score += 1
                    
                else:
                    snake.pop()#remove last body segment to keep length the same
            
            
    #render section----------------
    screen.fill((0,0,0))
    draw_gird()
    
    pygame.draw.rect(screen, (200, 40, 40), (food[0]* 20, food[1]*20, 20, 20)) #draw the food
    
    i = 0
    while i < len(snake):
        part = snake[i]
        draw_snake_head(part[0], part[1], colorInput)
        i = i + 1
        
    if not alive:
        #display a simple "Game over:
        font = pygame.font.SysFont(None, 48)
        text = font.render("you suck :)", True, (255, 255, 255))
        screen.blit(text, (220, 200))
    font = pygame.font.SysFont(None, 48)
    text2 = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(text2, (8, 8))
    pygame.display.flip()
    
pygame.quit()
