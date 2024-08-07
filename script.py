import pyautogui
import time
import keyboard
import threading

# Flag to control the emergency stop
stop_flag = threading.Event()

# Function to read tags from a text file in chunks of 14
def read_tags(file_path, chunk_size=14):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    for i in range(0, len(lines), chunk_size):
        yield [line.strip() for line in lines[i:i+chunk_size]]

# Function to automate the process
def automate_process(tags, cell):
    if stop_flag.is_set():
        print("Emergency stop triggered!")
        return

    # Print tags and their length for debugging
    print(f"Processing {len(tags)} tags: {tags}")

    # Focus on the ChatGPT workspace
    pyautogui.click(x=338, y=1020)  # Adjust x, y coordinates to the ChatGPT input box

    # Paste tags into ChatGPT
    pyautogui.write(''.join(tags), interval=0.01)  # Set interval to 0 for instant typing
    time.sleep(6)
    pyautogui.press('enter')

    # Wait for the response
    time.sleep(60)  # Adjust the sleep time as needed for ChatGPT to generate responses

    # Skip to bottom
    pyautogui.click(x=610, y=960)
    
    time.sleep(1)
    # Copy the generated description
    pyautogui.click(x=371, y=916)  # Adjust x, y coordinates to the ChatGPT copy button

    time.sleep(1)

    # Search for the correct cell in Google Sheets
    cell_with_letter = f'B{cell}'  # Prepend 'B' to the cell number
    pyautogui.click(x=1013, y=189)
    pyautogui.write(cell_with_letter, interval=0)
    time.sleep(0.5)
    pyautogui.press('enter')

    time.sleep(0.5)
    # Paste the description
    pyautogui.hotkey('ctrl', 'v')

# Function to monitor for emergency stop key press
def monitor_stop_key():
    keyboard.wait('esc')  # Set 'esc' as the emergency stop key
    stop_flag.set()  # Set the stop flag when 'esc' is pressed

# Main function to read tags and automate the process
def main():
    global stop_flag
    initial_cell = 1142
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
        if iterations >= 50:  # How many loops of the tags
            break
        automate_process(tags, initial_cell)
        initial_cell += 14
        iterations += 1
        time.sleep(5)  # Wait before starting the next batch to ensure everything is pasted correctly

if __name__ == '__main__':
    main()
