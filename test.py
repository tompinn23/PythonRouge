name = input("Whats your name?")
print("Hello " + name)
print("Are you happy or are you sad?")#
correct = False
while correct is not True:
    happy = input()
    if happy == "happy":
        print("i am happy too")
        correct = True
    if happy == "sad":
        print("i am sad too")
        correct = True
    else:
        print("please enter  happy or sad!")

