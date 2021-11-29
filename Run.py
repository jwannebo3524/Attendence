import Imageifier as im
import readingWriting as rw
import datetime

PREVIEW = False

today = datetime.date.today()
TodayPath = "" + str(today.month) + str(today.day) + str(int(today.year) - 2000) + "-WildStang_Attendance.csv"
i = im.Imageifier('null',preveiw = PREVIEW)
e = im.Exit()
readwrite = rw.ReadWrite(TodayPath,60)
#readwrite.getSheet()
readwrite.daysFile()
while True:
    i.ImageLoop(readwrite,e)
    print("autosaving. blink LED or something")
    readwrite.setSheet(readwrite.sheet)
    print("autosave complete")

