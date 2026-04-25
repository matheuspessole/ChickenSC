
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

if not os.path.exists("module.lua"):
    messagebox.showerror("Critical Failure", "Dependency Error: 'module.lua' not found. Execution halted.")
    root.destroy()
    sys.exit()

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
    try:
        if not IsPosix:
            distro = platform.win32_edition()
            version = f"{platform.system()} {platform.release()} {distro}"
        else:
            data = platform.freedesktop_os_release()
            distro = data["PRETTY_NAME"]
            version = f"{distro} - {platform.system()}"
    except Exception:
        version = "N/A"

    machine = platform.machine()
    ram = round(psutil.virtual_memory()[0] / (1024**3), 2)
    disk = round(psutil.disk_usage('/').total /1024**3, 2)
    arch = str

    if "64" in machine: 
        arch = Compatibility_Label + " (64/32 bits)"
    else: 
        arch = Compatibility_Label + " (32 bits)"
    lua = LuaRuntime(unpack_returned_tuples=True)
    with open("module.lua", "r", encoding="utf-8") as arq:
        arq = lua.eval(arq.read())
    
    log_template = arq(version, cpu, arch, ram, disk)

    with open("logs.txt", "w", encoding="utf-8") as arquivo:
        arquivo.writelines(log_template)
    webbrowser.open(os.path.realpath("logs.txt"))

# Layout

text_label = CTK.CTkLabel(master=root, text="Compatibility with:", text_color="white", font=("Arial", 20))
text_label.place(relx=0.5, rely=0.25, anchor="center")

cpu_label = CTK.CTkLabel(master=root, text=texto, text_color=cor, font=("Arial", 40))
cpu_label.place(relx=0.5, rely=0.5, anchor="center")

butao = CTK.CTkButton(master=root, text="Diagnostic", font=("Arial", 20), corner_radius=15,
 command=open_logs, border_width=2, fg_color="#2B2B2B", hover_color="#3A3A3A", 
 border_color="#0AA5BF", text_color="#0AA5BF")
butao.place(relx=0.5, rely=0.7, anchor="center")

# Run
if not IsPosix:
    if os.path.exists("app.ico"):
        try:
            root.iconbitmap("app.ico")
        except Exception:
            messagebox.showwarning("System Alert", "Asset 'app.ico' is corrupted. Using default icon.")
    else:
        messagebox.showwarning("System Alert", "Asset 'app.ico' missing. UI will load with default icon.")
root.mainloop()