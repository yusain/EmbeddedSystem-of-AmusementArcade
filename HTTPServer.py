from http.server import HTTPServer, BaseHTTPRequestHandler
import time
HOST = "192.168.47.1"
PORT = 9999

class NeuralHttp(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        self.wfile.write(bytes("<html><body><h1>HELLO WORD</h1></body></html", "utf-8"))

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        date = time.strftime("%Y-%m %H:%M:", time.localtime(time.time()))
        self.wfile.write(bytes('{"time":"'+ date +'"}', "utf-8"))
server = HTTPServer((HOST, PORT), NeuralHttp)
print ("Server now running...")

server.serve_forever()
server.server_close()
print ("Server stopped...")
#161655116161

