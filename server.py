import socket
import random
import os

SERVER_HOST = ""
SERVER_PORT = 7777

WELCOME_MSG = """
== Welcome to the Number Guessing Game ==
Please enter your username:"""

def generate_random_number(low, high):
    return random.randint(low, high)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)

print(f"Server is listening on port {SERVER_PORT}")

LEADERBOARD_DIR = "leaderboards"
if not os.path.exists(LEADERBOARD_DIR):
    os.makedirs(LEADERBOARD_DIR)

leaderboard = {}

while True:
    conn, addr = server_socket.accept()
    print(f"New client connected: {addr[0]}")
    conn.sendall(WELCOME_MSG.encode())

    client_input = conn.recv(1024)
    username = client_input.decode().strip()

    conn.sendall(b"""
Choose difficulty level:
1. Easy (1-50)
2. Medium (1-100)
3. Hard (1-500)
Enter the corresponding number:""")

    client_input = conn.recv(1024)
    difficulty_level = int(client_input.decode().strip())
    if difficulty_level == 1:
        secret_number = generate_random_number(1, 50)
        leaderboard_filename = os.path.join(LEADERBOARD_DIR, "easy.txt")
    elif difficulty_level == 2:
        secret_number = generate_random_number(1, 100)
        leaderboard_filename = os.path.join(LEADERBOARD_DIR, "medium.txt")
    elif difficulty_level == 3:
        secret_number = generate_random_number(1, 500)
        leaderboard_filename = os.path.join(LEADERBOARD_DIR, "hard.txt")
    else:
        conn.sendall(b"Invalid choice. Please enter a number (1-3): ")
        conn.close()
        continue

    conn.sendall(b"Let's start the game!\nEnter your guess:")

    tries = 0
    while True:
        client_input = conn.recv(1024)
        guess = int(client_input.decode().strip())
        tries += 1
        print(f"User guess: {guess}")
        if guess == secret_number:
            conn.sendall(b"Correct Answer!")
            break
        elif guess > secret_number:
            conn.sendall(b"Guess Lower!\nEnter guess: ")
        elif guess < secret_number:
            conn.sendall(b"Guess Higher!\nEnter guess:")

    leaderboard[username] = tries

    with open(leaderboard_filename, "a") as leaderboard_file:
        leaderboard_file.write(f"{username}: {tries} tries\n")

    conn.close()

print("\n=== Leaderboard ===")
for filename in os.listdir(LEADERBOARD_DIR):
    with open(os.path.join(LEADERBOARD_DIR, filename), "r") as leaderboard_file:
        print(f"\nLeaderboard for {filename}:")
        print(leaderboard_file.read())

server_socket.close()
