import time
import re
from monitor_class import LatencyGraph, SpeedGraph, SondaServer


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
            
            server[s_ip] = dict()
            server[s_ip]["Latency"] = LatencyGraph(s_ip)
            server[s_ip]["Speed"] = SpeedGraph(s_ip)
            server[s_ip]["Server"] = SondaServer(s_ip)
            sonda_ip = sonda_file.readline()


    while 1:
        for sonda in server:
            print("-> "+sonda+" ")
            server[sonda]["Latency"].create()
            server[sonda]["Speed"].create()
            if server[sonda]["Server"].pull() == True:
                data = server[sonda]["Server"].getdict()
                print(data)
                server[sonda]["Speed"].update(data['download'])
                server[sonda]["Latency"].update(data['latency'])
            server[sonda]["Speed"].generate()
            server[sonda]["Latency"].generate()
        time.sleep(60)