import time
import os
import random

def leak_memory():
    print(f"Mod Simulator (PID: {os.getpid()}) starting. Simulating production churn...")
    leaky_list = []
    
    try:
        while True:
            # Randomly allocate between 2MB and 12MB
            chunk_size = random.randint(2, 12) * 1024 * 1024
            leaky_list.append(" " * chunk_size)
            
            # 20% chance to "free" some memory, creating a sawtooth pattern
            if random.random() < 0.2 and len(leaky_list) > 1:
                leaky_list.pop(random.randint(0, len(leaky_list) - 1))
                print("--- Background GC event simulated ---")

            current_mb = sum(len(s) for s in leaky_list) / (1024 * 1024)
            print(f"Current usage: {current_mb:.2f}MB")
            time.sleep(1.5)
    except KeyboardInterrupt:
        print("Stopping simulation.")

if __name__ == "__main__":
    leak_memory()
