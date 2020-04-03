#!/bin/python3
'''
This file contains definitions used by this project
@Author Alex Khristov
@Date 30 MAR 2020
@License Copyright Alex Khristov
'''

# HTTP/1.0
HTTP_10 = {
    status_200: 'HTTP/1.0 200 OK',
    status_201: 'HTTP/1.0 201 Created',
    status_202: 'HTTP/1.0 202 Accepted',
    status_204: 'HTTP/1.0 204 No Content',
    #
    status_300: 'HTTP/1.0 300 Multiple Choices',
    status_301: 'HTTP/1.0 301 Moved Permanently',
    status_302: 'HTTP/1.0 302 Moved Temporarily',
    status_304: 'HTTP/1.0 304 Not Modified',
    #
    status_400: 'HTTP/1.0 400 Bad Request',
    status_401: 'HTTP/1.0 401 Unauthorized',
    status_403: 'HTTP/1.0 403 Forbidden',
    status_404: 'HTTP/1.0 404 Not Found',
    #
    status_500: 'HTTP/1.0 500 Internal Server Error',
    status_501: 'HTTP/1.0 501 Not Implemented',
    status_502: 'HTTP/1.0 502 Bad Gateway',
    status_503: 'HTTP/1.0 503 Service Unavailable',
}

# HTTP/1.1 -- RFC 7231
HTTP_11 = {                                                     # Defined in...  
    status_100: 'HTTP/1.1 100 Continue',                        # Section 6.2.1
    status_101: 'HTTP/1.1 101 Switching Protocols',             # Section 6.2.2
    #
    status_200: 'HTTP/1.1 200 OK',                              # Section 6.3.1
    status_201: 'HTTP/1.1 201 Created',                         # Section 6.3.2
    status_202: 'HTTP/1.1 202 Accepted',                        # Section 6.3.3
    status_203: 'HTTP/1.1 203 Non-Authoritative Information',   # Section 6.3.4
    status_204: 'HTTP/1.1 204 No Content',                      # Section 6.3.5
    status_205: 'HTTP/1.1 205 Reset Content',                   # Section 6.3.6
    status_206: 'HTTP/1.1 206 Partial Content',                 # Section 4.1 of [RFC7233]
    #
    status_300: 'HTTP/1.1 300 Multiple Choices',                # Section 6.4.1 
    status_301: 'HTTP/1.1 301 Moved Permanently',               # Section 6.4.2 
    status_302: 'HTTP/1.1 302 Found',                           # Section 6.4.3 
    status_303: 'HTTP/1.1 303 See Other',                       # Section 6.4.4 
    status_304: 'HTTP/1.1 304 Not Modified',                    # Section 4.1 of [RFC7232]
    status_305: 'HTTP/1.1 305 Use Proxy',                       # Section 6.4.5 
    status_307: 'HTTP/1.1 307 Temporary Redirect',              # Section 6.4.7 
    #
    status_400: 'HTTP/1.1 400 Bad Request',                     # Section 6.5.1 
    status_401: 'HTTP/1.1 401 Unauthorized',                    # Section 3.1 of [RFC7235]
    status_402: 'HTTP/1.1 402 Payment Required',                # Section 6.5.2 
    status_403: 'HTTP/1.1 403 Forbidden',                       # Section 6.5.3 
    status_404: 'HTTP/1.1 404 Not Found',                       # Section 6.5.4 
    status_405: 'HTTP/1.1 405 Method Not Allowed',              # Section 6.5.5 
    status_406: 'HTTP/1.1 406 Not Acceptable',                  # Section 6.5.6 
    status_407: 'HTTP/1.1 407 Proxy Authentication Required',   # Section 3.2 of [RFC7235]
    status_408: 'HTTP/1.1 408 Request Timeout',                 # Section 6.5.7 
    status_409: 'HTTP/1.1 409 Conflict',                        # Section 6.5.8 
    status_410: 'HTTP/1.1 410 Gone',                            # Section 6.5.9 
    status_411: 'HTTP/1.1 411 Length Required',                 # Section 6.5.10
    status_412: 'HTTP/1.1 412 Precondition Failed',             # Section 4.2 of [RFC7232]
    status_413: 'HTTP/1.1 413 Payload Too Large',               # Section 6.5.11
    status_414: 'HTTP/1.1 414 URI Too Long',                    # Section 6.5.12
    status_415: 'HTTP/1.1 415 Unsupported Media Type',          # Section 6.5.13
    status_416: 'HTTP/1.1 416 Range Not Satisfiable',           # Section 4.4 of [RFC7233]
    status_417: 'HTTP/1.1 417 Expectation Failed',              # Section 6.5.14
    status_426: 'HTTP/1.1 426 Upgrade Required',                # Section 6.5.15
    #
    status_500: 'HTTP/1.1 500 Internal Server Error',           # Section 6.6.1
    status_501: 'HTTP/1.1 501 Not Implemented',                 # Section 6.6.2
    status_502: 'HTTP/1.1 502 Bad Gateway',                     # Section 6.6.3
    status_503: 'HTTP/1.1 503 Service Unavailable',             # Section 6.6.4
    status_504: 'HTTP/1.1 504 Gateway Timeout',                 # Section 6.6.5
    status_505: 'HTTP/1.1 505 HTTP Version Not Supported',      # Section 6.6.6
}

#MIME types
MIME_TYPES = {
    '.jpg': 'image/jpg',
    '.css': 'text/css',
    '.png': 'image/png',
    '.svg': 'image/svg',
    '.gif': 'image/gif',
    '.midi': 'audio/sp-midi',
    '.mp3': 'audio/mpeg',
    '.ogg': 'audio/ogg',
    '': 'text/html',
}
