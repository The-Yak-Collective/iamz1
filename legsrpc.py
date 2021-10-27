from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import time
import servo_util

PORTFORLEGS=9502 #position of each servo

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
with SimpleXMLRPCServer(('localhost', PORTFORLEGS),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    lastrecorded=(0,[])
    # Register a function under a different name
    def legpos():
        t=time.time()
        if t-lastrecorded[0]>0.1:
            lastrecorded=(t,servo_util.read_all_servo_pos)
        return lastrecorded

    server.register_function(legpos, 'legpos')

    # Run the server's main loop
    server.serve_forever()