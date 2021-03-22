# each python code that can run starts command of the format rover= Rover(camera='R',legs='W',time=30)
# means - want to get a rover object and i need rights of R for camera and W of legs. and i want 30 minutes. this information is put in a common table.
# each bot has a different model which is served locally for example, for spiderPI it includes camera, servos, legs and gaits. also "move". so:
# the call to Rover gives you a submodel of this model, the part you have access to.
# the command rover.leg1.tipto((x,y,z)). will check if leg1 is part of the model and if you have the right to do "tipto()" and if yes, move the tip of the leg to that position. same with command rover.move(20,22)
# video stream (when we decide how to do, maybe twitch?) will also be such a resource, which disconnects when the time allocated is done.
# you can also have complex rights like maximum power, maximum speed of a particular servo, etc. so not only RW

# Output is in log file put on discord
# You also get a command to send back messages


# communication. we will have a text-type channel between anything (also rovers) and rovers. one example can be to have a flask server on vultr and use webhook to communicate. resulting IP may be used for direct communication maybe.

#need also a function that knows what bot is capable of. also via database. can be used as a limit on capabilities - for example, it prevents you from going past an angle or getting permission past an angle. maybe we need to ask for commands to have "max" rather than a number. user should be able to give a fallback value as well as a desired number. fallback can be "max" or "best". maybe we even have flex mode where we say how much we want to get it (try, force, etc.)
#will need watchdog that tracks if bot meets ability. maye also rover model can "complain" it did not get what it wanted. example: maximum speed. and/or maybe we have a self test mode of some kind (a gym).

#watchdog: 1. has modules that can check stuff, like range using ULS, position using INS
#2. and can have various abilities, like block commands, allow only some, force rewind. etc.

Class Rover:
    pass