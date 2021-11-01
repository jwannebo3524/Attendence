import secrets
import time
from flask import Flask, render_template, redirect, url_for, request, make_response

class LoginInfo:
    def GetStatus(path):
        MaxTime = 3600 #certificates are valid for an hour
    #Note session can go on longer- new certificate is given each interaction with server
    
        fileObj = open(path+"Types.txt","r")  #account types
        Types = fileObj.read().splitlines()
        fileObj.close()
    
        ValidFile = open(path+"Valid.txt", "r+") #valid certificates
        Valid = ValidFile.read().splitlines()
    
        TimeFile = open(path+"Times.txt","r+")    #certificate times
        Times = TimeFile.read().splitlines()

        ctypesFile = open(path+"Ctypes.txt","r+")  #certicate types
        Ctypes = ctypesFile.read().splitlines()
    
        cidsFile = open(path+"Cids.txt","r+")  #UserID of corresponding certificate
        Cids = cidsFile.read().splitlines()

    #Determine permissions 
        Status = "None"
        UserID = 0
        Certificate = request.cookies.get('Certificate')
        if(Certificate in Valid):
            z = Valid.index(Certificate)
            CurrentTime = time.time()
            if(CurrentTime-float(Times[z])<MaxTime):
                Status = Ctypes[z]
                UserID = Cids[z]
            Valid.pop(z) #Discard used or exipred certificate
            Times.pop(z)
            Ctypes.pop(z)
            Cids.pop(z)
        ValidFile.truncate(0)
        TimeFile.truncate(0)
        ctypesFile.truncate(0)
        cidsFile.truncate(0)
        for line in Valid:
            ValidFile.write(line + "\n")
        for line in Times:
            TimeFile.write(line + "\n")
        for line in Ctypes:
            ctypesFile.write(line + "\n")
        for line in Cids:
            cidsFile.write(line + "\n")
        ValidFile.close()
        ctypesFile.close()
        TimeFile.close()
        cidsFile.close()
        return Status,int(UserID)

    def WriteCertificate(path,UserID):
    
        fileObj = open(path+"Types.txt","r")  #account types
        Types = fileObj.read().splitlines()
        fileObj.close()
    
        ValidFile = open(path+"Valid.txt", "r+") #valid certificates
        Valid = ValidFile.read().splitlines()
    
        TimeFile = open(path+"Times.txt","r+")    #certificate times
        Times = TimeFile.read().splitlines()

        ctypesFile = open(path+"Ctypes.txt","r+")  #certicate types
        Ctypes = ctypesFile.read().splitlines()

        cidsFile = open(path+"Cids.txt","r+")  #UserID of corresponding certificate
        Cids = cidsFile.read().splitlines()
        Certificate = secrets.token_hex(100)
        while(Certificate in Valid):
            Certificate = secrets.token_hex(100) #generate certificate
        Valid.append(Certificate)
        Times.append(time.time())
        Ctypes.append(Types[int(UserID)])
        Cids.append(UserID)

        ValidFile.truncate(0)
        TimeFile.truncate(0)
        ctypesFile.truncate(0)
        cidsFile.truncate(0)
        for line in Valid:
            ValidFile.write(line + "\n")
        for line in Times:
            TimeFile.write(str(line) + "\n")
        for line in Ctypes:
            ctypesFile.write(line + "\n")
        for line in Cids:
            cidsFile.write(str(line) + "\n")
        ValidFile.close()
        ctypesFile.close()
        TimeFile.close()
        cidsFile.close()
        return Certificate
