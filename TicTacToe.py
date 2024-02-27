import pygame

def drawLine(surface, color, start_pos, end_pos,width):
    pygame.draw.line(surface, color, start_pos, end_pos, width=width)
def drawX(surface, color,gridsize,width,start_pos):
    end_pos = (start_pos[0]+gridsize,start_pos[1]+gridsize)
    drawLine(surface, color, start_pos, end_pos,width)
    end_pos = (start_pos[0],start_pos[1]+gridsize)
    start_pos = (start_pos[0]+gridsize,start_pos[1])
    drawLine(surface, color, start_pos, end_pos,width)
def drawO(surface,color,gridsize,width,firstpos):
    pos = (firstpos[0]+gridsize/2,firstpos[1]+gridsize/2)
    drawCircle(surface, color, pos, gridsize/2, width)
def drawRect(surface, color, x,y,width):
    rect = pygame.Rect(x, y, width, width)
    pygame.draw.rect(surface, color, rect, width=0, border_radius=0, border_top_left_radius=-1, border_top_right_radius=-1,
         border_bottom_left_radius=-1, border_bottom_right_radius=-1)
def drawCircle(surface, color, pos, radius, width):
    pygame.draw.circle(surface, color, pos, radius, width=width)
def renderBase(screen,backgroundcolor,fieldcoler,gridsize,screenWidth,pressedState):
    screen.fill(backgroundcolor)
    for i in range(3):
        xPos = screenWidth/2-gridsize*(1.5-i)
        for x in range(3):
            yPos = screenWidth/2-gridsize*(1.5-x)
            drawRect(screen, fieldcoler[pressedState[x][i]], xPos, yPos, gridsize)
    yPos = screenWidth / 2 - gridsize * (1.5)
    for i in range(2):
        xPos = screenWidth/2-gridsize*(0.5-i)
        drawLine(screen,(255,255,255),(xPos,yPos),(xPos,(yPos + 3*gridsize)),1)
        drawLine(screen, (255, 255, 255), (yPos,xPos), ((yPos + 3 * gridsize),xPos), 1)
def checkIfTouchingRect(gridsize,screenWidth):
    mousePos = pygame.mouse.get_pos()
    xLeftCorner = screenWidth/2-gridsize*(1.5)
    touched = [[0,0,0],
               [0,0,0],
               [0,0,0]]
    for i in range(3):
        for x in range(3):
            xPos = [xLeftCorner +(i*gridsize),xLeftCorner+(gridsize*(i+1))]
            if (mousePos[0] >xPos[0] and mousePos[0] <=xPos[1] and mousePos[1] >xLeftCorner +x*gridsize and mousePos[1] <=xLeftCorner+(gridsize*(x+1))):
                touched[x][i]=1
            else:
                touched[x][i] = 0
    return touched
def checkForNewGameState(pressedState,GameStaten,playerX):
    winner = 0
    for i in range(3):
        for x in range(3):
            if pressedState[i][x] == 1 and GameStaten [i][x] == 0:
                if playerX == True:
                    GameStaten [i][x] = 1
                else:
                    GameStaten[i][x] = 2
                winner = checkForWinner(GameStaten)
                playerX = not playerX
                break
    return GameStaten,playerX,winner

def renderGameState(screen, colorFX,colorFO, gridsize, screenWidth,GameStaten):
    for i in range(3):
        yPos = screenWidth / 2 - gridsize * (1.5 - i)
        for x,state in enumerate(GameStaten[i]):
            xPos = screenWidth / 2 - gridsize * (1.5 - x)
            if state == 1:
                drawX(screen, colorFX,gridsize,1,(xPos,yPos))
            elif state == 2:
                drawO(screen, colorFO,gridsize,1,(xPos,yPos))

def Rendering(screen, backgroundcolor, fieldcoler, gridsize, screenWidth, pressedState,GameStaten):
    renderBase(screen, backgroundcolor, fieldcoler, gridsize, screenWidth, pressedState)
    renderGameState(screen, (255,255,255),(255,255,255), gridsize, screenWidth, GameStaten)

def checkForWinner(Gamestate):
    winner = 0
    Zeros = 0
    for i in range(3):
        for x in Gamestate[i]:
            if x == 0 :
                Zeros+=1
    if Zeros == 0 :
        winner = 3
    for i in range(2):
        for x in range(3):
            if(Gamestate[x][0]==i+1 and Gamestate[x][1] ==i+1 and Gamestate[x][2] == i+1):
                winner = i+1
        for x in range(3):
            if(Gamestate[0][x]==i+1 and Gamestate[1][x] ==i+1 and Gamestate[2][x] == i+1):
                winner = i+1
        if (Gamestate[0][0] == i + 1 and Gamestate[1][1] == i + 1 and Gamestate[2][2] == i + 1):
            winner = i + 1
        elif (Gamestate[0][2] == i + 1 and Gamestate[1][1] == i + 1 and Gamestate[2][0] == i + 1):
            winner = i +1

    return winner
def RenderWinningScreen(winner,backgroundcolor):
    screen.fill(backgroundcolor)
    font = pygame.font.SysFont(None, 50)
    if(winner == 1):
        player = "X"
    elif(winner == 2):
        player = "O"
    else:
        player = "None"
    img = font.render('The Player Who Won Is '+ player, True, (255,255,255))
    screen.blit(img, (100, 100))
    font = pygame.font.SysFont(None, 25)
    img = font.render('Press any key to play again', True, (255, 255, 255))
    screen.blit(img, (200, 400))
def Gamereset():
    winner = 0
    playerX = True
    GameStaten = [[0,0,0],
                  [0,0,0],
                  [0,0,0]]
    return winner,playerX,GameStaten
# pygame setup
pygame.init()
screenWidth = 720
winner = 0
playerX = True
screen = pygame.display.set_mode((screenWidth, screenWidth))
clock = pygame.time.Clock()
running = True
pressedState = [[0,0,0],
                [0,0,0],
                [0,0,0]]
GameStaten= [[0,0,0],
             [0,0,0],
             [0,0,0]]#1=X 2=O
backgroundcolor = (10,10,10)
fieldcoler = ((40,40,40),(80,80,80))


gridsize=100

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif(winner == 0):
            if event.type == pygame.MOUSEBUTTONUP:
                GameStaten,playerX,winner = checkForNewGameState(pressedState,GameStaten,playerX)
        elif(event.type == pygame.KEYDOWN):
            winner,playerX,GameStaten = Gamereset()
    if(winner==0):
        pressedState = checkIfTouchingRect(gridsize,screenWidth)


        Rendering(screen,backgroundcolor,fieldcoler,gridsize,screenWidth,pressedState,GameStaten)
    else:
        RenderWinningScreen(winner,backgroundcolor)
    pygame.display.flip()

    clock.tick(120)

pygame.quit()