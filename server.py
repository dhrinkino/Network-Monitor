import threading
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

# kedze standardny http handler je strasne narocny a robi mnoho veci ktore nepotrebujem, som si zvolil ze vyuzijem polymorfizmus v takom zmysle ze si upravim metodu do_GET ktora sa stara o GET pozriadavky a navrhnem si ju do vlastneho stylu
class JsonHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # standardizovana odpoved (200-OK)
        # classa BaseHTTPRequestHandler z ktorej som si vytiahol tuto funkciu ktora sa mi stara o odpovedanie na GET dotaz
        self.send_response(200)
        self.end_headers()
        # kedze web server je navrhnuty tak ze berie vstup v bytes a nefunguje str alebo dict
        # takze po nahrani subora do dict prevadzam do stringu a encodujem do bytes cez str
        with open('out.json',"r+") as json_file:
            try:
                json_content = json.load(json_file)
            except:
                json_content = "Invalid_data"
        www_cont = str.encode(str(json_content))
        self.wfile.write(www_cont)



# vytvara sa mi druhy thread ktory bezi na pozadi, kedze tento proces je pre mna "menej" dolezity
class WebThread(threading.Thread):
    def run(self):
        # spustenie http servera s vlastnym handlerom
        httpd = HTTPServer(('0.0.0.0', 8000), JsonHandler)
        httpd.serve_forever()

        