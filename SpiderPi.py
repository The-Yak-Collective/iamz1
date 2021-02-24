# each python code that can run starts command of the format rover= Rover(camera='R',legs='W',time=30)
# means - want to get a rover object and i need rights of R for camera and W of legs. and i want 30 minutes. this information is put in a common table.
# each bot has a different model which si served locallyt for example, for spiderPI it includes camera, servos, legs and gaits. so:
# the call to Rover gives you a submodel of this model, the part you have access to.
# the command rover.leg1.tipto((x,y,z)). will check if leg1 is part of the model and if you have the right to do "tipto()" and if yes, move the tip of the leg to that position.
# video stream (when we decide how to do, maybe twitch?) will also be such a resource, which disconnects when the time allocated is done.
# you can also have complex rights like maximum power, maximum speed of a particular serveo, etc. so not only RW

# Output is in log file put on discord
# You also get a command to send back messages


# communication. we will have a text-type channel between anything (also rovers) and rovers. one example can be to have a flask server on vultr and use webhook to communicate. resulting IP may be used for direct communication maybe.

Class Rover:
    pass