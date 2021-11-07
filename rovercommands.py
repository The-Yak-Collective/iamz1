import subprocess
import time,datetime
import os,io
import re
import shutil
import sys
import asyncio

from dotenv import load_dotenv, find_dotenv

ourdir=os.path.dirname(os.path.abspath(__file__))
load_dotenv(find_dotenv()) #'.env')
USERHOMEDIR=os.getenv('USERHOMEDIR',default="/media/pi/z1-drive/") 
WHEREIRUNDIR=os.getenv('WHEREIRUNDIR',default="/media/pi/z1-drive/maier/iamz1/") 
TWITTERHOMEDIR=os.getenv('TWITTERHOMEDIR',default="/media/pi/z1-drive/maier/twit/Rover-Twitter/") 
#PREAMBLE=os.getenv('YAK_ROVER_NAME') #happens in discord file

tweet_outcome=False
auto_unload=False
make_clip=False
logging_object=None

shutil.copy(WHEREIRUNDIR+'onroverdb_template',WHEREIRUNDIR+'onroverdb')



def dotest(who):
    s='this is a test response from z1 rover bot who got a message from '+who
    return s
    

def docmdupload(thefilename,ioobj): 
    ioobj.seek(0)
    with open(WHEREIRUNDIR+"/cmd/"+thefilename,'wb') as f:
        f.write(ioobj.getbuffer())
    s="uploaded file "+thefilename
    return s

def docmdlist():
    thedir=WHEREIRUNDIR+'cmd'
    f=os.listdir(thedir)
    ff=[x for x in f if x[-3:]=='.py']
    s="list of python files in cmd directory:\n"+"\n".join(ff)
    return s

def docmdrun(aname,name,*args):
    s='i am running  file {0} in home directory, ({3}) with parameters {2}, for user {1}'.format(name,aname," ".join(args),WHEREIRUNDIR)
#check there is a file and directory. if not say "oops"
    thefiletorun=WHEREIRUNDIR+'cmd/'+name
    if not os.path.exists(thefiletorun):
        print('oops no such file: '+thefiletorun)
        s='oops no such file: '+thefiletorun
        return s
