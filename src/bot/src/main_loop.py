# src/bot/src/main_loop.py


# Imports
from threading import Thread


class MainLoop:
    def __init__(self):
        self.terminate_flag = False
        self.thrd = Thread(target=self._loop)

    
    def __call__(self):
        self.thrd.start()
    
    
    def stop(self):
        self.terminate_flag = True
        self.thrd.join()
    
    
    def _loop(self):
        pass

main_loop = MainLoop()