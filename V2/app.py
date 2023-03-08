import socket
from tkinter import *
from segment import *
from collection import *
from multiprocessing import Manager

def main():
    state = {
        "recording_session": {
            "user":"",
            "state": Manager().Value('state', Segment.Label.AMBIGUOUS.value),
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

    collection = Collection.join(LandingSegment(state),
                                 IntroSegment(state),
                                 StartOSCSegment(state),
                                 #ContinuousVideoSessionCollection(state=state, media='media/New_York/New_York_000.mp4'),
                                 ContinuousVideoSessionCollection(state=state, media='../../Training Footage/Faster/go_left_medium.mp4'),
                                 BreakCollection(state, 60*3),
                                 ContinuousVideoSessionCollection(state=state, media='../../Training Footage/Faster/go_left_medium.mp4'),
                                 EndOSCSegment(state),
                                 DoneSegment(state))

    collection.play()


    try:
        window.mainloop()
    except KeyboardInterrupt:
        window.destroy()

if __name__ == "__main__":
    main()
