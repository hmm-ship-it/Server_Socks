#!/bin/python3
'''
This is an extention of Server_Socks that implements an http server
@Author Tim Hanneman
@Date MAR 20 2020
@License GPLv2
'''
#@TODO: Clean-up logging events, and write them to standard error, put standard error into a logfile.
#@TODO: It works, but basically just for the default case. Make sure it works for everything.
#@TODO: Enforce stricter scope on things. 
#@TODO: Make a maximum thread count.
#@TODO: Upgrade to httpv2 at some point, track timeouts for more efficient server/socket resource usage.

from Server_Socks import Server_Socks
import hashlib
import os
import Defs
#from multiprocessing.dummy import Pool as ThreadPool
import threading
import time
import logging

class Http_Server(Server_Socks):
    log = logging.getLogger(__name__)

    def __init__(self, runOptions=False, addr='127.0.0.1', port=8080):
        
        #logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', level=logging.INFO)
        #self._start_Log()
        #self.get_logger()
        log.warning('Server starting up.}')
        self._build_Index()
        self._set_File_Index()
        self.launch_options(runOptions, addr, port)
        self.create_http_server()

    def accept_connection(self, c):
        try:
            c_socket, c_address = c.accept()
            line_in = c_socket.recv(1024).decode('utf-8')
            print(c_address, end=" ")
            log.info("%s ", str(c_address))
            request = line_in.strip().split(' ')
            print("Request: " + str(request[:3]))
            #status_code = request[0]
            #uri_get = request[1]
            #proto_ver = request[2]
            return c_socket, request;
        except Exception as socket_accept_error:
            print(" An error has occurred in processing the request")
            print(socket_accept_error)
            c_socket.close()
            return 1;

    def sanitize_request(self, request):
        try:
            if request[0]==1:
                return 1
            elif request[0]== 'GET':
                request_b = str(request[1]).encode()
                request_hash = hashlib.sha512(request_b)
                return request_hash
            else:
                return 1
        except Exception as e:
            print('Sanitize/Hash Failed: ' + e)

    def get_request(self, request_hash, c_socket):
        try:
            if request_hash.hexdigest() in self._get_File_Index():
                indexed_request_is = '.' + self._get_File_Index()[request_hash.hexdigest()].rstrip()
                mime = "." + indexed_request_is.split('.')[-1]
            else:
                indexed_request_is = '.' + '/index.html'
                mime = '.html'
        except Exception as hash_fail:
            print('Get_Request Failed ' + hash_fail)

        try:
            get_file = open(str(indexed_request_is), 'rb')
            response = get_file.read()
            get_file.close()
        except:
            print('reading file failed')
            
        try:
            header = Defs.HTTP_10['status_200'] + "\n" + 'Content-Type: ' + Defs.MIME_TYPES[mime] + '\n\n'
        except Exception as e:
            print('Header failed, likely invalid mime type. Add appropriate mime to defs.py')
            header = Defs.HTTP_10['status_200'] + "\n" + 'Content-Type: ' + Defs.MIME_TYPES['.html'] + '\n\n'

        final_response = header.encode('utf-8') + response
        c_socket.send(final_response)
        c_socket.close()


        return

    def head_request(self):
        pass
    def post_request(self):
        pass

        #umm remove this?
        return uri

    def process_Connection(self, c):
        c_socket, request = self.accept_connection(c)
        #If there is an error in accepting the request return.
        if request[0] == 1:
            c_socket.send(Defs.HTTP_10['status_501'].encode('utf-8'))
            c_socket.close()
            return 1
        else:
            self.get_request(self.sanitize_request(request),c_socket)
        c_socket.close()

    def create_http_server(self):

        threads_list = []
        c = self.create_Server()

        while 1:
            #print('New Thread btw')
            t1 = threading.Thread(target=self.process_Connection, args=(c,))
            threads_list.append(t1)
            t1.start()
            t1.join()

if __name__=='__main__':
    sock = Http_Server(True)