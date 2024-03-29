import socket
from tkinter import *
from segment import *
from collection import *
from multiprocessing import Manager
import glob
import random

def main():
    state = {
        "recording_session": {
            "user":"",
            "state": Manager().Value('state', Segment.Label.AMBIGUOUS.value),
            "direction_state": Manager().Value('direction', Segment.Label.AMBIGUOUS.value),
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

    media = glob.glob('test_media/*')

    media_sample = random.sample(media, 2)

    collection = Collection.join(LandingSegment(state),
                                 IntroSegment(state),
                                 #StartOSCSegment(state),
                                 ContinuousVideoSessionCollection(state=state, media=media_sample[0]),
                                 BreakCollection(state, 60),
                                 ContinuousVideoSessionCollection(state=state, media=media_sample[1]),
                                 #EndOSCSegment(state),
                                 DoneSegment(state))

    collection.play()


    try:
        window.mainloop()
    except KeyboardInterrupt:
        window.destroy()

if __name__ == "__main__":
    main()
