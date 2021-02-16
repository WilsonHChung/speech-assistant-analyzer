from flask import Flask, render_template, request, redirect
import json
from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
import threading
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import pandas as pd

# from flask_bootstrap import Bootstrap


app = Flask(__name__)

# bootstrap = Bootstrap(app)


# the home page now can upload and post function
@app.route("/", methods=["GET", "POST"])
def record():
    authenticator = IAMAuthenticator('ukQ17BPHEoBP0tBYovtuQn_Dlb5dfH4waoA5Zpy_w8aO')
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

# def index():
#     #transcript is empty as initialize
#     transcript = ""

#     if request.method =="POST":
#         print("FORM DATA RECEIVED")

#         # 2 cases failure
#         #if no file part existing, redirect to home page
#         if "file" not in request.files:
#             return redirect(request.url)
#         #required to submit a file instead of submit a blank file
#         file = request.files["file"]
#         # if the file is blank, redirect to home page
#         if file.filename == "":
#             return redirect(request.url)

#         #if file existed
#         if file:
#             recognizer = sr.Recognizer()
#             # 2steps
#             #1. Create audio file object, open audio file object with uploaded file
#             audioFile = sr.AudioFile(file)
#             # 2. open and reading uploaded file though recognizer
#             with audioFile as source:
#                 data = recognizer.record(source)

#             # Can use mutiple API here
#             transcript = recognizer.recognize_google(data, key=None)
#             print(transcript)
#     # inside template, it will look for index.html
#     return render_template('index.html', transcript= transcript)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)

    

