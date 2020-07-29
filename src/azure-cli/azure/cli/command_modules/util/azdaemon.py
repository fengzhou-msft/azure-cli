import time
from daemons.prefab import run

class AzDaemon(run.RunDaemon):

    def run(self):
        while True:
            print("I am a daemon...")
            time.sleep(10)