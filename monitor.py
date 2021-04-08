import time
import re
from monitor_class import SondaCall, LatencyGraph, SpeedGraph, SondaServer



if __name__ == "__main__":

    try:
        sonda_file = open("sonda-list.txt", "r")                          
    except IOError:
        print("Nepodarilo sa otvorit subor so sondami")
        exit
    
    server = dict()
    with sonda_file:
        sonda_ip = sonda_file.readline()
        while sonda_ip:
            s_ip = sonda_ip.rstrip("\n")
            server[s_ip] = SondaCall(s_ip)
            sonda_ip = sonda_file.readline()


    while 1:
        for sonda in server:
            print("-> "+sonda+" ")
            server[sonda].Latency.create()
            server[sonda].Speed.create()
            if server[sonda].Server.pull() == True:
                data = server[sonda].Server.getdict()
                print(data)
                server[sonda].Speed.update(data['download'])
                server[sonda].Latency.update(data['latency'])
            server[sonda].Latency.generate()
            server[sonda].Speed.generate()
        time.sleep(60)