# Sentinel: Custom Process Guardian 
Think of Sentinel as a digital "bouncer" for your computer. It’s a high-performance tool designed to watch specific programs (like games, data science models, or servers) and make sure they don’t "misbehave" by hogging all your system’s memory.

## Architecture
<img width="983" height="781" alt="image" src="https://github.com/user-attachments/assets/38b283c2-2daa-42c1-85de-f0e8d9e75ff8" />

## Terminal UI
<img width="647" height="130" alt="image" src="https://github.com/user-attachments/assets/ed2d995c-9ef6-4020-ae5c-c459622b3a0d" />

## Dashboard
<img width="1222" height="476" alt="gauge_mod" src="https://github.com/user-attachments/assets/e84ec790-d61a-4f9f-b006-bf63b06fffa9" />
<img width="1215" height="423" alt="test_mod" src="https://github.com/user-attachments/assets/53183c75-8065-48e2-8b06-8c4bea835161" />

### Core Concepts

* **Tiered Termination:** Sentinel isn't just a blunt instrument. It tries a polite `SIGTERM` (Signal 15) first to let the process clean up its mess, waits 3 seconds, and then brings out the `SIGKILL` (Signal 9) only if the process is totally hung.
* **Non-Blocking IPC:** I used `socket.AF_UNIX` with non-blocking mode. This means the guardian can "glance" at the socket for incoming commands without freezing the main monitoring loop.
* **Observability:**
* **TUI Dashboard:** A live terminal table built with `rich` so you can see PIDs and memory usage in real-time.
* **Prometheus Exporter:** Sentinel exposes an HTTP endpoint on port 8000. Prometheus pulls these metrics every 5 seconds.
* **Grafana:** I use this to turn raw numbers into staircase graphs that make memory leaks obvious.



---

### File Breakdown

* **`main.py`**: The entry point. It orchestrates the startup, initializes the `Guardian` and `IPCServer`, and runs the main loop that updates the `rich` dashboard.
* **`sentinel_pkg/guardian.py`**: The "brain." It uses `subprocess` to spawn the child process and `psutil` to query the `/proc` filesystem for Resident Set Size (RSS) memory. It also contains the tiered logic for `SIGTERM` and `SIGKILL`.
* **`sentinel_pkg/ipc.py`**: Handles the Unix Domain Socket server. It listens at `/tmp/sentinel.socket` and uses a non-blocking check to see if any external client (like `nc`) is sending commands.
* **`sentinel_pkg/metrics.py`**: Sets up the Prometheus `Gauge` objects and starts the HTTP server. It includes a `try/except` block to handle port 8000 collisions, allowing the monitor to fail gracefully if another instance is already reporting.
* **`tests/leaker.py`**: A "chaos" script designed to simulate a memory leak by steadily appending data to a list, used to verify that Sentinel actually kills rogue processes.

---

### Setup and Launch

**1. Build the environment**
Start the observability stack (Prometheus and Grafana) in the background:

```bash
docker-compose up -d prometheus grafana

```

**2. Launch the Sentinel Workstation**
Start the Sentinel container in an interactive bash session:

```bash
docker-compose run --rm sentinel /bin/bash

```

**3. Run a test case**
Inside the container, run the memory leaker:

```bash
sentinel python3 tests/leaker.py

```

### Testing the "Backdoor"

Open a **second terminal** on your host and run this to poke the guardian while it's working:

```bash
# Get a status report via the IPC socket
echo "status" | nc -U /tmp/sentinel.socket

# Force a remote stop
echo "stop" | nc -U /tmp/sentinel.socket

```

---

### What's Next?

* **cgroups v2 Integration:** Moving beyond RSS polling to use true Linux kernel container limits.
* **Multi-process Supervision:** Adding the ability to watch a cluster of processes with custom alerting rules.
* **Alerting Pipelines:** Hooking Prometheus up to Slack or webhooks for instant notifications.
* **Helm Charts:** Packaging this as a Kubernetes sidecar for easy cloud deployment.
* **eBPF Metrics:** Diving deeper into kernel tracing for zero-overhead observability.

---

