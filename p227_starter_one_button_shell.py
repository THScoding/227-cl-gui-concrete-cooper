import subprocess
import tkinter as tk
import tkinter.scrolledtext as tksc
from tkinter import filedialog
from tkinter.filedialog import asksaveasfilename
import sys
import platform
from tkinter import ttk
import matplotlib as matt
import random
import matplotlib.pyplot as plt

rainbow_running = False


def do_command(command):
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


def generate_random_hex_color():
  """Generates a random 6-digit hexadecimal color code."""
  # Generate a random integer between 0 and 0xFFFFFF (16777215)
  random_int = random.randint(0, 0xFFFFFF)
  # Format it into a 6-digit hex string, prefixed with '#'
  return '#{:06x}'.format(random_int)


color_choices = ("Neon Pink", "yellow", "red", "random", "Epilepsy")

root = tk.Tk()
frame_URL = tk.Frame(root) # change frame color
frame = tk.Frame(root, borderwidth= 5)
frame_URL.grid(row=0, column=0, sticky="ew")
frame.grid(row=1, column=0, sticky="nsew")
root.minsize(900, 500)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=3)
root.grid_columnconfigure(0, weight=1)
frame_URL.grid_columnconfigure(0, weight=0)  # label stays tight
frame_URL.grid_columnconfigure(1, weight=1)  # entry expands
frame_URL.grid_columnconfigure(2, weight=1)
frame_URL.grid_columnconfigure(3, weight=1)

frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)


# creates the frame with label for the text box


def change_ui_color(event=None):
    global rainbow_running

    selection = color_listbox.get(color_listbox.curselection())

    # Stop rainbow if switching modes
    rainbow_running = False

    if selection == "Neon Pink":
        color = "#ff2fd2"
    elif selection == "yellow":
        color = "yellow"
    elif selection == "red":
        color = "red"
    elif selection == "random":
        color = generate_random_hex_color()
    elif selection == "Epilepsy":
        rainbow_running = True
        rainbow_cycle()
        return
    else:
        return

    root.configure(bg=color)
    frame_URL.configure(bg=color)
    frame.configure(bg=color)
    button_frame.configure(bg=color)

    def recolor(widget):
        try:
            widget.configure(
                bg=color,
                activebackground=color,
                highlightbackground=color
            )
        except tk.TclError:
            pass

    for container in (frame_URL, frame, button_frame):
        for widget in container.winfo_children():
            recolor(widget)

    command_textbox.configure(bg=color)
    color_listbox.configure(bg=color)


def rainbow_cycle():
    if not rainbow_running:
        return

    color = generate_random_hex_color()

    root.configure(bg=color)
    frame_URL.configure(bg=color)
    frame.configure(bg=color)
    button_frame.configure(bg=color)

    def recolor(widget):
        try:
            widget.configure(
                bg=color,
                activebackground=color,
                highlightbackground=color
            )
        except tk.TclError:
            pass

    for container in (frame_URL, frame, button_frame):
        for widget in container.winfo_children():
            recolor(widget)

    command_textbox.configure(bg=color)
    color_listbox.configure(bg=color)

    # speed control (lower = faster)
    root.after(10, rainbow_cycle)



# decorative label
url_label = tk.Label(frame_URL, text="Enter a URL of interest: ", 
    compound="center",
    font=("comic sans", 14),
    bd=0, 
    relief=tk.FLAT)

url_entry= tk.Entry(frame_URL,  font=("comic sans", 14)) # change font
url_label.grid(row=0, column=0, padx=5, sticky="w")
url_entry.grid(row=0, column=1, padx=5, sticky="ew")
button_frame = tk.Frame(frame_URL)
url_entry.configure(width=1)
button_frame.grid(row=3, column=1, columnspan=4, pady=5, sticky="ew")
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)
button_frame.grid_columnconfigure(2, weight=1)
button_frame.grid_columnconfigure(3, weight=1)
for i in range(4):
    button_frame.grid_columnconfigure(i, weight=1)

# Color listbox (LEFT of buttons)
color_listbox = tk.Listbox(
    button_frame,
    height=5,
    width=12,
    exportselection=False
)

for color in color_choices:
    color_listbox.insert(tk.END, color)

color_listbox.grid(row=0, column=0, rowspan=2, padx=10)

color_listbox.bind("<<ListboxSelect>>", change_ui_color)


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
command_textbox.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
show_output = tk.BooleanVar(value=True)
def toggle():
    if show_output.get():
        print("showing")
        command_textbox.grid()
    else:
        print("hiding")
        command_textbox.grid_remove()

color_listbox.grid(row=0, column=0, rowspan=2, padx=10, sticky="ns")

# Makes the command button pass it's name to a function using lambda
if sys.platform.startswith('win'):
    ping_btn = tk.Button(button_frame, text="Ping",width=10, command=lambda:do_command("ping"))        
elif sys.platform == 'darwin':
    ping_btn = tk.Button(button_frame, text="Ping",width=10, command=lambda:do_command("ping -c 4"))
ping_btn.grid(row= 0, column= 1, padx=3)

Nslookup_btn = tk.Button(button_frame, text="Nslookup", width=10, command=lambda: do_command("nslookup"))
Nslookup_btn.grid(row=0, column=2, padx=3)

Netstat_btn = tk.Button(button_frame, text="Netstat", width=10, command=lambda: do_command("netstat -n"))
Netstat_btn.grid(row=0, column=3, padx=3)

if sys.platform.startswith('win'):
    Tracert = tk.Button(button_frame, text="Tracert", width=10, command=lambda:do_command("tracert"))        
elif sys.platform == 'darwin':
    Tracert = tk.Button(button_frame, text="Traceroute", width=10, command=lambda:do_command("traceroute"))
Tracert.grid(row= 1, column= 2, padx=3)

save_btn = tk.Button(button_frame, text = "Save", width=10, command= mSave)
save_btn.grid(row= 1, column= 3, padx=3)

sh_cmd_txtbox = tk.Checkbutton(button_frame, text= "Show output",variable=show_output, width=10,command= toggle)
sh_cmd_txtbox.grid(row= 1, column=1, padx=3)


root.mainloop()
