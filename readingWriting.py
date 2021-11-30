from os import O_LARGEFILE
import os
#import cv2
from pyzbar.pyzbar import decode
import time
import numpy as np
import datetime

rows = []
editIndexes = [[],[]] # [[index of the sign in],[]]

class ReadWrite:
    def __init__(self,path,MinTime):
        nothingvar = self.CreateFileIfNeeded()
        print(nothingvar)
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
        filename = "D:/"+str(datetime.date().month)+str(datetime.date().day)+str((datetime.date().year)-2000)+"-WildStang_Attendance.csv"
        daysFile = open(filename,"r")
        if (daysFile != ""):
            return "SHIT IDK \_('_')_/"
        daysFile.close()
        daysFile = open(filename, "a")
        baseFile = open("Base_Attendance.txt","r")
        daysFile.write(baseFile.read())
        daysFile.close()
        baseFile.close()
    def CreateFileIfNeeded(self):
        today = datetime.date.today() 
        filename = "" + str(today.month) + str(today.day) + str(int(today.year) - 2000) + "-WildStang_Attendance.csv"
        if os.path.isfile(filename):
            return "File Already Exists"
        else:
            daysFile = open(filename,"w")
            daysFile.close()
            return "File created"

    def readBar(self,image):    #gets image bar code
        global editIndexes
        path = self.path           
        MinTime = self.minTime      
        print("scanning...")
        print(np.shape(image))
        if(len(np.shape(image))>0):
            dectectedBarcodes = decode(image)  #all barcodes in image
        else:
            detectedBarcodes = []
        print("tick")
        if(len(np.shape(image))>0):
            for barcode in dectectedBarcodes:
      #  (x, y, w, h) = barcode.rect                       -uncomment if displaying image
      #  cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 5)  
                logIn = time.time()   #logs the time detected
                now = datetime.datetime.now()
                HumanReadable = now.strftime("%H:%M:%S")
                print("barcode detected...")
                print(logIn)
                print(barcode.type)
                print(int(barcode.data))
            
                if barcode.data in self.Barcodes:   #has bar code been checked in
                    self.Barcodes.reverse()         #most recent Log In
                    self.Times.reverse()
                    index = self.Barcodes.index(int(barcode.data))   
                    dif = time.time()-self.Times[index]
                    self.Barcodes.reverse()
                    self.Times.reverse()
                    if ((dif)>(MinTime)):           #has min log in time been reached
                        self.Times.append(logIn)
                        self.Barcodes.append(int(barcode.data))
                        index = self.sheet[:][0].index(int(barcode.data))
                       # editIndexes.append([index,logIn]) #logs the activity
                        print('Welcome,'+self.sheet[index][1])
                        self.sheet[index][4] = HumanReadable
                        if(self.sheet[index][3] == -1):
                        
                            self.sheet[index][3] = HumanReadable
                        
                else:
                    if(int(barcode.data) in self.sheet[:][0]):
                        self.Times.append(logIn)
                        self.Barcodes.append(int(barcode.data))
                        index = self.sheet[:][0].index(int(barcode.data))
                        print('Welcome,'+self.sheet[index][1])
                        self.sheet[index][4] = HumanReadable
                        editIndexes.append([index,logIn]) #logs the activity
                        if(self.sheet[index][3] == -1):
                            self.sheet[index][3] = HumanReadable
                    else:
                        print("Error: unrecognized barcode")
        #if barcode.data in code and -dif <
        #DONE write in if statment to compare difference of time and to check if barcode data is there before it writes data in
        
        #TODO - comma seperated format   guess not
           
        print("loop done")
    #cv2.imshow("Image", image)

    #cv2.waitkey(0)
    #cv2.destroyAllWindows()
    def close(self):
        self.setSheet(self.sheet)
    def getSheet(self):
        global rows
        sheetFile = open(self.path,"r")
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

        sheetFile = open(self.path,"w")
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
class Wrapper(object):
    def __init__(self,function):
        self.function = function
    def write(self,s):
        self.function(s)
