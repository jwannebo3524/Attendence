barcode = input()
if int(barcode) > 99999 and int(barcode) < 1000000:
    barcodefile = open("barcodes.txt", "a")
    barcodefile.write(barcode + "\n")
    barcodefile.close()
