class Node():
    def __init__(self, data):
        self.data = None
        self.link = None
class LinkedList():
    def __init__(self):
        self.head = None
        self.counter = 0
    def insert(self, place, data):
        if self.counter == 0:
            newNode = Node(data)
            self.head = newNode
            self.counter+=1
        elif place == 0:
            newNode = Node(data)
            newNode.link = self.head
            self.head = newNode
            self.counter+=1
        else:
            node = self.head
            for x in range(place-1):
                node = node.link
            newNode.link = node.link
            node.link = newNode
            self.counter+=1
    def printer(self):
        node = self.head
        for x in range(self.counter-1):
            print("["+str(x)+"] "+node.data)
            node = node.link
        print("["+str(self.counter-1)+"] "+node.data)
    def simplePrinter(self):
        node = self.head
        for x in range(self.counter-1):
            print(node.data)
            node = node.link
        print(node.data)
    def remove(self, place):
        if place == 0:
            self.head = self.head.link
            self.counter-=1
        else:
            node = self.head
            for x in range(place-2):
                node = node.link
            node.link = node.link.link
            self.counter-=1
    def peek(self):
        return self.head.data