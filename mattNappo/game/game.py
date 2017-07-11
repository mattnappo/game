import pyglet, random
from time import time
from pyglet.window import key

lasers = []
global runAnimation
runAnimation = False
global runEnemyAnimation
enemyRunAnimation = True
global indexio
indexio = 0
global eIndex
eIndex = 0
global caller
caller = False
global leftArrImages
leftArrImages = []
global arrImages
arrImages=[]
global yellowLeftArrImages
yellowLeftArrImages = []
global yellowArrImages
yellowArrImages=[]
global enemyArrImages
enemyArrImages = []
global leftEnemyArrImages
leftEnemyArrImages=[]
global coinIndex
coinIndex = 0
global coinAnimation
coinAnimation = True
global coinArrImages
coinArrImages = []
def loader(location, listName, amount):
    for i in range(amount):
        tmpImg = pyglet.image.load(location+str(i)+".png")
        runSprite = pyglet.sprite.Sprite(tmpImg, x=0, y=-0)
        listName.append(runSprite)
loader("img/spr/anim/step", arrImages, 4)
loader("img/spr/anim/left/step", leftArrImages, 4)
loader("img/spr/anim/yellow/step", yellowArrImages, 4)
loader("img/spr/anim/yellow/left/step", yellowLeftArrImages, 4)
loader("img/spr/anim/enemy/step", enemyArrImages, 4)
loader("img/spr/anim/enemy/left/step", leftEnemyArrImages, 4)
loader("img/coin/anim/", coinArrImages, 6)
def updateIndex(dt):
    global indexio
    if runAnimation == True:
        if indexio < 3:
            indexio+=1
        else:
            indexio = 0
def updateEIndex(dt):
    global eIndex
    if enemyRunAnimation == True:
        if eIndex < 3:
            eIndex+=1
        else:
            eIndex = 0
def updateCoinIndex(dt):
    global coinIndex
    if coinAnimation == True:
        if coinIndex < 5:
            coinIndex+=1
        else:
            coinIndex = 0
class Background():
    def __init__(self):
        self.img = pyglet.image.load("img/backgrounds/lvl1.jpg") 
        self.background = pyglet.sprite.Sprite(self.img, x=0, y=0)
class Laser():
    def __init__(self, x, y, heavy):
        self.width = 50
        self.height = 14
        self.x = x
        self.y = y
        self.left = False
        self.heavy = heavy
        self.firedBy = ""
        self.right = False
        self.img = [pyglet.image.load("img/laser/rightLaser.png"), 
                    pyglet.image.load("img/laser/leftLaser.png"), 
                    pyglet.image.load("img/laser/enemy/right.png"), 
                    pyglet.image.load("img/laser/enemy/left.png"),
                    pyglet.image.load("img/laser/heavy/right.png"),
                    pyglet.image.load("img/laser/heavy/left.png")]
        self.lasers = pyglet.sprite.Sprite(self.img[0], x=self.x, y=self.y)
        self.detected = False
    def detect(self):
        if self.x <= 0:
            lasers.remove(self)
        if self.x >= 1440:
            lasers.remove(self)
    def move(self):
        if self.left == True:
            if self.firedBy == "enemy":
                self.lasers = pyglet.sprite.Sprite(self.img[1], x=self.x, y=self.y+10)
            elif self.firedBy == "character":
                if self.heavy == True:
                    self.lasers = pyglet.sprite.Sprite(self.img[5], x=self.x, y=self.y+10)
                else:
                    self.lasers = pyglet.sprite.Sprite(self.img[3], x=self.x, y=self.y+40)
            self.x = self.x - 10
            self.lasers.x = self.x
        if self.right == True:
            if self.firedBy == "enemy":
                self.lasers = pyglet.sprite.Sprite(self.img[0], x=self.x, y=self.y+10)
            elif self.firedBy == "character":
                if self.heavy == True:
                    self.lasers = pyglet.sprite.Sprite(self.img[4], x=self.x, y=self.y+10)
                else:
                    self.lasers = pyglet.sprite.Sprite(self.img[2], x=self.x, y=self.y+40)
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
        self.normalCoin = "normal"
        self.img = [pyglet.image.load("img/coin/normal.png"), pyglet.image.load("img/coin/health.png"), pyglet.image.load("img/coin/speed.png")]
        self.spr = pyglet.sprite.Sprite(self.img[0], x=self.x, y=self.y)
    def updatePos(self):
        self.spr.x = self.x
        self.spr.y = self.y
    def spawn(self, points):
        doWhat = random.randint(1, 5)
        self.x = random.randint(20, 1000)
        self.y = random.randint(300, 600)
        if doWhat > 2:
            self.normalCoin = "normal"
            coinAnimation = True
            #self.spr = pyglet.sprite.Sprite(self.img[0], x=self.x, y=self.y)
        elif doWhat == 1 and points > 20:
            self.normalCoin = "health"
            self.spr = pyglet.sprite.Sprite(self.img[1], x=self.x, y=self.y)
            coinAnimation = False
        elif doWhat == 2 and points > 20:
            self.normalCoin = "speed"
            self.spr = pyglet.sprite.Sprite(self.img[2], x=self.x, y=self.y)
            coinAnimation = False
        self.updatePos()
