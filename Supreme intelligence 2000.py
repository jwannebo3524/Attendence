import time
#originally named Dementia bot 2000
while True:
    name = input("what's your name?")+' '
    print(name+' is a very stupid name.')
    time.sleep(2)
    no = input("wait, what was your name again- jeffery?, right?")

    while("yes" in no):
        print("nice to meet you, jeffry.")
        time.sleep(2)
        no = input("wait, what was your name again- jeffery?, right?")
    print("so then...")
    time.sleep(0.35)
