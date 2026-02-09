import sys, time
from rich.live import Live
from rich.table import Table
from sentinel_pkg.guardian import Guardian
from sentinel_pkg.ipc import IPCServer

def generate_dashboard(guardian):
    # Generate a real-time table UI
    table = Table(title="Sentinel: System Guardian", show_header=True, header_style="bold magenta")
    table.add_column("PID", style="dim", width=12)
    table.add_column("Status", justify="center")
    table.add_column("Memory Limit", justify ="right")

    # fetching current status
    status = guardian.get_status()
    pid = str(guardian.process.pid) if guardian.process else "N/A"

    table.add_row(pid, status, f"[green]{guardian.limit} MB[/green]")
    return table

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

    # Manage Process while it's running
    with Live(generate_dashboard(guardian), refresh_per_second=4) as live:
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
                # update dashboard
                live.update(generate_dashboard(guardian))
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\nSentinel shutting down..")
            guardian.kill()

    print(f"Final report:{guardian.get_status()}")

if __name__ == '__main__':
    main()

