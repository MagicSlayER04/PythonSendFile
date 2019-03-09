#####################################
##      Not Safe agiast MITM        #
#####################################
import socket
import tkinter
import re
from tkinter import messagebox
from tkinter import filedialog

class PSF(object):
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        tkinter.Tk().withdraw()

    def startserver(self):
        print("Starting Server....")
        self.socket.bind((self.ip,self.port))
        self.socket.listen(1)
        self.data,self.addr = self.socket.accept()
        messagebox.showinfo("Connected","Someone Sends you a File")
        self.receivefile()

    def connect(self):
        print("Connecting Server....")
        self.socket.connect((self.ip,self.port))
        messagebox.showinfo("Connected","Connected!")
        self.sendfile()

    def sendfile(self):
        #OpenFile
        try:fileN = filedialog.askopenfile().name
        except AttributeError:exit("Exited")
        with open(fileN,"rb") as File:
            self.FileD = File.read()
        self.socket.send(fileN.encode())
        print("Sended Filename : {}".format(fileN))
        self.socket.send(self.FileD)
        print("Sended data")

    def GetFileType(self,name):
        name = name.decode()
        #print("Filename : {}".format(name))
        try:self.fileType = re.search("\.(.*)",name).group()
        except AttributeError:exit()
        print("Extentions : {}".format(self.fileType))

    def receivefile(self):
        self.GetFileType(self.data.recv(1000)) # Receive filename
        File = filedialog.asksaveasfile(mode="wb",defaultextension="*.*",filetypes=[("FileType",self.fileType),("All Files","*.*")])
        if File is None:exit("Exited")
        File.write(self.data.recv(1000000)) # 1GB MAX
        File.close()
    
