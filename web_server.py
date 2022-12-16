from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import compare_db
import dumper


hostName = ""
serverPort = 8001

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        compareDB = compare_db.CompareDB()
        # print (compareDB)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(str(compareDB), "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")