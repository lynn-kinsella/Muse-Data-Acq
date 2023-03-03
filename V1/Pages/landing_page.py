from tkinter import *
from Pages.recording_page_with_videoplayer import get_recording_in_progress
from state_enums import *
from Pages.utils import mount_page

# Callback function from the ready button on the info page
def start_session(state):
    mount_page(state, get_recording_in_progress(state))

# Info page components
def get_ready_prompt(state):
    ready_prompt_components = []
    
    title = Label(text="Muse OSC Interface", font=("Arial", 48))
    ip_info = Label(text="Set the Server IP in Mind Monitor to " + state["ip"], font=("Arial", 25))
    id_info = Label(text="Recording session for " + state["recording_session"]["user"], font=("Arial", 18))
    session_text ="""
    A recording session lasts 5 minutes, during which you will be asked to focus on the thought of either \"Stop\" or \"Go\". 
    Each prompt will last 15 seconds, with 15 seconds of break between prompts. Please configure your muse headset and 
    Mind Monitor app and click ready to begin when you are ready."""
    session_info =  Label(text=session_text, justify=LEFT, font=("Arial", 18))

    ready_button = Button(command = lambda: start_session(state), text="Ready", font=("Arial", 48))

    ready_prompt_components.append((title, {"pady": 5}))
    ready_prompt_components.append(ip_info)
    ready_prompt_components.append((id_info, {"pady": 5}))
    ready_prompt_components.append(session_info)
    ready_prompt_components.append((ready_button, {"pady": 10}))
    
    return ready_prompt_components

# Callback function from the submit button on the landing page
def submit_user (state, user_id):
    ## TODO: validate user id
    state["recording_session"]["user"] = user_id
    state["render_state"] = render_state.READY_PROMPT
    mount_page(state, get_ready_prompt(state))

# Landing page components
def get_landing_page(state):
    user_enter_components = []

    title = Label(text="Muse OSC Interface", font=("Arial", 48))
    ip_info = Label(text="Set the Server IP in Mind Monitor to " + state["ip"], font=("Arial", 25))
    id_prompt = Label(text="Enter subject id for session  ", font=("Arial", 18))
    id_entry = Entry(font=("Arial", 18))
    id_submit = Button(command = lambda: submit_user(state, id_entry.get()), text="Submit")

    user_enter_components.append((title, {"pady": 5}))
    user_enter_components.append(ip_info)
    user_enter_components.append(id_prompt)
    user_enter_components.append((id_entry, {"pady": 5}))
    user_enter_components.append(id_submit)
    return user_enter_components