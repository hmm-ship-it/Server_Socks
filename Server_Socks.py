#!/bin/bash/python3
'''
This is a simple webserver based on the sockets library
@Author Tim Hanneman
@Date MAR 19 2020
@License GPLv2

@TODO: Make subclasses that define the server type.
@TODO: Add a way for the server to be shutdown gracefully
@TODO: How should I jail this code?
@TODO: Get commandline arguments for setting ip and port
@TODO: Don't rebuild the index every server restart....
@TODO: Make the build_Index code more flexible..and protected
@TODO: Create modules with known types of vulnerabilities for cyber security practice

import socket
import os
import Defs
import hashlib
import logging as log

class Server_Socks:
  'Defines a socket, port and address, to setup a server.'
   
   #These variables define the defaults. You should use the methods to access them.
  __host_addr = '127.0.0.1'
  __host_port = 8080
  __ASSET_DIRECTORY = 'WWW'
  __SOCK_DRAWER_FILE_INDEX = {}

  ##Maybe this will work for logging???
  opticon = log.getLogger(__name__)

  # Constructor, designed essentially to run the lanch_options method
  # Via the Server_Socks class itself, console, or from other code.
  def __init__(self, noConfig=False, addr='127.0.0.1', port=8080):
    #log.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', level=log.INFO)
    #self._start_Log()
    log.warning('Server starting up.}')
    self._build_Index()
    self._set_File_Index()
    self.launch_options(noConfig, addr, port)

  # After starting up and doing the config, let's point python to another directory
  # Maybe that will give it a bit more security?
  def _set_Working_Directory(self):
    try:
      __cwd = './' + self.__ASSET_DIRECTORY
      log.warning('Changing working directory to %s}', __cwd)
      os.chdir(__cwd)
      return __cwd
    except:
      log.warning('Setting the working directory failed. Is this Windows?}')
      __cwd = '.\\' + self.__ASSET_DIRECTORY
      os.chdir(__cwd)
      return __cwd

  # Sets the server listening address
  def set_Addr(self, addr):
    self.__host_addr = addr
    #print("setting address to : " + str(self.get_Addr()) + "}")
    log.info("setting address to : %s}", self.get_Addr())

  # Get the server listening address
  def get_Addr(self):
    return self.__host_addr
   
  # Set the port to listen on
  def set_Port(self, port):
    self.__host_port = port
    #print("setting the port to: " + str(self.get_Port()) + "}")
    log.info("setting the port to: %s}", str(self.get_Port()))

  # Get the port that the server listens on
  def get_Port(self):
    return self.__host_port

  # Set both the address and the port that the server listens on
  def set_Both(self, addr, port):
    self.set_Addr(addr)
    self.set_Port(port)

  # Get the server files to serve index
  def _get_File_Index(self):
    return self.__SOCK_DRAWER_FILE_INDEX

  # Set the server files index
  def _set_File_Index(self):
    try:
      with open("sock_drawer.index", "r") as fi:
        for line in fi:
          (key, value)=line.split(',')
          self.__SOCK_DRAWER_FILE_INDEX[key]=value
        fi.close()
    except Exception as e:
      log.error('Setting the file index failed for some reason}')

  #This will build an index of files to serve.
  #WARNING THIS MUST BE RUN BEFORE ANYTHING ELSE...OTHERWISE IT WILL TRAVERSE
  #SOME RANDOM DIRECTORY.
  def _build_Index(self):
    log.info('rebuilding index}')
    try:
      log.info('removing any prior index}')
      os.remove("sock_drawer.index")
    except:
      log.info('Creating new index file}')

    f = open("sock_drawer.index", "a")
    cut_at = self.__ASSET_DIRECTORY+'/'
    crawl = os.getcwd() + '/' + cut_at
    for directory_name, sub_dir_list, fileList in os.walk(crawl):
      folder=directory_name.split(cut_at,1)
      for _ in fileList:
        name = (folder[-1]+'/'+_).encode()
        hashis = hashlib.sha512(name).hexdigest() + ',' + folder[-1]+'/'+_+'\n';
        f.write(hashis)
    f.close()

  # Launch options can be used several ways. 
  #
  # CASE 1) If no parameters are passed OR if noConfig is set to False.
  # It will first search for a configuration file. If no config file is found it will then set the default values, or the user supplied values.
  #
  # CASE 2) noConfig is set to True.
  # This will bring up a prompt, so that the user can enter in values they want to use. There is some code that will try auto set the ip for them.
  # No guarantee that the auto config works, especially on systems with multiple interfaces.
  def launch_options(self, noConfig=False, addr='127.0.0.1', port=8080):
    if(noConfig == False):
      #Begin by searching for a configuration file
      try:
        for root, dirs, files in os.walk(os.getcwd()):
          if '.config' in files:
            log.info('Starting from configuration file: }')
            cfg = open('.config')
            addr, port = cfg.readline().split()
            self.set_Both(addr, int(port))
            cfg.close()
            self._set_Working_Directory()
            return

      except:
        log.warning('Read from config failed}')

    elif noConfig:
      print("Enter IP (v4) and port to listen on, or try to auto detect with auto: \n>addr port")
      cli = input()
       
      if cli == 'auto':
        try:
          addr = socket.gethostbyname(socket.gethostname())
          self.set_Both(addr, 8080)
          #print('IP to use is:' + self.get_Addr() + " and the port will be " + str(self.get_Port()))
          log.info('IP to use is: %s and the port will be %s}', self.get_Addr(),str(self.get_Port()))
          self._set_Working_Directory()
          return

        except:
          log.warning('auto-config failed}')
          print("Enter IP (v4) and port to listen on, or try to auto detect with auto: \n>addr port")
          cli = input()
      else:
        try:
          addr, port = cli.split()
          self.set_Both(addr,int(port))
          self._set_Working_Directory()
          return

        except:
          log.info('invalid user input for starting config}')

    self.set_Both(addr,port)
    self._set_Working_Directory()

  # This creates a socket which is listened to.
  # It won't be useful unless you do something with
  # what you are listening to.
  #@Todo: Potentially allows you to create several sockets to listen on,
  #       if the ports and addr become some sort of list, or if you don't
  #       care what the values are after a socket is created.
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


  logFormat = log.Formatter('[%(levelname)s] - %(asctime)s - %(message)s')

  logFile = log.FileHandler("serverInteractions.log".format('~/', 'test_log1'))
  logFile.setFormatter(logFormat)
  console = log.StreamHandler()
  console.setFormatter(logFormat)

  root = log.getLogger()
  root.setLevel(os.environ.get("LOGLEVEL","INFO"))
  root.addHandler(console)
  root.addHandler(logFile)

  server = Server_Socks(True)
  server.create_Server
