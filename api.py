#install and import dependencies
import json 
from os.path import join, dirname 
from ibm_watson import SpeechToTextV1 #extracted the speech to text class
from ibm_watson.websocket import RecognizeCallback, AudioSource 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator 
   
# 1. Setup Service
# Insert API Key in place of 
authenticator = IAMAuthenticator('VeyOajQ9p5WCQ138lHwv5drR0BS_1aJbZnm5nQzQKITh')  #set up authenticator using api key
service = SpeechToTextV1(authenticator = authenticator) #instance conver speech to text
   
#Insert URL in place of 'API_URL'  
service.set_service_url('https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/8addfeda-7fa3-4fa6-bc66-edb70cbfbc50') 
   
#2. Open audio Source and convert
# Insert local mp3 file path in 

with open(join(dirname('audio-file.flac'), r'C:\Users\steve\flask_app\audio-file.flac'),  
          'rb') as audio_file: #perform convertion
      # Use service.recognize to convert audio and pass through audio=audio_file
      # model='en-US_NarrowbandModel to specific file mp3 and langugae model
        dic = json.loads( 
                json.dumps( 
                    service.recognize( 
                        audio=audio_file, 
                        content_type='audio/flac',    
                        model='en-US_NarrowbandModel', 
                    continuous=True).get_result(), indent=2)) 


#with open(join(dirname('audio-file.mp3'), r'C:\Users\steve\flask_app\audio-file.mp3'),  
#          'rb') as audio_file: #perform convertion
#      # Use service.recognize to convert audio and pass through audio=audio_file
#      # model='en-US_NarrowbandModel to specific file mp3 and langugae model
#        dic = json.loads( 
#                json.dumps( 
#                    service.recognize( 
#                        audio=audio_file, 
#                        content_type='audio/mp3',    
#                        model='ja-JP_NarrowbandModel', 
#                    continuous=True).get_result(), indent=2)) 

# Stores the transcribed text 
str = "" 
# extracted conversion to text
while bool(dic.get('results')): 
    str = dic.get('results').pop().get('alternatives').pop().get('transcript')+str[:] 
print(str) 
with open('output.txt', 'w') as out:
    out.writelines(str)