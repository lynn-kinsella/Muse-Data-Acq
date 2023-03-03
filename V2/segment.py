import log
import logging
import time
import copy
from enum import Enum
from utils import mount_page, load_video
from tkinter import *
from random import random
from tkVideoPlayer import TkinterVideo
import osc
from pythonosc import dispatcher, osc_server
import datetime
from time import sleep
import threading
from os import path

LOGGER = logging.getLogger('GUI')
log.configure_logger(LOGGER, 'training_gui.log')

class Segment(object):
    """
    Defines the primitive type of segment
    """
    class Label(Enum):
        REST = 0
        STOP = 1
        GO = 2
        DISCONNECTED = 3
        AMBIGUOUS = 4
    
    def __init__(self, label: Label, state: dict):
        """
        Constructor
        """
        self.label = label
        self.state = state
        self.next_segment = None
        self.components = []

    def __iter__(self):
        """
        Get a copy of all the segments in the collection
        """
        yield self

    def __len__(self):
        """
        Get length, just so it works well with collections
        """
        return 1

    def __getitem__(self, items):
        """
        Make it behave like a list
        """
        return [self].__getitem__(items)

    def play(self):
        """
        Another function for mounting the segment
        """
        self.mount_segment()

    def mount_segment(self):
        """
        Override function for mounting the segment
        """
        # Update the state label
        self.state['recording_session']['state'] = self.label.value

        # Exchange the components
        if len(self.state["rendered_components"]) != 0:
            for component in self.state["rendered_components"]:
                if type(component) == tuple:
                    component[0].destroy()
                else:
                    component.destroy()
        for component in self.components:
            if type(component) == tuple:
                component[0].pack(**component[1])
            else: 
                component.pack()
        self.state["rendered_components"] = self.components

    def mount_next_segment(self):
        """
        Mount the next segment in the linked list
        """
        if self.next_segment:
            self.next_segment.mount_segment()
        else:
            LOGGER.info("Reached the end of the segment chain")
            self.state['window'].destroy()
            return False

class StartOSCSegment(Segment):
    """
    Segment for starting the OSC server
    """
    ip = "0.0.0.0"
    port = 5000
    def __init__(self, state):
        """
        Constructor
        """
        timestamp = (int)(time.mktime(datetime.datetime.now().timetuple()))
        self.datapath = ""
        super().__init__(self.Label.AMBIGUOUS, state)


    def check_data_exists(self):
        if not path.exists(self.datapath):
            self.state['recording_session']['active'] = False
            self.server.server_close()
            segment = ErrorSegment(self.state)
            segment.mount_segment()
        else:
            self.mount_next_segment()

    
    def mount_segment(self):
        """
        Start the OSC server
        """
        self.state['recording_session']['active'] = True

        timestamp = (int)(time.mktime(datetime.datetime.now().timetuple()))
        self.datapath = self.state['recording_session']['user'] + '_' + str(timestamp) + '.csv'
        self.state['recording_session']['file'] = open(self.datapath, 'w')
        dispatch = dispatcher.Dispatcher()
        dispatch.map("/muse/eeg", osc.eeg_handler)
        self.server = osc_server.BlockingOSCUDPServer((self.ip, self.port), dispatcher)

        osc_thread = threading.Thread(target=self.server.serve_forever)
        osc_thread.daemon = True
        osc_thread.start()

        prompt = Label(text="Starting OSC Server...", font=("Arial", 40))
        self.components.append((prompt, {"pady": 50}))

        prompt.after(1000, self.check_data_exists)

        super().mount_segment()

class EndOSCSegment(Segment):
    """
    Segment for starting the OSC server
    """
    def __init__(self, state):
        """
        Constructor
        """
        super().__init__(self.Label.AMBIGUOUS, state)

    def mount_segment(self):
        """
        End the thread
        """
        self.state['recording_session']['active'] = False

        self.mount_next_segment()

