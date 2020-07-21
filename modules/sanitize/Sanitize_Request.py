#!/bin/python3
'''
This module takes in a request and hashes it. It returns a hash.
@Author Timothy Hanneman
@Date July 18 2020
@License GPLv2
'''
import logging as log
import hashlib

    # This has problems when GET also has nothing with it
class Sanitize_Request():

    def __init__(self):
        __VERSION__ = "v0.1"
        opticon = log.getLogger(__name__)

    def sanitize(request):
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