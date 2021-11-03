#very primitive setup just to see it works. next step is to extract the rag, etc. commands from iamz1 and turn them into a stand-alone library. or better, a service

import os
from flask import Flask, request, redirect

app = Flask(__name__)
listofrag=os.listdir("/home/pi/SpiderPi/ActionGroups")
listofrag=[f[:-4] for f in listofrag if f[-4:] in [".csv",".d6a"]]
listofrag=list(set(listofrag))
WHEREIRUNUNDER="/home/pi/test/iamz1/"

@app.route('/')
def index():
    global listofrag
    buts=[ragbutton(f,1) for f in listofrag] 
    return " ".join(buts)
@app.route('/dorag')
def dorag():
    name=request.args.get('name')
    rep=request.args.get('repeat',default=1,type=int)
    subprocess.Popen(['/usr/bin/python3', 'rag.py', name]+list(rep),
           cwd=WHEREIRUNDIR,
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    return redirect("/")
    return "i would run a rag command here:rag {0} {1}".format(name,rep)

def ragbutton(s,rep):
    return '''<button onclick="window.location.href='/dorag?name={0}&repeat={1}'">{0}</button>'''.format(s,rep) #later change to a form or something so we can also read the repeats setting. or simply reserve the page

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')