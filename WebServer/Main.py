import secrets
import time
from flask import Flask, render_template, redirect, url_for, request, make_response

path = "C:/Users/132/Desktop/WebServer/" #Change this if not me

app = Flask(__name__,template_folder= path+"templates")

#(cmd prompt reminder)---

#set FLASK_APP = 'C:/Users/132/Desktop/WebServer/Main'
#flask run

#---


@app.route("/", methods=['GET', 'POST'])
def Login():
    global path
    if request.method == 'POST':

        message = ''
        fileObj = open(path+"Usernames.txt", "r")
        Usernames = fileObj.read().splitlines()
        fileObj.close()
    
        fileObj = open(path+"Passwords.txt", "r") 
        Passwords = fileObj.read().splitlines()
        fileObj.close()
    
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
        

        if request.form['Username'] in Usernames:
            UserID = Usernames.index(request.form['Username'])
            if request.form['Password'] == Passwords[UserID]:   
                message = 'Login successful. Something should happen now'
                out = render_template('login.html',message = message)
                response = make_response(redirect(url_for('Home')))
                Certificate = secrets.token_hex(100)
                while(Certificate in Valid):
                    Certificate = secrets.token_hex(100) #generate certificate
                Valid.append(Certificate)
                Times.append(time.time())
                Ctypes.append(Types[int(UserID)])
                Cids.append(UserID)
                response.set_cookie('Certificate',Certificate)
                out = response
                
            else:
                message = 'Invalid Password'
                out = render_template('login.html',message = message)
        else:
            message = 'No.'
            out = render_template('login.html',message = message)

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
    else:
        message = None
        out = render_template('login.html',message = message)
    return out

def GetStatus():
    MaxTime = 3600 #certificates are valid for an hour
    #Note session can go on longer- new certificate is given each interaction with server
    fileObj = open(path+"Usernames.txt", "r")
    Usernames = fileObj.read().splitlines()
    fileObj.close()
    
    fileObj = open(path+"Passwords.txt", "r") 
    Passwords = fileObj.read().splitlines()
    fileObj.close()
    
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

    #Detirmine permissions 
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

def WriteCertificate(UserID):
    fileObj = open(path+"Usernames.txt", "r")
    Usernames = fileObj.read().splitlines()
    fileObj.close()
    
    fileObj = open(path+"Passwords.txt", "r") 
    Passwords = fileObj.read().splitlines()
    fileObj.close()
    
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


@app.route("/home", methods=['GET', 'POST'])
def Home():
        #currently generic. TODO: add functionality and probably additional pages
    Status,UserID = GetStatus() #security
    
    if(Status == "None"):
        response = make_response(render_template('Error.html'))
    if(Status == "Student"):
    
        response = make_response(render_template('StudentHome.html'))
        
        Certificate = WriteCertificate(UserID)       #new certificate
        response.set_cookie('Certificate',Certificate)
        
    if(Status == "Admin"):
        response = make_response(render_template('AdminHome.html'))

        Certificate = WriteCertificate(UserID)       #new certificate
        response.set_cookie('Certificate',Certificate)
    return response
    
