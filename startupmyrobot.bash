#! /bin/bash
#this script starts up all the various functions of the rover, including self-test. basically - BOS (Bos Operating System)
#now drafted in the form of one script, but for modularity reasons, some parts should be in seperate files (to make them easy to re-run)

#open question - hwo do we define preparedness of rover. on the one hand, there is a minimum. on teh other, if something doe snot work, that si simply a new configuration

#need env variables?
#source ....

#start basic services

    #start motor service(s) (rag)
    
    #start sensor service(s) (cam)
    
    #start logger service
    
    #start other basic h/w interfacing stuff
    
    #start safety lock to prevent movement

#start communication connectivity
    #check re internet connection - wifi, etc. 
    
    ##what if we fail? lets say there is a background check every X seconds. and when it works, it redoes this section, so section shoudl be in its own file
    HAVEINT=true

#start secondary s/w components

    #not clear which ones, yet
    
    #start human interface (speech = {mic, spkr}, lights, etc.)
    
    #start blockchain node
    
    #start continuous-learning module
    
    #start continuous discover module - a layer which translates component protocol into a protocol which can be used immediately (any command does something) and has small steps towards greater use
    
#start self-configuration. testinga nd reconfiguring can be mission specific. how to do?

    #identify components (how do we make architecture discoverable) and self name
    #for each component run its own self-check
    #additional self checks, as defined. esp. for combinations of components (e.g., leg, coordination, etc)

    #test actuators by moving, a tiny bit
    #test/configure inert parts, using other sensors on rover

#check integrity - using blockchain here could be interesting
    #check checksums
    #check s/w components exist
    #security
    #malicious code (what is that beyond viruses? maybe that commands do what you expect and so do sensors?)
    #autonomy (not clear how you check the integrety of this. and can it be done this stage of process)
    
#do the configuration
    #reconfigure based on results - should drivers be like in s/w or are robotic drivers more complex or more integrated into s/w or BOS than standard OS drivers?
    #build self model - format and contenst not clear yet,  - is it just uploading a library? how do we reconfigure other s/w to match model?

    
    
    
#start higher behavioral components

    #start "i have rhythm"
    
    #start "location sense"
    
    #start "posture sense"
    
#start "enviroment sensing"
    
#evaluate physical safty 
    #check power level (voltage as a proxy for power levels)
    #check environment ("weather")
    #bootstrap situation construction
    #check posture
    #check posture/location risk = am i about to fall off the table
    #check for (and handle) alerts


    
#now start doing things

    #check social network (who is up, etc.)
    #sync blockchain
    #look for orientation landmarks, including ones set before "off"
    #generate position estimate (exact or generalized info about)
    #local whereami - clearence within reach
    #release safety lock
    
    
#start command stuff
    #check for ongoing mission
    
        #mission specific checkup
    #check for incoming messages
    #integrate inputs and decide on priorities

#start accepting commands only if $HAVEINT is true. or something and only after everything works
    if $HAVEINT ; then
    #start connection to base station, other remote monitor controller

    #start pagekite

    #start webserver 
    
    #start discord client
    
    #start "social sense"
    
    fi

#all (or enough) is working. so release rover

    if $MINWORKS; then
    #start "what do i do now script"
    fi 
    #what do we do if not?
    