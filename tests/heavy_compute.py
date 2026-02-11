import time
import math
import os

def sine_wave_memory():
    print(f"Heavy Compute (PID: {os.getpid()}) generating memory hills...")
    print("Goal: Stay between 200MB and 400MB (Safe below 512MB limit).")
    
    # Configuration
    base_memory = 300 * 1024 * 1024  # 300 MB Center
    amplitude = 78 * 1024 * 1024    # +/- 100 MB Swing
    
    wave_data = []
    t = 0
    
    try:
        while True:
            # Sine wave logic: range is [base - amp, base + amp]
            target_size = base_memory + (amplitude * math.sin(t))
            
            # Re-allocate a single large string to shift the memory usage
            wave_data = [" " * int(target_size)]
            
            current_mb = target_size / (1024 * 1024)
            print(f"Current Sine Level: {current_mb:.2f} MB")
            
            # Adjust 't' to control how fast the hills move (0.1 is slow and smooth)
            t += 0.1 
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping compute.")

if __name__ == "__main__":
    sine_wave_memory()
