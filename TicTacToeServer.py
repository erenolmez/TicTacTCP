import socket
import threading
import sys
from random import randint

# global variables
game_not_over = True
clients = []
lock = threading.Lock()
board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
current_turn = 0  # Player 0 starts the game originally, it can be changed
# if we want to start order randomly generated, the below code will be uncommented
# current_turn = (randint(0,1))
symbols = ['X', 'O']
chat_mode = False  # Needs to be true to enable chat mode

def send_message(client, message):
    client.sendall(message.encode())

def send_board_state(client):
    global clients
    global board
    global current_turn

    message = "State of the board:\n"
    message += " —————————" + "\n"
    message += " " + board[0][0] + " | " + board[0][1] + " | " + board[0][2] + "\n"
    message += " " + board[1][0] + " | " + board[1][1] + " | " + board[1][2] + "\n"
    message += " " + board[2][0] + " | " + board[2][1] + " | " + board[2][2] + "\n"
    send_message(client, message)

# initial board state
for i in range(3):
    for j in range(3):
        board[i][j] = "_"

def validate_move(player_id, row, col):
    global board
    if player_id == current_turn:
        if row < 0 or row > 2 or col < 0 or col > 2:
            return False
        if board[row][col] == '_':
            return True
    return False

def make_move(player_id, row, col):
    global board
    global current_turn
    board[row][col] = symbols[player_id]
    current_turn = (current_turn + 1) % 2

def handle_client_move(client, player_id, move):
    global clients
    global current_turn
    global game_not_over
    global board
    global chat_mode

    if move.startswith("chat"):
        chat_message = move.split(" ", 1)[1]
        broadcast_message(client, f"Chat message: {chat_message}\n")
        return

    try:
        row, col = map(int, move.split(','))
        if player_id != current_turn:
            send_message(client, "It's not your turn!\n")
            print(f"Received {symbols[player_id]} on {row, col}. It is an illegal move.\n")
            return
    except:
        send_message(client, "Invalid move format! Please enter row and column numbers separated by a comma.\n")
        return

    if validate_move(player_id, row, col):
        print(f"Received {symbols[player_id]} on {row, col}. It is a legal move.\n")
        make_move(player_id, row, col)
        for client in clients:
            if player_id != current_turn:
                message = f"Turn information: Player {current_turn}'s turn!\n"
                send_message(client, message)
            send_board_state(client)
        if check_winner():
            print(f"Player {player_id} wins!\n")
            send_message(client, f"Player {player_id} wins!\n")
            game_not_over = False
            for other_client in clients:
                if other_client != client:
                    send_message(other_client, f"Player {player_id} wins!\n")
        elif check_draw():
            print("It's a draw!\n")
            send_message(client, "It's a draw!\n")
            game_not_over = False
            for other_client in clients:
                if other_client != client:
                    send_message(other_client, "It's a draw!\n")
        elif chat_mode:
            broadcast_message(client, f"Chat message: {move}\n")
            chat_mode = False
    else:
        print(f"Received {symbols[player_id]} on {row, col}. It is an illegal move.\n")
        send_message(client, "This is an illegal move. Please change your move!\n")

def broadcast_message(sender_client, message):
    for client in clients:
        if client != sender_client:
            send_message(client, message)

def check_winner():
    global board
    for i in range(3):
        if board[i][0] != '_' and board[i][0] == board[i][1] == board[i][2]:
            return True
        if board[0][i] != '_' and board[0][i] == board[1][i] == board[2][i]:
            return True
    if board[0][0] != '_' and board[0][0] == board[1][1] == board[2][2]:
        return True
    if board[0][2] != '_' and board[0][2] == board[1][1] == board[2][0]:
        return True
    return False

def check_draw():
    global board
    for row in board:
        if '_' in row:
            return False
    return True

def thread_run(client, player_id):
    counter = 1
    global game_not_over
    global current_turn
    send_message(client, f"Connected to the server.\n")
    send_message(client, f"Retrieved symbol {symbols[player_id]} and ID={player_id}.\n")
    cond = True
    while game_not_over:
        if player_id == current_turn:
            send_message(client, "Turn information: Your turn!\n")
            if counter == 1:
                send_board_state(client)
                counter = 0
            cond = True
        elif cond:
            send_message(client, f"Turn information: Player {current_turn}'s turn!\n")
            if counter == 1:
                send_board_state(client)
                counter = 0
            cond = False
        move = client.recv(1024).decode().strip()
        handle_client_move(client, player_id, move)

    client.close()

def accept_connections(server_socket):
    global game_not_over
    while game_not_over:
        client, addr = server_socket.accept()
        print("Accepted connection from:", addr)
        with lock:
            player_id = len(clients)
            clients.append(client)

        print(f"A client is connected, and it is assigned with the symbol {symbols[player_id]} and ID={player_id}.\n")
        if len(clients) == 2:
            print("The game is started.\n")
        threading.Thread(target=thread_run, args=(client, player_id)).start()

def main():
    if len(sys.argv) != 2:
        print("Usage: python TicTacToeServer.py <port_number>")
        return

    host = '127.0.0.1'
    port = int(sys.argv[1])

    # forming server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)  # listening for the two clients

    threading.Thread(target=accept_connections, args=(server_socket,)).start()

    # waiting until the game is over
    input("Press Enter to end the game\n")
    global game_not_over
    game_not_over = False

    # closing the socket
    server_socket.close()

if __name__ == '__main__':
    main()