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


def eeg_handler(address: str, fixed_args: list, *args):
    state = fixed_args[0]
    file = state['recording_session']['file']
    label = state['recording_session']['state']

    if not state['recording_session']['active']:
        sys.exit()

    global results_buffer
    dateTimeObj = datetime.now()
    timestamp = time.time_ns() 
    printStr = str(timestamp)
    if len(args) == 4: 
        printStr += ", " + str(label)
        for arg in args:
            printStr += ", "+str(arg)

        file.write(printStr+'\n')