class TimedSegment(Segment):
    """
    Defines a timed segment type, child of Segment
    """
    def __init__(self, label: Segment.Label, state: dict,
                 duration_avg: float, duration_range: float):
        self.duration_avg = duration_avg
        self.duration_range = duration_range
        super().__init__(label, state)

    def get_segment_period(self):
        """
        Generate the period of the segment based on the durations given in ms
        """ 
        return int(1000*self.duration_avg + random()*self.duration_range - self.duration_range/2)

    def update_countdown_timer(self, timer, time_ms, minutes=False):
        """
        Update the timer field passed in for the class
        """
        if minutes:
            timer.configure(text = time.strftime("%M:%S", time.gmtime(time_ms//1000)))
        else:
            timer.configure(text=int(time_ms//1000))

        if time_ms != 0:
            self.state["afters"]["timer_update"] = (timer.after(1000, lambda: self.update_countdown_timer(timer, time_ms - 1000, minutes)), timer)

    def mount_segment(self):
        """
        Mount the close after timer rule
        """
        self.state["afters"]["finish_prompt"] = (self.state['window'].after(self.get_segment_period(),
                                                      lambda: self.mount_next_segment()))
        super().mount_segment()

class VideoSegment(TimedSegment):
    """
    Defines a video type of segment for prediction training
    """
    def __init__(self, media: str, label: Segment.Label,
                 state: dict, duration_avg: float, duration_range: float):
        """
        Constructor
        """
        self.media_filepath = media

        super().__init__(label, state, duration_avg, duration_range)

    @staticmethod
    def load_video(file, state):
        vidplayer = TkinterVideo(master=state["window"], scaled=True, keep_aspect=True)
        vidplayer.load(file)
        return vidplayer

    def mount_segment(self):
        """
        Mount a segment GUI and record data
        """
        # Update the state label
        self.state['recording_session']['count'] += 1

        # Create the GUI
        vid = self.load_video(self.media_filepath, self.state)
        vid.play()

        # mount the page
        self.components.append((vid, {"expand":True,
                                       "fill":"both"}))

        super().mount_segment()

class RestSegment(TimedSegment):
    """
    Defines a rest type of segment for prediction training
    """
    def __init__(self, state: dict, duration_avg: float, duration_range: float):
        """
        Constructor
        """
        super().__init__(self.Label.REST, state, duration_avg, duration_range)

    def mount_segment(self):
        """
        Mount a segment GUI and record data
        """
        # Create the GUI
        #text = "You have completed prompt number\n\n" + str(self.state["recording_session"]["count"])
        #rest_text = Label(text=text, font=("Arial", 40))

        ## mount the page
        #self.components.append((rest_text, {"expand":True,
        #                                     "fill":"both"}))

        super().mount_segment()

class CountdownSegment(TimedSegment):
    """
    Defines a countdown segment for starting a trial
    """
    def __init__(self, state: dict, duration_avg: float, duration_range: float=0):
        """
        Constructor
        """
        super().__init__(self.Label.AMBIGUOUS, state, duration_avg, duration_range)

    def mount_segment(self):
        """
        Mount a segment GUI and record data
        """
        # Create the GUI
        text = "Starting session in...\n"
        countdown_text = Label(text=text, font=("Arial", 40))

        timer = Label(font=("Arial", 60))

        self.update_countdown_timer(timer, self.get_segment_period())

        self.components.append((countdown_text, {"pady":60}))
        self.components.append(timer)

        super().mount_segment()

class BreakSegment(TimedSegment):
    """
    Defines a timed break segment in between sessions
    """
    def __init__(self, state: dict, duration_avg: float, duration_range: float=0):
        """
        Constructor
        """
        super().__init__(self.Label.DISCONNECTED, state, duration_avg, duration_range)

    def mount_segment(self):
        """
        Mount a GUI for this segment
        """
        text = "Time for a Break!\n\nKeep your headset off until instructed to put it on\n\nThe next session begins in\n\n"
        break_text = Label(text=text, font=("Arial", 40))

        timer = Label(font=("Arial", 60))

        self.update_countdown_timer(timer, self.get_segment_period(), minutes=True)

        self.components.append((break_text, {"pady":60}))
        self.components.append(timer)

        super().mount_segment()


class PromptedSegment(Segment):
    def __init__(self, label: Segment.Label, state: dict):
        """
        Constructor
        """
        self.button = Button(command = lambda: self.mount_next_segment())
        super().__init__(label, state)

class RemoveHeadsetSegment(PromptedSegment):
    """
    Defines a segment prompting you to remove your headset
    """
    def __init__(self, state: dict):
        """
        Constructor
        """
        super().__init__(self.Label.AMBIGUOUS, state)

    def mount_segment(self):
        """
        Mount the page prompting you to remove your headset
        """
        self.state['recording_session']['session_count'] += 1

        prompt_text = ("\n\nYou have completed session %s out of %s\n\n"
                       "Please remove your headset for a break.\n\n"
                       "Press the 'Headset Removed' button once you've removed your headset."
                            % (self.state['recording_session']['session_count'],
                               self.state['recording_session']['total_sessions']))
        prompt = Label(text=prompt_text, font=("Arial", 30))
        
        self.button.configure(text="Headset Removed", font=("Arial", 48))

        self.components.append((prompt, {"pady": 50}))
        self.components.append((self.button, {"pady":30}))

        super().mount_segment()

class RemoveHeadsetSegment(PromptedSegment):
    """
    Defines a segment prompting you to remove your headset
    """
    def __init__(self, state: dict):
        """
        Constructor
        """
        super().__init__(self.Label.AMBIGUOUS, state)

    def mount_segment(self):
        """
        Mount the page prompting you to remove your headset
        """
        self.state['recording_session']['session_count'] += 1
        prompt_text = ("\n\nYou have completed session %s out of %s\n\n"
                       "Please remove your headset for a break.\n\n"
                       "Press the 'Headset Removed' button once you've removed your headset."
                            % (self.state['recording_session']['session_count'],
                               self.state['recording_session']['total_sessions']))
        prompt = Label(text=prompt_text, font=("Arial", 30))
        
        self.button.configure(text="Headset Removed", font=("Arial", 48))

        self.components.append((prompt, {"pady": 50}))
        self.components.append((self.button, {"pady":30}))

        super().mount_segment()

class PlaceHeadsetSegment(PromptedSegment):
    """
    Defines a segment prompting you to put on your headset
    """
    def __init__(self, state: dict):
        """
        Constructor
        """
        super().__init__(self.Label.AMBIGUOUS, state)

    def mount_segment(self):
        """
        Mount the page prompting you to remove your headset
        """
        prompt_text = ("\n\nYou are now starting session %s\n\n"
                       "Please place your headset on your head and ensure full contact of all electrodes.\n\n"
                       "Press the 'Ready' button once you've put on your headset."
                            % (self.state['recording_session']['session_count']+1))
        prompt = Label(text=prompt_text, font=("Arial", 30))
        
        self.button.configure(text="Ready", font=("Arial", 48))

        self.components.append((prompt, {"pady": 50}))
        self.components.append((self.button, {"pady":30}))

        super().mount_segment()

class DoneSegment(PromptedSegment):
    """
    Complete the session and save recording
    """
    def __init__(self, state: dict):
        """
        Constructor
        """
        super().__init__(self.Label.AMBIGUOUS, state)

    def mount_segment(self):
        """
        Mount the done segment
        """
        # Make GUI elements
        text = ("You have completed your the experiment!\n"
                "Your results are being saved. Thank you for participating!")
        self.components.append(Label(text=text, font=("Arial", 40)))

        self.button.configure(text='Exit', font=("Arial", 40))

        super().mount_segment()

class ErrorSegment(PromptedSegment):
    """
    Error and exit
    """
    def __init__(self, state: dict):
        """
        Constructor
        """
        super().__init__(self.Label.AMBIGUOUS, state)

    def mount_segment(self):
        """
        Mount the done segment
        """
        # Make GUI elements
        text = "The OSC server has not been connected, please connect it and start again.\n"
        self.components.append(Label(text=text, font=("Arial", 40)))

        self.button.configure(text='Exit', font=("Arial", 40))

        self.components.append(self.button)

        super().mount_segment()

class LandingSegment(PromptedSegment):
    """
    Create the landing page and ask for user name
    """
    def __init__(self, state: dict):
        """
        Constructor
        """
        super().__init__(self.Label.AMBIGUOUS, state)

    def mount_segment(self):
        """
        Mount landing page components
        """
        def submit_user(user_id):
            self.state['recording_session']['user'] = user_id
            self.mount_next_segment()

        title = Label(text="Muse OSC Interface", font=("Arial", 48))
        ip_info = Label(text="Set the Server IP in Mind Monitor to " + self.state["ip"], font=("Arial", 25))
        id_prompt = Label(text="Enter subject id for session  ", font=("Arial", 18))
        id_entry = Entry(font=("Arial", 18))
        id_submit = Button(command = lambda: submit_user(id_entry.get()), text="Submit", font=("Arial", 25))

        self.components.append((title, {"pady": 5}))
        self.components.append(ip_info)
        self.components.append(id_prompt)
        self.components.append((id_entry, {"pady": 5}))
        self.components.append(id_submit)

        super().mount_segment()

class IntroSegment(PromptedSegment):
    """
    Introduction segment talking about what there is
    """
    def __init__(self, state: dict):
        """
        Constructor
        """
        super().__init__(self.Label.AMBIGUOUS, state)

    def mount_segment(self):
        """
        Mount intro page components
        """
        title = Label(text="Muse OSC Interface", font=("Arial", 48))
        ip_info = Label(text="Set the Server IP in Mind Monitor to " + self.state["ip"], font=("Arial", 25))
        id_info = Label(text="Recording session for " + self.state["recording_session"]["user"], font=("Arial", 18))
        session_text ="""
        A recording sitting lasts approximately 10 minutes, during which a series of videos will be shown to you with a blank screen in between.
        You will be given a 3 minute break halfway in between to take off your headset and rest your eyes.

        Please configure your muse headset and Mind Monitor app and click ready to begin when you are ready."""
        session_info =  Label(text=session_text, justify=LEFT, font=("Arial", 18))

        self.button.configure(text="Ready", font=("Arial", 48))

        self.components.append((title, {"pady": 5}))
        self.components.append(ip_info)
        self.components.append((id_info, {"pady": 5}))
        self.components.append(session_info)
        self.components.append((self.button, {"pady": 10}))

        super().mount_segment()

