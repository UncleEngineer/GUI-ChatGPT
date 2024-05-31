from tkinter import *
from tkinter import ttk
#########################
import sounddevice as sd
from scipy.io.wavfile import write
import time
import threading
from thonburian2text import transcribe_text
from groq_talk import groq_chat
from gtts import gTTS
from playsound import playsound

fs = 44100

sd.default.device = 1
# print(sd.query_devices())

GUI = Tk()
GUI.geometry('600x600')
GUI.title('UNCLE AI by Loong')

v_result = StringVar()
v_result.set('กรุณากดปุ่ม Speak ด้านล่างนี้')

T = ttk.Label(GUI,textvariable=v_result ,font=('Angsana New',30))
T.pack(pady=40)

button_img = PhotoImage(file='mic.png')

def setresult():
    v_result.set('กำลังบันทึกเสียง. . .')

def settext():
    task = threading.Thread(target=setresult)
    task.start()

def soundrecord():
    seconds = 7
    print('Start recording...')
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write('output-record.wav',fs,recording)
    print('Stop Recording!')
    v_result.set('กรุณารอสักครู่...')
    time.sleep(2)


def SpeechToText():
    text = transcribe_text('output-record.wav')
    return text

def Groq_API():
    text = SpeechToText() # sound to text / MIC -> Text
    groq_res = groq_chat(text)
    print('RESULT: ', groq_res)
    print([groq_res.text])

    tts = gTTS(groq_res.text, lang='th')
    import random
    filename = str(random.randint(1,1000000)) # 123413
    name = '{}.mp3'.format(filename)
    tts.save(name)
    time.sleep(1)
    playsound(name)



def Record():
    settext()

    task = threading.Thread(target=soundrecord)
    task.start()

    task = threading.Thread(target=Groq_API)
    task.start()
    

B = ttk.Button(GUI,text='Speak',image=button_img,compound='top',command=Record)
B.pack(ipadx=30,ipady=30)

GUI.mainloop()