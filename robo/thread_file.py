from threading import Thread
from time import sleep



class thread(Thread):
    all_thread = []

    def __init__(self, func, **kwargs):
        Thread.__init__(self)
        self.func = func
        self.kwargs = kwargs
        thread.all_thread.append(self)

    def run(self):
        self.func(**self.kwargs)


