
# --- Libraries ---

import os, psutil, platform, webbrowser
import sys, getpass, configparser
import customtkinter as CTK
from lupa import LuaRuntime
from tkinter import messagebox, filedialog
from datetime import datetime, timezone

# --- Initial Configuration ---

template = rf"""[STARTUP]
; Run logs automatically on open (true/false)
auto_run = false
; Show window (true) or terminal only (false)
use_gui = true

[STORAGE]
; Where to save the results
output_folder = {os.getcwd()}

[FILE_DETAILS]
; Open the log file automatically when finished
open_after_finish = true
; Name of the PC in the file name
add_pc_name = true
; Date and time inside the log
add_timestamp = true
"""

def load_ini():
    config = configparser.ConfigParser()
    
    if not os.path.exists("config.ini"):
        with open("config.ini", "w", encoding='utf-8') as arq:
            arq.write(template)
    
    config.read('config.ini', encoding='utf-8')
    return config

cfg = load_ini()

file_name = "logs"
pass_mode = False
user = getpass.getuser()
save_log_path = cfg.get('STORAGE', 'output_folder')


# --- System & CPU: Checkup ---

if os.name == "nt":
    cpu = os.popen('wmic cpu get name /value').read().replace("Name=", "").strip()
    IsPosix = False
else:
    cpu = os.popen("grep -m 1 'model name' /proc/cpuinfo | cut -d: -f2").read().strip()
    IsPosix = True

if "AMD" in cpu or "Intel" in cpu:
    texto = "AMD"
    cor = "#0071C5"
    Compatibility_Label = "AMD64 / x86_64"
else:
    texto = "ARM"
    cor = "#ED1C24"
    Compatibility_Label = "ARM (ARM64 / AArch64)"


# --- Functions ---


def generate_logs(mode):
    
    # --- Variables ---
    
    global file_name, save_log_path

    machine = platform.machine()
    arch = str

    # --- Computer: Get Info ---

    try:
        if not IsPosix:
            distro = platform.win32_edition()
            sys = f"{platform.system()} {platform.release()} {distro}"
        else:
            data = platform.freedesktop_os_release()
            DISTRO_NAME = data["NAME"]
            VERSION_ID = data["VERSION_ID"]
            sys = f"{platform.system()} {DISTRO_NAME} {VERSION_ID}"
    except Exception:
        sys = "N/A"

    if "64" in machine:
        arch = " (Suporte: 64/32 bits)"
    else:
        arch = " (Suporte: 32 bits)"

    total_bytes = psutil.virtual_memory().total
    total_mb = total_bytes // (1024**2)

    if total_mb >= 1024:
        ram = f"{total_mb / 1024:.2f} GB"
    else:
        ram = f"{total_mb} MB"
    
    tech = Compatibility_Label + arch

    # --- Generate Logs ---

    try:
        lua = LuaRuntime(unpack_returned_tuples=True)

        with open("module.lua", "r", encoding="utf-8") as arq:
            arq = lua.eval(arq.read())

        log_template = arq(sys, cpu, ram, tech)
        fullpath = os.path.join(save_log_path, file_name + ".txt")

        with open(fullpath, "w", encoding="utf-8") as arquivo:
            arquivo.writelines(log_template)

        if mode == "open":
            
            webbrowser.open(fullpath)

    except Exception as e:
        messagebox.showerror("Critical Failure", f"Failed in 'module.lua': {e}")
        sys.exit()


def warn(mode):
    errors = {
        "corrupted": ("System Alert", "[0x01] Asset 'app.ico' is corrupted.\nUsing default icon.", "warning"),
        "ico": ("System Alert", "[0x02] Asset 'app.ico' missing.\nUsing default icon.", "warning"),
        "module": ("Critical Failure", "[0x03] Dependency 'module.lua' missing.\nExecution halted.", "error")
    }

    title, msg, level = errors[mode]

    match mode:
        case "corrupted": messagebox.showerror(title, msg)
        case "ico": messagebox.showerror(title, msg)
        case "module": messagebox.showerror(title, msg); sys.exit()

def open_logs():
    global pass_mode
    if pass_mode: 
        generate_logs(mode="open")
    else: generate_logs(mode=None)



def select_dir():
    
    # --- Variables ---

    global save_log_path
    if IsPosix: base_dir = "~"
    else:   base_dir = rf"C:/users/{user}"

    new_path = filedialog.askdirectory(parent=root, title="SCTool | Select Output Destination", 
        initialdir=base_dir, mustexist=True)
    
    if new_path != "" and new_path != ():  save_log_path = new_path

    cfg = load_ini()
    cfg['STORAGE'] = {'output_folder': save_log_path}

    with open('config.ini', 'w', encoding='utf-8') as f:
        cfg.write(f)


# --- CustomTkinter Configuration ---

root = CTK.CTk()
root.title("SCTool")
root.geometry("225x225")
root.resizable(0, 0)

CTK.set_appearance_mode("dark")

text = CTK.CTkLabel(master=root, text="Compatibility with:", text_color="white", font=("Arial", 20))
text.place(relx=0.5, rely=0.25, anchor="center")

cpu_label = CTK.CTkLabel(master=root, text=texto, text_color=cor, font=("Arial", 40))
cpu_label.place(relx=0.5, rely=0.5, anchor="center")

butao = CTK.CTkButton(master=root, text="Diagnostic", font=("Arial", 20), corner_radius=15,
 command=open_logs, border_width=2, fg_color="#2B2B2B", hover_color="#3A3A3A", 
 border_color="#0AA5BF", text_color="#0AA5BF")
butao.place(relx=0.5, rely=0.7, anchor="center")

butao2 = CTK.CTkButton(master=root, text="+", font=("Arial", 20), corner_radius=0,
 command=select_dir, border_width=2, fg_color="#2B2B2B", hover_color="#3A3A3A", 
 border_color="#0AA5BF", text_color="#0AA5BF", height=10, width=10)
butao2.place(relx=0.85, rely=0.7, anchor="center")

# --- Depedencies: CheckUp ---

if not os.path.exists("module.lua"): warn("module")

if not IsPosix:
    if os.path.exists("app.ico"):
        try:
            root.iconbitmap("app.ico")
        except Exception:
            warn(mode="corrupted")
    else:
        warn(mode="ico")


# Load options: .ini and run

cfg = load_ini()

if cfg.get('FILE_DETAILS', 'add_pc_name'):
    file_name = file_name + rf"_{user}"
if cfg.get('FILE_DETAILS', 'add_timestamp'):
    agora_utc = datetime.now(timezone.utc)
    timestamp = agora_utc.strftime("%Y-%m-%d")
    
    file_name = file_name + rf"_{timestamp}"

if cfg.getboolean('FILE_DETAILS', 'open_after_finish'): pass_mode = True

if cfg.getboolean('STARTUP', 'auto_run'):
    if cfg.getboolean('FILE_DETAILS', 'open_after_finish'): 
        pass_mode = True
        generate_logs(mode="open")
    else: generate_logs(mode=None)
    if not cfg.getboolean('STARTUP', 'use_gui'):
        sys.exit()

if cfg.getboolean('STARTUP', 'use_gui'): root.mainloop()
