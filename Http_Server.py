#!/bin/python3
'''
This is an extention of Server_Socks that implements an http server
@Author Tim Hanneman
@Date MAR 20 2020
@License GPLv2
'''
#@TODO: It works, but basically just for the default case. Make sure it works for everything.
#@TODO: Enforce stricter scope on things.
#@TODO: Upgrade to httpv2 at some point, track timeouts for more efficient server/socket resource usage.
#@TODO: (Use stateful connection for multiple transfers)
#@TODO: Load index into RAM so it doesn't need to always read the file. (Maybe as an exception try and look for a file)

from Server_Socks import Server_Socks
import hashlib
import os
import Defs
from Defs import http_header
#from multiprocessing.dummy import Pool as ThreadPool
import threading
import time
import logging as log

class Http_Server(Server_Socks):
    opticon = log.getLogger(__name__)
    _thread_count = 0

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
        ## Be sure to update this method in parallel with 'update_request'
        try:
            c_socket, c_address = c.accept()
            line_in = c_socket.recv(1024).decode('utf-8')
            #log.warning(c_socket) Sometimes invalid bytes are sent through the decoder. This is a weakness if there is an exploit for it.
            full_request = line_in.strip().split('\r\n')
            request = full_request[0].split(' ')
            log.info("%s Request: %s }", str(c_address),str(request[:3]))

            #status_code = request[0]
            #uri_get = request[1]
            #proto_ver = request[2]
            #raise Exception('BAD')

        except Exception as socket_accept_error:
            log.warning(" An error has occurred in processing the connection attempt }")
            log.warning(socket_accept_error)
            #There was some other code for how to log exceptions that I should look at
            print(socket_accept_error)
            # c_socket.send(Defs.HTTP_10['status_501'].encode('utf-8'))
            c_socket.close()
            return 'Error';

        request_type, sani = self.sanitize_request(request)

        if request_type == 'UNK':
            log.debug(" An error has occurred in the request type}")
            try:
                c_socket.send(Defs.HTTP_10['status_501'].encode('utf-8'))
            except Exception as socket_error:
                log.debug("Unexpected socket error")
            c_socket.close()
            return 'Error';
        elif request_type == 'GET':
            self.get_request(sani, c_socket)
            c_socket.close()
            return;

        #I don't think this code should ever run
        else:
            log.info("Unrecognized request type}")
            try:
                c_socket.send(Defs.HTTP_10['status_501'].encode('utf-8'))
            except Exception as socket_error:
                log.debug("Unexpected socket error")
            c_socket.close()
            return 'Error';

    def update_request(self, c_socket):
        ## Be sure to update this method in parallel with 'accept_connection'
        line_in = c_socket.recv(1024).decode('utf-8')
        print(c_address, end=" ")
        log.info("%s }", )
        full_request = line_in.strip().split('\r\n')
        request = full_request[0].split(' ')
        log.info("%s Request: %s }", str(c_address),str(request[:3]))
        return request, full_request;

    # This has problems when GET also has nothing with it
    def sanitize_request(self, request):
        try:
            if request[0]== 'GET':
                if request[1]:
                    request_b = str(request[1]).encode()
                    request_hash = hashlib.sha512(request_b)
                return 'GET', request_hash
            else:
                request_b = str("/index.html").encode()
                request_hash = hashlib.sha512(request_b)
                return 'GET', request_hash

        except Exception as e:
            log.debug('Sanitize/Hash Failed: }')
            print(e)
            request_b = str("/index.html").encode()
            request_hash = hashlib.sha512(request_b)
            return 'GET', request_hash

    def get_request(self, request_hash, c_socket):

        # set up variable for the response test later
        response = bytes("is_null", 'utf-8')

        try:
            if request_hash.hexdigest() in self._get_File_Index():
                indexed_request_is = '.' + self._get_File_Index()[request_hash.hexdigest()].rstrip()
                mime = "." + indexed_request_is.split('.')[-1]
            else:
                indexed_request_is = '.' + '/index.html'
                mime = '.html'
        except Exception as hash_fail:
            log.info('Finding indexed page & default to serve failed }')
            print(hash_fail)
            return 'Error'

        try:
            get_file = open(str(indexed_request_is), 'rb')
            response = get_file.read()
            get_file.close()
        except:
            log.debug('reading file to send failed }')
            return 'Error'
            
        try:
            header = http_header(Defs.HTTP_11['status_200'], Defs.MIME_TYPES[mime], len(response))
        except Exception as e:

            log.debug('Header failed, likely invalid mime type. Add appropriate mime to defs.py }')
            header = http_header(Defs.HTTP_11['status_200'], Defs.MIME_TYPES['.html'], len(response))

        # test for valid response
        if response != b'is_null':
            final_response = header.to_string().encode('utf-8') + response
            c_socket.send(final_response)
            c_socket.close()

        return

    def head_request(self):
        pass
    def post_request(self):
        pass

    def create_http_server(self):

        threads_list = []
        c = self.create_Server()

        while 1:
            _thread_count = threading.enumerate()
            if len(_thread_count) < 50:
                t1 = threading.Thread(target=self.accept_connection, args=(c,))
                threads_list.append(t1)
                t1.start()
                #t1.join()

if __name__=='__main__':
    logFormat = log.Formatter('[%(levelname)s] - %(asctime)s - %(message)s')
    logFile = log.FileHandler("serverInteractions.log".format('~/', 'test_log1'))
    logFile.setFormatter(logFormat)
    console = log.StreamHandler()
    console.setFormatter(logFormat)

    root = log.getLogger()
    root.setLevel(os.environ.get("LOGLEVEL","DEBUG"))
    root.addHandler(console)
    root.addHandler(logFile)
    
    sock = Http_Server(True)
