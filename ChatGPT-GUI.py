from tkinter import *
from tkinter import ttk
import sounddevice as sd
from scipy.io.wavfile import write
import threading
########################
from thonburian2text import transcribe_text
from groq_talk import groq_chat
from gtts import gTTS
from playsound import playsound
import time
import random
# import vlc

def ChatGPTAPI():
    text = transcribe_text("output-gui.wav")
    print(text)
    groq_res = groq_chat(text)
    print(groq_res)
    text = str(groq_res)
    text = text.split('=')[1].split('comments')[0]

    tts=gTTS(text =text, lang='th')
    filename = str(random.randint(1,1000000))
    name = '{}.mp3'.format(filename)
    tts.save(name)
    time.sleep(1)
    playsound(name)
    return text


# def RunChatGPTAPI():
#     task = threading.Thread(target=ChatGPTAPI)
#     task.start()


########################

# media = vlc.MediaPlayer('googlespeak.wav')
# media.play()



fs = 44100 # sampling rate
seconds = 5
sd.default.device = 1


GUI = Tk()
GUI.geometry('500x500')
GUI.title('ChatGPT Assistant')

global check
check = True

result = StringVar()
result.set('กดปุ่ม Record เพื่ออัดเสียง')
L = ttk.Label(textvariable=result, font=('Angsana New',20))
L.pack(pady=20)

def Record():
    # global check
    # while check:
    result.set('record...')
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write('output-gui.wav', fs, myrecording)
    print('running..')
    time.sleep(1)
    t = ChatGPTAPI()
    result.set(t)


def start_record():
    task = threading.Thread(target=Record)
    task.start()

B1 = ttk.Button(GUI,text='Record',command=start_record)
B1.pack()

def Stop():
    global check
    check = False
    print('---------STOP----------')

GUI.mainloop()




'''
import sounddevice as sd
from scipy.io.wavfile import write
select = sd.query_devices()
fs = 44100 # sampling rate
seconds = 5
sd.default.device = 1
myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
sd.wait()
write('output4.wav', fs, myrecording)
'''