from win32com.client import Dispatch
import speech_recognition as sr
from os import system
from re import search
import webbrowser
import requests
import subprocess
from random import random
from weather import Weather
import sys

def talkToMe(audio):
    #speaks text passed as argument
    speak = Dispatch("SAPI.SpVoice")
    # print(audio)
    for line in audio.splitlines():
        speak.Speak(line)

def is_connected():
    #Checks the network
    try:
        res = subprocess.check_output(['ping','-n','2','www.google.co.in'],
            stderr=subprocess.STDOUT,
            universal_newlines=True)
    except subprocess.CalledProcessError:
        res = None
    if not(res==None):
        return True
    else:
        return False

def myCommand():
    #listens for commands from Microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            talkToMe("Say Something!")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)

        try:
            command = r.recognize_google(audio).lower()
            print('You said: ' + command + '\n')
            assistant(command)

        #loop back to continue to listen for commands if unrecognizable speech is received
        except sr.UnknownValueError:
            talkToMe('Sorry,I didn\'t hear you!')
            command = myCommand()
        except:
            talkToMe("Im not in the cloud")

        return command

def assistant(command):
    #if statements for executing commands
    try:
        if 'open website' in command:
            reg_ex = search('open website (.+)', command)
            if reg_ex:
                domain = reg_ex.group(1)
                url = 'https://www.' + domain
                webbrowser.open(url)
                talkToMe('Done!')
            else:
                pass
        elif 'joke' in command:
            res = requests.get(
                    'https://icanhazdadjoke.com/',
                    headers={"Accept":"application/json"}
                    )
            if res.status_code == requests.codes.ok:
                talkToMe(str(res.json()['joke']))
                print(str(res.json()['joke']))
            else:
                talkToMe('Oops! I ran out of jokes')

        elif 'weather in' in command:
            reg_ex = search('weather in (.*)', command)
            if reg_ex:
                city = reg_ex.group(1)
                weather = Weather()
                location = weather.lookup_by_location(city)
                condition = location.condition()
                res = 'The Current weather in %s is %s The tempeture is %.1f degree' % (city, condition.text(), (int(condition.temp())-32)/1.8)
                talkToMe(res)
                print(res)

        elif 'weather forecast in' in command:
            reg_ex = search('weather forecast in (.*)', command)
            if reg_ex:
                city = reg_ex.group(1)
                weather = Weather()
                location = weather.lookup_by_location(city)
                forecasts = location.forecast()
                for i in range(0,2):
                    talkToMe('On %s it will be %s. The maximum temperture will be %.1f degree.'
                             'The lowest temperature will be %.1f degrees.' % (forecasts[i].date(), forecasts[i].text(), (int(forecasts[i].high())-32)/1.8, (int(forecasts[i].low())-32)/1.8))
        elif 'search' in command:
            reg_ex = search('search (.*)',command)
            keyword = reg_ex.group(1)
            url = 'https://www.google.com/search?q=' + keyword
            webbrowser.open(url)
            talkToMe('Here are the results!')
            print('Here are the results!')
        elif 'bye' in command:
            bye = ["See you soon!","Ok Bye","Well then, come back soon","iam gonna miss you","byeee","ok Bye, see ya"]
            talkToMe(bye[int(random()*10)%len(bye)])
        else:
            emsg = ["Sorry I cant do that for You!","oops . Not possible","Well then, I tried my best","I feel sorry for you"]
            talkToMe(emsg[int(random()*10)%len(emsg)])
    except:
        talkToMe("Sorry,Im not in the cloud!")

if(sys.argv[1] != 'null'):
    cmd = ""
    for i in range(len(sys.argv)):
        cmd+=str(sys.argv[i]) + " "
    cmd = cmd.replace(sys.argv[0],"")
    assistant(cmd)
else:
    myCommand()
