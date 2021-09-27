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
        #currently generic. TODO: add functionality and probably additional pages
    Status,UserID = LoginInfo.GetStatus(path) #security
    
    if(Status == "None"):
        response = make_response(render_template('Error.html'))
    if(Status == "Student"):
    
        response = make_response(render_template('StudentHome.html'))
        
        Certificate = LoginInfo.WriteCertificate(path,UserID)       #new certificate
        response.set_cookie('Certificate',Certificate)
        
    if(Status == "Admin"):
        response = make_response(render_template('AdminHome.html'))

        Certificate = LoginInfo.WriteCertificate(path,UserID)       #new certificate
        response.set_cookie('Certificate',Certificate)
    return response
    
