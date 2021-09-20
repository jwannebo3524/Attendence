barcode = input()
barcodefile = open("barcodes.txt", "a")
barcodefile.write(barcode + "\n")
barcodefile.close()