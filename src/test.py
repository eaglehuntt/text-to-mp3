import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')

print(voices)

engine.setProperty('voice', voices[1].id)
engine.say("Hello World!")
engine.runAndWait()
engine.stop()

""" for voice in voices:
    print(voice, voice.id)
    engine.setProperty('voice', voice.id)
    engine.say("Hello World!")
    engine.runAndWait()
    engine.stop() """

#print(len(voices))

# male = 0 female = 1 