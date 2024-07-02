# Peer to peer encrypted terminal chat box using the my own rsa like encryption algorithm


import socket
import threading
import my_rsa

# Generated new public and private keys and stored them in seperate variables
public_key, private_key = my_rsa.newkeys()
public_partner = None

choise = input('Do you want to host(1) or to connect(2): ')

if choise == '1':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # In this project, we are going to connect as both the host and the clint. Hence used the local host IP address
    server.bind(('127.0.0.1', 31415))
    server.listen()

    clint, address = server.accept() # Accepted function to accept the connection from the clint
    clint.send((my_rsa.save_pkcs1(public_key)).encode())  # Sending our public key to the clint
    public_partner = my_rsa.load_pkcs1(clint.recv(1024).decode())  # Receiving the clint's public key

elif choise == '2':
    clint = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clint.connect(('127.0.0.1', 31415))  # Connecting to the host
    public_partner = my_rsa.load_pkcs1(clint.recv(1024).decode())  # Receiving the host's public key
    clint.send((my_rsa.save_pkcs1(public_key)).encode())  # Sending our public key to the host

else:
    print('Invalid choise')
    exit()

# Function to send messages
def sending_msg(clint):
    while True:  # An infinite loop for sending as many msgs as we want
        message = my_rsa.encrypt(input(), public_partner)
        clint.send(message.encode())

# Function for receiving messages
def receiving_msg(clint):
    while True:  # An infinite loop for receiving all the messages that our partner sends
        print('Partner: ' + my_rsa.decrypt(clint.recv(1024).decode(), private_key))
 

 # Initiating threads to run the send and receive functions simultaniously
threading.Thread(target=sending_msg, args=(clint,)).start()
threading.Thread(target=receiving_msg, args=(clint,)).start()