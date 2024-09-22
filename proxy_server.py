from socket import *
import select
import sys

if len(sys.argv) <= 1:
    #print('Usage : "python3 ProxyServer.py server_ip"')
    print(f'Usage : python3 {sys.argv[0]} IP Port')
    print('[IP : It is the IP Address Of Proxy Server')
    sys.exit(2)

#for i in range(len(sys.argv)):
#    print(f'argv[{i}] = {sys.argv[i]}')

serverName = sys.argv[1]
serverPort = int(sys.argv[2])

#if len(sys.argv) > 
#serverPort = 8888

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((serverName, serverPort))
tcpSerSock.listen(1)
print('Listening on port %s ...' % serverPort)

good_target_host = ''
while True:    
    # Start receiving sata from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()

    print('Received a connection from:', addr)
    # Get the client request

    message = ''

    # use select to stop the recv from hanging
    msg_select = True
    if msg_select:
        tcpCliSock.setblocking(False)
        timeout = 5.0
        while True:
            ready = select.select([tcpCliSock], [], [], timeout)
            if ready[0]:
                partial = tcpCliSock.recv(1024).decode()
                if not partial:
                    break
                message += partial
            else:
                break
        if len(message) == 0:
            #print('len(message):', len(message))
            tcpCliSock.close() # our socket to the client (Chrome)
            continue
    else:
        message = tcpCliSock.recv(1024).decode()
    print(f'message - {message}')

    # Send HTTP response
    filename = message.split()[1].partition("/")[2]
    print('filename:', filename)
    filetouse = "/" + filename
    print('filetouse:', filetouse)
    #tcpCliSock.sendall(filename.encode())
    
    #get target_host from filename
    target_host = ''
    for i, line in enumerate(message.split('\n')):
        line_split = line.split()
        if line_split:
            #print(i, str(line_split))
            if line.split()[0] == 'Host:':
                target_host = line.split()[1]
                #print('target_host:', target_host)
    print('target_host:', target_host)
    print('serverName:', serverName)

    host = target_host.split(':')[0]
    print('host:', host)

    if host == serverName:
        print('We are target_host...')
        target_host = filename.split('/')[0]
    print('New target_host:', target_host)

    #get target_path from filename
    path = filetouse.split('/')
    clean_path_list = []
    clean_target_path = '/'
    for item in path:
        #print('item:', item)
        if item != target_host:
            #clean_path_list.append('/')
            clean_path_list.append(item)
            #print('list:', clean_path_list)
    for item in clean_path_list:
        clean_target_path += '/'
        clean_target_path += item
    #clean_target_path = '/'.join(clean_path_list)
    print('clean_target_path:', clean_target_path)


    # create socket and bind socket on port 80
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # trying this to keep sockets from waiting too long
    # https://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method
    # https://docs.python.org/3/library/socket.html#socket.socket.settimeout
    tcpCliSock.settimeout(5.0)


    # try to connect to the web host
    try:
        clientSocket.connect((target_host, 80))
        good_target_host = target_host
        print('good_target_host:', good_target_host)
    except gaierror:
        print(f'gaierrror - trying {good_target_host}')
        # need this or we might not see what we're trying
        sys.stdout.flush()
        clientSocket.connect((good_target_host, 80))
        target_host = good_target_host
        clean_target_path = filetouse
        print(f'Clean target host is - {clean_target_path}')

    # now we should be connected, so make the request

    request = f"GET {clean_target_path} HTTP/1.1\r\nHost:{target_host}\r\n\r\n"
    print('request:', request)
    clientSocket.sendall(request.encode())

    # trying this to speed up page loading
    # https://stackoverflow.com/questions/19741196/recv-function-too-slow
    tcpCliSock.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
    
    # use select to stop the recv from hanging
    use_select = True
    if use_select:
        print("use_select:", use_select)
        clientSocket.setblocking(False)
        tcpCliSock.setblocking(False)
        timeout = 5.0
        #clientSocket.settimeout(timeout)
        while True:
            #print("waiting for select to be ready")
            ready = select.select([clientSocket], [], [], timeout)
            if ready[0]:
                response = clientSocket.recv(2048)
                if not response:
                    break
                tcpCliSock.send(response)
            else:
                #print("len(response):", len(response))
                break
    else:        
        # set to true to collect all the responses before sending to client
        aggregate_response_before_sending = False

        if aggregate_response_before_sending:
            response = b'' 
            while True:
                partial = clientSocket.recv(32768)
                if not partial:
                    break
                #print(partial.decode())
                response += partial
            tcpCliSock.send(response)
        else:
            while True:
                partial = clientSocket.recv(32768)
                if not partial:
                    break
                tcpCliSock.send(partial)

    # finished forwarding responses to client, so close the sockets
    clientSocket.close() # our socket to the web host
    tcpCliSock.close() # our socket to the client (Chrome)

# Close socket
tcpSerSock.close() # our socket for accepting connections
