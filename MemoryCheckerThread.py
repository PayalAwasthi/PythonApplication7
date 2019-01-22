'''
Created on Jan 25, 2017

@author: savarshn
'''

import threading, time, subprocess, os
import config


class MemoryCheckerThread():
    """ The run() method will be started and it will run in the background until the main program exits"""

    def __init__(self, interval=600):
        self.interval = interval
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            if os.name == "nt":
                cmdStr = 'tasklist /V /FI "IMAGENAME eq Adobe CEF Helper.exe"'
            else:
                cmdStr = "top -stats pid,command,mem -l 1 | grep 'Adobe\ CEF\ Helper\|COMMAND'"
            config.logObj.info("Running the thread module")
            process = subprocess.Popen(cmdStr, shell = True, stdout = subprocess.PIPE)
            stdoutput = process.communicate()[0]
            config.threadDataStream += "-----------------------------------------------------------------------------------------------------------------<br>"
            for i in stdoutput.split('\n'):
                config.threadDataStream += str(i)+"<br>"
            config.threadDataStream += "<br>"
            time.sleep(self.interval)
