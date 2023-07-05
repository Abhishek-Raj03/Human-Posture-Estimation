from flask import Flask,redirect,url_for,render_template,request,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import time
import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
from mpl_toolkits import mplot3d
# from celluloid import Camera
from scipy import spatial
# import pyshine as ps
from calc_angle import calculateAngle,Average,convert_data,dif_compare,diff_compare_angle
from extract_keypoints import extractKeypoint
from compare_pose import compare_pose
from main import main
from dumble import dumb
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from pushup import push
from squats import squats_fun

class UploadFileForm(FlaskForm):
    file=FileField("File")
    submit=SubmitField("Upload File")

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


app=Flask(__name__,static_url_path='',static_folder='./static')
app.secret_key = "secret key"

app.config['SECRET_KEY']='supersecretkey'
app.config['UPLOAD_FOLDER']='static/video'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'thisisasecretkey'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(20),nullable = False)
    age = db.Column(db.Integer(),nullable = False)


# class RegisterForm(FlaskForm):
#     username = StringField(validators=[
#                            InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "User Name"})

#     password = PasswordField(validators=[
#                              InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
#     confirm_password = PasswordField(validators=[
#                              InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Confirm Password"})
#     name = StringField(validators=[
#                            InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Your name"})
#     age = IntegerField(validators=[
#                            InputRequired()], render_kw={"placeholder": "Age"})

#     submit = SubmitField("Register")

#     def validate_username(self, username):
#         existing_user_username = User.query.filter_by(
#             username=username.data).first()
#         if existing_user_username:
#             raise ValidationError(
#                 'That username already exists. Please choose a different one.')

# class LoginForm(FlaskForm):
#     username = StringField(validators=[
#                            InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

#     password = PasswordField(validators=[
#                              InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

#     submit = SubmitField('Login')


@app.route('/')
def fun():
    return render_template('index.html')


# @app.route('/register',methods = ['POST','GET'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         if form.password.data == form.confirm_password.data:
#             hashed_password = bcrypt.generate_password_hash(form.password.data)
#             new_user = User(username=form.username.data, password=hashed_password,name = form.name.data,age= form.age.data)
#             db.session.add(new_user)
#             db.session.commit()
#             return redirect(url_for('login'))
#         else:
#             return redirect(url_for('register'))

#     return render_template('register.html',form = form)

@app.route('/register_page')
def register_pager():
    return render_template('register.html')

@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        existing_username = User.query.filter_by(
        username=request.form.get('username')).first()
        if existing_username:
            return redirect(url_for('login'))
        # if request.form.get('password') == "":
        #     return redirect(url_for('register'))
            
        if request.form.get('password') == request.form.get('confirm_password'):
            hashed_password = ""
            if request.form.get('password'):
                hashed_password = bcrypt.generate_password_hash(request.form.get('password'))
            else:
                return redirect(url_for('register'))
            new_user = User(username=request.form.get('username'), password=hashed_password,name = request.form.get('password'),age= request.form.get('age'))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return redirect(url_for('register'))
    else:
        return redirect(url_for('register'))


# @app.route('/login',methods = ['POST','GET'])
# def login():
#     form = LoginForm()

#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user:
#             if bcrypt.check_password_hash(user.password, form.password.data):
#                 login_user(user)
#                 return redirect(url_for('dashboard'))

#     return render_template('login.html',form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username= request.form.get('username')).first()
        if user:
            if bcrypt.check_password_hash(user.password, request.form.get('password')):
                login_user(user)
                
                return redirect(url_for('features'))
                # return redirect(url_for('dashboard'))

        
            
    return render_template('login.html',title = 'Login')




@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    flash("Logged in")
    return render_template('dashboard.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/features')
@login_required
def features():
    return render_template('feature.html')

@app.route('/yogaMain',methods=['GET','POST'])
@login_required
def yogaMain():
    form=UploadFileForm()
    if form.validate_on_submit():
        file=form.file.data # grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # save the file
        main(file.filename)
        os.remove("static/video/"+file.filename)
        return redirect(url_for('yogaMain'))
    else:
        return render_template('yogaMain.html',form=form)


@app.route('/pose/<id>')
def pose(id):
    # referrer=request.headers.get('Referer')
    main(id)
    return redirect(url_for('yogaMain'))
    # return redirect(referrer)

@app.route('/gym')
def gym():
    return render_template('gym.html')

@app.route('/dumble')
def dumble():
    dumb()
    return redirect(url_for('gym'))

@app.route('/pushup')
def pushup():
    push()
    return redirect(url_for('gym'))

@app.route('/squats')
def squats():
    squats_fun()
    return redirect(url_for('gym'))

if __name__ == '__main__':
    app.run(debug=True)