import socket
import threading
from queue import Queue

## global variable to kill the server

def main():
    print('server : started')
    UDP_IP = '0.0.0.0'
    UDP_PORT = 7345
    
    kill_udp = Queue()
    kill_udp.put(False)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((UDP_IP, UDP_PORT))

    print(f'server : listening on {UDP_IP}:{UDP_PORT}')
    inputlistener = threading.Thread(target=input_start, args=(kill_udp, ))
    udpserver = threading.Thread(target=server_start, args=(s, UDP_IP, UDP_PORT, kill_udp))
    inputlistener.start()
    udpserver.start()
    inputlistener.join()
    udpserver.join()
    s.close()
    

def input_start(q):
    print('command line listening')
    while True:
        inp = input()
        if 'kill' == inp:
            q.put(True)
            break
    return

def server_start(sock, ip, port, q):
    
    print('server thread started')
    # s.listen()
    kill = False
    connections = []
    # print('Connection address:', addr)
    while True:
        if True == q.get():
            break
        else:
            q.put(False)
        print(kill)
        data, connection = sock.recvfrom(4096)
        print(data)
        command = ''
        try:
            command = data.decode('UTF-8')
        except:
            pass
        
        if 'INIT_CONN' == command:
            print('connection added : ', connection)
            if connection not in connections:
                connections.append(connection)
        elif 'CLOSE_CONN' == command:
            print('connection removed : ', connection)
            connections.remove(connection)
        else:
            for conn in connections:
                print(f'send data : {data} to {conn}')
                sendsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sendsock.connect(conn)
                sendsock.send(data)
                sendsock.close()
    return


if __name__ == '__main__':
    main()

    # print('new connection from ', connection)
    # while data = conn.recv(BUFFER_SIZE):
    #     print("received data:", data)
    #     conn.send(data)  # echo
    # conn.close()