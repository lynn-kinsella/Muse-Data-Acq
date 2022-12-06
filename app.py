import socket
from tkinter import *
from state_enums import *
from random import randint
from Pages.utils import mount_page
from Pages.landing_page import get_landing_page


if __name__ == "__main__":

    state = {
        "recording_session": {
            "user":"",
            "state": recording_state(randint(1,2)),
            "count": 0,
            "active": False,
        },
        "render_state": render_state.USER_ENTER,
        "rendered_components": [],
        "ip":"",
        "window":None,
        "afters": {
            "finish_prompt": None,
            "update_timer": None,
            "check_collection": None
        },
        "osc_server": None,
    }
    
    state["ip"] = socket.gethostbyname_ex(socket.gethostname())[-1][-1]

    window = Tk()
    state["window"] = window
    w, h = window.winfo_screenwidth(), window.winfo_screenheight()
    window.attributes("-fullscreen", True)
    mount_page(state, get_landing_page(state))

    window.mainloop()

    