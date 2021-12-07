import numpy as np
from os import listdir
from os.path import isfile, join
import datetime

class InfoManager:
    def __init__(self,path):
        self.Path = path
        self.Total = []
    def GetSummary(self,date = "null"):
        files = [f for f in listdir(self.Path) if isfile(join(self.Path, f))]
        FileList = listdir(self.Path)
        if(date == "null"):
            today = self.getSheet(str(datetime.date.month)+str(datetime.date.day)+"-wildstang_attendance")
            date = str(datetime.date.month)+'/'+str(datetime.date.day)
        else:
            if(str(date)+"-wildstang_attendance" in FileList):
                today = self.getSheet(FileList[(str(date)+"-wildstangattendance")])
                date = date[0:2]+'/'+date[2:]
            else:
                today = self.getSheet(str(datetime.date.month)+str(datetime.date.day)+"-wildstang_attendance")
                date = str(datetime.date.month)+'/'+str(datetime.date.day)
        full = "<table>"
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
                absent.append(today[c])
            elif(today[c][3]=today[c][4]):
                present.append(today[c])
            else:
                checkedout.append(today[c])
            c += 1
            full.append("</tr>")
        full.append("</table>")
        atable = self.GenerateTable(absent)
        ptable = self.GenerateTable(present)
        ctable = self.GenerateTable(checkedout)
        return Table,date
    def AdminDay(self,date = "null"): #return table with editing boxes
        files = [f for f in listdir(self.Path) if isfile(join(self.Path, f))]
        FileList = listdir(self.Path)
        if(date == "null"):
            today = self.getSheet(str(datetime.date.month)+str(datetime.date.day)+"-wildstang_attendance")
            date = str(datetime.date.month)+'/'+str(datetime.date.day)
        else:
            if(str(date)+"-wildstang_attendance" in FileList):
                today = self.getSheet(FileList[(str(date)+"-wildstangattendance")])
                date = date[0:2]+'/'+date[2:]
            else:
                today = self.getSheet(str(datetime.date.month)+str(datetime.date.day)+"-wildstang_attendance")
                date = str(datetime.date.month)+'/'+str(datetime.date.day)
        full = "<table>"
        aTable = full
        pTable = full
        cTable = full
        Table = self.GenerateEditableTable(today)
        return Table
    def GetIds(self):
        today = self.getSheet(str(datetime.date.month)+str(datetime.date.day)+"-wildstang_attendance")
        return np.array(today[:,0]).tolist()
    def GetTotalMatrix(self):
        files = [f for f in listdir(self.Path) if isfile(join(self.Path, f))]
        days = []
        c = 0
        while(c<len(files)):
            days.append(self.getSheet(files[c])) #open all the files and matrix!
            c += 1
        self.Total = np.array(days)
        return days
    def GetUserData(self,num):
        if(len(self.Total)<1):
            null = self.GetTotalMatrix()
        UserData = []
        Total = datetime.timedelta()
        c = 0
        while(c<len(self.Total)):
            if(num in self.Total[:,0]):
                z = self.Total[:,0].tolist().index(num)
                UserData.append(self.Total[z])
                ExitTime = datetime.timedelta(hours = self.Total[z][4][0:2],minutes = self.Total[z][4][3:5])
                EnterTime = datetime.timedelta(hours = self.Total[z][3][0:2],minutes = self.Total[z][3][3:5])
                Total += ExitTime-EnterTime
            c += 1
        return UserData,Total,UserData[0][1],UserData[0][2]
    def UserSummary(self,num):
        UserData,Total,Fname,Lname = self.GetUserData(num)
        full = """<table>
          <tr>
        <th>Fisrt Name</th>
        <th>Last Name</th>
        <th>Check In</th>
        <th>Check Out</th>
          </tr>"""
        c = 0  
        while(c<len(UserData)): #generate summary tables
            full.append("<tr>")
            c2 = 1 #b/c 0 is the number 
            while(c2<len(UserData[c])):
                full.append("<td>"+UserData[c][c2]+"</td>")
                c2 += 1
            c += 1
            full.append("</tr>")
        full.append("</table>")
        return full
                    
    def AdminOverride(self,override,date,number,Out = True):
        FileList = listdir(self.Path)
        if(str(date)+"-wildstang_attendance" in FileList):
            files = [f for f in listdir(self.Path) if isfile(join(self.Path, f))]
            today = self.getSheet(files[FileList.index(str(date)+"-wildstangattendance")])
        else:
            return False
        today = np.array(today)
        Index = today[:,0].tolist().index(number)
        today = today.tolist()
        today[Index][3+Out] = override
        self.setSheet(today,str(date)+"-wildstang_attendance")
        return True
   
    def getSheet(self,file):
        sheetFile = open(file,"r")
        rows = sheetFile.read().splitlines()
        sheetFile.close()
        sheet = []
        c = 0
        while(c<len(rows)):
            #if (str(c) in rows)
                #sheet.append(rows[c].split(','))
            sheet.append(rows[c].split(','))
        
            c += 1

        return sheet

    def setSheet(self,sheet,file):
        #global editIndexes
        #tempList = []
        #self.organizeIndexes()
        rows = [] 
        for j in sheet:
                rows[j] = self.sheet[j]

        sheetFile = open(file,"w")
        sheetFile.truncate(0) #may not be needed
        for j in rows:
            sheetFile.write(str(sheet[j])[1:(len(rows[j])-1)]) 
            #if (j != editIndexes[0,0]):
                #tempList = rows[j].split(',')
                #if ()
            #sheetFile.write(rows[j])
            
        #editIndexes = []
        sheetFile.close()
    def GenerateEditableTable(self,matrix):
        c = 0
        out = "<table>"
        while(c<len(matrix)): #generate summary tables
            out.append("<tr>")
            c2 = 1 #b/c 0 is the number 
            while(c2<len(matrix[c])):
                out.append("<td>"+matrix[c][c2]+"</td>")
                c2 += 1
            c += 1
            out.append("""<td> <input type="text" placeholder="Check In" name="CheckIn" value="{{
          request.form.CheckIn }}"></td>""")
            out.append("""<td> <input type="text" placeholder="Check Out" name="CheckOut" value="{{
          request.form.CheckOut }}"></td>""")
            out.append("""<td> <input type="radio" name="CheckOut" value="{{
          request.form.Edit"""+matrix[c][0]+"""}}"></td>""")
            out.append("""<td> <input type="radio" name="CheckOut" value="{{
          request.form.Edit"""+matrix[c][0]+"""}}"></td>""")
            out.append("""<input type="submit" value="Submit">""")
            out.append("</tr>")
            
        out.append("</table>")
        return out
    def GenerateTable(self,matrix):
        c = 0
        out = "<table>"
        while(c<len(matrix)): #generate summary tables
            out.append("<tr>")
            c2 = 1 #b/c 0 is the number 
            while(c2<len(matrix[c])):
                out.append("<td>"+matrix[c][c2]+"</td>")
                c2 += 1
            c += 1
            out.append("</tr>")
            
        out.append("</table>")
        return out
