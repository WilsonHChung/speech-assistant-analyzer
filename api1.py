import speech_recognition as sr

def main():
    # initialize the recognition
    r = sr.Recognizer()
    # source could be audio file or microphone
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print ("Start listenning")
        #input source
        audio = r.listen(source)
        #use recognizer to convert audio into text
        try: 
            print("Assistant voice AI: \n" + r.recognize_google(audio))
        except Exception as e:
            print("failure: \n" + str(e))
    
if __name__ == "__main__":
    main()