import pyautogui
import time

try:
    print("Press Ctrl+C to stop.")
    while True:
        x, y = pyautogui.position()
        print(f"Current mouse position: (x={x}, y={y})")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopped.")
