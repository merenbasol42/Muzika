from threading import Thread

class Event:
    def __init__(self):
        self.name = "ahmet" #For debugging
        self.cb_list = []
        self.cb_set = set()
        self.event_thread:Thread
        self.event_thread_target = None

    def __thread_invoke(self):
        self.event_thread = Thread(target=self.event_thread_target)
        self.event_thread.start()

    def __thread_zzz(self):
        self.event_thread = None

    def sync_trigger(self):
        self.event_thread_target = self.__sync_trigger
        self.__thread_invoke()

    def __sync_trigger(self):
        for func in self.cb_list:
            func()

        self.__thread_zzz()

    def async_trigger(self):
        self.event_thread_target = self.__async_trigger
        self.__thread_invoke()

    def __async_trigger(self):
        for func in self.cb_list:
            t = Thread(target=func)
            t.start()

        self.__thread_zzz()

    def myself_trigger(self):
        for func in self.cb_list:
            func()

    def subscribe(self, callback):
        """Add a function to the list of subscribers."""
        if not callable(callback):
            raise TypeError("Callback must be a callable.")
        if callback not in self.cb_set:
            self.cb_list.append(callback)
            self.cb_set.add(callback)

    def describe(self, callback, safe=False):
        try:
            self.cb_list.remove(callback)
            self.cb_set.remove(callback)
        except Exception as e:
            if safe: return 
            else: raise e


class EventWithArgs:
    def __init__(self):
        self.cb_list = []
        self.event_thread:Thread = None
        self.event_thread_target = None

    def __thread_invoke(self):
        self.event_thread = Thread(target=self.event_thread_target)
        self.event_thread.start()

    def __thread_zzz(self):
        self.event_thread = None

    def sync_trigger(self, *args):
        self.event_thread_target = lambda: self.__sync_trigger(*args)
        self.__thread_invoke()
        self.__thread_zzz()

    def __sync_trigger(self, *args):
        for func in self.cb_list:
            func(*args)

    def async_trigger(self, *args):
        self.event_thread_target = lambda: self.__async_trigger(*args)
        self.__thread_invoke()
        self.__thread_zzz()

    def __async_trigger(self, *args):
        for func in self.cb_list:
            t = Thread(target=lambda:func(*args))
            t.start()
        
    def subscribe(self, callback):
        """Add a function to the list of subscribers."""
        if callable(callback):
            self.cb_list.append(callback)
        else:
            raise TypeError("Callback must be a callable.")