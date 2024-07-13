import os
import cv2
import datetime
from database import User, RegisterModel, LoginModel, engine
from sqlmodel import Session , select
from pydantic import ValidationError
from flask import Flask, render_template, send_file,request,redirect,session as flask_seesion,url_for,flash
import bcrypt


app = Flask("Personal WebSite")
app.secret_key="its my app"

@app.route("/")
def my_root():
    if flask_seesion.get('userid'):
        flask_seesion.pop('userid')
        flask_seesion.pop('username')
    return render_template("index.html")

@app.route("/home")
def home():
    if flask_seesion.get('userid'):
        flask_seesion.pop('userid')
        flask_seesion.pop('username')
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/do")
def do():
    return render_template("do.html")

@app.route("/portfolio")   
def portfo():
    if flask_seesion.get('userid'):
        return render_template("portfolio.html")    
    else:  
        return redirect(url_for("home"))
    
@app.route("/Logout")
def Logout():
    if flask_seesion.get('userid'):
        flask_seesion.pop('userid')
        flask_seesion.pop('username')
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))  
      
@app.route("/login" , methods=['GET', 'POST'])
def login():
   if request.method == "GET":
         return render_template("login.html")
   elif request.method == "POST":
        try:
            login_model = LoginModel(
            username = request.form["username"],
            password = request.form["password"]       
            )
        
        except:
            flash("Enter a valid data","danger") 
            return redirect(url_for("login"))
        
        with Session(engine) as db_session:
    
            statement = select(User).where(User.username == login_model.username)
            user = db_session.exec(statement).first()
            
        if user :
            password_byte = login_model.password.encode("utf-8")
            if bcrypt.checkpw(password_byte, user.password):
               flask_seesion['username']=user.username
               flask_seesion['userid']=user.id
               if  flask_seesion.get('userid'):
                  flash("Wellcome You are loggin ("+flask_seesion.get('username')+")", "success")
               return redirect(url_for("portfo"))
            else:
                flash ("password is  incorect" , "danger")
                return redirect(url_for("login"))
        else:
           flash("username Not found" , "danger") 
           return redirect(url_for("login"))
        


@app.route("/register" , methods=['GET', 'POST'])
def register():
    if request.method == "GET":
         return render_template("register.html")
    elif request.method == "POST":     
        
       try:    
       
           register_data=RegisterModel(
             city = request.form["city"], 
             username = request.form["username"], 
             password = request.form["password"],
             confirm_password = request.form["confirm_password"],
             firstname = request.form["firstname"],
             lastname = request.form["lastname"],
             country = request.form["country"],
             age = request.form["age"],
             email = request.form["email"],
             join_time=str(datetime.date.today())
             
         )  
         
       except:
            flash("Enter a valid data","danger")
            return redirect(url_for("register")) 
            
       with Session(engine) as db_session:
            statement = select(User).where(User.username == register_data.username)    
            result = db_session.exec(statement).first()
            
       if not result:
             if(register_data.password==register_data.confirm_password) :    
               
                with Session(engine) as db_session:
                    user = User(
                        username = register_data.username,
                        city = register_data.city,
                        password  = bcrypt.hashpw(register_data.password.encode('utf-8'),bcrypt.gensalt()),
                        firstname = register_data.firstname,
                        lastname = register_data.lastname,
                        country = register_data.country,
                        age = register_data.age,
                        email = register_data.email, 
                        join_time = register_data.join_time
                    )
                    db_session.add(user)
                    db_session.commit()  
                    flash("your register done successfully", "success")  
                    return redirect(url_for("login"))    
             else:
                flash("Password is incorrect","danger")
                return redirect(url_for("register")) 
       else:
            flash("Username is already exist,Try another username", "danger")
            return redirect(url_for("register")) 
       

  