import json
from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
import threading
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import pandas as pd

authenticator = IAMAuthenticator('ukQ17BPHEoBP0tBYovtuQn_Dlb5dfH4waoA5Zpy_w8aO')
service = SpeechToTextV1(authenticator=authenticator)
service.set_service_url('https://stream.watsonplatform.net/speech-to-text/api')

models = service.list_models().get_result()

model = service.get_model('en-US_BroadbandModel').get_result()

output = ""
index = 0
index_limit = False

# inputs the audio file into the IBM Watson Cloud service to figure out speech to text 

with open(join(dirname(__file__), 'hesitation.wav'),
          'rb') as audio_file:
    output = service.recognize(
            audio=audio_file,
            content_type='audio/wav').get_result()
    # print(json.dumps(output, indent=2))

# filters the JSON dump to print out only the transcript 

while index_limit == False:
    try:
        print(output['results'][index]['alternatives'][0]['transcript'], end = ' ')
        index += 1
    except IndexError:
        index_limit = True
        break


class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_transcription(self, transcript):
        print(transcript)

    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        print('Service is listening')

    def on_hypothesis(self, hypothesis):
        print(hypothesis)

    def on_data(self, data):
        print(data)

