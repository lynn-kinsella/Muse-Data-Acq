from state_enums import *
import subprocess

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


def start_sample(state):
    print("Starting sample collection")
    state["recording_session"]["active"] = True
    data_label = str(state["recording_session"]["state"]).split(".")[1]
    state['osc_server'] = subprocess.Popen(['python','osc_server.py', data_label, state["recording_session"]["user"], str(get_sample_period())])
    # state['osc_server'] = subprocess.Popen(['python','mock_osc_server.py', data_label, state["recording_session"]["user"]], get_sample_period())


def end_sample(state, refresh_function):
    print("Completed sample collection")
    state["recording_session"]["active"] = False
    state['osc_server'].kill()  
    state['osc_server'] = None

    refresh_function(state)

def get_sample_period():
    return 10000

def get_sample_count():
    return 5