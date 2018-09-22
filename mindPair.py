from flask import Flask, jsonify, render_template, request,  redirect, url_for,g, session
import os,sys, inspect 
from hmac import compare_digest
import flask_login
from flask_pymongo import PyMongo
#from hash import hasher
from pymongo import MongoClient
from flask_bcrypt import Bcrypt


app =Flask(__name__, template_folder="./")

# starts mongo
#client = MongoClient('mongodb://Tumas:labanaktis34@ds259912.mlab.com:59912/mindpairbigdata')
app.config['Mongo_DBNAME']='mindpairbigdata'
app.config['MONGO_URI'] = 'mongodb://Tumas:labanaktis34@ds259912.mlab.com:59912/mindpairbigdata'

mongo = PyMongo(app)

bcrypt = Bcrypt(app)
users = mongo.db.users

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

app.secret_key = os.urandom(24)

@app.route('/createAccount',methods=['GET','POST'])
def createAccount():
	if request.method == 'POST':
		#get mongo db
		existingUser= users.find_one({'name': request.form['created_email']})

		if existingUser is None:
			hashpass= bcrypt.generate_password_hash(request.form['created_password']).decode('utf-8')

			hashConfirmPass = bcrypt.generate_password_hash(request.form['confirm_created_password']).decode('utf-8')
			if bcrypt.check_password_hash(hashpass,hashConfirmPass):
				return 'Enter the same password twice'
			#hashpass=str(hashpass)
			users.insert({'name': request.form['created_email'], 'password' : hashpass})
			session['username'] = request.form['created_email']
			return redirect(url_for('Home'))
		return "That Username Already Exists!"
	#return render_template("register.html")

	if request.method == 'GET':
		#print('get method works....')
		return  render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
	

	if request.method == 'GET':
		return render_template('login.html')
   		

	email = request.form['email']
	preHash = request.form['password']
	fin = preHash
    #fin = str(fin)
    #look for user data to set up getting it to match with others
   # users = mongo.db.users
	login_youser = users.find_one({'name':email})
	print('Found email is: ',login_youser['name'])
	loginPass = login_youser['password']

	print("found password is: ", loginPass)
	if login_youser != None:
	#print('loginPass is:  ',loginPass)

		#if bcrypt.check_password_hash(loginPass,fin):
			# session['username'] = request.form['username']
			# print("authenticated")
		#	login_user(user)
		return redirect(url_for('dashboard'))
		#return "Invalid Credentials. Please try again."

	#for bug testing    dataBaseQuery = users[email]['password']
	return "Invalid Credentials. Please try again."

@app.route("/")
def dashboard():
	return render_template('dashboard.html')

@app.route("/pair")
def pair():
	# insert recommender system lol
	return render_template('pair.html')


@app.route('/profile')
def profile():
	return render_template('profile.html')