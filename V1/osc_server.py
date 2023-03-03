"""
Mind Monitor - Minimal EEG OSC Receiver
Coded: James Clutterbuck (2021)
Requires: pip install python-osc
"""
from datetime import datetime
import sys
import time
from pythonosc import dispatcher
from pythonosc import osc_server
from os import path

dateTimeObj_start = datetime.now()
ip = "0.0.0.0"
port = 5000

global results_buffer
results_buffer = []


def eeg_handler(address: str,*args):
    global results_buffer
    dateTimeObj = datetime.now()
    timestamp = time.time_ns() 
    printStr = str(timestamp)
    printStr = dateTimeObj.strftime("%Y-%m-%d %H:%M:%S.%f")
    data_path ="./data/"+sys.argv[1] + "/" + sys.argv[2]+ "_" +sys.argv[4]+".csv"
    if(not path.exists(data_path)):
        print("First packet recieved at " + (str)((int)(time.mktime(dateTimeObj.timetuple()))))
        for arg in args:
            printStr += ", "+str(arg)
        with open(data_path, "a") as myfile:
            myfile.write(printStr+"\n")
        print("First packet written at " + (str)((int)(time.mktime(datetime.now().timetuple()))))
    else:
        if len(args) == 4: 
            for arg in args:
                printStr += ", "+str(arg)
            results_buffer.append(printStr)
            if len(results_buffer) >= 100:
                results_to_write = "\n".join(results_buffer)
                results_buffer = []
                with open(data_path, "a") as myfile:
                    myfile.write(results_to_write+"\n")
    
    if (dateTimeObj-dateTimeObj_start).total_seconds() >= int(sys.argv[3])/1000:
        results_to_write = "\n".join(results_buffer)
        results_buffer = []
        with open(data_path, "a") as myfile:
            myfile.write(results_to_write+"\n")
        print("timeout")
        sys.exit("Successful timeout, closing server")
if __name__ == "__main__":
    open_time = datetime.now()
    print((int)(time.mktime(open_time.timetuple())))
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/muse/eeg", eeg_handler)

    # server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    server = osc_server.BlockingOSCUDPServer((ip, port), dispatcher)
    print("Listening on UDP port "+str(port))
    server.serve_forever()
