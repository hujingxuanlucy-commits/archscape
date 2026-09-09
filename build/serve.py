import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
from http.server import HTTPServer, SimpleHTTPRequestHandler
print('ArchScape on http://localhost:4318/archscape.html')
HTTPServer(('127.0.0.1', 4318), SimpleHTTPRequestHandler).serve_forever()
