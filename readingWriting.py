
import cv2
from pzbar.pzbar import decode
import time

def readBar(image):
    path = "Temporary/Path/FixThis"
    MinTime = 60
    
    dectectedBarcodes = decode(image)
    for barcode in dectectedBarcodes:
      #  (x, y, w, h) = barcode.rect                       -uncomment if displaying image
      #  cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 5)  

        logIn = time.time()
        file1 = open(path + "Times Logged", "r+")
        code2 = file1.read().splitlines()
        code2.reverse()


        
        print(logIn)
        
        file2 = open(path, "Barcodes", "r+")
        code = file2.read().splitlines()
        code.reverse()
        if barcode.data in code:
            index = code.index(barcode.data)
            dif = code2[index] - time.time()
            if ((dif)<(-1*MinTime)):
                file1.write(logIn)
                file2.write(barcode.data)
        else:
            file1.write(logIn)
            file2.write(barcode.data) 
        #if barcode.data in code and -dif <
        #DONE write in if statment to compare difference of time and to check if barcode data is there before it writes data in
        
        #TODO - comma seperated format
        print(barcode.data)
        print(barcode.type)
        file1.close()
        file2.close()
    #cv2.imshow("Image", image)

    #cv2.waitkey(0)
    #cv2.destroyAllWindows()
