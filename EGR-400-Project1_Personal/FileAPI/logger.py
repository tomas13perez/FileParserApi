import platform
import datetime
import os

"""
The Logger class will create a log file if it does not
already exist. The log file provides timestamps for
when a file is parsed by the main program.

@authors: Tomas Perez, Lauren Nelson, Roberto Rodriguez 
"""


class Logger:
    def __init__(self, logfile):
        self.logfile = logfile
        # Verify that the log file is not a directory.
        if os.path.isdir(logfile):
            raise Exception("The path for the log file must be a file, not a directory.")
        # Verify directory exists (note file not needed)
        folder = os.path.dirname(logfile)
        if not os.path.dirname(folder):
            raise Exception("The folder for the log file does not exist.")

    def log(self, msg):
        machine = platform.node()
        now = datetime.datetime.now()
        date = "{0}_{1}_{2} {3}:{4}:{5}".format(
            now.year, now.month, now.day,
            now.hour, now.minute, now.second)
        text = "{0}/{1}: {2}".format(machine, date, msg)
        print("    log=" + text)
        # Append line to log file
        with open(self.logfile, 'a+') as file_out:
            file_out.write("{0}\n".format(text))
