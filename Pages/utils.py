from state_enums import *
import subprocess


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
    print("Starting sample collection")
    state["recording_session"]["active"] = True
    data_label = str(state["recording_session"]["state"]).split(".")[1]
    state['osc_server'] = subprocess.Popen(['python','osc_server.py', data_label, state["recording_session"]["user"], str(get_sample_period())])
    # state['osc_server'] = subprocess.Popen(['python','mock_osc_server.py', data_label, state["recording_session"]["user"]], get_sample_period())


# Close osc server 
def end_sample(state, refresh_function):
    print("Completed sample collection")
    state["recording_session"]["active"] = False
    state['osc_server'].kill()  
    state['osc_server'] = None

    refresh_function(state)


# Time which a user will focus on a command for 
def get_sample_period():
    return 15000

# Amount of samples to collect
def get_sample_count():
    return 10

# ^ Reccomended 15000/10 for a 5 minute session