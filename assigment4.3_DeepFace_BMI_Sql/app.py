import os
import cv2
import datetime
from database import User, RegisterModel, LoginModel, engine
from sqlmodel import Session , select
from pydantic import ValidationError
from flask import Flask, render_template, send_file,request,redirect,session,url_for
import bcrypt
from ultralytics import YOLO


app = Flask("analyze_face")
app.config["UPLOAD_FOLDER"]="./uploads"
app.config["ALLOWED_EXTENSION"]={'PNG','JPG','JPEG'}

def auth(email,password):
    if email == "mzahrajafari94@gmail.com" and password == "1234":
        return True
    else:
        return False
    
def allowed_file(filename:str):
    format = filename.split(".")[1]
    if format == "jpg" or format == "png" or format == "jpeg":
        return True
    else:
        return False    

@app.route("/")
def my_root():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/about")
def project():
    return render_template("about.html")

@app.route("/contact")
def blog():
    return render_template("contact.html")

@app.route("/do")
def contact():
    return render_template("do.html")

@app.route("/result")
def result():
    return render_template("result.html")

@app.route("/resultbmr")
def resultbmr():
    return render_template("resultbmr.html")

@app.route("/BMR" , methods=["GET", "POST"])
def BMR():
    if request.method == "GET":
        return render_template("BMR.html")
    else:
        height = float(request.form["height"])
        weight = float(request.form["weight"])
        age = float(request.form["age"])
        gender = str(request.form["gender"])

        if gender == "female":
            bmi = (10 * weight) + (6.25 * height) - (5 * age) - 161
            return render_template("resultbmr.html", bmi=bmi)
        elif gender == "male":
            bmi = (10 * weight) + (6.25 * height) - (5 * age) + 5 
            return render_template("resultbmr.html", bmi=bmi)
        else:
             return render_template("BMR.html")

@app.route("/upload" , methods=['GET', 'POST'])
def upload():
    result={} 
    if request.method=="GET":
        return render_template("upload.html")
    elif request.method=="POST":
        my_image = request.files['image']
        if my_image.filename == "":
            return redirect(url_for("upload"))
        else:
            if my_image and allowed_file(my_image.filename):
                save_path = os.path.join(app.config["UPLOAD_FOLDER"], my_image.filename)
                my_image = cv2.imread(save_path)
                model = YOLO("yolov8n.pt")
                results = model(my_image)
                annotated_img = results[0].plot()
                return render_template("result.html", results=annotated_img)

        

@app.route("/login" , methods=['GET', 'POST'])
def login():
    if request.method == "GET":
         return render_template("login.html")
    elif request.method == "POST":
        try:
            login_model = LoginModel(
            username = request.form["username"],
            password = request.form["password"],
            
            
            )
            
        except:
           
            return redirect(url_for("login"))
        
        with Session(engine) as db_session:
    
            statement = select(User).where(User.username == login_model.username)
            user = db_session.exec(statement).first()
            
        if user:
            password_byte = login_model.password.encode("utf-8")
            if bcrypt.checkpw(password_byte, user.password):
               return redirect(url_for("upload"))
            else:
                print ("password is  incorect")
                return redirect(url_for("login"))
        else:
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
                    return redirect(url_for("login"))    
             else:
                return redirect(url_for("register")) 
       else:
            return redirect(url_for("register")) 
                    