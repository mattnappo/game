from linkedList import LinkedList
pwlist = LinkedList()
pwlist.insert(pwlist.counter, "one")
pwlist.insert(pwlist.counter, "two")
pwlist.insert(pwlist.counter, "three")
pwlist.insert(pwlist.counter, "four")
while True:
    x = input("[V]iew, [S]tring append, [A]ppend, [I]nsert, [R]emove, [P]eek? ")
    if x == "V" or x == "v":
        pwlist.printer()
    elif x == "S" or x == "s":
        pwlist.insert(pwlist.counter, input("Enter data: "))
    elif x == "A" or x == "a":
        dataType = input("Append [B]oolean, [S]tring, [I]nteger, or [L]ist? ")
        if dataType == "B" or dataType == "b":
            pwlist.insert(pwlist.counter+1, bool(input("Enter 'True' or enter 'False': ")))
        elif dataType == "S" or dataType == "s":
            pwlist.insert(pwlist.counter+1, input("Enter a string: "))
        elif dataType == "I" or dataType == "i":
            pwlist.insert(pwlist.counter+1, eval(input("Enter an integer: ")))
        elif dataType == "L" or dataType == "l":
            print("Format: 'item1,item2,item3,item4'")
            preList = input("Enter list: ")
            newList = preList.split(",")
            print(newList)
            pwlist.insert(pwlist.self.counter+1, newList)
    elif x == "I" or x == "i":
        pwlist.insert(eval(input("Enter place number: ")), input("Enter data: "))
    elif x == "R" or x == "r":
        pwlist.remove(eval(input("Enter place number: ")))
    elif x == "P" or x == "p":
        print(pwlist.peek())