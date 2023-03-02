import socket
from tkinter import *
#from state_enums import *
from utils import mount_page
from segment import *

def main():
    state = {
        "recording_session": {
            "user":"",
            "state": 0,
            "count": 0,
            "session_count": 0,
            "total_sessions": 2,
            "active": False,
        },
        "render_state": 0,
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

    ready_screen = PlaceHeadsetSegment(state)
    countdown_screen = CountdownSegment(state, 4)
    vid_screen = VideoSegment('../Pages/GO.mp4', 1, state, 4, 2)
    vid_screen_2 = VideoSegment('../Pages/GO.mp4', 1, state, 4, 2)
    remove_screen = RemoveHeadsetSegment(state)
    rest_screen = RestSegment(state, 4, 2)

    ready_screen.next_segment = countdown_screen
    countdown_screen.next_segment = vid_screen
    vid_screen.next_segment = vid_screen_2
    vid_screen_2.next_segment = remove_screen
    remove_screen.next_segment = rest_screen

    ready_screen.mount_segment()

    try:
        window.mainloop()
    except KeyboardInterrupt:
        window.destroy()

if __name__ == "__main__":
    main()
