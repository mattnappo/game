if self.type.isChar == True:
    if int(char.health/20) <= 0:
        print("this ran?")
        dead()
        self.spr = pyglet.sprite.Sprite(pyglet.image.load("img/health/hearts/0.png"), x=self.x, y=self.y)
else:
    if int(enemy.health/4) <= 0:
        global t
        if self.TIMECHECK == False:
            t = time()
            self.TIMECHECK = True
            enemy.character = pyglet.sprite.Sprite(pyglet.image.load("img/explosion.png"), x=enemy.x, y=enemy.y)
            #print("exploded")
            enemy.character.draw()
        else:
            if time() >= t + .5:
                char.points+=7
                enemy.health = 20
                enemy.spawn()
    else:
        self.spr = pyglet.sprite.Sprite(pyglet.image.load("img/health/hearts/"+str(health)+".png"), x=self.x, y=self.y)

if self.type.isChar == False:
    self.y = self.type.y + self.type.height + 15
    self.x = self.type.x - 32
else:
    self.y = self.type.y + self.type.height + 10
    self.x = self.type.x - 23
if self.type.isChar == True:
    health = int(self.type.health/20)
    if int(health/20) > 0:
        print("working here")
        self.spr = pyglet.sprite.Sprite(pyglet.image.load("img/health/hearts/"+str(health)+".png"), x=self.x, y=self.y)
else:
    health = int(self.type.health/4)
if health > 0:
    self.spr = pyglet.sprite.Sprite(pyglet.image.load("img/health/hearts/"+str(health)+".png"), x=self.x, y=self.y)
else:
    if self.type.isChar == True:
        dead()
        print('THIS ran?')
        self.spr = pyglet.sprite.Sprite(pyglet.image.load("img/health/hearts/0.png"), x=self.x, y=self.y)