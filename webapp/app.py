#very primitive setup just to see it works. next step is to extract the rag, etc. commands from iamz1 and turn them into a stand-alone library. or better, a service

import os
from flask import Flask, request, redirect
import subprocess

app = Flask(__name__)
listofrag=os.listdir("/home/pi/SpiderPi/ActionGroups")
listofrag=[f[:-4] for f in listofrag if f[-4:] in [".csv",".d6a"]]
listofrag=list(set(listofrag))
listofrag.sort()
WHEREIRUNDIR="/home/pi/test/iamz1/"
reps=1

@app.route('/')
def index():
    global listofrag, reps
    buts=[ragbutton(f,reps) for f in listofrag]+unloadbut()+repbuts()
    return " ".join(buts)
    
@app.route('/dorag')
def dorag():
    global reps
    name=request.args.get('name')
    #rep=request.args.get('repeat',default=1,type=int)
    subprocess.Popen(['/usr/bin/python3', 'rag.py', name]+[str(reps)],
           cwd=WHEREIRUNDIR,
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    return redirect("/")
    return "i would run a rag command here:rag {0} {1}".format(name,rep)

@app.route('/unload')
def dounload():
    subprocess.Popen(['/usr/bin/python3', 'testunload.py'],
           cwd=WHEREIRUNDIR,
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    return redirect("/")

@app.route('/setrep')
def dosetrep():
    global reps
    value=request.args.get('value', type=int)
    reps=value
    return redirect("/")

def repbuts():
    s=[]
    global reps
    for i in [1,2,5,10]:
        q="*" if reps==i else ""
        s.append('''<button onclick="window.location.href='/setrep?value={0}'">{1}{0}</button>'''.format(i,q))
    return s
    
def ragbutton(s,rep):
    return '''<button onclick="window.location.href='/dorag?name={0}&repeat={1}'">{0}</button>'''.format(s,rep) #later change to a form or something so we can also read the repeats setting. or simply reserve the page
    
def unloadbut():
    return '''<button onclick="window.location.href='/unload'">unload</button>'''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')