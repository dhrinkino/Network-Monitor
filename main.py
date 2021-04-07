import time
import json
from sonda import Sonda 
from server import WebThread
 
if __name__ == "__main__":
    # main funkcia 

    try:
        settings_file = open("settings.json", "r")
    except IOError:
        print("Nepodarilo sa otvorit subor")
        exit
    with settings_file:
        settings = json.load(settings_file)


    webthread = WebThread()
    webthread.start()


    sonda = Sonda(settings['ip'],settings['server']);
    
    while 1:
        if sonda.check_monitor():
            sonda.speed(10)
            sonda.ping()
            sonda.save()
            time.sleep(int(settings['interval']))
        else:
            print("Monitor is down")
    del sonda