coins = Coin()
#coins.spawn(0)
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
        self.x = xx
        self.y = yy
        self.isChar = True
        self.health = 100
        self.amount = 7
        self.points = 0
        self.velocity = 0
        self.normalColor = True
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.lastDir = 0
        self.width = 80
        self.height = 80
        self.img = pyglet.image.load("img/spr/right.png")
        self.character = pyglet.sprite.Sprite(self.img, x=self.x, y=self.y)
    def move(self, genesis):
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
            if genesis == False:
                self.character = pyglet.sprite.Sprite(pyglet.image.load("img/nothing.png"), x=self.x, y=self.y)
                enemyHealth.spr = pyglet.sprite.Sprite(pyglet.image.load("img/nothing.png"), x=enemyHealth.x, y=enemyHealth.y)
            else:
                runAnimation = False
                if self.lastDir == 1:
                    if self.normalColor == False:
                        spr = pyglet.image.load("img/spr/yellow/right.png")
                        self.character = pyglet.sprite.Sprite(spr, x=self.x, y=self.y)
                    else:
                        spr = pyglet.image.load("img/spr/right.png")
                        self.character = pyglet.sprite.Sprite(spr, x=self.x, y=self.y)
                else:
                    if self.normalColor == False:
                        spr = pyglet.image.load("img/spr/yellow/left.png")
                        self.character = pyglet.sprite.Sprite(spr, x=self.x, y=self.y)
                    else:
                        spr = pyglet.image.load("img/spr/left.png")
                        self.character = pyglet.sprite.Sprite(spr, x=self.x, y=self.y)
        #jump
        if self.up == True:
            if(self.velocity == 0):
                self.velocity = 9
            self.y = self.velocity + self.y
            self.character.y = self.y
        #down
        if self.down == True:
            if self.y > 185 and self.velocity == 0:
                    self.y = self.y - 12
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
                if coins.normalCoin == "normal":
                    self.points+=1
                    self.amount = 7
                elif coins.normalCoin == "health":
                    if self.health < 90:
                        self.points-=10
                        self.amount = 7
                        self.health = 100
                elif coins.normalCoin == "speed":
                    self.amount = 12
                    self.points-=5
                coins.spawn(self.points)
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
        self.health = 20
        self.width = 80
        self.left = False
        self.isChar = False
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
        self.health = 20
        possibleY = [299,299,299,179,433,443,588]
        place = random.randint(0, 3)
        self.y = possibleY[place]
        possibleX = [random.randint(467,467+450),random.randint(0,0+299),random.randint(1175,1175+185),random.randint(0,1440),random.randint(910,910+255),random.randint(200,200+260),random.randint(447,447+470)]
        self.x = possibleX[place]
        if self.x >= char.x:
            self.direction = "left"
            #self.character = pyglet.sprite.Sprite(self.img[1], x=self.x, y=self.y)
        elif self.x <= char.x:
            self.direction = "right"
            #self.character = pyglet.sprite.Sprite(self.img[0], x=self.x, y=self.y)
        self.character.x = self.x
        self.character.y = self.y
    def wallDetector(self):
        if self.x <= 5:
            self.direction = "right"
            self.right = True
            self.left = False
            self.x = 2
            self.character.x = self.x
        elif self.x >= 1347:
            self.direction = "left"
            self.left = True
            self.right = False
            self.x = 1358
            self.character.x = self.x
    def detectLaser(self):
        if len(lasers) != 0: # detect laser
            for i in range(len(lasers)):
                if lasers[i].firedBy == "character":
                    if lasers[i].x >= self.x and lasers[i].x <= self.x + self.width:
                        if lasers[i].y >= self.y and lasers[i].y <= self.y + self.height:
                            if lasers[i].heavy == False:
                                self.health-=1
                            else:
                                print(lasers[i].heavy)
                                self.health=0
