# Peer to peer encrypted terminal chat box using the actual rsa encryption


import socket
import threading
import rsa

# Generated new public and private keys and stored them in seperate variables
public_key, private_key = rsa.newkeys(1024)
public_partner = None

choise = input('Do you want to host(1) or to connect(2): ')

if choise == '1':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # In this project, we are going to connect as both the host and the clint. Hence used the local host IP address
    server.bind(('127.0.0.1', 31415))  
    server.listen()

    clint, address = server.accept()  # Accepted function to accept the connection from the clint
    clint.send(public_key.save_pkcs1("PEM")) # Sending our public key in .pem format to the clint
    public_partner = rsa.PublicKey.load_pkcs1(clint.recv(1024)) # Receiving the clint's public key

elif choise == '2':
    clint = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clint.connect(('127.0.0.1', 31415))  # Connecting to the host
    public_partner = rsa.PublicKey.load_pkcs1(clint.recv(1024)) # Receiving the host's public key
    clint.send(public_key.save_pkcs1("PEM"))

else:
    print('Invalid choise')
    exit()

# Function to send messages
def sending_msg(clint):
    while True: # An infinite loop for sending as many msgs as we want
        clint.send(rsa.encrypt(input().encode('ascii'), public_partner))

# Function for receiving messages
def receiving_msg(clint):
    while True: # An infinite loop for receiving all the messages that our partner sends
        print('Partner: ' + rsa.decrypt(clint.recv(1024), private_key).decode('ascii'))
 

# Initiating threads to run the send and receive functions simultaniously
threading.Thread(target=sending_msg, args=(clint,)).start()
threading.Thread(target=receiving_msg, args=(clint,)).start()