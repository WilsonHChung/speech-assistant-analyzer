import json
from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
import threading
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import pandas as pd

authenticator = IAMAuthenticator('1kbeHrn4ONq6qluCLyiqMYRBcHX9J6vjtZ4ddrg8uWtD')
service = SpeechToTextV1(authenticator=authenticator)
service.set_service_url('https://stream.watsonplatform.net/speech-to-text/api')

models = service.list_models().get_result()
# print(json.dumps(models, indent=2))

model = service.get_model('en-US_BroadbandModel').get_result()
# print(json.dumps(model, indent=2))

output = ""

with open(join(dirname(__file__), 'hesitation.wav'),
          'rb') as audio_file:
    output = service.recognize(
            audio=audio_file,
            content_type='audio/wav',
            timestamps=True,
            word_confidence=True).get_result()
    print(json.dumps(output, indent=2))
    print("Transcript Output:", output['results'][0]['alternatives'][0]['transcript'])



# Example using websockets
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

# Example using threads in a non-blocking way
# mycallback = MyRecognizeCallback()
# audio_file = open(join(dirname(__file__), 'hesitation.wav'), 'rb')
# audio_source = AudioSource(audio_file)
# recognize_thread = threading.Thread(
#     target=service.recognize_using_websocket,
#     args=(audio_source, "audio/l16; rate=44100", mycallback))
# recognize_thread.start()

# df = pd.DataFrame([i for elts in output for i in elts['speaker_labels']])
# print(df)