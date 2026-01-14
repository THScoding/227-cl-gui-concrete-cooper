import subprocess
import tkinter as tk
import tkinter.scrolledtext as tksc
from tkinter import filedialog
from tkinter.filedialog import asksaveasfilename

def do_command():
    command = ["ping", "localhost"]
    # Windows version to limit to 4 requests: command = ["ping", "localhost", "-n", "4"]
    # Mac version to limit to 4 requests:     command = ["ping", "localhost", "-n", "4"]
    
    subprocess.run(command)
    
root = tk.Tk()
frame = tk.Frame(root)
frame.pack()
root.wm_geometry("500x300")


# set up button to run the do_command function
ping_btn = tk.Button(frame, text="ping", command=do_command)
ping_btn.pack()

root.mainloop()
