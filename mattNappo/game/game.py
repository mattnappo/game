import pyglet
from pyglet.window import key
import random

lasers = []
global runAnimation
runAnimation = False

global indexio
indexio = 0
global arrImages

global leftArrImages
leftArrImages = []
arrImages=[]

for i in range(4):
    tmpImg = pyglet.image.load("img/spr/anim/step"+str(i)+".png")
    runSprite = pyglet.sprite.Sprite(tmpImg, x=45, y=175)
    arrImages.append(runSprite)
    
for i in range(4):
    tmpImg = pyglet.image.load("img/spr/anim/left/step"+str(i)+".png")
    runSprite = pyglet.sprite.Sprite(tmpImg, x=45, y=175)
    leftArrImages.append(runSprite)
    
def updateIndex(dt):
    global indexio
    if runAnimation == True:
        if indexio < 3:
            indexio+=1
        else:
            indexio = 0
    
class Background():
    def __init__(self):
        self.img = pyglet.image.load("img/background.jpg") 
        self.background = pyglet.sprite.Sprite(self.img, x=0, y=0)
class Laser():
    def __init__(self, x, y):
        self.width = 50
        self.height = 14
        self.x = x
        self.y = y
        self.left = False
        self.firedBy = ""
        self.right = False
        self.img = [pyglet.image.load("img/rightLaser.png"), pyglet.image.load("img/leftLaser.png")]
        self.lasers = pyglet.sprite.Sprite(self.img[0], x=self.x, y=self.y)
        self.detected = False
    def detect(self):
        if self.x <= 0:
            lasers.remove(self)
        if self.x >= 1440:
            lasers.remove(self)
    def move(self):
        if self.left == True:
            self.lasers = pyglet.sprite.Sprite(self.img[1], x=self.x, y=self.y)
            self.x = self.x - 10
            self.lasers.x = self.x
        if self.right == True:
            self.lasers = pyglet.sprite.Sprite(self.img[0], x=self.x, y=self.y)
            self.x = self.x + 10
            self.lasers.x = self.x
def moveLaser():
    if lasers:
        for laser in lasers:
            laser.move()
            laser.detect()
class Coin():
    def __init__(self):
        self.value = 1
        self.x = 75
        self.y = 350
        self.height = 75
        self.width = 75
        self.normalCoin = True
        self.img = [pyglet.image.load("img/coin.png"), pyglet.image.load("img/green.png")]
        self.spr = pyglet.sprite.Sprite(self.img[0], x=self.x, y=self.y)
    def spawn(self, points):
        doWhat = random.randint(1, 5)
        if doWhat > 1:
            self.normalCoin = True
            self.x = random.randint(20, 1000)
            self.y = random.randint(300, 600)
            self.spr = pyglet.sprite.Sprite(self.img[0], x=self.x, y=self.y)
            self.spr.x = self.x
            self.spr.y = self.y
        elif doWhat == 1 and points > 20:
            self.normalCoin = False
            self.x = random.randint(20, 1000)
            self.y = random.randint(300, 600)
            self.spr = pyglet.sprite.Sprite(self.img[1], x=self.x, y=self.y)
            self.spr.x = self.x
            self.spr.y = self.y
coins = Coin()
coins.spawn(0)
class Platform():
    def __init__(self, x, y, length):
        self.x = x
        self.y = y
        self.length = length
