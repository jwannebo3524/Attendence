import Imageifier as im
import readingWriting as rw

i = im.Imigeifier('null')
e = im.Exit()
readwrite = rw.ReadWrite(TodayPath,60)
readwrite.getSheet()
readwrite.daysFile()
while True:
    i.VideoLoop(readwrite,i)
    print("autosaving. blink LED or something")
    readwrite.setSheet(readwrite.sheet)
    print("autosave complete")
