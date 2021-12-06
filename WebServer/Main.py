import secrets
import datetime
import time
from flask import Flask, render_template, redirect, url_for, request, make_response
from LoginInfo import LoginInfo
import displayManager as dm
import numpy as np
path = "C:/Users/132/Desktop/WebServer/" #Change this if not me

app = Flask(__name__,template_folder= path+"templates")

#(cmd prompt reminder)---

#set FLASK_APP=C:/Users/132/Desktop/WebServer/Main
#flask run

#---


@app.route("/", methods=['GET', 'POST'])
def Login():
    global path
    if request.method == 'POST':

        message = ''
       # fileObj = open(path+"Usernames.txt", "r")
        #Usernames = fileObj.read().splitlines()
        #fileObj.close()
    
        fileObj = open(path+"LoginData.txt", "r") 
        LoginData = fileObj.read().splitlines()
        fileObj.close()
        sheet = []
        c = 0
        while(c<len(LoginData)):
            sheet.append(LoginData[c].split(','))
            c += 1
        #
        
        InfoSheet = np.array(sheet)
        #if request.form['Username'] in Usernames:
          #  UserID = Usernames.index(request.form['Username'])
          #  if request.form['Password'] == Passwords[UserID]:   
             #   message = 'Login successful. Something should happen now'
            ##    out = render_template('login.html',message = message)
              #  response = make_response(redirect(url_for('Home')))
             #   Certificate = LoginInfo.WriteCertificate(path,UserID)
              #  response.set_cookie('Certificate',Certificate)
              #  out = response
        if(request.form['Email'] in InfoSheet[:,0]):
            z = today[:,0].tolist().index(request.form['Email'])
            if(request.form['First'] == today[:,1]):
                if(request.form['Last'] == today[:,2]):
                    message = 'Login Succsesful'
                    response = make_response(redirect(url_for('Home')))
                    Certificate = LoginInfo.WriteCertificate(path,UserID)
                    response.set_cookie('Certificate',Certificate)
                    out = response
                else:
                    message = 'Typo?'
                    out = render_template('login.html',message = message)    
            else:
                message = 'Typo?'
                out = render_template('login.html',message = message)
        else:
            message = 'Email not recognized.'
            out = render_template('login.html',message = message)
    else:
        message = None
        out = render_template('login.html',message = message)
    return out


@app.route("/home", methods=['GET', 'POST'])
def Home():
    global path
        #currently generic. TODO: add more functionality and probably additional pages
    Status,UserID = LoginInfo.GetStatus(path) #security
    
    if(Status == "None"):
        response = make_response(render_template('Error.html'))
    if(Status == "Student"):
        message = ""
        Info = dm.InfoManager(path)
        uTab,UserTime,first,last,IsHere = Info.GetUserData(UserID)
        if(request.methos == 'POST'):
            now = datetime.datetime.now()
            CurrentTime =  HumanReadable = now.strftime("%H:%M:%S")
            CurrentDate = str(datetime.date.month)+str(datetime.date.day)
            if(request.form['CheckIn']):
                if(not IsHere):
                    nothing = Info.AdminOverride(CurrentTime,CurrentDate,UserID,Out = False)
                else:
                    message = "You are already checked in."
            elif(request.form['CheckOut']):
                if(IsHere):
                    nothing = Info.AdminOverride(CurrentTime,CurrentDate,UserID,Out = True)
                else:
                    message = "You are not currently checked in, so you may not check out."
        response = make_response(render_template('StudentHome.html'),table = uTab,name = str(first)+str(last),message = message)
                            
        
        Certificate = LoginInfo.WriteCertificate(path,UserID)       #new certificate
        response.set_cookie('Certificate',Certificate)
        
    if(Status == "Admin"):
        Info = dm.InfoManager(path)
        if(request.method == 'POST'):
            response = make_response(redirect(url_for('Home')))
            if(request.form['A']):
                response.set_cookie('Disp','absent')
            if(request.form['P']):
                response.set_cookie('Disp','present')
            if(request.form['C']):
                response.set_cookie('Disp','checked out')
            if(request.form['UserSearch']):
                response.set_cookie('User',request.form['IDnumber'])
            if(request.form['Session']):
                response.set_cookie('From',request.form['Session'])
            if(request.form['Clear']):
                response.set_cookie('Disp','null',max_age = 0)
                response.set_cookie('User','null',max_age = 0)
                response.set_cookie('From','null',max_age = 0)
                
            Ids = Info.getIds()       
            c = 0
            while(c<len(Ids)):
                if(request.form['Edit'+str(Ids[c])]):
                    response = make_response(redirect(url_for('Home')))
                    date = request.cookies.get('Session')
                    checkIn = request.form['CheckIn'+str(Ids[c])]
                    checkOut = request.form['CheckOut'+str(Ids[c])]
                    nothing = Info.AdminOverride(checkOut,date,Ids[c],Out = True)
                    nothing = Info.AdminOverride(checkIn,date,Ids[c],Out = False)
                c += 1

        else:
            if(request.cookies.get('User')):
                if(request.cookies.get('User') >= 0):
                    uTab,UserTime,first,last = Info.GetUserData(request.cookies.get('User'))
                    response = make_response(render_template('AdminHome.html'),table = uTab,head=str(first)+" "+str(last))
            else:     
                if(request.cookies.get('From')):   
                    Ftab,Atab,Ptab,Ctab,headdate = Info.GetSummary(request.cookies.get('Session'))
                else:
                    Ftab,Atab,Ptab,Ctab,headdate = Info.GetSummary(str(datetime.date.month)+str(datetime.date.day))
                if(request.cookies.get('Disp')):
                    q = request.cookies.get('Disp')
                    if(q == "absent"):
                        response = make_response(render_template('AdminHome.html'),table = Atab,head="Absent "+headdate)
                    elif(q == "present"):
                        response = make_response(render_template('AdminHome.html'),table = Ptab,head="Currently Present "+headdate)
                    elif(q == "checked out"):
                        response = make_response(render_template('AdminHome.html'),table = Ctab,head="Checked Out "+headdate)
                    elif(q == "user"):
                        none = Info.GetTotalMatrix()
                        uTab,UserTime,first,last = Info.GetUserData(request.cookies.get('User'))
                        response = make_response(render_template('AdminHome.html'),table = Ctab,head=str(first)+" "+str(last))               
                else:
                    response = make_response(render_template('AdminHome.html'),table = Ftab,head=headdate)

        
        Certificate = LoginInfo.WriteCertificate(path,UserID)       #new certificate
        response.set_cookie('Certificate',Certificate)
    return response