p1 = Platform(467, 299, 450) # center
p2 = Platform(0, 299, 190) # left
p3 = Platform(1175, 299, 185) # right
p4 = Platform(0, 179, 1440) # ground
p5 = Platform(910, 433, 255) #  upper right
p6 = Platform(200, 433, 260) # upper left
p7 = Platform(447, 588, 470) # upper center
global platforms
platforms = [p1, p2, p3, p4, p5, p6, p7]
background = Background()
class Character():
    def __init__(self, xx, yy):
        '''global arrImages
        global leftArrImagess'''
        self.x = xx
        self.y = yy
        self.health = 100
        self.amount = 7
        self.points = 0
        self.velocity = 0
        self.normalColor = True
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.lastDir = None
        self.width = 80
        self.height = 80
        '''self.rightAnimSprites = arrImages
        self.leftAnimSprites = leftArrImages'''
        self.img = pyglet.image.load("img/spr/right.png")
        self.character = pyglet.sprite.Sprite(self.img, x=self.x, y=self.y)
    def move(self):
        global runAnimation
        #gravity
        self.velocity = self.velocity - .4
        if self.velocity < -8:
            self.velocity = -8
        self.y = self.velocity + self.y
        self.character.y = self.y
        #DETECTION
        for i in range(len(platforms)):
            if self.x >= platforms[i].x and self.x <= platforms[i].x + platforms[i].length:
                if self.y <= platforms[i].y + 4 and self.y >= platforms[i].y - 11:
                    self.velocity = 0
                    self.y = platforms[i].y
                    self.character.y = self.y
        #no movement
        if self.left == False and self.right == False:
            print(self.left)
            print(self.right)
            runAnimation = False
            if self.lastDir == 0:
                if self.normalColor == True:
                    spr = pyglet.image.load("img/spr/left.png")
                    self.character = pyglet.sprite.Sprite(spr, x=self.x, y=self.y)
            elif self.lastDir == 1:
                if self.normalColor == True:
                    spr = pyglet.image.load("img/spr/right.png")
                    self.character = pyglet.sprite.Sprite(spr, x=self.x, y=self.y)
        #jump
        if self.up == True:
            if(self.velocity == 0):
                self.velocity = 9
            self.y = self.velocity + self.y
            self.character.y = self.y
        
        #left and right movement
        if self.left == True:
            self.x = self.x - self.amount
            self.character.x = self.x
            self.lastDir = 0
        if self.right == True:
            self.x = self.x + self.amount
            self.character.x = self.x
            self.lastDir = 1
    def coinDetect(self):
        if self.x + self.width - 5 >= coins.x and self.x <= coins.x + coins.width - 5:
            if self.y + self.height - 5 >= coins.y and self.y <= coins.y + coins.height -5:
                if coins.normalCoin == True:
                    self.normalColor = True
                    self.points+=1
                    coins.spawn(self.points)
                else:
                    self.normalColor = False
                    self.points-=20
                    coins.spawn(self.points)
                    self.health = 100
    def spiderSense(self): #left and right detection
        if self.x <= 0:
            self.health-=1
            self.x = 2
            self.character.x = self.x
        elif self.x >= 1356:
            self.health-=1
            self.x = 1358
            self.character.x = self.x

class Enemy(Character):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.health = 15
        self.width = 80
        self.left = False
        self.lastDir = 0
        self.amount = 3
        self.up = False
        self.down = False
        self.right = False
        self.velocity = 0
        self.normalColor = True
        self.height = 80
        self.direction = ""
        self.img = [pyglet.image.load("img/spr/enemy/right.png"), pyglet.image.load("img/spr/enemy/left.png")]
        self.character = pyglet.sprite.Sprite(self.img[0], x=self.x, y=self.y)
    def spawn(self):
        possibleY = [299,299,299,179,433,443,588]
        place = random.randint(0, 3)
        self.y = possibleY[place]
        possibleX = [random.randint(467,467+450),random.randint(0,0+299),random.randint(1175,1175+185),random.randint(0,1440),random.randint(910,910+255),random.randint(200,200+260),random.randint(447,447+470)]
        self.x = possibleX[place]
        if self.x >= char.x:
            self.direction = "left"
            self.character = pyglet.sprite.Sprite(self.img[1], x=self.x, y=self.y)
        elif self.x <= char.x:
            self.direction = "right"
            self.character = pyglet.sprite.Sprite(self.img[0], x=self.x, y=self.y)
        self.character.x = self.x
        self.character.y = self.y
    def detectLaser(self):
        if len(lasers) != 0: # detect laser
            for i in range(len(lasers)):
                if lasers[i].firedBy == "character":
                    if lasers[i].x >= self.x and lasers[i].x <= self.x + self.width:
                        if lasers[i].y >= self.y and lasers[i].y <= self.y + self.height:
                            if self.health <= 0:
                                self.health = 50
                                char.points+=2
                                self.spawn()
                            else: 
                                self.health-=1

window = pyglet.window.Window(1440, 900)
window.set_caption("Remake of Mario")

global char
char = Character(45, 175)

enemy = Enemy()
enemy.spawn()

keys = key.KeyStateHandler()
window.push_handlers(keys)

enemies = []

@window.event
def on_draw():
    global indexio
    global animSprites
    global leftAnimSprites
    window.clear()
    background.background.draw()
    #char.character.draw()
    if char.right == True or char.left == True:
        if char.lastDir == 1:
            char.character = arrImages[indexio]
        else:
            char.character = leftArrImages[indexio]
    char.character.draw()
    health = pyglet.text.Label("Health: " + str(char.health), font_name='Times New Roman', font_size=36, x=20, y=20)
    health.draw()
    points = pyglet.text.Label("Points: " + str(char.points), font_name='Times New Roman', font_size=36, x=300, y=20)
    points.draw()
    enemy.character.draw()
    coins.spr.draw()
    for x in range(len(lasers)):
        lasers[x].lasers.draw()

