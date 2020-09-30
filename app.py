from flask import Flask, render_template, request, redirect
import speech_recognition as sr

app = Flask(__name__)
# the home page now can upload and post function
@app.route("/", methods=["GET", "POST"])
def record():
    record = ""
    # initialize the recognition
    recognizer = sr.Recognizer()
    # source could be audio file or microphone
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print ("Start listenning")
        #input source
        audio = recognizer.listen(source)
        #use recognizer to convert audio into text
        record = recognizer.recognize_google(audio)
        print(record)
    return render_template('record.html',record = record )
def index():
    #transcript is empty as initialize
    transcript = ""

    if request.method =="POST":
        print("FORM DATA RECEIVED")

        # 2 cases failure
        #if no file part existing, redirect to home page
        if "file" not in request.files:
            return redirect(request.url)
        #required to submit a file instead of submit a blank file
        file = request.files["file"]
        # if the file is blank, redirect to home page
        if file.filename == "":
            return redirect(request.url)

        #if file existed
        if file:
            recognizer = sr.Recognizer()
            # 2steps
            #1. Create audio file object, open audio file object with uploaded file
            audioFile = sr.AudioFile(file)
            # 2. open and reading uploaded file though recognizer
            with audioFile as source:
                data = recognizer.record(source)

            # Can use mutiple API here
            transcript = recognizer.recognize_google(data, key=None)
            print(transcript)
    # inside template, it will look for index.html
    return render_template('index.html', transcript= transcript)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)

    

