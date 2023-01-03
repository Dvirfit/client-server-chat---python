# Dvir Fitoussi 315015073
import socket
import threading
import time

HOST = '127.0.0.1'  # Standard loopback IP address (localhost)
PORT = 50001  # Port to listen on (non-privileged ports are > 1023)
FORMAT = 'utf-8'  # Define the encoding format of messages from client-server
ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT

count_id = 0
connects = []
groups = {}  # {ID1:{conn:[conn1,conn2...],password:'12345',name:dvir},ID2:..}
massage_to_send = ''




# Function that starts the server
def start_server():
    server_socket.bind(ADDR)  # binding socket with specified IP+PORT tuple

    print(f"[LISTENING] server is listening on {HOST}")
    server_socket.listen()  # Server is open for connections

    while True:
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}\n")  # printing the amount of threads working

        connection, address = server_socket.accept()  # Waiting for client to connect to server (blocking call)
        thread = threading.Thread(target=client, args=(connection, address))  # Creating new Thread object.
        # Passing the handle func and full address to thread constructor
        thread.start()  # Starting the new thread (<=> handling new client)

        # print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}\n")  # printing the amount of threads working
        # on this process (opening another thread for next client to come!)


# Function that handles a single client connection
# Operates like an echo-server
def client(conn, addr):
    try:
        global count_id
        global groups
        conn.send(" 1- Connect to group chat\n 2- Create a group chat\n 3- Exit from server\n".encode(FORMAT))
        option = conn.recv(1024).decode(FORMAT)
        if '1' in option:
            conn.send(" What is your name?".encode(FORMAT))
            name = conn.recv(1024).decode(FORMAT)

            conn.send(" Enter group ID".encode(FORMAT))
            while True:
                group_id = conn.recv(1024).decode(FORMAT)
                print(groups.keys())
                print('groupid:' + group_id)
                if group_id not in groups.keys():
                    conn.send(" The ID is invalid, start over".encode(FORMAT))
                else:
                    conn.send(" The ID valid.".encode(FORMAT))
                    print(f'Got group ID: {group_id}')
                    break
            conn.send(" Enter group password".encode(FORMAT))
            while True:
                password = conn.recv(1024).decode(FORMAT)
                if groups[group_id]['password'] == password:
                    groups[group_id]['connections'].append(conn)
                    conn.send('valid password'.encode(FORMAT))
                    break
                else:
                    conn.send('invalid password'.encode(FORMAT))
        elif '2' in option:
            conn.send(" What is your name?".encode(FORMAT))
            name = conn.recv(1024).decode(FORMAT)
            conn.send(" What is your password?".encode(FORMAT))
            password = conn.recv(1024).decode(FORMAT)

            groups[str(count_id)] = {'connections': [conn], 'password': password,
                                     'threads': []}  # add the group with the password
            group_id = str(count_id)
            print('group id:' + str(count_id))
            conn.send(f"your ID is: ({count_id}); to exit send: ### start chat".encode(FORMAT))
            count_id += 1
        elif '3' in option:
            print("[CLIENT DISCONNECTED] on address: ", addr)
            return
        else:
            print('nu nu nu')
            return

    except Exception as e:
        print("[CLIENT CONNECTION INTERRUPTED] on address: ", addr)
        print(e)

    receiver = threading.Thread(target=sending_server, args=(conn, group_id))
    groups[group_id]['threads'].append(receiver)
    receiver.start()
    print(groups[group_id]['threads'])


def sending_server(conn, group_to_send):
    try:
        while True:
            print('into the while')
            mass_to_send = conn.recv(1024).decode(FORMAT)
            print('after the listening')
            for c in groups[group_to_send]['connections']:
                c.send(mass_to_send.encode(FORMAT))
                print(f'sent to: {c}: {mass_to_send}')
            if '###' in mass_to_send:
                groups[group_to_send]['connections'].remove(conn)
                return
    except Exception as e:
        print(e)



#################   Main  #####################
if __name__ == '__main__':
    IP = socket.gethostbyname(socket.gethostname())  # finding your current IP address

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Opening Server socket

    print("[STARTING] server is starting...")
    start_server()

    print("THE END!")












'''

def lisening_server(conn,grou):
    t = threading.Thread(target=sending_server, args=(conn, grou))
    groups[grou]['threads'].append(t)
    t.start()


def thread_activate(conn, group_to_send):
    return threading.Thread(target=sending_server, args=(conn, group_to_send)).start()

    for grou in groups.keys():
        # t_list = [threading.Thread(target=sending_server, args=(conn, group_to_send)).start() for conn in groups[grou]['connections']]
        print('grou '+grou)
        print(groups)
        for conn in groups[grou]['connections']:
            t = threading.Thread(target=sending_server, args=(conn, grou))
            groups[grou]['threads'].append(t)
            t.start()
        # t_list = [thread_activate(conn, grou) for conn in groups[grou]['connections']]
        print(groups[grou]['threads'])
        print(groups[grou]['conn'])
    print('hhhiiii')
        # for conn in groups[grou]['connections']:
        #     t_list.append(thread_activate())
        #     group_to_send = grou
        # if massage_to_send == '###':
        #     return
'''