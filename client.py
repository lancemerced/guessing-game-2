import socket

SERVER_HOST = "localhost"
SERVER_PORT = 7777

def play_game():
    client_socket = socket.socket()
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    print(client_socket.recv(1024).decode().strip())

    while True:
        user_input = input("").strip()
        client_socket.sendall(user_input.encode())
        reply = client_socket.recv(1024).decode().strip()
        if "Correct" in reply:
            print(reply)
            break
        print(reply)
        continue

    client_socket.close()

while True:
    play_game()
    print("\nDo you want to:")
    print("(A) Play Again")
    print("(B) Quit")
    choice = input("Enter key: ")
    if choice.upper() != "A":
        print("Thank you for playing!")
        break
