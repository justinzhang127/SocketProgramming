from socket import *
import threading

serverName = '127.0.0.1'

tcpPort = 12000
udpPort = 5000

users = {"justin", "siya", "mongezi"}
onlineUsers = {}
groups = {}
lock = threading.Lock()

def udp_discovery():
    udpSocket = socket(AF_INET, SOCK_DGRAM)
    udpSocket.bind((serverName, udpPort)) #this is for my local machine for now
    print("UDP discovery running...")

    while True:
        message, clientAddress = udpSocket.recvfrom(1024)

        if message.decode() == "DISCOVER":
            response = f"CHAT_SERVER|{tcpPort}"
            udpSocket.sendto(response.encode(), clientAddress)

def tcp_server():
    serverSocket= socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', tcpPort))
    serverSocket.listen()
    print("TCP server running...")

    while True:
        connectionSocket, addr = serverSocket.accept()
        thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
        thread.start()

def handle_client(connectionSocket, addr):
    username = None

    while True:
        data = connectionSocket.recv(1024)
        if not data:
            break
        
        message = data.decode()
        parts = message.split("|")
        if len(parts) == 0:
            continue
        command = parts[0]

        # LOGIN
        if command == "LOGIN":
            reqUsername = parts[1]
            with lock:
                if reqUsername in onlineUsers or reqUsername not in users:
                    connectionSocket.send("ERROR".encode())
                else:
                    onlineUsers[reqUsername] = connectionSocket
                    username = reqUsername
                    connectionSocket.send("ACK".encode())
        elif command == "LOGOUT":
            with lock:
                if username in onlineUsers:
                    del onlineUsers[username] 
                connectionSocket.send("ACK".encode())
                break
        elif command == "JOIN_GROUP":
            groupName = parts[1]

            with lock:
                if groupName in groups:
                    groups[groupName].add(username)
                    connectionSocket.send("ACK".encode())
                else:
                    connectionSocket.send("ERROR".encode())
        elif command == "LEAVE GROUP":
            groupName = parts[1]
            with lock:
                if groupName in groups and username in groups[groupName]:
                    groups[groupName].remove(username)
                    connectionSocket.send("ACK".encode())
                else:
                    connectionSocket.send("ERROR".encode())
        elif command == "CREATE GROUP":
            groupName = parts[1]
            with lock:
                if groupName not in groups:
                    groups[groupName] = set()
                    groups[groupName].add(username) # assuming user becomes user in the group they created
                    connectionSocket.send("ACK".encode())
                else:
                    connectionSocket.send("ERROR".encode())



            
    with lock:
        if username and username in onlineUsers:
            del onlineUsers[username]
    connectionSocket.close()
    
if __name__ == "__main__":
    threading.Thread(target=udp_discovery, daemon=True).start()
    tcp_server()