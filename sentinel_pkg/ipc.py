import os, socket

class IPCServer:
    def __init__(self, socket_path="/tmp/sentinel.socket"):
        self.path = socket_path
        self.server = None

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

