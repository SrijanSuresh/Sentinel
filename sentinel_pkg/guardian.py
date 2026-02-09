import os, sys, subprocess, psutil

class Guardian:
    def __init__(self, command, limit):
        self.cmd = command
        self.limit = limit
        self.process = None

    def start(self):
        # we start the process
        self.process = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # to make sure the output pipe is non blocking so that .read() doesn't freeze our loop
        os.set_blocking(self.process.stdout.fileno(), False)

    def poll(self):
        # returns True if the status is not running
        return self.process.poll() is not None

    def kill(self):
        # terminates a running process (either gentle or force)
        if self.process:
            print(f"Terminating process {self.process.pid}...")
            self.process.terminate() # calling signal 15
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                print("Process refused to die. USING SIGKILL..")
                self.process.kill() # calling signal 9

    def get_status(self):
        # we check if our process is still running -> return string format
        if self.poll():
            return f"FINISHED (Exit Code: {self.process.returncode})"
        return "RUNNING"

    def check_resources(self):
        try:
            proc_id = self.process.pid
            # calculation here memory is returned in bytes, so convert to megabytes(MB)
            memory = psutil.Process(proc_id).memory_info().rss / (1024**2) # 1024 bytes = 1 KB, 1024 KB = 1 MB
            # if the memory usage exceeds our limit we end the process
            if memory > self.limit:
                self.kill()
        except psutil.NoSuchProcess as e:
            print(f"{e}: race condition, process ended before memory calculation")

