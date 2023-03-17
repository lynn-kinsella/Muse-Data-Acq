from segment import *
import random
import glob
import os

class Collection(object):
    """
    Class defining a collection of segments
    """
    def __init__(self, state):
        """
        Constructor
        """
        self.segment_playlist = []
        self.state = state

    def __iter__(self):
        """
        Get a copy of all the segments in the collection
        """
        for segment in self.segment_playlist:
            yield segment

    def __getitem__(self, items):
        """
        Get a copy of all the segments in the collection
        """
        return self.segment_playlist.__getitem__(items)

    def __len__(self):
        """
        Get length of collection
        """
        return len(self.segment_playlist)

    def add_segment(self, segment):
        """
        Add segment to segment playlist
        """
        if self.segment_playlist:
            self.segment_playlist[-1].next_segment = segment

        self.segment_playlist.append(segment)

    @staticmethod
    def join(*collections):
        """
        Join segments and collections together in order
        return a new collection
        """
        if not collections:
            return []

        state = collections[0].state

        new_collection = Collection(state)

        for collection in collections:
            for segment in collection:
                new_collection.add_segment(segment)

        return new_collection


    def play(self):
        """
        Play the parts of the collection
        """
        self.segment_playlist[0].mount_segment()

class BreakCollection(Collection):
    """
    Class defining segments for a break
    """
    def __init__(self, state, break_time):
        """
        Constructor
        """
        self.break_time = break_time
        super().__init__(state)

        self.populate_session()

    def populate_session(self):
        self.add_segment(RemoveHeadsetSegment(self.state))

        self.add_segment(BreakSegment(self.state, self.break_time))

        self.add_segment(PlaceHeadsetSegment(self.state))

class StopGoVideoSessionCollection(Collection):
    """
    Class defining a collection of segments for the Stop Go Video session
    """
    VARIATION_RANGE = 1
    COUNTDOWN_TIME = 3
    GO_MEDIA = glob.glob('../../Training Footage/Faster/go_*')
    STOP_MEDIA = glob.glob('../../Training Footage/Faster/stop_straight_*')

    def __init__(self, state, trials, rest_time, focus_time):
        """
        Constructor
        """
        self.trials = trials
        self.rest_time = rest_time
        self.focus_time = focus_time
        super().__init__(state)

        self.populate_session()

    def populate_session(self):
        """
        Populate the session with segments
        """
        # Add countdown segment
        self.add_segment(CountdownSegment(self.state, duration_avg=self.COUNTDOWN_TIME))

        classes = []
        classes.append({"media": self.GO_MEDIA,
                       "label": Segment.Label.GO})
        classes.append({"media": self.STOP_MEDIA,
                       "label": Segment.Label.STOP})

        for i in range(self.trials):
            clss = random.choice(classes)

            self.add_segment(VideoSegment(media=random.choice(clss['media']), label=clss['label'],
                                          state=self.state, duration_avg=self.focus_time,
                                          duration_range=self.VARIATION_RANGE))

            self.add_segment(RestSegment(state=self.state, duration_avg=self.rest_time,
                                         duration_range=self.VARIATION_RANGE))

class VariableLengthVideoSessionCollection(Collection):
    """
    Class defining the variable length video session
    """
    COUNTDOWN_TIME = 3

    def __init__(self, state, media_dir):
        """
        Constructor
        """
        self.media = self.collect_media(media_dir)
        super().__init__(state)
        self.populate_session()

    def collect_media(self, media_dir):
        
        labels = glob.glob(os.path.join(media_dir, '*'))

        files = []
        for label_path in labels:
            clip_files = glob.glob(os.path.join(label_path, "*.mp4"))

            label_ind = int(os.path.basename(label_path)[0])
            for clip in clip_files:
                files.append((Segment.Label(label_ind), clip))


        return sorted(files, key=lambda x: os.path.basename(x[1]))

    def populate_session(self):
        """
        Populate the session with segments
        """
        # Add countdown segment
        self.add_segment(CountdownSegment(self.state, duration_avg=self.COUNTDOWN_TIME))

        for label, media_path in self.media:
            self.add_segment(VariableLengthVideoSegment(media_path, label, self.state))

class ContinuousVideoSessionCollection(Collection):
    """
    Class defining the continuous video session
    """
    COUNTDOWN_TIME = 3

    def __init__(self, state, media):
        """
        Constructor
        """
        self.media = media
        super().__init__(state)
        self.populate_session()

    def populate_session(self):
        """
        Populate the session with segments
        """
        # Add countdown segment
        self.add_segment(CountdownSegment(self.state, duration_avg=self.COUNTDOWN_TIME))

        self.add_segment(InteractiveVariableLengthVideoSegment(self.media, None, self.state))
