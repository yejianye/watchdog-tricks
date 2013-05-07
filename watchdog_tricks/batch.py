import Queue
import subprocess
from watchdog.tricks import Trick
from watchdog_tricks import utils
from threading import Thread

class BatchTrick(Trick):
    """ Batching events within a time window and send it as a single event
    This would be particularly useful for things like restarting a server after code changes.
    You don't want to restart the server mutliple times when multiple files are modified due to a save command 
    in the text editor or more commonly when the user does a git pull.
    """
    def __init__(self, *args, **kwargs):
        super(BatchTrick, self).__init__(*args, **kwargs)
        self.event_queue = Queue.Queue() 
        self.timeout = 0.5
        self.timer_thread = Thread(target=self.timer_loop)
        self.timer_thread.daemon = True
        self.timer_thread.start()

    @utils.trace_event
    def on_modified(self, event):
        self.event_queue.put(event)

    @utils.trace_event
    def on_deleted(self, event):
        self.event_queue.put(event)

    @utils.trace_event
    def on_created(self, event):
        self.event_queue.put(event)

    @utils.trace_event
    def on_moved(self, event):
        self.event_queue.put(event)

    def timer_loop(self):
        events = []
        while True:
            try:
                event = self.event_queue.get(timeout=self.timeout)
                events.append(event)
            except Queue.Empty:
                if events:
                    self.on_multiple_events(events)
                    events = []

    def on_multiple_events(self, events):
        raise NotImplementedError()

class ServerRestartTrick(BatchTrick):
    def __init__(self, restart_command, **kwargs):
        super(ServerRestartTrick, self).__init__(**kwargs)
        self.restart_command = restart_command 
    
    def on_multiple_events(self, events):
        subprocess.call(self.restart_command, shell=True) 
