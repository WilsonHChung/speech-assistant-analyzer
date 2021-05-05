from flask import Flask, render_template, request, redirect, url_for, Response
import json
from werkzeug.utils import secure_filename

from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
import threading
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import mysql.connector
from mysql.connector import errorcode
from flaskext.mysql import MySQL


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['IMAGE_UPLOADS'] = '/'


sql_hostname = "localhost"
sql_port = 3306

file_name = ""
audio_file = ""

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

# def generate_transcript():

#     authenticator = IAMAuthenticator('1kbeHrn4ONq6qluCLyiqMYRBcHX9J6vjtZ4ddrg8uWtD')
#     service = SpeechToTextV1(authenticator=authenticator)
#     service.set_service_url('https://stream.watsonplatform.net/speech-to-text/api')

#     # models = service.list_models().get_result()
#     # model = service.get_model('en-US_BroadbandModel').get_result()

#     output = ""
#     record = ""
#     index = 0
#     index_limit = False

#     with open(join(dirname(__file__), 'hesitation.wav'),
#           'rb') as audio_file:
#         output = service.recognize(
#         audio=audio_file,
#         content_type='audio/wav').get_result()

#     while index_limit == False:
#         try:
#             record += output['results'][index]['alternatives'][0]['transcript']
#             index += 1
#         except IndexError:
#             index_limit = True
#             break

#     return record

def generate_transcript(file_name):

    authenticator = IAMAuthenticator('AeWcu0gUgQQwm8PKD7knwKGXxVYuqYp9kRb9qH96-ZBs')
    service = SpeechToTextV1(authenticator=authenticator)
    service.set_service_url('https://stream.watsonplatform.net/speech-to-text/api')

    # models = service.list_models().get_result()
    # model = service.get_model('en-US_BroadbandModel').get_result()

    output = ""
    record = ""
    index = 0
    index_limit = False

    # if(toggle == "file"):

    with open(join(dirname(__file__), file_name),
          'rb') as audio_file:
        output = service.recognize(
        audio=audio_file,
        content_type='audio/wav').get_result()

    while index_limit == False:
        try:
            record += output['results'][index]['alternatives'][0]['transcript']
            index += 1
        except IndexError:
            index_limit = True
            break

    return record



# the home page now can upload and post function
@app.route("/", methods=["GET", "POST"])
def record():
    global speech_id
    global file_name
    global audio_file
    toggle = "0"
    display_transcript = ""

    if request.method == 'POST':
        # data = request.get_data()
        # data = json.loads(data)
        # file_name = data["file_name"]
        # toggle = data["toggle"]

        file_name = request.files['file']
        audio_file = file_name.filename
        print(audio_file)

        file_name.save(secure_filename(file_name.filename))
        print("Audio file saved successfully and its transcript will be generated")

        # if ".wav" in audio_file:
        #     display_transcript = generate_transcript(audio_file)
        #     file_name = ""
        #     audio_file = ""

        # toggle = "live" or "file"
        

    # 1. Check if file was uploaded if so then update the transcript

    if ".wav" in audio_file:
        display_transcript = generate_transcript(audio_file)
        cnx = connect_to_db(sql_hostname, sql_port)
        cursor = cnx.cursor()

        insert_stmt = (
            "INSERT INTO speech(speech_id, file_name, transcript, total_number_of_words, total_number_of_hesitations, accuracy)"
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        word_list = display_transcript.split()
        number_of_words = len(word_list)
        number_of_hesitations = display_transcript.count('%HESITATION')
        data = (speech_id, audio_file, display_transcript, number_of_words, number_of_hesitations, (100 - ((number_of_hesitations / number_of_words) * 100)))
        cursor.execute(insert_stmt, data)
        # cursor.execute("INSERT INTO speech(speech_id, file_name, transcript) VALUES(1, 'hello.wav', 'Hello World')")
        # cursor.execute("INSERT INTO speech(speech_id, file_name, transcript) VALUES({0}, '{1}', '{2}')".format(1, file_name, display_transcript))
        cnx.commit()

        speech_id += 1
        file_name = ""
        audio_file = ""

    # display_transcript = generate_transcript(file_name)


    # 2. Check if live speech-to-text recording was done if so then update the transcript

    # else if toggle == "live":
    #     display_transcript = LIVE_generate_transcript()

    # 3. Else output an empty transcript on the frontend 

    # else:
    #     display_transcript = ""


    return render_template('base.html', record = display_transcript)

@app.route("/analytics", methods=["GET", "POST"])
def analytics():
    
    total_number_of_words= ""
    total_number_of_hesitations= ""

    cnx = connect_to_db(sql_hostname, sql_port)
    cursor = cnx.cursor()
    query = (
        "SELECT total_number_of_words, total_number_of_hesitations, accuracy FROM speech "
        "WHERE speech_id=1"
    )
    cursor.execute(query)
    t = cursor.fetchall()
    result = t[0]
    total_number_of_words = result[0]
    total_number_of_hesitations = result[1]
    accuracy = result[2]


    return render_template('analytics.html',test = t, total_number_of_words=total_number_of_words, total_number_of_hesitations=total_number_of_hesitations, accuracy = accuracy)















# Functional routing of downloading audio file from frontend into flask directory
# @app.route('/', methods = ['POST', 'GET'])
# def upload():
#     if request.method == 'POST':
#         f = request.files['file']
#         f.save(secure_filename(f.filename))
#         return "File saved successfully"




# Stream audio file in different directory (https://gist.github.com/hosackm/289814198f43976aff9b)
# @app.route("/wav")
# def streamwav():
#     def generate():
#         with open("signals/song.wav", "rb") as fwav:
#             data = fwav.read(1024)
#             while data:
#                 yield data
#                 data = fwav.read(1024)
#     return Response(generate(), mimetype="audio/x-wav")




if __name__ == "__main__":
    app.run(debug=True, threaded=True)

    

