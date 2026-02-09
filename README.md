# Sentinel: Custom Process Guardian 
## What is this?
Sentinel is a lightweight, modular "sidecar" I built to babysit Linux processes. It’s essentially a focused SRE tool that watches a child process, monitors its physical memory (RSS) in real-time, and provides a "backdoor" via Unix Domain Sockets so I can talk to it without interrupting the main loop.

## The "Why"
I wanted to understand exactly how tools like systemd or Kubernetes handle resource limits and health checks at the kernel level. Instead of just using them, I decided to build a "mini" version from scratch to handle:

- Memory Leaks: If a process (like my chaos.py bomb) starts eating RAM, Sentinel catches it and kills it before the OOM Killer crashes my whole WSL instance.
- Asynchronous Control: I wanted to be able to "ping" my monitor from a different terminal to get a status report without stopping the execution.

## The "Nitty Gritty" (What I actually did)
- Modular Architecture: I refactored the whole thing into a sentinel_pkg. One module handles the Guardian (the enforcer) and another handles the IPC (the mailbox).
- Non-Blocking Sockets: This was the biggest hurdle. I used socket.AF_UNIX and set it to non-blocking mode (setblocking(False)). This allows the script to "glance" at the socket for commands and then immediately go back to checking memory—no freezing allowed.
- Tiered Termination: I didn't just SIGKILL everything. I implemented a "polite" SIGTERM, waited 3 seconds, and only then brought out the hammer (SIGKILL) if the process was hung.
- Live Dashboard: I integrated the rich library to create a clean TUI (Terminal User Interface) so I don't have to look at scrolling logs. I get a live table with PIDs and memory stats.

## Current Tech Stack
- Language: Python 3 (specifically avoiding the heavy stuff, focusing on subprocess, socket, and os).
- Library: psutil for deep-diving into the /proc filesystem.
- Interface: rich for the TUI and netcat for IPC testing.

## What's Next?
- Prometheus Exporter: Turning Sentinel into a metrics endpoint so I can see these stats in Grafana.
- Docker Sidecar: Wrapping this as a container manager.

## How to verify the work
- Fire it up: sentinel python3 chaos.py
- Poke it: From another terminal: echo "status" | nc -U /tmp/sentinel.socket
- Watch it die: Watch the dashboard as chaos.py hits the 100MB limit and Sentinel executes the kill.
