import json
from flask import render_template, flash, redirect, url_for, jsonify, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from ibm_watson import IAMTokenManager
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.models import User
from datetime import datetime
import mysql.connector
from mysql.connector import errorcode
from flaskext.mysql import MySQL

# app = Flask(__name__)
# app.config['TEMPLATES_AUTO_RELOAD'] = True
# app.config['IMAGE_UPLOADS'] = '/'

sql_hostname = "localhost"
sql_port = 3306

file_name = ""
speech_id = 1

def connect_to_db(hostname, port):
    connected = False
    
    # MySQL configurations
    app.config['MYSQL_DATABASE_USER'] = "root"
    app.config['MYSQL_DATABASE_PASSWORD'] = "password"
    app.config['MYSQL_DATABASE_DB'] = "speech_app"
    app.config['MYSQL_DATABASE_HOST'] = "db"
    app.config['MYSQL_DATABASE_PORT'] = 3306
   
    mysql = MySQL()
    mysql.init_app(app)
    try:
        conn = mysql.connect()
        connected  = True
    except Exception as ex:
        print(ex)
        return None

    if connected:
        return conn

    return None

@app.route('/')
@app.route('/index')
def index():
    speech = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland'
        }, 
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', speech=speech)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # flash('Login requested for user {}, remember_me={}'.format(
        #     form.username.data, form.remember_me.data
        # ))
        # logic to redirect to the page that required login by getting the value from "next" arg 
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/token')
@login_required
def token():
    # In your API endpoint use this to generate tokens
    iam_token_manager = IAMTokenManager(apikey='ukQ17BPHEoBP0tBYovtuQn_Dlb5dfH4waoA5Zpy_w8aO')
    token = iam_token_manager.get_token()
    return jsonify({"accessToken": token, "url": "https://api.us-south.speech-to-text.watson.cloud.ibm.com"})

@app.route('/speech', methods=['POST', 'GET'])
@login_required
def speech():

    global speech_id
    global file_name

    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        file_name = data["file_name"]
        transcript = data["transcript"]
        method = data["method"]
        print("File name:", file_name)
        print("Transcript:", transcript)
        print("Method:", method)

        cnx = connect_to_db(sql_hostname, sql_port)
        cursor = cnx.cursor()

        insert_stmt = (
            "INSERT INTO speech(speech_id, file_name, transcript, total_number_of_words, total_number_of_hesitations, accuracy)"
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        word_list = transcript.split()
        number_of_words = len(word_list)
        number_of_hesitations = transcript.count('%HESITATION')
        data = (speech_id, file_name, transcript, number_of_words, number_of_hesitations, (100 - ((number_of_hesitations / number_of_words) * 100)))
        cursor.execute(insert_stmt, data)
        cnx.commit()

        speech_id += 1
        file_name = ""


    return render_template('speech_to_text.html')

@app.route('/file_upload', methods=['POST', 'GET'])
@login_required
def file_upload():

    global speech_id
    global file_name

    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        file_name = data["file_name"]
        transcript = data["transcript"]
        method = data["method"]
        print("File name:", file_name)
        print("Transcript:", transcript)
        print("Method:", method)


        cnx = connect_to_db(sql_hostname, sql_port)
        cursor = cnx.cursor()

        insert_stmt = (
            "INSERT INTO speech(speech_id, file_name, transcript, total_number_of_words, total_number_of_hesitations, accuracy)"
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        word_list = transcript.split()
        number_of_words = len(word_list)
        number_of_hesitations = transcript.count('%HESITATION')
        data = (speech_id, file_name, transcript, number_of_words, number_of_hesitations, (100 - ((number_of_hesitations / number_of_words) * 100)))
        cursor.execute(insert_stmt, data)
        cnx.commit()

        speech_id += 1
        file_name = ""



    return render_template('file_upload.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    speech = [
        {'author': user, 'body': 'Test speech #1'},
        {'author': user, 'body': 'Test speech #2'}
    ]
    return render_template('user.html', user=user, speech=speech)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route("/analytics", methods=["GET", "POST"])
def analytics():
    
    total_number_of_words= ""
    total_number_of_hesitations= ""

    cnx = connect_to_db(sql_hostname, sql_port)
    cursor = cnx.cursor()
    # query = (
    #     "SELECT total_number_of_words, total_number_of_hesitations, accuracy FROM speech "
    #     "ORDER by speech_id desc"
    # )
    # cursor.execute(query)
    # t = cursor.fetchall()
    # result = t[0]
    # total_number_of_words = result[0]
    # total_number_of_hesitations = result[1]
    # accuracy = result[2]


    # return render_template('analytics.html',test = t, total_number_of_words=total_number_of_words, total_number_of_hesitations=total_number_of_hesitations, accuracy=accuracy)

    query = (
        "SELECT file_name, transcript, total_number_of_words, total_number_of_hesitations, accuracy FROM speech "
        "ORDER by speech_id desc"
    )
    cursor.execute(query)
    rows = cursor.fetchall()
    return render_template('analytics.html', rows=rows)