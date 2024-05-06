import socket

host = "localhost"
port = 7777

def play_game():
    s = socket.socket()
    s.connect((host, port))

    print(s.recv(1024).decode().strip())

    while True:
        user_input = input("").strip()
        s.sendall(user_input.encode())
        reply = s.recv(1024).decode().strip()
        print(reply)
        if "Correct" in reply:
            break

    s.close()

while True:
    play_game()
    choice = input("\nDo you want to play again? (y/n): ").strip().lower()
    if choice != "y":
        print("Thank you for playing!")
        break
