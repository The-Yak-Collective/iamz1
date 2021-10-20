#get a filename. convert it into one or more error files (if it has a split argument) and make an image for each one.
#usage feedbacktoerror sourcefile targetdirectory [lots]
import subprocess
import sys
import math
import os

sourcefile=sys.argv[1]
targetdirectory=sys.argv[2]
if not os.path.exists(targetdirectory):
    os.mkdir(targetdirectory)
elif os.path.isfile(targetdirectory):
    print("directory please, not file:",targetdirectory)

lots=False
sumerror=[0]*18

if len(sys.argv)>3 and sys.argv[3]=='lots':
    lots=True
with open(sourcefile) as fin:
    lines=fin.readlines()
for idx,i in enumerate(range(int(len(lines)/3))):
    #print(lines[i*3])
    tmp=lines[i*3].split(':')
    shouldbe=tmp[len(tmp)-1].split()[1:] 
    tmp=lines[i*3+1].split(':')
    measured=tmp[len(tmp)-1].split()[1:]
    error=[]
    for j in zip(shouldbe,measured):
        error.append(int(((int(j[0])-int(j[1]))**2.0)*255/3000))
    if lots:
        subprocess.run(['python3', 'showerr.py',targetdirectory+sourcefile.split('.')[0]+str(idx)+'.jpg'], input=" ".join(map(str,error)),universal_newlines=True)
    else:
        for idx,k in enumerate(error):
            #print(idx,k,error)
            sumerror[idx]=sumerror[idx]+k
    #print (error,sumerror)
if not lots:
    #print(sumerror)
    for idx,k in enumerate(sumerror):
        sumerror[idx]=int(sumerror[idx]/(len(lines)/3))
    subprocess.run(['python3', 'showerr.py',targetdirectory+sourcefile.split('.')[0]+'sum'+'.jpg'], input=" ".join(map(str,sumerror)),universal_newlines=True)
    #print(sumerror)

