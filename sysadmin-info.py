import platform
import socket
import psutil
import getpass
import subprocess
import tkinter as tk
import requests
import functions
import webbrowser
from tkinter import ttk
import wmi
import ctypes
import ssd_checker

root = tk.Tk()

#show storage info button
def show_storage_info():
    storage_info_window = tk.Toplevel(root)
    storage_info_window.title("Storage Info")

    storage_info = functions.get_storage_info()
    print("Storage Info:", storage_info) # added print statement
    for i, info in enumerate(storage_info):
        if "SSD" in info[1]:
            storage_info[i][1] = "SSD"
        else:
            storage_info[i][1] = "HDD"

    tree = ttk.Treeview(storage_info_window)
    tree["columns"] = ("Drive", "File System Type", "Storage Type", "Total Space (GB)", "Used Space (GB)", "Free Space (GB)", "Percent Used (%)")
    tree.column("Drive", width=100, anchor="center")
    tree.column("File System Type", width=100, anchor="center")
    tree.column("Storage Type", width=100, anchor="center")
    tree.column("Total Space (GB)", width=100, anchor="center")
    tree.column("Used Space (GB)", width=100, anchor="center")
    tree.column("Free Space (GB)", width=100, anchor="center")
    tree.column("Percent Used (%)", width=100, anchor="center")
    tree.heading("Drive", text="Drive")
    tree.heading("File System Type", text="File System Type")
    tree.heading("Storage Type", text="Storage Type")
    tree.heading("Total Space (GB)", text="Total Space (GB)")
    tree.heading("Used Space (GB)", text="Used Space (GB)")
    tree.heading("Free Space (GB)", text="Free Space (GB)")
    tree.heading("Percent Used (%)", text="Percent Used (%)")
    for i, info in enumerate(storage_info):
        tree.insert("", i, values=info)
    tree.pack(fill="both", expand=True)
    tree.column("#0", stretch=False, width=0)


root.title("SysAdmin-Info")

system_info = functions.get_system_info()
hostname, ip, dns_servers = functions.get_dns_info()

system_info_label = tk.Label(root, text=system_info)
system_info_label.pack()

if functions.is_domain_joined():
    domain_controllers = functions.get_domain_controllers()
    domain_controllers_label = tk.Label(root, text="Is domain joined: Yes\nDomain controllers: " + str(domain_controllers))
    domain_controllers_label.pack()
else:
    domain_controllers_label = tk.Label(root, text="Is domain joined: No")
    domain_controllers_label.pack()

storage_info_button = tk.Button(root, text="Storage Info", command=show_storage_info)
storage_info_button.pack()

footer_label = tk.Label(root, text="\nCreated by Robbie Mueller")
footer_label.pack()
website_link = tk.Label(root, text="www.robbiemueller.com", fg="blue", cursor="hand2")
website_link.pack()
website_link.bind("<Button-1>", lambda e: webbrowser.open_new("http://www.robbiemueller.com"))

root.mainloop()