@window.event
def on_key_press(symbol, modifiers):
    global runAnimation
    if symbol == key.A:
        char.left = True
        runAnimation = True
    if symbol == key.D:
        char.right = True
        runAnimation = True
    if symbol == key.SPACE:
        char.up = True
    if symbol == key.K:
        background.background = pyglet.sprite.Sprite(pyglet.image.load("img/something.jpg"), x=0, y=0)
def enemyFire(dt):
    laser = Laser(enemy.x, enemy.y)
    if enemy.direction == "right":
        enemy.character = pyglet.sprite.Sprite(enemy.img[0], x=enemy.x, y=enemy.y)
        laser.firedBy = "enemy"
        laser.right = True
        laser.x -= laser.width
    elif enemy.direction == "left":
        enemy.character = pyglet.sprite.Sprite(enemy.img[1], x=enemy.x, y=enemy.y)
        laser.firedBy = "enemy"
        laser.left = True
        laser.x += enemy.width
    if laser.left or laser.right:
        lasers.append(laser)
def enemyKill(): # checks if enemy laser hits character
    global char
    if len(lasers) != 0: # detect laser
        for i in range(len(lasers)): 
            if char.x + char.width >= lasers[i].x and char.x <= lasers[i].x + lasers[i].width:
                if char.y + char.height >= lasers[i].y and char.y <= lasers[i].y + lasers[i].height:
                    char.health-=1
    if char.x + char.width >= enemy.x and char.x <= enemy.x + enemy.width:# Detect character
        if char.y + char.height >= enemy.y and char.y <= enemy.y + enemy.height:
            char.health-=2
def dead():
    global char
    if char.health <= 0:
        platforms = []
        background.img = pyglet.image.load("img/gameOver.jpg")
        background.background = pyglet.sprite.Sprite(background.img, x=0, y=0)
        char.character = pyglet.sprite.Sprite(pyglet.image.load("img/nothing.png"), x=0, y=0)
        coins.spr = pyglet.sprite.Sprite(pyglet.image.load("img/nothing.png"), x=0, y=0)
def changeEnemyLocation():
    global platforms
    if enemy.x > char.x:
        enemy.direction = "left"
        enemy.right = False
        enemy.left = True
        enemy.character = pyglet.sprite.Sprite(enemy.img[1], x=enemy.x, y=enemy.y)
    elif enemy.x < char.x:
        enemy.direction = "right"
        enemy.left = False
        enemy.right = True
        enemy.character = pyglet.sprite.Sprite(enemy.img[0], x=enemy.x, y=enemy.y)
    print(enemy.x)
    print(char.x)
    if enemy.x == char.x:
        if char.lastDir == 1:
            enemy.direction = "left"
            enemy.right = False
            enemy.left = True
            enemy.character = pyglet.sprite.Sprite(enemy.img[1], x=enemy.x, y=enemy.y)
        else:
            enemy.direction = "right"
            enemy.left = False
            enemy.right = True
            enemy.character = pyglet.sprite.Sprite(enemy.img[0], x=enemy.x, y=enemy.y)
    for z in range(len(platforms)):
        if enemy.x + enemy.width >= platforms[z].x and enemy.x <= platforms[z].x + platforms[z].length:
            if platforms[z].y - 155 > enemy.y :
                enemy.up = True
            else:
                enemy.up = False
@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        laser = Laser(char.x, char.y)
        laser.firedBy = "character"
        if not(char.left or char.right):
            if char.lastDir == False:
                laser.firedBy = "character"
                laser.left = True
                laser.x -= laser.width
            else:
                laser.firedBy = "character"
                laser.right = True
                laser.x += char.width
        elif char.left == True:
            laser.firedBy = "character"
            laser.left = True
            laser.x -= laser.width
        elif char.right == True:
            laser.firedBy = "character"
            laser.right = True
            laser.x += char.width
        if laser.left or laser.right:
            lasers.append(laser)
@window.event
def on_key_release(symbol, modifiers):
    global runAnimation
    if symbol == key.A:
        char.left = False
    if symbol == key.D:
        char.right = False
    if symbol == key.SPACE:
        char.up = False
def deClogger(dt):
    moveLaser()
    char.move()
    enemy.move()
    char.spiderSense()
    char.coinDetect()
    enemy.detectLaser()
    enemyKill()
    dead()
    changeEnemyLocation()
    
pyglet.clock.schedule_interval(deClogger, 1/60.0)
pyglet.clock.schedule_interval(enemyFire, 1/0.8)
pyglet.clock.schedule_interval(updateIndex,1/6)
pyglet.app.run()