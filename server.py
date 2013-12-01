#!/usr/bin/env python
# coding: utf-8

import pyjsonrpc

def add(username, password):
    """Test function"""
    print username
    print password
    return ( "00:00:00:00:00:01", "10.0.0.2" )

class RequestHandler(pyjsonrpc.HttpRequestHandler):

    # Register public JSON-RPC methods
    methods = {
        "add": add
    }

# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = ('localhost', 8080),
    RequestHandlerClass = RequestHandler
)
print "Starting HTTP server ..."
print "URL: http://localhost:8080"
http_server.serve_forever()
