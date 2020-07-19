#!/bin/python3
'''
This is the base class for request types. It takes what sanitize has and sends
the request to the proper section of code for that type of request. e.g. GET
@Author Tim Hanneman
@Date Jul 19 2020
@License GPLv2
'''

import logging as log

class Request():
    
    def __init__():
        __VERSION__ = "v0.1_Request"
        opticon = log.getLogger(__name__)
        
    def what_request(server, request_type, sani, c_socket, get_obj):
            #This bit of code changes depending on what sanitize returns, this is already behind
        if request_type == 'UNK':
            log.debug(" An error has occurred in the request type}")
            try:
                c_socket.send(Defs.HTTP_10['status_501'].encode('utf-8'))
            except Exception as socket_error:
                log.debug("Unexpected socket error")
            c_socket.close()
            return 'Error';

        elif request_type == 'GET':
            get_obj.get(server, sani, c_socket)
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