class HealthBar():
    def __init__(self, x, y, thingy):
        self.x = x
        self.y = y
        self.timeCheck = False
        self.type = thingy
        self.spr = pyglet.sprite.Sprite(pyglet.image.load("img/health/hearts/5.png"), x=self.x, y=self.y)
    def set(self):
        global t
        if self.type.isChar == True:
            if int(self.type.health/20) <= 0:
                dead()
                self.spr = pyglet.sprite.Sprite(pyglet.image.load("img/health/hearts/0.png"), x=self.x, y=self.y)
            else:
                health = int(self.type.health/20)
                self.spr = pyglet.sprite.Sprite(pyglet.image.load("img/health/hearts/"+str(health)+".png"), x=self.x, y=self.y)
            self.y = self.type.y + self.type.height + 10
            self.x = self.type.x - 23
        else:
            if int(self.type.health/4) <= 0:
                if self.timeCheck == False:
                    t = time()
                    self.timeCheck = True
                if time() >= t + .5:
                    char.points+=7 
                    self.type.health = 20
                    self.type.spawn()
                    self.timeCheck = False
            else:
                self.y = self.type.y + self.type.height + 15
                self.x = self.type.x - 32
                health = int(self.type.health/4)
                self.spr = pyglet.sprite.Sprite(pyglet.image.load("img/health/hearts/"+str(health)+".png"), x=self.x, y=self.y)
window = pyglet.window.Window(1440, 900)
window.set_caption("Megaman - Matt Nappo")

global char
char = Character(45, 175)

enemy = Enemy()
enemy.spawn()
enemyHealth = HealthBar(1000,700, enemy)
charHealth = HealthBar(1000,700, char)
keys = key.KeyStateHandler()
window.push_handlers(keys)

enemies = []

@window.event
def on_draw():
    global indexio
    global eIndex
    global platforms
    global coinIndex
    window.clear()
    background.background.draw()
    if int(enemy.health/4) <= 0:
        global enemyRunAnimation
        enemyRunAnimation = False
        enemy.right = False
        enemy.left = False
        enemy.character = pyglet.sprite.Sprite(pyglet.image.load("img/explosion.png"), x=enemy.x, y=enemy.y)
        enemy.character.draw()
    else:
        enemyRunAnimation = True
    if char.right == True or char.left == True:
        if char.lastDir == 1:
            if char.normalColor == False:
                char.character = yellowArrImages[indexio]
            else:
                char.character = arrImages[indexio]
        else:
            if char.normalColor == False:
                char.character = yellowLeftArrImages[indexio]
            else:
                char.character = leftArrImages[indexio]
    if enemy.right == True:
        enemy.character = enemyArrImages[eIndex]
    elif enemy.left == True:
        enemy.character = leftEnemyArrImages[eIndex]
    if coins.normalCoin == "normal":
        coins.spr = coinArrImages[coinIndex]
    else:
        coinAnimation = False
    if char.points < 0:
        char.points = 0
    if char.points >= 50:
        background.background = pyglet.sprite.Sprite(pyglet.image.load("img/backgrounds/lvl2.jpg"), x=0, y=0)
        char.points = 0
        p1 = Platform(467, 299, 450) # center
        p2 = Platform(50, 303, 265) # left
        p3 = Platform(1100, 299, 265) # right
        p4 = Platform(0, 179, 1440) # ground
        p5 = Platform(960, 437, 180) # middle right
        p6 = Platform(50, 437, 265) # upper left
        p7 = Platform(447, 588, 470) # upper center
        p8 = Platform(980, 670, 287) # upper right
        p9 = Platform(637, 440, 250) # middle center
        p10 = Platform(210, 670, 235) # upper left
        platforms = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]
    enemy.move(False)
    enemy.character.draw()
    char.move(True)
    char.character.draw()
    points = pyglet.text.Label("Points: " + str(char.points), font_name='Times New Roman', font_size=36, x=20, y=20)
    points.draw()
    coins.updatePos()
    coins.spr.draw()
    enemyHealth.spr.draw()
    charHealth.spr.draw()
    for x in range(len(lasers)):
        lasers[x].lasers.draw()

