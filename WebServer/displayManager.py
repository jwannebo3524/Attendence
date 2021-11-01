import numpy as np
from os import listdir
from os.path import isfile, join
import readingWriting as rw
class InfoManager:
    def __init__(self,path):
        self.Path = path
        self.Total = []
    def GetSummary(self,fromEnd):
        files = [f for f in listdir(self.Path) if isfile(join(self.Path, f))]
        today = self.getSheet(files[-fromEnd])
        full = """<table>
          <tr>
        <th>Fisrt Name</th>
        <th>Last Name</th>
        <th>Check In</th>
        <th>Check Out</th>
          </tr>"""
        aTable = full
        pTable = full
        cTable = full
        c = 0
        absent = []
        present = []
        checkedout = []
        while(c<len(today)): #generate summary tables
            full.append("<tr>")
            c2 = 1 #b/c 0 is the number 
            while(c2<len(today[c])):
                full.append("<td>"+today[c][c2]+"</td>")
                c2 += 1
            if(len(today[c][3])<3):
                absent.append(c)
            elif(len(today[c][4])<3):
                present.append(c)
            else:
                checkedout.append(c)
            c += 1
            full.append("</tr>")
        full.append("</table>")
        c = 0
        while(c<len(absent)):
            aTable.append("<tr>")
            i = absent[c]
            c2 = 1
            while(c2<len(today[i])):
                aTable.append("<td>"+today[i][c2]+"</td>")
                c2 += 1
            aTable.append("</tr>")
            c += 1
        aTable.append("</table>")
        c = 0
        while(c<len(present)):
            pTable.append("<tr>")
            i = present[c]
            c2 = 1
            while(c2<len(today[i])):
                pTable.append("<td>"+today[i][c2]+"</td>")
                c2 += 1
            pTable.append("</tr>")
            c += 1
        pTable.append("</table>")
        while(c<len(checkedout)):
            cTable.append("<tr>")
            i = checkedout[c]
            c2 = 1
            while(c2<len(today[i])):
                cTable.append("<td>"+today[i][c2]+"</td>")
                c2 += 1
            cTable.append("</tr>")
            c += 1
        cTable.append("</table>")
        return full,aTable,pTable,cTable
    def GetTotalMatrix(self):
        files = [f for f in listdir(self.Path) if isfile(join(self.Path, f))]
        while(c<len(files)):
            days.append(self.getSheet(files[c])) #open all the files and matrix!
            c += 1
        self.Total = days
        return days
    def GetUserData(self,num):
        if(len(self.Total)<1):
            null = self.GetTotalMatrix()
        UserData = []
        Total = 0
        while(c<len(self.Total)):
            if(num in self.Total[:][0]):
                z = self.Total[:][0].index(num)
                UserData.append(self.Total[z])
                Total += self.Total[z][4]-self.Total[z][3]
            c += 1
        return UserData,Total,UserData[0][1],UserData[0][2]
    
    def getSheet(self.self):
        #FIXTHIS
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
        #FIXTHIS MORE
        sheetFile = open(self.path+"Sheet","w")
        sheetFile.truncate(0)
        sheetFile.write(sheet)
        sheetFile.close(
