import os, socket

class IPCServer:
    def __init__(self, guardian, socket_path="/tmp/sentinel.socket"):
        self.path = socket_path
        self.server = None
        self.guardian = guardian

    def start(self):
        # removes binded file to avoid collision
        if os.path.exists(self.path):
            os.unlink(self.path)
        # socket creation Unix Domain Sockets (IPC)
        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server.bind(self.path)
        self.server.listen(1)
        self.server.setblocking(False) # turn off blocking so that we dont pause the child process

    def check_for_client(self):
        try:
            # return the socket obj accepted from client with its decoded data ("status") msg
            conn, _ = self.server.accept()
            data = conn.recv(1024).decode().strip()
            return conn, data    
        except (BlockingIOError, socket.error):
            # skip if no communication
            return None, None
    # to handle web
    def handle_command(self, data):
        command = data.decode().strip() if isinstance(data, bytes) else data.strip()
        print(f"DEBUG: Received Command -> '{command}'") # TRACE 1
        
        if command == "status":
            return f"{self.guardian.get_current_memory():.2f}"
        
        elif command == "stop":
            print("DEBUG: Executing STOP") # TRACE 2
            self.guardian.kill()
            return "Process Terminated"
        
        elif command.startswith("run:"):
            cmd_str = command.replace("run:", "").replace("sentinel ", "").strip()
            print(f"DEBUG: Attempting to LAUNCH -> '{cmd_str}'") # TRACE 3
            
            success = self.guardian.start_new_process(cmd_list=cmd_str.split()) 
            print(f"DEBUG: Launch Result -> {success}") # TRACE 4
            return "Launch Successful" if success else "Launch Failed"
        
        return "Unknown Command"