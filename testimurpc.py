import time
import rpcservices
def vec32short(x):
    return ['%.2f' % y for y in x]

while True:
    t=time.time()
#    print("imu:",rpcservices.getimudata())
#    print("pos:",rpcservices.getimupos())
    poses=rpcservices.getimupos()
    s=", ".join([*vec32short(poses[0]),*vec32short(poses[1]),*vec32short(poses[2])])
    print("pos:",s.replace("'",""))
#    print("leg:",rpcservices.leg_pos())
    t1=time.time()
    tts=0.1-(t1-t)
#    print(t, t1, tts)
    if tts>0:
        time.sleep(tts)