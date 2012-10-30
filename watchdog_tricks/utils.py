import subprocess
from functools import wraps 

def trace_event(func):
    @wraps(func)
    def _traced_func(self, event):
        if hasattr(event, 'dest_path'):
            print '%s: %s -> %s' % (event.event_type, event.src_path, event.dest_path)
        else:
            print '%s %s' % (event.event_type, event.src_path)
        return func(self, event)
    return _traced_func

def exec_cmd(cmd):
    print 'Execute command:', cmd
    process = subprocess.Popen(cmd, shell=True)
    process.wait()

