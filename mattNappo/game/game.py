import pyglet, webbrowser
from pyglet.window import key
import random, time
from os import system
from pyglet.libs.win32.libwintab import CTX_SYSORGX

lasers = []
class Background():
    def __init__(self):
        self.img = pyglet.image.load("img/background.jpg") 
        self.background = pyglet.sprite.Sprite(self.img, x=0, y=0)
class Laser():
    def __init__(self, x, y):
        self.width = 50
        self.x = x
        self.y = y
        self.left = False
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



def moveLaser(dt):
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
platforms = [p1, p2, p3, p4, p5, p6, p7]

background = Background()
class Character():
    def __init__(self, xx, yy):
        self.x = xx
        self.y = yy
        self.health = 100
        self.amount = 7.5
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
        self.img = [pyglet.image.load("img/spr/right.png"), pyglet.image.load("img/spr/left.png"), pyglet.image.load("img/nothing.png")]
        self.character = pyglet.sprite.Sprite(self.img[0], x=self.x, y=self.y)
    def move(self, dt):
        if self.health <= 0:
            background.img = pyglet.image.load("img/gameOver.jpg")
            background.background = pyglet.sprite.Sprite(background.img, x=0, y=0)
            coins = None
            self.character = None
        #gravity
        self.velocity = self.velocity - .4
        if self.velocity < -8:
            self.velocity = -8
        self.y = self.velocity + self.y
        self.character.y = self.y
        #print("y: ", str(self.y), "vel: ", str(self.velocity))
        #DETECTION
        for i in range(len(platforms)):
            if self.x >= platforms[i].x and self.x <= platforms[i].x + platforms[i].length:
                if self.y <= platforms[i].y + 4 and self.y >= platforms[i].y - 11:
                    self.velocity = 0
                    self.y = platforms[i].y
                    self.character.y = self.y
        
        #no movement
        if self.left == False and self.right == False:
            if self.lastDir == 0:
                if self.normalColor == True:
                    spr = pyglet.image.load("img/spr/left.png")
                    self.character = pyglet.sprite.Sprite(spr, x=self.x, y=self.y)
                else:
                    spr = pyglet.image.load("img/spr/green/left.png")
                    self.character = pyglet.sprite.Sprite(spr, x=self.x, y=self.y)
            elif self.lastDir == 1:
                if self.normalColor == True:
                    spr = pyglet.image.load("img/spr/right.png")
                    self.character = pyglet.sprite.Sprite(spr, x=self.x, y=self.y)
                else:
                    spr = pyglet.image.load("img/spr/green/right.png")
                    self.character = pyglet.sprite.Sprite(spr, x=self.x, y=self.y)
                
        #jump
        if self.up == True:
            if(self.velocity == 0):
                self.velocity = 9
            self.y = self.velocity + self.y
            self.character.y = self.y
        
        #left and right movement
        if self.left == True:
            if self.normalColor == True:
                spr = pyglet.image.load("img/spr/runLeft.png")
                self.character = pyglet.sprite.Sprite(spr, x=self.x, y=self.y)
            else:
                spr = pyglet.image.load("img/spr/green/runLeft.png")
                self.character = pyglet.sprite.Sprite(spr, x=self.x, y=self.y)
            self.x = self.x - self.amount
            self.character.x = self.x
            self.lastDir = 0
        if self.right == True:
            if self.normalColor == True:
                spr = pyglet.image.load("img/spr/runRight.png")
                self.character = pyglet.sprite.Sprite(spr, x=self.x, y=self.y)
            else:
                spr = pyglet.image.load("img/spr/green/runRight.png")
                self.character = pyglet.sprite.Sprite(spr, x=self.x, y=self.y)
            self.x = self.x + self.amount
            self.character.x = self.x
            self.lastDir = 1
    def coinDetect(self, dt):
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
                    
    def spiderSense(self, dt): #left and right detection
        if self.x <= 0:
            self.health-=1
            self.x = 2
            self.character.x = self.x
        elif self.x >= 1356:
            self.health-=1
            self.x = 1358
            self.character.x = self.x

class Enemy():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.health = 50
        self.width = 80
        self.height = 80
        self.lookingLeft = True
        self.img = [pyglet.image.load("img/spr/enemy/right.png"), pyglet.image.load("img/spr/enemy/left.png")]
        self.character = pyglet.sprite.Sprite(self.img[0], x=self.x, y=self.y)
    def spawn(self):
        possibleY = [299,299,299,179,433,443,588]
        place = random.randint(0, 3)
        self.y = possibleY[place]
        possibleX = [random.randint(467,467+450),random.randint(0,0+299),random.randint(1175,1175+185),random.randint(0,1440),random.randint(910,910+255),random.randint(200,200+260),random.randint(447,447+470)]
        self.x = possibleX[place]
        if self.x >= 720:
            self.lookingLeft = True
            self.character = pyglet.sprite.Sprite(self.img[1], x=self.x, y=self.y)
        else:
            self.lookingRight = False
        self.character.x = self.x
        self.character.y = self.y
    def detectLaser(self, dt):
        if char.x + char.width >= self.x and char.x <= self.x + self.width:# Detect character
            if char.y + char.height >= self.y and char.y <= self.y + self.height:
                char.health-=2

        if len(lasers) != 0: # detect laser
            for i in range(len(lasers)):
                if lasers[i].x >= self.x and lasers[i].x <= self.x + self.width:
                    if lasers[i].y >= self.y and lasers[i].y <= self.y + self.height:
                        if self.health <= 0:
                            self.health = 50
                            self.spawn()
                        else: 
                            self.health-=1
                            print(self.health)
                            
enemy = Enemy()
enemy.spawn()

window = pyglet.window.Window(1440, 900)
window.set_caption("Remake of Mario")

char = Character(45, 175)

keys = key.KeyStateHandler()
window.push_handlers(keys)

enemies = []

@window.event
def on_draw():
    window.clear()
    background.background.draw()
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
    if symbol == key.A:
        char.left = True
    if symbol == key.D:
        char.right = True
    if symbol == key.SPACE:
        char.up = True
def enemyFire(dt):
    laser = Laser(enemy.x, enemy.y)
    if enemy.lookingLeft == True:
        laser.left = True
        laser.x -= laser.width
    elif enemy.lookingLeft == False:
        laser.right = True
        laser.x += enemy.width
    if laser.left or laser.right:
        lasers.append(laser)
@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        laser = Laser(char.x, char.y)
        if not(char.left or char.right):
            if char.lastDir == False:
                laser.left = True
                laser.x -= laser.width
            else:
                laser.right = True
                laser.x += char.width
        elif char.left == True:
            laser.left = True
            laser.x -= laser.width
        elif char.right == True:
            laser.right = True
            laser.x += char.width
        if laser.left or laser.right:
            lasers.append(laser)

@window.event
def on_key_release(symbol, modifiers):
    if symbol == key.A:
        char.left = False
    if symbol == key.D:
        char.right = False
    if symbol == key.SPACE:
        char.up = False
pyglet.clock.schedule_interval(moveLaser, 1/60.0)
pyglet.clock.schedule_interval(char.move, 1/60.0)
pyglet.clock.schedule_interval(char.spiderSense, 1/60.0)
pyglet.clock.schedule_interval(char.coinDetect, 1/60.0)
pyglet.clock.schedule_interval(enemy.detectLaser, 1/60.0)
#pyglet.clock.schedule_interval(enemyFire, 1/60.0)
pyglet.app.run()