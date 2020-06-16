from difflib import SequenceMatcher
import pyttsx3, win32com.client, wolframalpha, random
import speech_recognition as sr
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

APP_ID='97YY7U-AXUTH742TV'

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

results = sp.search(q='work music', limit=20)
for idx, track in enumerate(results['tracks']['items']):
    print(idx, track['name'])


lastCommand = ''
lastAnswer = ''
name = 'Jack'
trigger = 'ok {}'.format(name)
currentRate = 135

r = sr.Recognizer() #starting the speech_recognition recognizer
r.pause_threshold = 0.7  #it works with 1.2 as well
r.energy_threshold = 400
shell = win32com.client.Dispatch("WScript.Shell")  
engine = pyttsx3.init()
engine.setProperty('rate', currentRate) 

wolframaClient = wolframalpha.Client(APP_ID)                                                      #api for wolfram alpha
att = wolframaClient.query('Test/Attempt')



static_answers = {
    'np':{
        'no problem... anytime..',
        'you are welcome',
    },
    'joke':{
        0:'are you kidding me!',
        1:'is that a joke ?',
        2:'haha very funny!'
    }
}
def similarity(a, b):
    ratio = SequenceMatcher(None, a, b).ratio()
    print('# similarity ' + str(ratio))
    return ratio
    

def speak(sentence):
    if static_answers.get(sentence):
        s = random.choice(list(static_answers.get(sentence).values()))
    else:
        lastAnswer = sentence
        s = sentence
    print('# Speaking  '+sentence)
    engine.say(s)
    engine.runAndWait()

def tellIp():
    ip = str(requests.get('http://icanhazip.com').text)
    speak('Your ip address is {}'.format(ip))

def tellName():
    speak('My name is {}'.format(name))

def tellLastCommand():
    speak('Last command was {}'.format(lastCommand))
def tellLastAnswer():
    speak('Last answer was {}'.format(lastAnswer))

commands = {
    'tellme': {
        'ip address': tellIp,
        'your name': tellName,
        'last command': tellLastCommand,
        'last answer': tellLastAnswer
    },
    'canyou':{},
    'whattime':{},
    'whois':{},
    'whatis':{}
}


def _getKeys(dict):        
    return list(dict.keys())
def _getVals(dict):
    return list(dict.values())

speak('Hello John!!')

while True: #The main loop

    with sr.Microphone() as source:
        try:
            audio = r.listen(source, timeout = None) # instantiating the mic (timeout = None)
            message = str(r.recognize_google(audio))
            print('You said: ' + message)
            if 'keyword list' in message:
                print('')
                print('[+] Say "info" to get information about me')
                print('[+] Say "set name ..." to give a new name')
                print('[+] Say "set trigger ..." to set a new trigger')
                print('')
            elif message == 'information':
                speak('My name is {}. My Current rate is {}.'.format(name,currentRate))
                if trigger:
                    speak('listening trigger is   {}'.format(trigger))
            elif message == 'thank you':
                if lastAnswer != '':
                    speak('np')
                else: 
                    speak('joke')
            elif 'play' in message:
                s = SpotifyLocal()
                s.connect()
                print(s.get_current_status())
            else:
                arr = message.split(' ')
                if len(arr) > 1:
                    pattern = ''.join(arr[0:2])
                    print(pattern)
                    if commands.get(pattern):
                        commandArr = arr[2:]
                        command = ' '.join(commandArr)
                        if len(commandArr) > 2:
                            res = wolframaClient.query(command)
                            speech = next(res.results).text
                            print(speech)
                            speak(speech)
                        else:
                            
                            for key in _getKeys(commands.get(pattern)):
                                print('# pattern => ' + pattern)
                                if similarity(key,command) > 0.6 :
                                    print('# command => ' + command)
                                    print('# key => ' + key)

                                    commands.get(pattern).get(key)()
                                    lastCommand = message
                    else:
                        speak('unknown pattern')
                        

        except sr.UnknownValueError:
            print("For a list of commands, say: 'keyword list'...")

        except sr.RequestError:
            speak("I'm sorry, I couldn't reach google")
            print("I'm sorry, I couldn't reach google")
        except KeyboardInterrupt:
            speak("See you later..")
            exit()
        except :
            speak("I'm sorry i've got no answer for you")