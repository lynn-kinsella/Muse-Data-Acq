from enum import Enum
class render_state (Enum):
    USER_ENTER = 0
    READY_PROMPT = 1
    SESSION_IN_PROGRESS = 2
    SAVING_RESULTS = 3
    THANK_YOU = 4
    ERROR = 5

class recording_state (Enum):
    REST = 0
    STOP = 1
    GO = 2
    DONE = 3
    ERROR = 4