def charLaser(powerValue):
    laser = Laser(char.x, char.y, powerValue)
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
global timeCheckerr
timeCheckerr = False

global ti
ti = 0
def heavyHit():
    global caller
    global ti
    global timeCheckerr
    if caller == True:
        
        if timeCheckerr == False:
            ti = time()
            timeCheckerr = True
            #change to load
        else:
            if time() >= ti + .5:
                charLaser(True)
                timeCheckerr = False
                caller = False

@window.event
def on_key_press(symbol, modifiers):
    global runAnimation
    global yellowRunAnimation
    global caller
    if symbol == key.A:
        char.left = True
        runAnimation = True
    if symbol == key.D:
        char.right = True
        runAnimation = True
    if symbol == key.S:
        char.down = True
    if symbol == key.SPACE:
        char.up = True
    if symbol == key.K:
        char.normalColor = False
    if symbol == key.J:
        caller = True
    if symbol == key.H:
        charLaser(False)
def enemyFire(dt):
    laser = Laser(enemy.x, enemy.y, False)
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
    global platforms
    platforms = []
    background.img = pyglet.image.load("img/backgrounds/gameOver.jpg")
    background.background = pyglet.sprite.Sprite(background.img, x=0, y=0)
    coins.spr = pyglet.sprite.Sprite(pyglet.image.load("img/nothing.png"), x=0, y=0)
def goLeft():
    enemyRunAnimation = True
    enemy.direction = "left"
    enemy.right = False
    enemy.left = True
    enemy.character = pyglet.sprite.Sprite(enemy.img[1], x=enemy.x, y=enemy.y)
def goRight():
    enemyRunAnimation = True
    enemy.direction = "right"
    enemy.left = False
    enemy.right = True
    enemy.character = pyglet.sprite.Sprite(enemy.img[0], x=enemy.x, y=enemy.y)
def changeEnemyLocation():
    global platforms
    if char.left == False and char.right == False:
        if char.lastDir == 0:
            goRight()
        else:
            goLeft()
    else:
        if enemy.x > char.x:
            goLeft()
        elif enemy.x < char.x:
            goRight()
    '''for z in range(len(platforms)):
        if enemy.x + enemy.width >= platforms[z].x and enemy.x <= platforms[z].x + platforms[z].length:
            if platforms[z].y > enemy.y:
                enemy.up = True
            else:
                enemy.up = False'''
    
    '''global platforms
    if char.left == False and char.right == False: # if character not moving
        if char.lastDir == 0: # if character facing left
            if enemy.x < char.x: # if enemy to the left of character
                goRight()
            else: # if enemy is to the right of the static character
                goLeft()
        else: # if character is static and facing right
            if enemy.x > char.x: # if enemy is to the right of character
                goLeft()
            else: # if enemy is to the left of character
                goRight()'''
    '''else:
        if enemy.x > char.x:
            goLeft()
        elif enemy.x < char.x:
            goRight()
                
    for z in range(len(platforms)):
        if enemy.x + enemy.width >= platforms[z].x and enemy.x <= platforms[z].x + platforms[z].length:
            if platforms[z].y > enemy.y:
                enemy.up = True
            else:
                enemy.up = False'''
@window.event
def on_key_release(symbol, modifiers):
    global runAnimation
    if symbol == key.A:
        char.left = False
    if symbol == key.D:
        char.right = False
    if symbol == key.SPACE:
        char.up = False
    if symbol == key.S:
        char.down = False
def deClogger(dt):
    moveLaser()
    char.spiderSense()
    char.coinDetect()
    enemy.detectLaser()
    enemyKill()
    heavyHit()
    enemy.wallDetector()
    changeEnemyLocation()
    enemyHealth.set()
    charHealth.set()

pyglet.clock.schedule_interval(deClogger, 1/60.0)
pyglet.clock.schedule_interval(enemyFire, 1/0.8)
pyglet.clock.schedule_interval(updateIndex, 1/8)
pyglet.clock.schedule_interval(updateEIndex, 1/6)
pyglet.clock.schedule_interval(updateCoinIndex, 1/7)
pyglet.app.run()
