import platform
import socket
import psutil
import getpass
import subprocess
import tkinter as tk
import requests
import wmi
import win32api
import win32file
import ctypes
import ssd_checker

#Get system info function
def get_system_info():
    public_ip = requests.get('https://api.ipify.org').text
    return f"User: {getpass.getuser()}\n" \
           f"Hostname: {socket.gethostname()}\n" \
           f"FQDN: {socket.getfqdn()}\n" \
           f"Private IP Address: {socket.gethostbyname(socket.gethostname())}\n" \
           f"Public IP Address: {public_ip}\n" \
           f"Operating System: {platform.system()}\n" \
           f"Platform: {platform.platform()}\n" \
           f"Processor: {platform.processor()}\n" \
           f"Physical memory: {round(psutil.virtual_memory().total / (1024.0 ** 3))} GB\n"

def get_storage_info():
    w = wmi.WMI()
    print(w)
    storage_info = []
    for disk in w.Win32_DiskDrive():
        print(disk)
        device_id = disk.DeviceID[:-1]
        try:
            for partition in w.Win32_Volume(DriveLetter=device_id):
                usage = psutil.disk_usage(partition.DriveLetter)
                storage_type = "SSD" if ssd_checker.check(device_id) else "HDD"
                storage_info.append([
                    partition.DriveLetter,
                    disk.FileSystem,
                    storage_type,
                    round(usage.total / (1024.0 ** 3)),
                    round(usage.used / (1024.0 ** 3)),
                    round(usage.free / (1024.0 ** 3)),
                    usage.percent
                ])
        except Exception as e:
            print("Error:", e)
    print("Storage Info from get:", storage_info) # added print statement
    return storage_info









#get dns info
def get_dns_info():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    dns = socket.getaddrinfo(hostname, None, socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    dns_servers = [d[4][0] for d in dns]
    return hostname, ip, dns_servers

#is domain joined?
def is_domain_joined():
    try:
        output = subprocess.run(["net", "domains"], capture_output=True, text=True)
        return "No domain" not in output.stdout
    except:
        return False

#get domain controllers
def get_domain_controllers():
    domain_controllers = []
    domain_name = ".".join(socket.getfqdn().split(".")[-2:])
    domain_controllers_output = subprocess.run(['nslookup', '-query=srv', '_ldap._tcp.dc._msdcs.' + domain_name], capture_output=True, text=True)
    for line in domain_controllers_output.stdout.split("\n"):
        if "srv" in line:
            domain_controllers.append(line.split()[-1])
    return domain_controllers        