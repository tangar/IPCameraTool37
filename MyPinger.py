import subprocess
import platform 

class MyPinger:
    def __init__(self,  count = 1, to = 100):
        self.count_prefix = '-n' if platform.system().lower()=='windows' else '-c'
        self.number = count
        self.timeout = to
        self.command = None
        self.ret = None
        
    def ping(host, count = 1, to = 100):
        count_prefix = '-n' if platform.system().lower()=='windows' else '-c'
        number = count
        timeout = to
        command = None
        ret = None
        command = ['ping', host, count_prefix, str(number), '-w', str(timeout)]
        ret = subprocess.run(command, capture_output=True, text=True)
        return ret.returncode