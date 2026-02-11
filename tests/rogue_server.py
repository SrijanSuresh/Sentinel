import signal
import time
import os

def ignore_term(signum, frame):
    # This ignores the polite SIGTERM (Signal 15)
    print(f"\n[!] RECEIVED SIGTERM ({signum}) - IGNORED. I'm not leaving!")

# Register the handler
signal.signal(signal.SIGTERM, ignore_term)

def rogue_leak():
    print(f"Rogue Server (PID: {os.getpid()}) started. Limit: 512MB.")
    bloat = []
    chunk = 20 * 1024 * 1024  # 20MB steps
    
    try:
        while True:
            # Gradually climb toward the 512MB limit
            bloat.append(" " * chunk)
            current_mb = (len(bloat) * 20)
            print(f"Rogue growth: {current_mb}MB... ignoring all warnings.")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Manual exit.")

if __name__ == "__main__":
    rogue_leak())
