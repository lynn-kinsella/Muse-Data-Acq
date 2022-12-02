"""
Mind Monitor - Minimal EEG OSC Receiver
Coded: James Clutterbuck (2021)
Requires: pip install python-osc
"""
from datetime import datetime
import time
from pythonosc import dispatcher
from pythonosc import osc_server
import random

import sys

global results_buffer
results_buffer = []
dateTimeObj_start = datetime.now()
label_time = (int)(time.mktime(dateTimeObj_start.timetuple()))

ip = "0.0.0.0"
port = 5000

open_time = datetime.now()

def serve_forever():
    global results_buffer

    dateTimeObj = datetime.now()
    printStr = dateTimeObj.strftime("%Y-%m-%d %H:%M:%S.%f")
    args = range(0,4)
    if len(args) == 4: 
        for arg in args:
            printStr += ", "+str(random.randint(0,1))
        results_buffer.append(printStr)
        if len(results_buffer) >= 6:
            results_to_write = "\n".join(results_buffer)
            results_buffer = []
            with open("./data/"+sys.argv[1] + "/" + sys.argv[2]+ "_" +str(label_time)+".mock", "a") as myfile:
                myfile.write(results_to_write+"\n")
    if (dateTimeObj-open_time).total_seconds() >= 15:
        exit()


    
if __name__ == "__main__":
    
    print("Listening on UDP port "+str(port))
    while(True):
        time.sleep(random.expovariate(200))
        serve_forever()
