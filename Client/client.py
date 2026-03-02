from socket import *
import threading 

udpPort = 5000

def discover_server(inputMessage):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    clientSocket.settimeout(5)

    message = inputMessage.encode()
    clientSocket.sendto(message, ('127.0.0.1', udpPort))

    try:
        data, serverAddress = clientSocket.recvfrom(1024)
        response = data.decode()
        print("Discovered:", response)

        parts = response.split("|")
        tcpPort = int(parts[1])

        return serverAddress[0], tcpPort
    except timeout:
        print("No server found")
        return None, None
    
def receive_message(socket):
    while True:
        try:
            data = socket.recv(1024)
            if not data:
                break
            print("\n>>>", data.decode())
        except:
            break

def main():
    discoverInput = input("Enter discover to connect to server:")
    if discoverInput == "DISCOVER":
        serverIP, tcpPort = discover_server(discoverInput)
    else:
        print("INVALID INPUT...")
        return

    if not serverIP:
        return 
    
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverIP, tcpPort))

    print("Connected")

    threading.Thread(target=receive_message, args=(clientSocket,), daemon=True).start()

    while True: 
        message = input()
        clientSocket.send(message.encode())

if __name__ == "__main__":
    main()