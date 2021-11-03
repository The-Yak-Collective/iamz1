#note - it is blocking. maybe we can put it in a locked thread
import threading
thelock=threading.Lock()
import pyttsx3
engine=pyttsx3.init()
def saythis(s):
    global engine
    engine.say(s)
    thelock.acquire()
    x=threading.Thread(target=runit)
    x.start()


def runit():
    engine.runAndWait()
    thelock.release()