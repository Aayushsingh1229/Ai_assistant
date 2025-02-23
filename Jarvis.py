from NetHyTech_STT import listen
from brain import generate_response
import threading
import os
import logging
from os import getcwd
from Automation._intregation_automation import Automation
from FUNCTION.function_intregation import Function_cmd
from NetHyTech_Pyttsx3_Speak import speak

# Configure logging
log_file = os.path.join(os.getcwd(), "templates", "log.txt")
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

bye_key_word = ["bye", "goodbye"]
exit_flag = False
input_file_path = os.path.join(getcwd(), "input.txt")

# Thread lock to prevent file read/write conflicts
lock = threading.Lock()

def clear_input_file():
    """ Clears the input file at the start. """
    with open(input_file_path, "w") as input_file:
        input_file.truncate(0)

def check_commands():
    """ Continuously checks input.txt for commands and processes them. """
    global exit_flag
    last_modified = None
    output_text = ""

    while not exit_flag:
        try:
            # Check if file has changed before reading
            if os.path.exists(input_file_path):
                current_modified = os.path.getmtime(input_file_path)
                if last_modified is None or current_modified > last_modified:
                    last_modified = current_modified

                    with lock:
                        with open(input_file_path, "r") as input_text:
                            current_text = input_text.read().strip().lower()  # Normalize case

                    if current_text and current_text != output_text:
                        output_text = current_text
                        process_command(output_text)
        except Exception as e:
            logging.error(f"Error in check_commands: {e}")

def process_command(command):
    """ Processes user commands, calls response functions, and handles system commands. """
    global exit_flag

    input_msg = f"User: {command}"

    if "jarvis" in command:
        response = generate_response(command)
        output_msg = f"Jarvis: {response}"
        speak(response, 0)
    else:
        Automation(command)
        Function_cmd(command)
        output_msg = ""

    with lock:
        with open(log_file, "a") as log_file_obj:
            log_file_obj.write(f"{input_msg}\n{output_msg}\n")

    # Check for exit command
    if any(keyword in command for keyword in bye_key_word):
        exit_flag = True

def main():
    """ Main function to initialize threads and start execution. """
    clear_input_file()
    listener_thread = threading.Thread(target=listen, daemon=True)
    checker_thread = threading.Thread(target=check_commands, daemon=True)

    listener_thread.start()
    checker_thread.start()

    listener_thread.join()
    checker_thread.join()

if __name__ == "__main__":
    main()
