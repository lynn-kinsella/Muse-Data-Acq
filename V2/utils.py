from datetime import datetime
from os import path
import time
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


