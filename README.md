Speech Assistant Analyzer
=============

Speech Assistant Analyzer is a web application assistant that helps you improve your speaking skills. You can practice your speeches by speaking into your microphone for live translation or uploading an audio file. It displays and highlights your stuttering or filler words such as "uh" or "like." The app also helps keep track of your speech performance over time providing you the awareness and knowledge in order to create the perfect speech. Anyone can use it - teachers, engineers, students, anybody!


Installation
---------------

Requirements:
* Windows 10, Mac OS, or Linux 
* Python 3
    - https://www.python.org/downloads/
* Docker 
    - https://docs.docker.com/get-docker/

Install using:
(Assuming you already have Docker and Python 3 installed)

    $ cd speech-assistant-analyzer
    $ make start 



Usage
---------------

    1. Create an account in the app
    
    2. Sign into the app
    
    3. Choose between the following within the "Practice" tab on the toolbar above: "Record your speech" or "Upload an audio file"
    
    
    "Record your speech" - Live translation or practicing for speeches 
      - Options:
        - Record audio: Allows you to do live translation in order to practice your speech in real-time 
        - Stop: Stop recording when you're done practicing the current speech
        - Show filler words: Highlights the filler words when your speech is shown on the display

    "Upload an audio file" - Upload an existing audio file you want to examine with audio playback 
      - Options:
        - Choose file: Upload an audio file with the supported types which include .wav, .mp3, .ogg, .opus, .flac, and .webm
        - Stop: You can stop audio playback and analysis anytime 
        - Show filler words: Highlights the filler words when your speech is shown on the display


    4. Finally, you can choose the option "Your Analytics" from the "Practice" tab when you're finsihed recording to check your progress.


Contributing
---------------
Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.



License
---------------
MIT <https://choosealicense.com/licenses/mit/>
