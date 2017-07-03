import pyglet
window = pyglet.window.Window(100,100)
global x
x = 0

arrImages=[]
for i in range(4):
    tmpImg = pyglet.image.load("img/spr/anim/step"+str(i)+".png")
    spr = pyglet.sprite.Sprite(tmpImg, x=0, y=0)
    arrImages.append(spr)

def updateIndex(dt):
    global x
    if x < 3:
        x+=1
    else:
        x = 0

@window.event
def on_draw():
    window.clear()
    global x
    img = arrImages[x]
    img.draw()

pyglet.clock.schedule_interval(updateIndex,1/6)
pyglet.app.run()