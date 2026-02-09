import time, os
"""
the purpose of this file is to stress test under chaotic memory usage
"""
data = []
print(f"Chaos started with PID: {os.getpid()}")

while 1:
    data.append(' '* 10**6)
    print(f"Current memory usage (approx): {len(data)} MB")
    time.sleep(0.5)
