import os
from flask import Flask, request

app = Flask(__name__)
listofrag=os.listdir("/home/pi/SpiderPi/ActionGroups")
listofrag=[f[:-4] for f in listofrag if f[-4:] in [".csv",".d6a"]]
listofrag=list(set(listofrag))

@app.route('/')
def index():
    global listofrag
    buts=[ragbutton(f,1) for f in listofrag] 
    return " ".join(buts)
@app.route('/dorag')
def dorag():
    name=request.args.get('name')
    rep=request.args.get('repeat',default=1,type=int)
    return "i would run a rag command here:rag {0} {1}".format(name,rep)

def ragbutton(s,rep):
    return '''<button onclick="window.location.href='/dorag?name={0}&repeat={1}'">{0}</button>'''.format(s,rep) #later change to a form or something so we can also read the repeats setting. or simply reserve the page

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')