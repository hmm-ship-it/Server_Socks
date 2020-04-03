#!/bin/bash/python3
'''
This is a simple webserver based on the sockets library
@Author Tim Hanneman
@Date MAR 19 2020
@License Copyright Tim Hanneman

@TODO: Split the createServer code into the creation of a socket and the type of server. Make a subclasses that define the server type.
@TODO: The default, acceptance and sending of objects needs improvement, seems to randomly fail sometimes
@TODO: Add a way for the server to be shutdown gracefully
@TODO: Sanitize web requests better for invalid input.
@TODO needs to be threaded, and test out how it fails.
@TODO: Can I chroot jail it?
@TODO: Get commandline arguments for setting ip and port
#DONE? Security audit, make sure it can only access files within it's directory.
#Seems like it is pretty resistant to accessing other parts of the hd. There might be ways around that though.
'''

import socket
import os
import Defs

class Server_Socks:
  'Defines a port and address to setup a server'
   
  __host_addr = '127.0.0.1'
  __host_port = 8080
  __ASSET_DIRECTORY = 'WWW'

  #@TODO: add parameters for add and port??? 
  def __init__(self, runOptions=False, addr='127.0.0.1', port=8080):
    self.launch_options(runOptions, addr, port)

  def _set_Working_Directory(self):
    try:
      __cwd = './' + self.__ASSET_DIRECTORY
      print('Changing working directory to' + __cwd)
      os.chdir(__cwd)
      return __cwd
    except:
      print('Setting the working directory failed. Is this Windows?')
      __cwd = '.\\' + self.__ASSET_DIRECTORY
      os.chdir(__cwd)
      return __cwd

  def set_Addr(self, addr):
    self.__host_addr = addr
    print("setting address to : " + str(self.__host_addr))

  def get_Addr(self):
    return self.__host_addr
   
  def set_Port(self, port):
    self.__host_port = port
    print("setting the port to: " + str(self.__host_port))

  def get_Port(self):
    return self.__host_port

  def set_Both(self, addr, port):
    self.set_Addr(addr)
    self.set_Port(port)

  def launch_options(self, runOptions=False, addr='127.0.0.1', port=8080):
    if(runOptions == False):
      #Begin by searching for a configuration file
      try:
        for root, dirs, files in os.walk(os.getcwd()):
          if '.config' in files:
            print('Starting from configuration file: ')
            cfg = open('.config')
            addr, port = cfg.readline().split()
            self.set_Both(addr, int(port))
            cfg.close()
            self._set_Working_Directory()
            return

      except:
        print('Read from config failed')

    elif runOptions:
      print("Enter IP (v4) and port to listen on, or try to auto detect with auto: \n>addr port")
      cli = input()
       
      if cli == 'auto':
        try:
          addr = socket.gethostbyname(socket.gethostname())
          self.set_Both(addr, 8080)
          print('IP to use is:' + self.get_Addr() + " and the port will be " + str(self.get_Port()))
          self._set_Working_Directory()
          return

        except:
          print('auto-config failed')
          print("Enter IP (v4) and port to listen on, or try to auto detect with auto: \n>addr port")
          cli = input()
      else:
        try:
          addr, port = cli.split()
          self.set_Both(addr,int(port))
          self._set_Working_Directory()
          return

        except:
          print('invalid input')

    self.set_Both(addr,port)

  def create_Server(self):
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    c.bind((self.get_Addr(),self.get_Port()))
    c.listen(1)
    return c

#def main(argv):
#  try:
#    opts, args = getopt.getopt(argv,"i" ["addr=","port="])
#  except getopt.GetoptError:
#    print("Options are:")
#    sys.exit(2)
        
if __name__ == '__main__':
#  import sys, getopt
#  main(sys.argv[1:])
#if((len(sys.argv)>0) and (len(sys.argv)<4)):
#arg_List = str(sys.argv).split()
#server = Server_Socks(bool(arg_List[0]),arg_List[1],int(arg_List[2]))

  server = Server_Socks(True)
  server.create_Server