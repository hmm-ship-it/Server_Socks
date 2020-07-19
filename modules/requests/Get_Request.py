#!/bin/python3
'''
This module processes a get request. Checks the index, and sends a webpage
@Author Timothy Hanneman
@Date July 18 2020
@License GPLv2
'''
#@TODO: Fix the way this finds the imports aka make it all into a package.

import logging as log
import hashlib
import os, sys
sys.path.append('D:\Programing\Personal\Server Socks')
import Defs
from Defs import http_header

class Get_Request():

    def __init__(self):
        __VERSION__ = "v0.1_GET"
        opticon = log.getLogger(__name__)


    def get(server, request_hash, c_socket):
        # set up variable for the response test later
        response = bytes("is_null", 'utf-8')

        try:
            if request_hash.hexdigest() in server._get_File_Index():
                indexed_request_is = '.' + server._get_File_Index()[request_hash.hexdigest()].rstrip()
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

 #'''   def update_request(self, c_socket):
 #       ## Be sure to update this method in parallel with 'accept_connection'
 #       line_in = c_socket.recv(1024).decode('utf-8')
 #       print(c_address, end=" ")
 #       log.info("%s }", )
 #       full_request = line_in.strip().split('\r\n')
 #       request = full_request[0].split(' ')
 #       log.info("%s Request: %s }", str(c_address),str(request[:3]))
 #       return request, full_request;'''