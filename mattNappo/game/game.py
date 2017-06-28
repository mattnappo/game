import pyglet, webbrowser
from pyglet.window import key
import random, time
from os import system
from pyglet.libs.win32.libwintab import CTX_SYSORGX

class Background():
    def __init__(self):
        self.img = pyglet.image.load("img/background.jpg") 
        self.background = pyglet.sprite.Sprite(self.img, x=0, y=0)

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
        
p1 = Platform(471, 296, 473)
platforms = [p1]
    
class Character():
    def __init__(self, xx, yy):
        self.x = xx
        self.y = yy
        self.health = 100
        self.amount = 7.5
        self.points = 19
        self.velocity = 0
        self.normalColor = True
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.lastDir = None
        self.width = 80
        self.height = 80
        self.img = [pyglet.image.load("img/spr/right.png"), pyglet.image.load("img/spr/left.png")]
        self.character = pyglet.sprite.Sprite(self.img[0], x=self.x, y=self.y)
    def move(self, dt):
        #DETECTION
        for i in range(len(platforms)):
            if self.x > platforms[i].x and self.x < platforms[i].x + platforms[i].length:
                self.y = platforms[i].y
        
        self.velocity = self.velocity - .4
        if self.y + self.height <= 255: # ground
            self.velocity = 0
            self.y = 255 - self.height
            self.character.y = self.y
        if self.y >= 287 and self.y < 298: # platform one (these numbers are the height)
            if self.x >= 478 and self.x <= 901: # these numbers are the length
                self.velocity = 0
                self.y = 296
                self.character.y = self.y
        if self.y >= 287 and self.y < 298: # right platform
            if self.x >= 1200 and self.x <= 1400:
                self.velocity = 0
                self.y = 296
                self.character.y = self.y
        if self.y >= 287 and self.y < 298: # left platform
            if self.x >= 0 and self.x <= 150:
                self.velocity = 0
                self.y = 296
                self.character.y = self.y
                
        #gravity
        self.y = self.velocity + self.y
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
        if self.x + self.width >= coins.x and self.x <= coins.x + coins.width:
            if self.y + self.height >= coins.y and self.y <= coins.y + coins.height:
                print(coins.normalCoin)
                if coins.normalCoin == True:
                    self.normalColor = True
                    self.points+=1
                    coins.spawn(self.points)
                else:
                    self.normalColor = False
                    self.points-=20
                    
    def spiderSense(self, dt): #left and right detection
        if self.x <= 0:
            self.health-=1
            self.x = 2
            self.character.x = self.x
        elif self.x >= 1355:
            self.health-=1
            self.x = 1357
            self.character.x = self.x
window = pyglet.window.Window(1440, 900)
window.set_caption("Remake of Mario")

background = Background()
char = Character(45, 175)
keys = key.KeyStateHandler()
window.push_handlers(keys)

@window.event
def on_draw():
    window.clear()
    background.background.draw()
    char.character.draw()
    health = pyglet.text.Label("Health: " + str(char.health), font_name='Times New Roman', font_size=36, x=20, y=20)
    health.draw()
    points = pyglet.text.Label("Points: " + str(char.points), font_name='Times New Roman', font_size=36, x=300, y=20)
    points.draw()
    coins.spr.draw()
@window.event
def on_key_press(symbol, modifiers):
    '''if symbol == key.W:
        char.up = True
    if symbol == key.S:
        char.down = True'''
    if symbol == key.A:
        char.left = True
    if symbol == key.D:
        char.right = True
    if symbol == key.SPACE:
        char.up = True

@window.event
def on_key_release(symbol, modifiers):
    '''if symbol == key.W:
        char.up = False
    if symbol == key.S:
        char.down = False'''
    if symbol == key.A:
        char.left = False
    if symbol == key.D:
        char.right = False
    if symbol == key.SPACE:
        char.up = False
pyglet.clock.schedule_interval(char.move, 1/60.0)
pyglet.clock.schedule_interval(char.spiderSense, 1/60.0)
pyglet.clock.schedule_interval(char.coinDetect, 1/60.0)
pyglet.app.run()