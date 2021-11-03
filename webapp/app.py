import os
from flask import Flask

app = Flask(__name__)
listofrag=os.listdir("/home/pi/SpiderPi/ActionGroups")
listofrag=[f[:-4] for f in listofrag if f[-4:] in [".csv",".d6a"]]
listofrag=list(set(listofrag))

@app.route('/')
def index():
    global listofrag
    return " ".join(listofrag)
@app.route('/rag')
def dorag():
    return "i would run a rag command here"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')