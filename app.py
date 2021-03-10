
from flask import Flask,render_template, request,redirect,url_for
import pickle
from PIL import Image
from mtcnn.mtcnn import MTCNN
from tensorflow import keras
import os
from numpy import expand_dims
import numpy
from werkzeug.utils import secure_filename
from keras.models import load_model
import sqlite3
from sqlalchemy.orm import sessionmaker
#from faculty import User
from sqlalchemy import create_engine, ForeignKey
from sqlite3 import Error
from flask import Flask,render_template,flash, redirect,url_for,session,logging,request,flash
from flask_sqlalchemy import SQLAlchemy


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']) #The formats in which user
#                                                                     can upload the photo
UPLOAD_FOLDER = '/home/sak/'
#A function to predict the names of def predictor(name): 
#students from embeddings

################################################################################################

def predictor(name): 
	p=[]
	m=pickle.load(open('pred_3_svm_face_model.pkl','rb')) #Loading my trained model for classification
	l=pickle.load(open('label.pkl','rb'))    			# Loading a saved dictionary in which 
	#                                                     names of all students are present
	face=extract_face_test(name)
	face=numpy.asarray(face)
	emb=get_emb(face)
	for i in emb:
	    pred=m.predict([i])
	    print(l[pred[0]])
	    p.append(l[pred[0]])
	return p


###############################################################################################

def get_embedding(model, face_pixels):
    face_pixels = face_pixels.astype('float32')
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean) / std
    samples = expand_dims(face_pixels, axis=0)
    ypred = model.predict(samples)
    return ypred[0]


################################################################################################

# A function to get embeddings of extracted face
def get_emb(face):
	mod=load_model('face_net.h5')     # Loading pre-trained Facenet model to get face-embeddings
	newx=list()                       # A list to store face embeddings
	for face_pixel in face:
		embedding=get_embedding(mod,face_pixel)
		newx.append(embedding)
	newx = numpy.asarray(newx)
	return newx

###################################################################################################
# A function to extract faces of person from image
def extract_face_test(name, required_size=(160, 160)):
    mf1=[]
    image = Image.open(name)
    image = image.convert('RGB')
    pixels = numpy.asarray(image)
    detector = MTCNN()              #To detect and extract faces of people form photo
    results = detector.detect_faces(pixels)
    for i in range(0,len(results)):
        if results[i]['confidence']>0.99:
            x1, y1, width, height = results[i]['box']
            x1, y1 = abs(x1), abs(y1)
            x2, y2 = x1 + width, y1 + height
            face = pixels[y1:y2, x1:x2]
            image = Image.fromarray(face)
            image = image.resize(required_size)
            face_array = numpy.asarray(image)
            mf1.append(face_array)
    return mf1


	

app=Flask(__name__) 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "flask rocks!"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)



class user(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80))
	email = db.Column(db.String(120))
	password = db.Column(db.String(80))

@app.route('/',methods=['GET','POST'])
def index():
	return render_template('index.html') 


@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == "POST":
		uname = request.form["uname"]
		passw = request.form["passw"]
		login = user.query.filter_by(username=uname, password=passw).first()
		if login is not None:
			return redirect(url_for("form"))
		else:
			return redirect(url_for("ERROR"))
	return render_template("login.html")


@app.route('/register.html', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        register = user(username = uname, email = mail, password = passw)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")

@app.route('/ERROR', methods=['GET','POST'])
def ERROR():
	return render_template('ERROR.html')

@app.route('/form', methods=['GET','POST'])
def form():
	return render_template('form.html')


################################################################################################

@app.route('/result.html', methods = ['POST']) 
def result(): 
	basepath="/home/sak/"
	r=[]
	if 'image' not in request.files:
		print("Error")
	else:
		image_file = request.files['image']
		name = image_file.filename
		file_path = os.path.join(basepath,name)
		image_file.save(file_path)
		r.append(predictor(file_path))
		print(r)
		names=r[0]
		print(names)
		con = sqlite3.connect('mydatabase34.db')
		try:
			con = sqlite3.connect(':memory:')
			print("Connection is established: Database is created in memory")
		except Error:
			print(Error)
		try: 
			con = sqlite3.connect('mydatabase34.db')
			print("Connected")
		except Error:
			print(Error)
		obj=con.cursor()
		obj.execute("CREATE TABLE if not exists student(name char(20) , attendance char(1))")
		con.commit()
		obj.execute("INSERT INTO student VALUES('sak','A'),('ankit','A'),('Abhishek','A')")
		con.commit()

		for n in names:
			print(n)
			obj.execute (" UPDATE student SET attendance='P' WHERE student.name='%s'" %(n))
			print("ATTENDACE MARKED FOR -",n)

		con.commit()
	return render_template('result.html', prediction = r[0]) 

