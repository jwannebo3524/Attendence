from tempfile import NamedTemporaryFile
import shutil
import csv
import datetime
import time

#filename = 'tmpEmployeeDatabase.csv'
tempfile = NamedTemporaryFile('w+t', newline='', delete=False)

class tempFile:
    def __init__ ():
        filename = "" + str(datetime.date().month) + str(datetime.date().day) + str((datetime.date().year) - 2000) + "-WildStang_Attendance.csv"

    def createTemp ():
        tempfile = NamedTemporaryFile('w+t', newline='', delete=False)


    def findID ():
        x=2


    with open(filename, 'r', newline='') as csvFile, tempfile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')
        writer = csv.writer(tempfile, delimiter=',', quotechar='"')


        for row in reader:
            row[1] = row[1].title()
            writer.writerow(row)

    shutil.move(tempfile.name, filename)
