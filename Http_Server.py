#!/bin/python3
'''
This is an extention of Server_Socks that implements an http server
@Author Tim Hanneman
@Date MAR 20 2020
@License Copyright Tim Hanneman
'''
#@TODO: Clean-up logging events, and write them to standard error, put standard error into a logfile.
#@TODO: Thread the server...way to slow like this
#@TODO: Build an index of files it will serve. This will help prevent directory walking.

from Server_Socks import Server_Socks
import os
import Defs

class Http_Server(Server_Socks):

    def __init__(self, runOptions=False, addr='127.0.0.1', port=8080):
        self.launch_options(runOptions, addr, port)
        self.create_http_server()

    #@Todo:
    def sanitize_request(self, line):
        pass
    def get_request(self):
        pass
    def head_request(self):
        pass
    def post_request(self):
        pass


        return uri
        
    def create_http_server(self):
        c = self.create_Server()
        while 1:
            try:
                c_socket, c_address = c.accept()
                line_in = c_socket.recv(1024).decode('utf-8')
                print(c_address, end=" ")
                #cfile = c_socket.makefile('rw', 1024)
                #line = cfile.readline().strip()
                request = line_in.strip().split(' ')
                print("Request: " + str(request[:3]))
                status_code = request[0]
                uri_get = request[1]
                proto_ver = request[2]

                #print(status_code + " " + uri_get + " " + proto_ver + "Is this spliting properly?")
           
            except:
                print(" An error has occurred in processing the request")
                ##cfile.close()
                c_socket.close()
                continue
           
            if status_code == 'GET':
                #print(uri_get + " uri_get")
                if uri_get == '/':
                    uri_get='./index.html'

                else:
                    try:
                        uri_get = uri_get.split('?')[0]
                        uri_get = './' + str(uri_get).lstrip('/')
                        #print(uri_get + "  uri_get value")
                        #could possibly check for an empty string here in uri_get to set the default page
                    except:
                        print('Processing the uri failed')
                        continue
            else:
                #cfile.write('HTTP/1.0 501 Not Implemented')
                #cfile.close()
                c_socket.send('HTTP/1.0 501 Not Implemented '.encode('utf-8'))
                c_socket.close()
                continue

            try:
                #print(uri_get)
                get_file = open(str(uri_get), 'rb')
                response = get_file.read()
                get_file.close()

                if(uri_get.endswith(".jpg")):
                    mimetype = 'image/jpg'
                elif(uri_get.endswith(".css")):
                    mimetype = 'text/css'
                elif(uri_get.endswith(".png")):
                    mimetype = 'image/png'
                elif(uri_get.endswith(".svg")):
                    mimetype = 'image/svg'
                elif(uri_get.endswith(".gif")):
                    mimetype = 'image/gif'
                elif(uri_get.endswith(".midi")):
                    mimetype = 'audio/sp-midi'
                elif(uri_get.endswith(".mp3")):
                    mimetype = 'audio/mpeg'
                elif(uri_get.endswith(".ogg")):
                    mimetype = 'audio/ogg'
                else:
                    mimetype = 'text/html'

                header = 'HTTP/1.0 200 OK\n' + 'Content-Type: ' + str(mimetype) + '\n\n'
                final_response = header.encode('utf-8') + response
                c_socket.send(final_response)
                c_socket.close()

            except:
                print(' Reading and sending the uri failed')
                continue
         

         
        c_socket.close()

if __name__=='__main__':
    sock = Http_Server(True)
