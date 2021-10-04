
import cv2
from pzbar.pzbar import decode
import time

class ReadWrite:
    def __init__(self,path):
        self.path = path  
        self.sheet = self.getSheet()
        self.Times = []
        self.Barcodes = []
                    #"Temporary/Path/FixThis"
    self.MinTime = 60
    def readBar(self,image):
        path = self.path
        MinTime = self.MinTime
    
        dectectedBarcodes = decode(image)
        for barcode in dectectedBarcodes:
      #  (x, y, w, h) = barcode.rect                       -uncomment if displaying image
      #  cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 5)  

            logIn = time.time()
            
            print(logIn)
            print(barcode.data)

            
            if barcode.data in self.Barcodes:
                self.Barcodes.reverse()
                self.Times.reverse()
                index = self.Barcodes.index(barcode.data)
                dif = time.time()-self.Times[index]
                self.Barcodes.reverse()
                self.Times.reverse()
                if ((dif)>(MinTime)):
                    self.Times.append(logIn)
                    self.Barcodes.append(barcode.data)
                    Index = self.sheet[:][0].index(barcode.data)
                    print('Welcome,'+self.sheet[Index][1])
                    self.sheet[Index][3] = logIn
                    if(self.sheet[Index][2] == -1):
                        self.sheet[Index][2] = logIn
                        
            else:
                self.Times.append(logIn)
                self.Barcodes.append(barcode.data)
                Index = self.sheet[:][0].index(barcode.data)
                print('Welcome,'+self.sheet[Index][1])
                self.sheet[Index][3] = logIn
                if(self.sheet[Index][2] == -1):
                    self.sheet[Index][2] = logIn
        #if barcode.data in code and -dif <
        #DONE write in if statment to compare difference of time and to check if barcode data is there before it writes data in
        
        #TODO - comma seperated format
           
            print(barcode.type)
            
    #cv2.imshow("Image", image)

    #cv2.waitkey(0)
    #cv2.destroyAllWindows()
    def close(self):
        self.setSheet(self.sheet)
    def getSheet(self):
        
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
       
        sheetFile = open(self.path+"Sheet","w")
        sheetFile.truncate(0)
        sheetFile.write(sheet)
        sheetFile.close()
    
