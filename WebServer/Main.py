import secrets
import time
from flask import Flask, render_template, redirect, url_for, request, make_response
from LoginInfo import LoginInfo
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
        fileObj = open(path+"Usernames.txt", "r")
        Usernames = fileObj.read().splitlines()
        fileObj.close()
    
        fileObj = open(path+"Passwords.txt", "r") 
        Passwords = fileObj.read().splitlines()
        fileObj.close()
           

        if request.form['Username'] in Usernames:
            UserID = Usernames.index(request.form['Username'])
            if request.form['Password'] == Passwords[UserID]:   
                message = 'Login successful. Something should happen now'
                out = render_template('login.html',message = message)
                response = make_response(redirect(url_for('Home')))
                Certificate = LoginInfo.WriteCertificate(path,UserID)
                response.set_cookie('Certificate',Certificate)
                out = response
                
            else:
                message = 'Invalid Password'
                out = render_template('login.html',message = message)
        else:
            message = 'No.'
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
        Info = dm.InfoManager(path)

        uTab,UserTime,first,last = Info.GetUserData(UserID)
        response = make_response(render_template('StudentHome.html'))
        
        Certificate = LoginInfo.WriteCertificate(path,UserID)       #new certificate
        response.set_cookie('Certificate',Certificate)
        
    if(Status == "Admin"):
        Info = dm.InfoManager(path)
        if(request.method == 'POST'):
            response = make_response(render_template('AdminReload.html'))
            if(request.form['A']):
                response.set_cookie('Disp','absent')
            if(request.form['P']):
                response.set_cookie('Disp','present')
            if(request.form['C']):
                response.set_cookie('Disp','checked out')
            response.set_cookie('User',request.form['IDnumber'])
            response.set_cookie('Session',request.form['Session'])
            if(request.form['Session']):
                response.set_cookie('From',request.form['Session'])
            else:
                response.set_cookie('From',1)
        else:
            if(response.cookies.get('User')):
                if(response.cookies.get('User') >= 0):
                    uTab,UserTime,first,last = Info.GetUserData(request.cookies.get('User'))
                    response = make_response(render_template('AdminHome.html'),table = Ctab,head=str(first)+" "+str(last))
            else:     
                if(request.cookies.get('From')):   
                    Ftab,Atab,Ptab,Ctab = Info.GetSummary(request.cookies.get('Session'))
                else:
                    Ftab,Atab,Ptab,Ctab = Info.GetSummary(1)
                if(request.cookies.get('Disp')):
                    q = request.cookies.get('Disp')
                    3if(q == "absent"):
                        response = make_response(render_template('AdminHome.html'),table = Atab,head="Absent")
                    elif(q == "present"):
                        response = make_response(render_template('AdminHome.html'),table = Ptab,head="Currently Present")
                    elif(q == "checked out"):
                        response = make_response(render_template('AdminHome.html'),table = Ctab,head="Checked Out")
                    elif(q == "user"):
                        none = Info.GetTotalMatrix()
                        uTab,UserTime,first,last = Info.GetUserData(request.cookies.get('User'))
                        response = make_response(render_template('AdminHome.html'),table = Ctab,head=str(first)+" "+str(last))               
                else:
                    response = make_response(render_template('AdminHome.html'),table = Ftab)

        response = make_response(render_template('AdminHome.html'),head = "In Development")
    
        Certificate = LoginInfo.WriteCertificate(path,UserID)       #new certificate
        response.set_cookie('Certificate',Certificate)
    return response


    

    
