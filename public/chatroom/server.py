import http.server
import socketserver
import os

directory_to_serve = './'

os.chdir(directory_to_serve)

PORT = 9000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving HTTP on port {PORT}")
    httpd.serve_forever()