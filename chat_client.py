import socket
import time
import threading

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 50001  # The port used by the server
FORMAT = 'utf-8'
ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT


def start_client():
    client_socket.connect((HOST, PORT))  # Connecting to server's socket

    starting_massage = client_socket.recv(1024).decode(FORMAT)
    choice = input(starting_massage)
    if choice == '3':
        return
    client_socket.send(choice.encode(FORMAT))
    print(client_socket.recv(1024).decode(FORMAT))
    if '1' in choice:  # the first option, connect to a chat
        name = input()
        client_socket.send(name.encode(FORMAT))  # send name
        print(client_socket.recv(1024).decode(FORMAT))
        while True:
            group_id = input()
            client_socket.send(group_id.encode(FORMAT))  # send group id
            message_serv = client_socket.recv(1024).decode(FORMAT)
            print(message_serv)
            if 'invalid' not in message_serv:
                break

        # send and validate password
        print(client_socket.recv(1024).decode(FORMAT))
        ok_pass = False
        while not ok_pass:
            password = input()
            client_socket.send(password.encode(FORMAT))
            validate_pass = client_socket.recv(1024).decode(FORMAT)
            if validate_pass == 'valid password':
                print(validate_pass + ' start chating (### to exit):')
                ok_pass = True
            else:
                print('password is invalid, please try again.')
    elif '2' in choice:     #the second option, make a new group ID
        name = input()
        client_socket.send(name.encode(FORMAT))  # send name

        print(client_socket.recv(1024).decode(FORMAT))
        password = input()
        client_socket.send(password.encode(FORMAT))  # send password

        print(client_socket.recv(1024).decode(FORMAT))

    else:
        print("nu nu nu!")
        client_socket.close()
        return
    # chating
    receiver = threading.Thread(target=client_rec_massage, args=(client_socket,))  # Creating new Thread object.
    receiver.start()  # Starting the new thread (<=> handling new client)
    client_sen_massage(client_socket, name)

    client_socket.close()  # Closing client's connection with server (<=> closing socket)


def client_rec_massage(client_socket):  # function that always listening to server
    while True:
        message = client_socket.recv(1024).decode(FORMAT)
        if '###' in message:
            print('Exit from server GoodBay :)')
            break
        print(message)


def client_sen_massage(client_socket, name):  # function that always listening to send
    while True:
        send_msg = name + ': ' + input()
        client_socket.send(send_msg.encode(FORMAT))
        if '###' in send_msg:
            break


if __name__ == "__main__":
    IP = socket.gethostbyname(socket.gethostname())
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    start_client()
