import socket
import threading
import sys

def receive_message(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
        except:
            break

def send_chat_message(client_socket):
    while True:
        message = input()
        if message.lower() == "chat":
            chat_message = input("Enter chat message: ")
            message = "chat " + chat_message
        client_socket.sendall(message.encode())

# tic tac toe label sign
def print_tic_tac_toe():
    print("╔═══════════════╗")
    print("║  TIC TAC TOE  ║")
    print("╚═══════════════╝")

def main():
    if len(sys.argv) != 2:
        print("Usage: python TicTacToeClient.py <port_number>")
        return

    host = '127.0.0.1'
    port = int(sys.argv[1])

    # Create a client socket and connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # thread for receiving messages (board state, warnings, turn information, etc.)
    threading.Thread(target=receive_message, args=(client_socket,)).start()

    print_tic_tac_toe()

    # chat message thread
    threading.Thread(target=send_chat_message, args=(client_socket,)).start()

    while True:
        # getting input from the players
        move = input()
        client_socket.sendall(move.encode())

    # Closing the socket
    client_socket.close()

if __name__ == '__main__':
    main()
