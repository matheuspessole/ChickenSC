
# Libraries

import os, psutil, platform, webbrowser, sys, getpass
import customtkinter as CTK
from lupa import LuaRuntime
from tkinter import messagebox

# --- CONFIGURAÇÃO INICIAL ---

root = CTK.CTk()
root.title("SCTool")
root.geometry("225x225")
root.resizable(0, 0)

CTK.set_appearance_mode("dark")

# Checkup

if os.name == "nt":
    cpu = os.popen('wmic cpu get name /value').read().replace("Name=", "").strip()
    IsPosix = False
else:
    cpu = os.popen("grep -m 1 'model name' /proc/cpuinfo | cut -d: -f2").read().strip()
    IsPosix = True


# Verify AMD/ARM

if "AMD" in cpu or "Intel" in cpu:
    texto = "AMD"
    cor = "#0071C5"
    Compatibility_Label = "AMD64 / x86_64"
else:
    texto = "ARM"
    cor = "#ED1C24"
    Compatibility_Label = "ARM (ARM64 / AArch64)"


# Functions

def open_logs():

    # Detect system & input data

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

    machine = platform.machine()

    # Architecure: Checkup

    arch = str

    if "64" in machine:
        arch = " (Suporte: 64/32 bits)"
    else:
        arch = " (Suporte: 32 bits)"
    
    # Memory Ram: Calculate

    total_bytes = psutil.virtual_memory().total
    total_mb = total_bytes // (1024**2)

    if total_mb >= 1024:
        ram = f"{total_mb / 1024:.2f} GB"
    else:
        ram = f"{total_mb} MB"
    
    tech = Compatibility_Label + arch

    # Write logs

    lua = LuaRuntime(unpack_returned_tuples=True)

    with open("module.lua", "r", encoding="utf-8") as arq:
        arq = lua.eval(arq.read())

    log_template = arq(sys, cpu, ram, tech)

    with open("logs.txt", "w", encoding="utf-8") as arquivo:
        arquivo.writelines(log_template)
    
    webbrowser.open(os.path.realpath("logs.txt"))

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
        
# Layout

text_label = CTK.CTkLabel(master=root, text="Compatibility with:", text_color="white", font=("Arial", 20))
text_label.place(relx=0.5, rely=0.25, anchor="center")

cpu_label = CTK.CTkLabel(master=root, text=texto, text_color=cor, font=("Arial", 40))
cpu_label.place(relx=0.5, rely=0.5, anchor="center")

butao = CTK.CTkButton(master=root, text="Diagnostic", font=("Arial", 20), corner_radius=15,
 command=open_logs, border_width=2, fg_color="#2B2B2B", hover_color="#3A3A3A", 
 border_color="#0AA5BF", text_color="#0AA5BF")
butao.place(relx=0.5, rely=0.7, anchor="center")


# Check depencies

if not os.path.exists("module.lua"): warn("module")

if not IsPosix:
    if os.path.exists("app.ico"):
        try:
            root.iconbitmap("app.ico")
        except Exception:
            warn(mode="corrupted")
    else:
        warn(mode="ico")

# Run

root.mainloop()
