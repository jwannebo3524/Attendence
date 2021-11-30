import Imageifier as im
import readingWriting as rw
import datetime
import time
import shutil

PREVIEW = False
today = datetime.date.today()

TodayPath = "D:/"+str(datetime.date.month)+str(datetime.date.day)+"-wildstang_attendance"
i = im.Imageifier('null',preveiw = PREVIEW)
import time
import shutil

TodayPath = "D:/"+str(datetime.date.month)+str(datetime.date.day)+"-wildstang_attendance"
i = im.Imigeifier('null')
e = im.Exit()
readwrite = rw.ReadWrite(TodayPath,60)
#readwrite.getSheet()
readwrite.daysFile()
while True:
    i.ImageLoop(readwrite,e)
    print("autosaving. blink LED or something")
    readwrite.setSheet(readwrite.sheet)
    print("autosave complete")

    if datetime.date.weekday(datetime.date.year, datetime.date.month, datetime.date.day) != 5:
        if datetime.time.hour == 21:
            True

    if datetime.date.weekday(datetime.date.year, datetime.date.month, datetime.date.day) == 5:
        if datetime.time.hour == 13:
            True


