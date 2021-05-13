import pygame
import random

pygame.init()

win = pygame.display.set_mode((400, 600))
pygame.display.set_caption('CATCH THE EGG!')

# IMAGES ------------------------------------------------------------
egg = pygame.transform.scale(pygame.image.load('egg_60x50.png'), (25, 30))
basket = pygame.transform.scale(pygame.image.load('basket_60x130.png'), (65, 30))
bg = pygame.image.load("background.png")


baskNum = 10       # set the total number of baskets
baskArray = []      # to store basket objects
direction = random.choice([-1, 1])  # random direction

curr_bask = 0
nextBask = curr_bask + 1    # to target the next basket

# function to select a random velocity for each basket
def getVel():   
    vel = random.choice([1, 5, -8, 7, 3, 10])
    return vel

#random starting X-coordinate for each basket
def randX():
    return random.randint(60, 400 - 70)

class Egg:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.vel = 0

    def blitEgg(self):
        win.blit(egg, (self.x, self.y))

    def move(self):
        self.x += self.vel * direction
        if self.x >= 400 - 65 + 22 or self.x <= 22:
            self.vel = -self.vel

class Basket:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = getVel()

    def blitBasket(self):
        win.blit(basket, (self.x, self.y))

    def getX(self):
        return self.x

    def setX(self, x):
        self.x = x

    def move(self):
        self.x += self.vel * direction
        if self.x >= 400 - 65 or self.x <= 0:
            self.vel = -self.vel
#creates basket object
def getBasket(a, b):
    return Basket(a, b)

def showScore():
    font = pygame.font.Font('freesansbold.ttf',16)
    text = font.render(str(baskNum-curr_bask-1)+' basket(s) to go!!',True,(255,255,0))
    textRect = text.get_rect()
    textRect.center = (330,15)
    win.blit(text, textRect)
    
def gameOver():
    font = pygame.font.Font('freesansbold.ttf',40)
    text = font.render('Game Over', True, (255,255,255)) 
    textRect = text.get_rect()  
    textRect.center = (200,250)
    win.fill((0,0,0))
    win.blit(text, textRect)

#winning screen
def winScreen():
    font = pygame.font.Font('freesansbold.ttf',50)
    text = font.render('GREAT !!!', True, (0,255,0)) 
    textRect = text.get_rect()  
    textRect.center = (200,250)
    win.fill((0,0,0))
    win.blit(text, textRect)

#refreshes display after each loop
def updateDisplay():
    win.blit(bg, (0, 0))
    eggObj.blitEgg()
    for obj in baskArray:
        if obj == baskArray[len(baskArray) - 1]:
            continue
        obj.blitBasket()
    showScore()
    if eggObj.y >=600:
        gameOver()
    if curr_bask == baskNum - 1:     
        winScreen()
    #pygame.draw.rect(win, (255,0,0), eggBox, 2)
    #pygame.draw.rect(win, (255,255,0), baskBox, 2)
    pygame.display.update()


# OBJECT CREATION AND LOOP-----------------------
eggObj = Egg()      # single egg object
randY = 520         # Y-position of 0th basket

# creating instances of Basket
for count in range(baskNum+1):
    tempObj = getBasket(randX(),randY)
    randY -= 150                        # spacing between baskets
    baskArray.append(tempObj)
eggObj.x = baskArray[curr_bask].x + 22  # centering egg object
eggObj.y = baskArray[curr_bask].y - 20

isJump = False
jumpCount = 10

running = True
while (running):
    pygame.time.delay(40)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # eggBox and baskBox are rectangles for collision detection
    eggBox = pygame.Rect(eggObj.x-8,eggObj.y-5,30,40)
    baskBox = pygame.Rect(baskArray[curr_bask+1].x+10,baskArray[curr_bask+1].y-5,45,40)

    # colliding : True when eggBox intersects baskBox
    colliding = eggBox.colliderect(baskBox)
    
    keys = pygame.key.get_pressed()     # list of keypress events
    if not(isJump):
        eggObj.vel = baskArray[curr_bask].vel
        eggObj.move()
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        eggObj.vel = 0        # X-axis motion of egg freezes when SPACE is pressed
        if jumpCount >= -20:
            neg = 1
            if jumpCount < 0:
                neg = -1
            eggObj.y -= (jumpCount ** 2) * 0.7 * neg
            jumpCount -= 1.5
            if colliding and neg == -1:
                jumpCount = 10
                isJump = False
                curr_bask += 1
                eggObj.x = baskArray[curr_bask].x + 22
                eggObj.y = baskArray[curr_bask].y - 20

        else:
           jumpCount = 10
           isJump = False
    
    for obj in baskArray:
        obj.move()

    #print(curr_bask)
    if curr_bask > 2:
        for obj in baskArray:
            obj.y += 2
        eggObj.y += 2


    updateDisplay()

pygame.quit()



