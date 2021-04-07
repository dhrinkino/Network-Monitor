import socket
import time
import urllib.request
import json
from tcp_latency import measure_latency


class Sonda:
    def __init__(self, ip, server):
        #constructor 
        # private variables
        self.__ip = ip
        self.__server = server
        self.__json = dict()
        self.__json['client'] = ip;

    def check_monitor(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # ak do 5s neodpovie server, zlyha test
        sock.settimeout(5)
        try:
            result = sock.connect_ex((self.__server, 80))
        except:
            return False
        return True


    def speed(self,type):

        start_timestamp = time.time()

        if type == 50:
            speed_lenght = 50
            url = "http://"+self.__server+"/50M.bin"
        elif type == 100:
            speed_lenght = 100
            url = "http://"+self.__server+"/100M.bin"
        else:
            speed_lenght = 10
            url = "http://"+self.__server+"/10M.bin"
        try:
            urllib.request.urlretrieve(url, 'test.bin')
            
        except:
            self.__json['download'] = 0
            return 0

        end_timestamp = time.time()
        download_time = end_timestamp - start_timestamp
        final_speed =  ( (speed_lenght / download_time) * 8)
        self.__json['download'] = final_speed
        
        return final_speed

    def ping(self):
        lat = measure_latency(host=self.__server)
        try:
            self.__json['latency'] = str(int(lat[0]))
        except:
            self.__json['latency'] = str(500)
        return self.__json['latency']

    def save(self):
        print(json.dumps(self.__json))
        with open("out.json", "w") as jsonfile:  
            json.dump(self.__json, jsonfile)