import random
code = random.randint(0,999999)
school = None
year = None
classNum = None
temp = code
codeLength = 0 

if code > 999999:
    print("oh no!")
else:
    classNum = code % 1000
    year = int(code/1000) % 100
    school = int(code/100000) 
    
    print (str(school) + "." + str(year) + "." + str(classNum))