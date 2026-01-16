import subprocess
import tkinter as tk
import tkinter.scrolledtext as tksc
from tkinter import filedialog
from tkinter.filedialog import asksaveasfilename
import sys
import platform
from tkinter import ttk



def do_command(command, progressbar):
    progressbar.start()
    # If url_entry is blank, use localhost IP address 
    url_val = url_entry.get()
    if (len(url_val) == 0):
        url_val = "127.0.0.1"
        # ::1 does not work on Mac, likely due to firewall settings
    
    command_textbox.delete(1.0, tk.END)
    command_textbox.insert(tk.END, command + " working....\n")
    command_textbox.update()

    command_list = command + " " + url_val
    #If running on Mac, replace commands where necessary
    if (platform.system() == "Darwin"):
        if (command == "tracert"):
            command = "traceroute"
        if (command == "ping"):
            command = "ping -c4" # Mac otherwise pings without limit
    
    # NOTE: For Mac, to avoid FileNotFoundError, create list of command args. (Alternative?: add shell=true option to Popen method call)
    command_list = (command + ' ' + url_val).split()
    
    """
    The following version of the subprocess failed to capture the first line of the command output
    (because not actually line buffering, because the PIPE is not a TTY; the stdout iteration starts too late):  
        subprocess.Popen(commandList, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)    
    """
    # These lines allow for real time output in the GUI
    with subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0, text=True) as p:
        for line in p.stdout:
            command_textbox.insert(tk.END,line)
            command_textbox.update()
    command_textbox.insert(tk.END, "Done")
    progressbar.end()
    

root = tk.Tk()
frame_URL = tk.Frame(root) # change frame color
frame_URL.grid()
frame = tk.Frame(root, borderwidth= 5)
frame.grid()
root.wm_geometry("1000x600")
root.resizable(False, False)
# creates the frame with label for the text box

# decorative label
url_label = tk.Label(frame_URL, text="Enter a URL of interest: ", 
    compound="center",
    font=("comic sans", 14),
    bd=0, 
    relief=tk.FLAT)
url_label.grid(column=1, row= 1, columnspan= 1)
url_entry= tk.Entry(frame_URL,  font=("comic sans", 14)) # change font
url_entry.grid(column=2, row= 1, columnspan= 3)
button_frame = tk.Frame(frame_URL)
button_frame.grid(row=3, column=1, columnspan=4, pady=5)

# Save function.
def mSave():
  filename = asksaveasfilename(defaultextension='.txt',filetypes = (('Text files', '*.txt'),('Python files', '*.py *.pyw'),('All files', '*.*')))
  if filename is None:
    return
  file = open (filename, mode = 'w')
  text_to_save = command_textbox.get("1.0", tk.END)
  
  file.write(text_to_save)
  file.close()

# Adds an output box to GUI.
command_textbox = tksc.ScrolledText(frame, height=15, width=140)
command_textbox.grid(pady= 5)
show_output = tk.BooleanVar(value=True)
def toggle():
    if show_output.get():
        print("showing")
        command_textbox.grid()
    else:
        print("hiding")
        command_textbox.grid_remove()

# Makes the command button pass it's name to a function using lambda
if sys.platform.startswith('win'):
    ping_btn = tk.Button(button_frame, text="Ping",width=10, command=lambda:do_command("ping"))        
elif sys.platform == 'darwin':
    ping_btn = tk.Button(button_frame, text="Ping",width=10, command=lambda:do_command("ping -c 4"))
ping_btn.grid(row= 0, column= 0, padx=3)

Nslookup_btn = tk.Button(button_frame, text="Nslookup", width=10, command=lambda: do_command("nslookup"))
Nslookup_btn.grid(row=0, column=1, padx=3)

Netstat_btn = tk.Button(button_frame, text="Netstat", width=10, command=lambda: do_command("netstat -n"))
Netstat_btn.grid(row=0, column=2, padx=3)

if sys.platform.startswith('win'):
    Tracert = tk.Button(button_frame, text="Tracert", width=10, command=lambda:do_command("tracert"))        
elif sys.platform == 'darwin':
    Tracert = tk.Button(button_frame, text="Traceroute", width=10, command=lambda:do_command("traceroute"))
Tracert.grid(row= 1, column= 1, padx=3)

save_btn = tk.Button(button_frame, text = "Save", width=10, command= mSave)
save_btn.grid(row= 1, column= 2, padx=3)

sh_cmd_txtbox = tk.Checkbutton(button_frame, text= "Show output",variable=show_output, width=10,command= toggle)
sh_cmd_txtbox.grid(row= 1, column=0, padx=3)

loading_bar = ttk.Progressbar(frame, orient="horizontal", length= 150, mode= "indeterminate")
loading_bar.grid()

root.mainloop()
