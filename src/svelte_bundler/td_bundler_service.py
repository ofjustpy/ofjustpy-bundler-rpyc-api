import os
import rpyc
retry_counter = 0

server_port = 4561

import rpyc
import sys

server_port = 4561

class ConnectionManager:
    def __init__(self):
        self.retry_counter = 0
        self.conn = None

    def __enter__(self):
        while True:
            try:
                self.conn = rpyc.connect("127.0.0.1",
                                         server_port)
                break
            except Exception as e:
                self.retry_counter += 1
                if self.retry_counter == 6:
                    print("Unable to connect to bundler")
                    sys.exit()
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn is not None:
            try:
                self.conn.root.stop()
            except Exception as e:
                #print("Caught exception while stopping: ", e)
                pass
            finally:
                self.conn.close()

                
# def setup_connection():
#     while True:
#         try:
#             conn = rpyc.connect("localhost",
#                                 server_port
#                                 )
#             break
#         except Exception as e:
#             retry_counter += 1
#             pass
#         if retry_counter == 6:
#             print ("unable to connect to bundler")
#             sys.exit()

#     yield conn

#     try: 
#         conn.root.stop()
        
#     except Exception as e:
#         print ("caught exception ", e)


if __name__ == "__main__":
    with ConnectionManager() as conn:
        # Do something with conn
        x, y, z = conn.root.build_bundle("w-5")
        print(x)
        print (z)
