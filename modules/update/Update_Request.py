class Update_Request():
    def update_request(c_socket):
        ## Be sure to update this method in parallel with 'accept_connection'
        line_in = c_socket.recv(1024).decode('utf-8')
        print(c_address, end=" ")
        log.info("%s }", )
        full_request = line_in.strip().split('\r\n')
        request = full_request[0].split(' ')
        log.info("%s Request: %s }", str(c_address),str(request[:3]))
        return request, full_request;