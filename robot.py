import comminter
import time
import random

i=0
comm = comminter.commInter(1)
random.seed()

while 1:
    comm.sendMessage("T", '0' +str(int(random.random()*5+1)), "1")
    time.sleep(0.1)
    comm.sendMessage("T", '0' +str(int(random.random()*5+1)), "0")
    time.sleep(0.1)
    comm.sendMessage("A", '01', str(random.uniform(1, 5)))
    time.sleep(0.1)
    