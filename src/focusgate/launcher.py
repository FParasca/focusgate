import tkinter as tk
from tkinter import messagebox
import ctypes
import subprocess
import sys
import os
from focusgate.state import write_state
from focusgate.constants import MODE_FREE, MODE_WORK

def launch_worker():
    
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.dirname(current_dir)
        python_exe = sys.executable
        cmd_command = f'set PYTHONPATH={src_dir} && "{python_exe}" -m focusgate --worker'
        
        
        result = ctypes.windll.shell32.ShellExecuteW(
            None, 
            "runas", 
            "cmd.exe", 
            f'/k {cmd_command}', 
            None, 
            1 
        )
        
        if result <= 32:
            messagebox.showerror("Error", "Failed to start work mode (UAC canceled or blocked).")
            return False
        return True

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while launching the worker:\n{e}")
        return False

def on_free_mode():
    write_state(MODE_FREE)
    root.destroy()

def on_work_mode():
    write_state(MODE_WORK)
    
    success = launch_worker()
    if success:
        root.destroy()
    else:
        pass

def run_launcher():
    global root
    root = tk.Tk()
    root.title("FocusGate - Select Mode")
    root.geometry("400x250")
    root.resizable(False, False)
    
    root.eval('tk::PlaceWindow . center')

    label = tk.Label(root, text="How do you want to use the PC today?", font=("Arial", 14, "bold"))
    label.pack(pady=20)

    btn_work = tk.Button(
        root, 
        text="Work Mode (Study/Focus)", 
        font=("Arial", 11), 
        bg="#e74c3c", 
        fg="white",
        width=30,
        height=2,
        command=on_work_mode
    )
    btn_work.pack(pady=10)

    btn_free = tk.Button(
        root, 
        text="Free Access (Unrestricted)", 
        font=("Arial", 11),
        width=30,
        height=2,
        command=on_free_mode
    )
    btn_free.pack(pady=10)

    aviso = tk.Label(
        root, 
        text="Attention: Exiting work mode requires restarting the PC.", 
        font=("Arial", 8, "italic"), 
        fg="gray"
    )
    aviso.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_launcher()