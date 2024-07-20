import os
import cv2
import datetime
from database import User, RegisterModel, LoginModel, engine
from sqlmodel import Session , select
from pydantic import ValidationError
from flask import Flask, render_template, send_file,request,redirect,session as flask_seesion,url_for , flash
import bcrypt
from src.face_analysis import FaceAnalysis
from PIL import Image
import numpy as np
from utils.image import encode_image
from src.face_detection import RetinaFace
from src.age_gender_estimation import AgeGenderEstimator
from datetime import datetime
from database import relative_time_from_string

app = Flask("analyze_face")
app.config["UPLOAD_FOLDER"]="./uploads"
app.config["ALLOWED_EXTENSION"]={'PNG','JPG','JPEG'}
app.secret_key="this is myproject"


    
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
def about():
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

@app.route("/card")
def card():
    return render_template("card.html")

@app.route("/resultbmr")
def resultbmr():
    return render_template("resultbmr.html")

@app.route("/Logout")
def Logout():
    if  flask_seesion.get('userid'):
        flask_seesion.pop('userid')
        flask_seesion.pop('username')
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))
       
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
    if flask_seesion.get('userid'):
        if request.method=="GET":
             return render_template("upload.html")
        elif request.method=="POST":
            my_image = request.files['image']
            if my_image.filename == "":
                return redirect(url_for("upload"))
            else:
                if my_image and allowed_file(my_image.filename):
                    input_image = Image.open(my_image.stream)
                    input_image = np.array(input_image)
                    face_detection_model_path="models/det_10g.onnx"
                    age_gender_estimation_model_path="models/genderage.onnx"
                    face_analysis = FaceAnalysis(face_detection_model_path, age_gender_estimation_model_path)
                    output_image, genders, ages = face_analysis.detect_age_gender(input_image)
                    #output_image , genders, ages = FaceAnalysis().detect_age_gender(image=input_image)
                    image_uri = encode_image(output_image)
                    return render_template("result.html", genders=genders, ages=ages, image_uri=image_uri) 
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
               flask_seesion['userid']=user.id
               flask_seesion['username']=user.username
               flask_seesion['firstname']=user.firstname
               flask_seesion['lastname']=user.lastname
               flash("WEllcome You are loggin ("+flask_seesion.get('username')+")", "success")
               return redirect(url_for("card"))
            else:
                flash ("password is  incorect" , "danger")
                return redirect(url_for("login"))
        else:
            flash ("Username is  incorect" , "danger")
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
             join_time=str(datetime.now())
             
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
                    flash("your register done successfully", "success") 
                    return redirect(url_for("login"))    
             else:
                    flash("Password is incorrect", "danger")
                    return redirect(url_for("register")) 
       else:
            flash("Username is already exist,Try another username", "danger")
            return redirect(url_for("register")) 

@app.route("/read-your-mind", methods=['GET', 'POST'] )    
def read_your_mind():
     if request.method=="POST":
         x=request.form["number"]
         return redirect(url_for("read_your_mind_result", x=x))


     return render_template("mind_reader.html")            

@app.route("/read-your-mind/result", methods=['GET', 'POST'] )    
def read_your_mind_result():
    y = request.args.get("x")
    return render_template("read_your_mind_result.html" , number=y)

@app.route("/pose")
def pose():
     return render_template("pose-detection.html")

@app.route("/admin")
def admin():
    if flask_seesion.get('userid'): 
      username1=flask_seesion.get('username')
      with Session(engine) as db_session:
         all_users = select(User)
         all_users = list( db_session.exec(all_users) )
         users_count = Session(engine).query(User).count()
         for user in all_users :
            joined_time = str(user.join_time)
            parsed_time = datetime.strptime(joined_time, '%Y-%m-%d %H:%M:%S.%f')
            formatted_time = parsed_time.strftime('%Y-%m-%d %H:%M:%S')
            user.join_time = relative_time_from_string(formatted_time)  
            print (str(flask_seesion.get('firstname')))
      return render_template("admin.html", username1= str(flask_seesion.get('firstname')) + " " + str(flask_seesion.get('lastname')) , users=all_users , user_count= users_count)

    return redirect(url_for("login"))