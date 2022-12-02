# Using This Repo, 12/2/22

## `app.py`
This is the front end for collecting data from the muse. This script runs the UI and when a user begins a session, opens an OSC server by calling osc_server.py. Then, after the sampling period is over, the osc server is terminated. Rinse and repeat until the session is finished.


## `Pages`
The UI is broken up into smaller page scripts, namely `landing_page.py` and `recording_page.py`, as well as a utils.py script for helper methods. The most important method in the `utils.py` class is `mount_page()`, which takes in the state variable, as well as a list of tkinter widgets (? I think, I'm not sure the actual name for what I'm passing, hopefully the code speaks for itself in this case). It then takes the list of widgets that are currently rendered from the state, removes them, stores the new widgets and renders them (along with any options that have been passed in with them).
### `landing_page.py`
This is the first two pages you see when you open up app.py, the user signin and the info screen.
### `recording_page.py`
This is the functional face of the UI, with frames for resting, STOP prompts and GO prompts. These make calls to the utils script to start and stop the OSC server.

## `osc_server.py`
This is script opens an OSC server for mindmonitor to send results to. It will read in each message from the phone and directly write it to a csv file, labelled `$username_$timestamp.data`
### Potential Errors
This script returns nothing to the main script, so the main script has no idea if there is, for example, no input coming in from mind monitor for whatever reason.


## `mock_osc_server.py`
This is a dummy clone of the `osc_server.py` that can be used in its place when testing UI without a connection to mindmonitor. It can be enabled by uncommenting line 24 in `utils.py` and commenting line 23 out.


## `state_enums.py`
Just some silly little enums for the UI state.

## `spectrogram_from_data.py`
This script is currently a proof of concept for how data processing on input data might look. This script must be run seperately from the main app.py. It reads data in from a given data file and can visualize it in time domain, as well as both continuous wavelet transforms (cwt) and signal squeezed wavelets (ssq_cwt).

## Next Steps
The next big step here is to implement real-time processing of the data, as a tech demo for the data that will eventually be streamed into the trained model. The shape this architecture will likely take is `app.py` -> `osc_server.py` -> (new)`data_processing.py`, where once messages are received by `osc_server.py`, a block will be sent to `data_processing.py`, which will process and change the domain of the data (likely to a cwt) and return it.