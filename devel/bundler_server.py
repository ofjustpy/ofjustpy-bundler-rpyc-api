import sys
from rpyc.utils.server import ThreadedServer
import rpyc

class BundlerServer(rpyc.Service):
    _server:ThreadedServer

    def __init__(self):
        pass

    @staticmethod
    def set_server(inst):
        BundlerServer._server = inst

    def on__connect(self, conn):
        # code that runs when a connection is created
        # (to init the service, if needed)
        print("client connected")
        pass


    def exposed_build_bundle(self, utility_tags):
        """
        
        """
        print ("exposed_build_bundle called")
        return b'hello', b"random", b"shandom"

    def exposed_stop(self):
        if self._server:
            self._server.close()
        

if __name__ == "__main__":

    server_handle = ThreadedServer(BundlerServer(),
                                   port=int(sys.argv[1])
                                   )
    BundlerServer.set_server(server_handle)
    server_handle.start()
    print("Shutting down proxy server")
    
            
