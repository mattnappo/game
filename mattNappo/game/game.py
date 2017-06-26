import pyglet, webbrowser
from pyglet.window import key
import random 
from os import system

class Background():
    def __init__(self):
        self.img = pyglet.image.load("img/background.jpg")
        self.background = pyglet.sprite.Sprite(self.img, x=0, y=0)

class Character():
    def __init__(self, xx, yy):
        self.x = xx
        self.y = yy
        self.velocity = 5
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.lastDir = None
        self.width = 50
        self.img = [pyglet.image.load("img/spr/right.png"), pyglet.image.load("img/spr/left.png")]
        self.character = pyglet.sprite.Sprite(self.img[0], x=self.x, y=self.y)
    def move(self, dt):
        if self.left == False and self.right == False:
            if self.lastDir == 0:
                spr = pyglet.image.load("img/spr/left.png")
                self.character = pyglet.sprite.Sprite(spr, x=self.x, y=self.y)
            elif self.lastDir == 1:
                spr = pyglet.image.load("img/spr/right.png")
                self.character = pyglet.sprite.Sprite(spr, x=self.x, y=self.y)
        if self.up == True:
            self.y = self.y + self.velocity
            self.character.y = self.y
        if self.down == True:
            self.y = self.y - self.velocity
            self.character.y = self.y
        if self.left == True:
            runImg = pyglet.image.load("img/spr/runLeft.png")
            self.character = pyglet.sprite.Sprite(runImg, x=self.x, y=self.y)
            self.x = self.x - self.velocity
            self.character.x = self.x
        if self.right == True:
            runImg = pyglet.image.load("img/spr/runRight.png")
            self.character = pyglet.sprite.Sprite(runImg, x=self.x, y=self.y)
            self.x = self.x + self.velocity
            self.character.x = self.x
            lastDir = 1
window = pyglet.window.Window(1440, 900)
window.set_caption("Remake of Mario")

background = Background()
char = Character(50, 50)
keys = key.KeyStateHandler()
window.push_handlers(keys)

@window.event
def on_draw():
    window.clear()
    background.background.draw()
    char.character.draw()
@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.W:
        char.up = True
    if symbol == key.S:
        char.down = True
    if symbol == key.A:
        char.left = True
    if symbol == key.D:
        char.right = True
@window.event
def on_key_release(symbol, modifiers):
    if symbol == key.W:
        char.up = False
    if symbol == key.S:
        char.down = False
    if symbol == key.A:
        char.left = False
    if symbol == key.D:
        char.right = False
pyglet.clock.schedule_interval(char.move, 1/60.0)
pyglet.app.run()