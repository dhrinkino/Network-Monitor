import json
import requests
import time
import rrdtool
import os.path

# caller classov a metod
class SondaCall():
    def __init__(self,s_ip):
        print(s_ip)
        self.Latency = LatencyGraph(s_ip)
        self.Speed = SpeedGraph(s_ip)
        self.Server = SondaServer(s_ip)


# tato trieda je skorej taky main template pre ostatne triedy, zahrna vsetky funkcie ktore su potrebne, dalej si robim vlastnu upravenu funkciu create
class Graph:
    def __init__(self,ip):
        self.ip = ip
    def generate(self):
        # vygenerovanie obrazku grafu, generuju sa 4 grafy. Day,Week,Month,Year
        rrdtool.graph( ""+self.filename+".png", "--start", "-24h",
        "DEF:ds1a="+self.filename+":ds1:AVERAGE",
        "LINE1:ds1a#0000FF:Hodnota"
        )
        rrdtool.graph( ""+self.filename+"-week.png", "--start", "-7d",
        "DEF:ds1a="+self.filename+":ds1:AVERAGE",
        "LINE1:ds1a#0000FF:Hodnota"
        )
        rrdtool.graph( ""+self.filename+"-month.png", "--start", "-31d",
        "DEF:ds1a="+self.filename+":ds1:AVERAGE",
        "LINE1:ds1a#0000FF:Hodnota"
        )
        rrdtool.graph( ""+self.filename+"-year.png", "--start", "-365d",
        "DEF:ds1a="+self.filename+":ds1:AVERAGE",
        "LINE1:ds1a#0000FF:Hodnota"
        )


    def update(self,value):
        try:
            rrdtool.update(self.filename, str(int(time.time()))+":"+str(value))
        except:
            print("Chyba pridavania do rrd")
            return False

# dedim z class Graph vsetky ostatne funkcie a pridavam si vlastnu create na latency
class LatencyGraph(Graph):

    def create(self):
        self.filename = self.ip + "-latency.rrd"
        # kontrola ci uz existuje nas rrd subor
        if os.path.isfile(self.filename) == False:
            # vytvorenie rrd db
            rrdtool.create(self.filename, '--start', 'now', '--step', '60', 'DS:ds1:GAUGE:600:U:U', 'RRA:AVERAGE:0.5:1:525600')
            # wait time, je to z dovodu aby nedoslo k nespravnej interpretacie
            time.sleep(30)
# dedim z class Graph vsetky ostatne funkcie a pridavam si vlastnu create na speed
class SpeedGraph(Graph):
    def create(self):
        self.filename = self.ip + "-speed.rrd"
        if os.path.isfile(self.filename) == False:
            rrdtool.create(self.filename, '--start', 'now', '--step', '60', 'DS:ds1:GAUGE:600:U:U', 'RRA:AVERAGE:0.5:1:525600')
            time.sleep(30)
    

# hlavna class na manipulacia s udajmi
class SondaServer:
    def __init__(self,ip):
        self.__ip = ip
        self.__dict = "";
    # ziskanie informacii
    def pull(self):
        # zadavanie url
        sonda_server = "http://" + self.__ip + ":8000"
        try:
            response = requests.get(sonda_server)
        except:
            # sonda je offline
            print("Sonda je nedostupna")
            return False
        try:
            self.__dict = json.loads(str(response.text).replace("'", '"'))
        except:
            # data sa zle prijali, nedokaze sa rozprarsovat json, neziskavaju sa ziadne udaje
            return False
        print("Get data success")
        return True

    # getter udajov / interface
    def getdict(self):
        # vratenie dictionary so vsetkymi udajmi
        return self.__dict
