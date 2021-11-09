from os import O_LARGEFILE
import cv2
from pzbar.pzbar import decode
import time
import numpy as np

rows = []
editIndexes = [[],[]] # [[index of the sign in],[]]

class ReadWrite:
    def __init__(self,path,MinTime):
       # MinTime = 60
       # path = str(datetime.date().month) + str(datetime.date().day) + str((datetime.date().year) - 2000) + "-WildStang_Attendance.csv"
        self.path = path  
        self.sheet = self.getSheet()
        self.Times = []
        self.Barcodes = []
        self.minTime = MinTime
                    #"Temporary/Path/FixThis"
   # self.minTime = 60
    def daysFile():
        filename = "" + str(datetime.date().month) + str(datetime.date().day) + str((datetime.date().year) - 2000) + "-WildStang_Attendance.csv"
        daysFile = open(filename,"r")
        if (daysFile != ""):
            return "SHIT IDK \_('_')_/"
        daysFile.close()
        daysFile = open(filename, "a")
        baseFile = open("Base_Attendance.txt","r")
        daysFile.write(baseFile.read())


    def readBar(self,image):    #gets image bar code
        global editIndexes
        path = self.path           
        MinTime = self.minTime      
    
        dectectedBarcodes = decode(image)  #all barcodes in image
        for barcode in dectectedBarcodes:
      #  (x, y, w, h) = barcode.rect                       -uncomment if displaying image
      #  cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 5)  

            logIn = time.time()   #logs the time detected 
            
            print(logIn)
            print(barcode.data)

            
            if barcode.data in self.Barcodes:   #has bar code been checked in
                self.Barcodes.reverse()         #most recent Log In
                self.Times.reverse()
                index = self.Barcodes.index(barcode.data)   
                dif = time.time()-self.Times[index]
                self.Barcodes.reverse()
                self.Times.reverse()
                if ((dif)>(MinTime)):           #has min log in time been reached
                    self.Times.append(logIn)
                    self.Barcodes.append(barcode.data)
                    index = self.sheet[:][0].index(barcode.data)
                    editIndexes.append([index,logIn]) #logs the activity
                    print('Welcome,'+self.sheet[index][1])
                    self.sheet[index][3] = logIn
                    if(self.sheet[index][2] == -1):
                        
                        self.sheet[index][2] = logIn
                        
            else:
                self.Times.append(logIn)
                self.Barcodes.append(barcode.data)
                index = self.sheet[:][0].index(barcode.data)
                print('Welcome,'+self.sheet[index][1])
                self.sheet[index][3] = logIn
                editIndexes.append([index,logIn]) #logs the activity
                if(self.sheet[index][2] == -1):
                    self.sheet[index][2] = logIn
        #if barcode.data in code and -dif <
        #DONE write in if statment to compare difference of time and to check if barcode data is there before it writes data in
        
        #TODO - comma seperated format   guess not
           
            print(barcode.type)
            
    #cv2.imshow("Image", image)

    #cv2.waitkey(0)
    #cv2.destroyAllWindows()
    def close(self):
        self.setSheet(self.sheet)
    def getSheet(self):
        global rows
        sheetFile = open(self.path+"Sheet","r")
        rows = sheetFile.read().splitlines()
        sheetFile.close()
        sheet = []
        c = 0
        while(c<len(rows)):
            sheet.append(rows[c].split(','))
        
            c += 1

        return sheet

    def setSheet(self,sheet):
        global rows
        rows = [] 
        for j in self.sheet:
                rows[j] = self.sheet[j]

        sheetFile = open(self.path+"Sheet","a")
        sheetFile.truncate(0)
        for j in rows:
            sheetFile.write(str(self.sheet[j])[1:(len(rows[j])-1)]+"\n") 
            
        sheetFile.close()
    
    def write(self,s): #wrapper
        self.readBar(s)
        
        
    #def organizeIndexes():
    #    global editIndexes
    #    tempMatrix = []
    #    tempIndex = int

    #    for i in editIndexes:
    #        inserted = False
    #        tempIndex = editIndexes[[i][0]]
    #        for j in tempMatrix:
    #            if (tempMatrix[[j][0]] < tempIndex & inserted == False):
    #                tempMatrix.insert(j, editIndexes[i])
    #                inserted = True
    #        if (inserted == False):
    #            tempMatrix.appened(editIndexes[i])
    #    editIndexes = [[],[]]
    #    editIndexes = tempMatrix
        





    
