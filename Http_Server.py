#!/bin/python3
'''
This is an extention of Server_Socks that implements an http server
@Author Tim Hanneman
@Date July 19 2020
@License GPLv2
'''
#@TODO: It works, but basically just for the default case. Make sure it works for everything.
#=========================Less important ==============================================
#@TODO: Enforce stricter scope on things?
#@TODO: Upgrade to httpv2 at some point, track timeouts for more efficient server/socket resource usage.
#@TODO: (Use stateful connection for multiple transfers)

from Server_Socks import Server_Socks
import hashlib
import os
from modules.Defs import http_header
#from multiprocessing.dummy import Pool as ThreadPool
import threading
#import time
import logging as log
import atexit

from modules.accept.Accept_Connection import Accept_Connection
from modules.sanitize.Sanitize_Request import Sanitize_Request
from modules.requests.Get_Request import Get_Request
from modules.requests.Request import Request

class Http_Server(Server_Socks):
    opticon = log.getLogger(__name__)
    _thread_count = 0
    __VERSION__ = "v0.1"

    def __init__(self, runOptions=False, addr='127.0.0.1', port=8080):
        
        #Each Http_Server instance will select the specific object type for these variables
        #But all server instances will need these therefore they are assigned at initialization.
        get_request_obj= None
        sanitize_request_obj = None
        accept_connection_obj = None
        request_obj = None
        http_header_obj = None

        log.warning('Server starting up.}')
        self._build_Index()
        self._set_File_Index()
        self.launch_options(runOptions, addr, port)
        self.server_parameters()
        self.create_http_server()
        atexit.register(log.warning,"Shutting down")
        


    def server_parameters(self):
        # Lets start with just loading what exists, and it can be parameterized later
        # This part of the code is in charge of creating the objects that will be used
        # to create the specific instance of this server.
        self.get_request_obj = Get_Request
        self.sanitize_request_obj = Sanitize_Request
        self.accept_connection_obj = Accept_Connection
        self.request_obj = Request
        self.http_header_obj = http_header
        #self._set_Working_Directory

    def modules_to_thread(self, c):
        request, c_socket = self.accept_connection_obj.accept(c)
        request_type, sani = self.sanitize_request_obj.sanitize(request)
        self.request_obj.what_request(self, request_type, sani, c_socket, self.get_request_obj)


    def create_http_server(self):

        threads_list = []
        c = self.create_Server()

        while 1:
            _thread_count = threading.enumerate()
            #print(len(_thread_count))
            if len(_thread_count) < 50:
                t2 = threading.Thread(target=self.modules_to_thread, args=(c,), daemon=True)
                threads_list.append(t2)
                t2.start()
                t2.join()
        
        t2.join()

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
