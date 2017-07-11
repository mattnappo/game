class Thing():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def shoutMyPosition(self):
        print("HEY I'M AT",str(self.x),",",str(self.y))
class SpecificThing(Thing):
    def __init__(self,x,y,color):
        super().__init__(x, y)
        self.color = color
    def printInfo(self):
        self.shoutMyPosition()
        print("AND I'M",self.color)
        print(self.x)
        print(self.y)
yo = SpecificThing(10,10,"Green")
yo.printInfo()