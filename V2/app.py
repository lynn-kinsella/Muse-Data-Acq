import socket
from tkinter import *
from segment import *
from collection import *


def main():
    state = {
        "recording_session": {
            "user":"",
            "state": 0,
            "count": 0,
            "session_count": 0,
            "total_sessions": 2,
            "active": False,
            "file": None
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

    session = StopGoVideoSessionCollection(state, 5, 2, 4)
    session2 = StopGoVideoSessionCollection(state, 5, 2, 4)

    break_session = BreakCollection(state, 60*3)

    collection = Collection.join(LandingSegment(state),
                                 IntroSegment(state),
                                 StartOSCSegment(state),
                                 CountdownSegment(state, 4),
                                 EndOSCSegment(state),
                                 DoneSegment(state))

    collection.play()


    try:
        window.mainloop()
    except KeyboardInterrupt:
        window.destroy()

if __name__ == "__main__":
    main()
