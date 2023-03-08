from tkVideoPlayer import TkinterVideo

class Video(TkinterVideo):
    """
    My own implementation of the tkinter video which plays the next segment
    after completion of play
    """
    def __init__(self, end_func, *args, **kwargs):
        """
        Constructor
        """
        super().__init__(*args, **kwargs)

        self.end_func = end_func

    def _load(self, path):
        super()._load(path)
        self.end_func()
