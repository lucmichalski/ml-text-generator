from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path
from titlegen import TitleGenerator
import json, io, sys

WEB_ROOT = 'static'

TGEN = None

class TheGarlicServer(BaseHTTPRequestHandler):
    mimeTypes = {
        'txt': 'text/plain',
        'html': 'text/html',
        'css': 'text/css',
        'js': 'application/javascript',
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'ico': 'image/x-icon'
    }

    def do_GET(self):
        if self.path.startswith('/api/post.json'):
            titles = dict(titles=[TGEN.generateTitle() for _ in range(5)])
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(titles).encode('utf-8'))
        else:
            filepath = self.path
            if filepath.endswith('/'):
                filepath += 'index.html'
            filepath = WEB_ROOT + path.join(*('.' + filepath).split('/'))[1:]
            try:
                ext = filepath.split('.')[-1]
                with io.open(filepath, 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-Type', self.mimeTypes.get(ext, 'application/octet-stream'))
                    self.end_headers()
                    self.wfile.write(f.read())
            except Exception as e:
                self.send_response(404)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(('404 ' + self.path).encode('utf-8'))

if __name__ == '__main__':
    TGEN = TitleGenerator(150)
    server_address = ('127.0.0.1', 9420)
    if len(sys.argv) > 1:
        server_address = ('', int(sys.argv[1]))
    httpd = HTTPServer(server_address, TheGarlicServer)
    print('running server...')
    httpd.serve_forever()