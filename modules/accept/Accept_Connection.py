#!/bin/python3
'''
This will contains the class code for accepting connections
It has been modularized to allow for variations in the code base.
'''
import logging as log
from modules.sanitize.Sanitize_Request import Sanitize_Request
from modules.requests.Get_Request import Get_Request

class Accept_Connection():
    def __init__(self):
        __VERSION__ = "v0.1_GET"
        opticon = log.getLogger(__name__)

    def accept(c, server, sani_obj, get_obj):
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

        #sani_obj = Sanitize_Request
        request_type, sani = sani_obj.sanitize(request)

        if request_type == 'UNK':
            log.debug(" An error has occurred in the request type}")
            try:
                c_socket.send(Defs.HTTP_10['status_501'].encode('utf-8'))
            except Exception as socket_error:
                log.debug("Unexpected socket error")
            c_socket.close()
            return 'Error';
        elif request_type == 'GET':
            #self.get_request(sani, c_socket)

            #get_obj = Get_Request.get(server, sani, c_socket)
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