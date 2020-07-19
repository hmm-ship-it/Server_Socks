#!/bin/python3
'''
This will contains the class code for accepting connections
It has been modularized to allow for variations in the code base.
@Author Tim Hanneman
@Date Jul 19 2020
@License GPLv2
'''
import logging as log


class Accept_Connection():
    def __init__(self):
        __VERSION__ = "v0.1_Accept"
        opticon = log.getLogger(__name__)

    def accept(c):
        #, server, sani_obj, get_obj
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
            c_socket.close()
            return 'Error';

        return request, c_socket

