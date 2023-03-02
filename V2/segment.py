import log
import logging
from enum import Enum
from utils import mount_page, load_video
from tkinter import *
from random import random
from tkVideoPlayer import TkinterVideo

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

    def mount_segment(self):
        """
        Override function for mounting the segment
        """
        # Update the state label
        self.state['recording_session']['state'] = self.label

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
            self.state['active'] = False
            # TODO: Set the render state to the end screen
            return False

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

    def update_countdown_timer(self, timer):
        """
        Update the timer field passed in for the class
        """
        old_time = int(timer.cget("text"))
        new_time = old_time - 1
        timer.configure(text = str(new_time))
        if new_time != 0:
            self.state["afters"]["timer_update"] = (timer.after(1000, lambda: self.update_countdown_timer(timer)), timer)

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
        text = "You have completed prompt number " + str(self.state["recording_session"]["count"])
        rest_text = Label(text=text, font=("Arial", 30))

        # mount the page
        self.components.append((rest_text, {"expand":True,
                                             "fill":"both"}))

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

        timer = Label(text=str(self.get_segment_period()//1000), font=("Arial", 60))

        self.state["afters"]["timer_update"] = \
                (timer.after(1000, lambda: self.update_countdown_timer(timer)), timer)

        self.components.append((countdown_text, {"pady":60}))
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