#call script that runs file, etc into a text file
#send back message with pid, for killing
#script will send back the output file by curl
    sys.path.append(WHEREIRUNDIR) #not clear if this is needed
    #sys.path.append('/home/pi/SpiderPi/HiwonderSDK') #this should not be here
    thestringlist=["/bin/bash",WHEREIRUNDIR+"runcommand.bash","runpython3.bash",thefiletorun]+list(args)
    print(thestringlist)
    out = subprocess.Popen(thestringlist, 
           cwd=WHEREIRUNDIR,
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    s=s+ '\n'+str(thestringlist)+'\n'+str(stdout,"utf-8").replace("\\n",'\n')
    return s

def doraglist():
    out = subprocess.Popen(['/usr/bin/python3', 'raglist.py'],
           cwd=WHEREIRUNDIR,
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    s='available action groups:\n'+str(stdout,"utf-8").replace("\\n",'\n')
    return s

def dostop():
    out = subprocess.Popen(['/bin/bash', "killrag.bash"],
           cwd=WHEREIRUNDIR,
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    #stdout,stderr = out.communicate()
    #s1='did i stop (freeze more like it)?'+str(stdout,"utf-8").replace("\\n",'\n')
    
    out1 = subprocess.Popen(['/bin/bash', "killcam.bash"],
           cwd=WHEREIRUNDIR,
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    #stdout,stderr = out.communicate()
    #s2=s1+'\n'+str(stdout,"utf-8").replace("\\n",'\n')
    s="did i stop/freeze all?"
    return s

def dotherag(name,*args):
    s="output problem"
    global make_clip
    if make_clip:
        do_make_clip()
    out = subprocess.Popen(['/usr/bin/python3', 'rag.py', name]+list(args),
           cwd=WHEREIRUNDIR,
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    try:
        stdout,stderr = out.communicate(timeout=2)
        s=str(stdout,"utf-8").replace("\\n",'\n')
    except subprocess.TimeoutExpired:
        pass
    if name != "list" and tweet_outcome:
        do_tweet_outcome("rag "+name+' '+" ".join(list(args)))
    if auto_unload:
        do_unload() #should be by new function
    return s

def dotheseq(name,*args):
    s="output problem"
    global make_clip
    if make_clip:
        do_make_clip()

    out = subprocess.Popen(['/usr/bin/python3', 'seq.py', name]+list(args),
           cwd=WHEREIRUNDIR,
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    try:
        stdout,stderr = out.communicate(timeout=10)#longer timeout as sequnce
        s=str(stdout,"utf-8").replace("\\n",'\n')
    except subprocess.TimeoutExpired:
        pass
    if name != "list" and tweet_outcome: #no support for seq list command, yet
        do_tweet_outcome("seq "+name+' '+" ".join(list(args)))

    if auto_unload:
        do_unload()
    return s

def dothecam(*args):
    s="comm problems"
    out = subprocess.Popen(['/usr/bin/python3', 'cam.py']+list(args),
           cwd=WHEREIRUNDIR,
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    try:
        stdout,stderr = out.communicate(timeout=2)
        s=str(stdout,"utf-8").replace("\\n",'\n')

    except subprocess.TimeoutExpired:
        pass
    return s

def dotheunload():
    do_unload()
    s='ah. feeling unloaded'
    return s

def dorun(aname,name,*args):
    s='i am running  file {0} in directory of {1} ({3}) with parameters {2}'.format(name,aname," ".join(args),name2filename(aname))
#check there is a file and directory. if not say "oops"
    thefiletorun=USERHOMEDIR+name2filename(aname)+'/'+name
    if not os.path.exists(thefiletorun):
        print('oops no such file: '+thefiletorun)
        s='oops no such file: '+thefiletorun
        return
#call script that runs file, etc into a text file
#send back message with pid, for killing
#script will send back the output file by curl
    thestringlist=["/bin/bash",WHEREIRUNDIR+"runcommand.bash",thefiletorun]+list(args)
    print(thestringlist)
    out = subprocess.Popen(thestringlist, 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    s=s+ '\n'+str(thestringlist)+'\n'+str(stdout,"utf-8").replace("\\n",'\n')
    return s

def dovideo(onoff,*arg):
    if len(arg)>0:
        dur=arg[0]
    else:
        dur="300"
    if (onoff=='off'):
        subprocess.call(['/bin/bash', 'stopvideo'],cwd=WHEREIRUNDIR)
        s='tried to turn off video using kill (stopvideo). if video was not running, effect on system stability unpredictable'
    else:
        subprocess.call(['/bin/bash', 'streamviatwilio', dur],cwd=WHEREIRUNDIR)
        s="tried to start video. unpredictible reults if last run not over yet. see video using 'runonviewer.html'."
    return s

def dotweetonoff(onoff):
    global tweet_outcome
    if (onoff=='off'):
        tweet_outcome=False
    else:
        tweet_outcome=True
    s="tweet onoff status is now {}". format(str(tweet_outcome))
    return s

def dounloadonoff(onoff):
    global auto_unload
    if (onoff=='off'):
        auto_unload=False
    else:
        auto_unload=True
    s="auto unload onoff status is now {}". format(str(auto_unload))
    return s

def dologonoff(onoff):
    global logging_object
    thedir=os.getenv('LOGDIR',None)
    if (onoff=='off'):
        if not thedir:
            s="logging was not on."
            return s
        logging_object.terminate()
        s="logging at {} now stopped.". format(str(thedir))
    elif (onoff=='on'):
        PARENTLOGDIR=os.getenv('PARENTLOGDIR','/home/pi/gdrive/logs/')
        thedir=str(int(time.time()))
        os.mkdir(PARENTLOGDIR+thedir)
        thedir=PARENTLOGDIR+thedir+"/"
        os.environ['LOGDIR']=thedir
        with open (thedir+"logoflogmaker",'w') as fn:
            logging_object = subprocess.Popen(['/usr/bin/python3', 'logmaker.py'], 
               cwd=WHEREIRUNDIR,
               #stdout=subprocess.PIPE, 
               #stderr=subprocess.STDOUT, 
               stdout=fn,
               stderr=fn,
               env={**os.environ})
        s="logging is now on at {}".format(str(thedir))
        if False: #for debugging
            stdout,stderr = logging_object.communicate() #this is blocking so only for debugging
            if not stdout:
                stdout=b'no output'
            if not stderr:
                stderr=b'no output'

            s=s+str(stderr,"utf-8").replace("\\n",'\n')+'\n'+str(stdout,"utf-8").replace("\\n",'\n')
        return s
    s="usage: $log on/off to start/stop logging to a log directory"
    return s

def docliponoff(onoff): #use this format - messahe is returned by function, which doe snot need ctx itself. lets see if that works for all
    global make_clip
    if (onoff=='off'):
        make_clip=False
    else:
        make_clip=True
    s="make_clip onoff status is now {}". format(str(make_clip))
    return(s)

def do_unload():
    out = subprocess.Popen(['/usr/bin/python3', 'testunload.py'],
           cwd=WHEREIRUNDIR,
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()

def do_make_clip():
    out = subprocess.Popen(['/bin/bash', 'makeaclip.bash'],
       cwd=WHEREIRUNDIR,
       stdout=subprocess.PIPE, 
       stderr=subprocess.STDOUT)

def do_tweet_outcome(inresponseto):
    out = subprocess.Popen(['/usr/bin/python3', 'snap.py'],
       cwd=WHEREIRUNDIR,
       stdout=subprocess.PIPE, 
       stderr=subprocess.STDOUT)
    if not make_clip:
        out = subprocess.Popen(['/usr/bin/python3', TWITTERHOMEDIR+'tweetthis.py', "in response to {}".format(inresponseto),"a_snap.png"],
            cwd=WHEREIRUNDIR,
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
        print("should have tweeted a pic")
    else:
        #we need to wait for clip to be ready!
        s=['/usr/bin/python3', TWITTERHOMEDIR+'tweetthis.py', "in response to {}".format(inresponseto),"a_clip.mp4"]
        out = subprocess.Popen(s,
            cwd=WHEREIRUNDIR,
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
        make_clip=False #only one clip, for now
        print("did i tweet a_clip?"," ".join(s)) 
