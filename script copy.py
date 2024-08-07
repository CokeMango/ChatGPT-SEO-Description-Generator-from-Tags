import pyautogui
import time
import keyboard
import threading

# Flag to control the emergency stop
stop_flag = threading.Event()

# Function to read tags from a text file in chunks of 14
def read_tags(file_path, chunk_size=5):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    for i in range(0, len(lines), chunk_size):
        yield [line.strip() for line in lines[i:i+chunk_size]]

# Function to automate the process
def automate_process(tags, cell):

    # Paste tags into ChatGPT
   # pyautogui.write('\n'.join(tags), interval= 0.05)  # Set interval to 0 for instant typing
    print(f"Processing {len(tags)} tags: {tags}")
    pyautogui.click(x=633, y=364)
    pyautogui.write('\n'.join(tags), interval=0.01)  # Set interval to 0 for instant typing
    
    time.sleep(4)
    pyautogui.press('enter')
        
# Function to monitor for emergency stop key press
def monitor_stop_key():
    keyboard.wait('esc')  # Set 'esc' as the emergency stop key
    stop_flag.set()  # Set the stop flag when 'esc' is pressed

# Main function to read tags and automate the process
def main():
    global stop_flag
    initial_cell = 300
    tags_file = r'C:\Users\roman\OneDrive\Documents\Gun Parts Website Script\Tags 193-458.txt'  # Use raw string for the file path

    # Start the thread to monitor the stop key
    stop_thread = threading.Thread(target=monitor_stop_key)
    stop_thread.daemon = True
    stop_thread.start()

    iterations = 0
    for tags in read_tags(tags_file):
        if stop_flag.is_set():  # Check if the stop flag is set
            print("Stopping script due to emergency stop.")
            break
        if iterations >= 1:  # Limit to five iterations for testing
            break
        automate_process(tags, initial_cell)
        initial_cell += 14
        iterations += 1
        time.sleep(5)  # Wait before starting the next batch to ensure everything is pasted correctly

if __name__ == '__main__':
    main()
