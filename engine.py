import sys, subprocess, time

class ManagedProcess:
    def __init__(self, command):
        self.cmd = command
        self.process = None

    def start(self):
        self.process = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def poll(self):
        return self.process.poll() is not None
    
    def get_status(self):
        if self.poll():
            return f"FINISHED (Exit Code: {self.process.returncode})"
        return "RUNNING"

def main():
    cmd = sys.argv[1:]

    if not cmd:
        print("Usage: python script.py <command>")
        sys.exit(1)

    Process = ManagedProcess(cmd)    
    Process.start()
    
    while Process.get_status() == "RUNNING":
        print(f"Heartbeat: Process {Process.process.pid} is still alive...")
        time.sleep(1)

    print(Process.get_status())
    return sys.exit(0)

if __name__ == '__main__':
    main()

