from datetime import datetime
from os import path
import time
from state_enums import *
import subprocess
import tkinter as tk


# Load the desired components and unload the components that are currently on screen
def mount_page(state, new_components):
    if len(state["rendered_components"]) != 0:
        for component in state["rendered_components"]:
            if type(component) == tuple:
                component[0].pack_forget()
            else:
                component.pack_forget()
    for component in new_components:
        if type(component) == tuple:
            component[0].pack(**component[1])
        else: 
            component.pack()
    state["rendered_components"] = new_components


# Open osc server 
def start_sample(state):
    state["recording_session"]["active"] = True
    data_label = str(state["recording_session"]["state"]).split(".")[1]
    timestamp = (int)(time.mktime(datetime.now().timetuple()))
    state["recording_session"]["timestamp"] = str(timestamp)
    timeout_counter = 0
    print("Starting sample collection for " + str(timestamp))
    while(state['osc_server'] != None and state['osc_server'].poll() == None):
        time.sleep(0.002)
        timeout_counter += 1
        if timeout_counter > 1000:
            state['osc_server'].kill()
            break
    state['osc_server'] = subprocess.Popen(['python','osc_server.py', data_label, state["recording_session"]["user"], str(get_sample_period()), str(timestamp)])
    # state['osc_server'] = subprocess.Popen(['python','mock_osc_server.py', data_label, state["recording_session"]["user"]], get_sample_period())


# Close osc server 
def end_sample(state, refresh_function):
    print("Completed sample collection")
    state["recording_session"]["active"] = False

    refresh_function(state)

# Check if recieving data from mindmonitor
def check_data_path_exists(state, refresh_function):
    data_path = "./data/"
    data_path += str(state["recording_session"]["state"]).split(".")[1] + "/"
    data_path += state["recording_session"]["user"] + "_"
    data_path += state["recording_session"]["timestamp"] + ".csv"
    print("Check for existance of " + data_path)
    if not path.exists(data_path):
        if state['osc_server'] != None:
            state['osc_server'].kill()
            state['osc_server'] = None
        state["recording_session"]["state"] = recording_state.ERROR
        end_sample(state, refresh_function)


# Time whioch a user will focus on a command for 
def get_sample_period():
    return 15000

# Amount of samples to collect
def get_sample_count():
    return 10

# ^ Reccomended 15000/10 for a 5 minute session