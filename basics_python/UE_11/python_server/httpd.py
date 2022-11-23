from http.server import HTTPServer, CGIHTTPRequestHandler

serveradresse = ("", 8000)
server = HTTPServer(serveradresse, CGIHTTPRequestHandler)

server.serve_forever()
