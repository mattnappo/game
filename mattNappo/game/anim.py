import pyglet
window = pyglet.window.Window(1000,1000)
counter=.0

def load_anim():
    arrImages=[]
    for i in range(2):
        tmpImg=pyglet.resource.image("img/spr/anim/step"+str(i)+".png")
        arrImages.append(tmpImg)
    return arrImages

def update_frames(dt):
    global counter
    counter=(counter+dt)%2

@window.event
def on_draw():
    print(counter)
    pyglet.gl.glClearColor(0,0,0,0)
    window.clear()
    frames[int(counter)].blit(320,200,0,
                              frames[int(counter)].width,
                              frames[int(counter)].height)

frames = load_anim()
pyglet.clock.schedule_interval(update_frames,1/100.0)
pyglet.app.run()