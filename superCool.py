import readingWriting
import Imageifier


read = readingWriting.ReadWrite("________", 60)
image = Imageifier.Imageifier("VeggieTables")

image.VideoLoop(read.readBar, "Yefshinegan")
read.close()