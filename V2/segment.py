import log
import logging
from utils import mount_page

LOGGER = logging.getLogger('GUI')
log.configure_logger(LOGGER, 'training_gui.log')

class Segment(object):
    """
    Defines the primitive type of segment
    """
    def __init__(self, label, state):
        """
        Constructor
        """
        self.label = label
        self.state = state
        self.next_segment = None

    def mount_segment(self):
        """
        Override function for mounting the segment
        """
        LOGGER.error("This function is not implemented, please use a Segment type")
        return

    def mount_next_segment(self):
        """
        Mount the next segment in the linked list
        """
        if self.next_segment:
            self.next_segment.mount_segment()
        else:
            LOGGER.info("Reached the end of the segment chain")
            return False
        
class VideoSegment(Segment):
    """
    Defines a video type of segment for prediction training
    """
    def __init__(self, media, label, state, duration_avg, duration_range):
        """
        Constructor
        """
        self.media_filepath = media
        self.duration_avg = duration_avg
        self.duration_range = duration_range

        super().__init__(label, state)


    def mount_segment(self):
        """
        Mount a segment GUI and record data
        """
        pass
        # Update the state label
        # Create the GUI
        # mount the page
        # Start the countdown
