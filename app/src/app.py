from flask import Flask, render_template, request, redirect
import json
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

sql_hostname = "localhost"
sql_port = 3306

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


# the home page now can upload and post function
@app.route("/", methods=["GET", "POST"])
def record():

    cnx = connect_to_db(sql_hostname, sql_port)
    cursor = cnx.cursor()

    cursor.execute("SHOW tables")
    cursor.execute("CREATE TABLE hello (the_date DATE)")
    cnx.commit()

    authenticator = IAMAuthenticator('AeWcu0gUgQQwm8PKD7knwKGXxVYuqYp9kRb9qH96-ZBs')
    service = SpeechToTextV1(authenticator=authenticator)
    service.set_service_url('https://stream.watsonplatform.net/speech-to-text/api')

    models = service.list_models().get_result()

    model = service.get_model('en-US_BroadbandModel').get_result()
    output = ""
    index = 0
    index_limit = False
    record = ""
    with open(join(dirname(__file__), 'hesitation.wav'),
          'rb') as audio_file:
        output = service.recognize(
        audio=audio_file,
        content_type='audio/wav').get_result()
    # print(json.dumps(output, indent=2))
    # filters the JSON dump to print out only the transcript 
    while index_limit == False:
        try:
            record += output['results'][index]['alternatives'][0]['transcript']
            # print(output['results'][index]['alternatives'][0]['transcript'], end = ' ')
            index += 1
        except IndexError:
            index_limit = True
            break
    return render_template('base.html',record = record)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)

    

