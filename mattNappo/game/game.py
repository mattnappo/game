import pyglet, webbrowser
from pyglet.window import key
import random, time
from os import system

class Background():
    def __init__(self):
        self.img = pyglet.image.load("img/newBackground.jpg") 
        self.background = pyglet.sprite.Sprite(self.img, x=0, y=0)
        '''
        
        Vf = Vi + at
        
        '''
        
class Character():
    def __init__(self, xx, yy):
        self.x = xx
        self.y = yy
        self.health = 100
        self.amount = 7.5
        self.velocity = 0
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
        self.velocity = self.velocity - .3
        if self.y + self.height <= 255: #ground
            self.velocity = 0
            self.y = 255 - self.height
            self.character.y = self.y
        if self.y >= 416 and self.y < 424: #platform one
            if self.x >= 689 and self.x <= 901:
                self.velocity = 0
                self.y = 420
                self.character.y = self.y
        self.y = self.velocity + self.y
        self.character.y = self.y
        if self.left == False and self.right == False:
            if self.lastDir == 0:
                spr = pyglet.image.load("img/spr/left.png")
                self.character = pyglet.sprite.Sprite(spr, x=self.x, y=self.y)
            elif self.lastDir == 1:
                spr = pyglet.image.load("img/spr/right.png")
                self.character = pyglet.sprite.Sprite(spr, x=self.x, y=self.y)
        if self.up == True:
            self.velocity = 3.5
            self.y = self.velocity + self.y
            self.character.y = self.y
        if self.down == True:
            self.y = self.y - self.amount
            self.character.y = self.y
        if self.left == True:
            runImg = pyglet.image.load("img/spr/runLeft.png")
            self.character = pyglet.sprite.Sprite(runImg, x=self.x, y=self.y)
            self.x = self.x - self.amount
            self.character.x = self.x
            self.lastDir = 0
        if self.right == True:
            runImg = pyglet.image.load("img/spr/runRight.png")
            self.character = pyglet.sprite.Sprite(runImg, x=self.x, y=self.y)
            self.x = self.x + self.amount
            self.character.x = self.x
            self.lastDir = 1
        
    def spiderSense(self, dt): #left and right detection
        if self.x <= 0:
            self.health-=1
            self.x = 2
            self.character.x = self.x
        elif self.x >= 1355:
            self.health-=1
            self.x = 1357
            self.character.x = self.x
        '''
        if self.x >= 680 and self.x <= 900:
            if self.y >= 320:
                self.y = 320 + self.height
                self.character.y = self.y
        '''
window = pyglet.window.Window(1440, 900)
window.set_caption("Remake of Mario")


background = Background()
char = Character(45, 175)
keys = key.KeyStateHandler()
window.push_handlers(keys)
health = pyglet.text.Label(str(char.health), font_name='Times New Roman', font_size=36, x=20, y=20)

@window.event
def on_draw():
    window.clear()
    background.background.draw()
    char.character.draw()
    health = pyglet.text.Label("Health: " + str(char.health), font_name='Times New Roman', font_size=36, x=20, y=20)
    health.draw()
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
pyglet.app.run()