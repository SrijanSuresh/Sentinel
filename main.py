import sys, time
from sentinel_pkg.guardian import Guardian
from sentinel_pkg.ipc import IPCServer

def main():
    # we skip our script name and just get the command
    cmd = sys.argv[1:]
    limit = 100 # limit by 100mb
    # we verify if our command exists
    if not cmd:
        print("Usage: python script.py <command>")
        return

    # creating instance of process manager and server
    guardian = Guardian(cmd, limit)
    server = IPCServer()

    guardian.start()
    server.start()
    print(f"Server active. Montoring PID: {guardian.process.pid}")
    # Manage Process while it's running
    try:
        while not guardian.poll():
            # checking incoming commands (IPC)
            conn, msg = server.check_for_client()
            if msg:
                if msg == "status":
                    res = f"Guardian: {guardian.get_status()}\n"
                    conn.sendall(res.encode())
                elif msg == "stop":
                    guardian.kill()
                    break
                conn.close() # we close our line after msg
            # lets verify our mem-usage here
            guardian.check_resources()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSentinel shutting down..")
        guardian.kill()
    print(f"Final report:{guardian.get_status()}")

if __name__ == '__main__':
    main()

