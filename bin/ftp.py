from ftplib import FTP
from tkinter.filedialog import *
from tkinter import messagebox
import ftplib
from tkinter.messagebox import *
import socket
import os, shutil


root = Tk()


class BuildFtp():
    def __init__(self, root):
        # 初始化
        self.root = root
        self.ftp = socket.socket()
        self.root.title('FTP Client')
        self.root.geometry("850x530")
        # 窗口部件配置管理
        # 布局管理器会将控件放置到一个二维的表格里。
        # 主控件被分割成一系列的行和列，表格中的每个单元都可以放置一个控件。
        self.root.configure()
        self.root.grid()#布局管理器
        self.root.resizable(0,0)#设置禁止拉伸窗口

        self.createframes()
        self.addbuttons()
        self.addlabel()
        self.addentrys()
        self.ftp = FTP()
        self.addlistbox()
        self.poppulatelocal()

        self.menubar = Menu(self.root)
        self.fmenu = Menu(self.menubar, tearoff=0)
        self.fmenu.add_command(label='退出', command=self.quit)
        self.menubar.add_cascade(label='文件', menu=self.fmenu)
        self.amenu = Menu(self.menubar, tearoff=0)
        self.amenu.add_command(label='操作指导', command=self.help)
        self.menubar.add_cascade(label='帮助', menu=self.amenu)
        self.bmenu = Menu(self.menubar, tearoff=0)
        self.bmenu.add_command(label='版本信息', command=self.version)
        self.menubar.add_cascade(label='关于', menu=self.bmenu)
        self.root['menu'] = self.menubar

    def createframes(self):
        """create The Frames"""
        # #定义文本框在第一行列表框在第二行按钮在第三行
        self.EntryFrm = Frame(self.root, )
        self.EntryFrm.grid(row = 0, column = 0)
        self.LstFrm = Frame(self.root )
        self.LstFrm.grid(row = 1, column = 0)
        self.BtnFrm = Frame(self.root)
        self.BtnFrm.grid(row = 2, column = 0)

    def addbuttons(self):
        # """添加按钮"""
        self.LoginBtn = Button(self.EntryFrm, text = "登录", height = 2, width = 6, fg = "black", activebackground = "yellow", bg = "light blue", command = self.login)
        self.LocalUpLvl = Button(self.BtnFrm, text = "上一层目录", fg = "black", activebackground = "yellow", bg = "light blue", command = self.uplocal)
        self.RemoteUpLvl = Button(self.BtnFrm, text = "上一层目录", fg = "black", activebackground = "yellow", bg = "light blue", command = self.upremote)
        self.RemoteNewF = Button(self.BtnFrm, text = "新建文件夹", fg = "black", activebackground = "yellow", bg = "light blue", command = self.newremotefolder)
        self.LocalNewF = Button(self.BtnFrm, text = "新建文件夹", fg = "black", activebackground = "yellow", bg = "light blue", command = self.newlocalfolder)
        self.remotedel = Button(self.BtnFrm, text = "删除", fg = "black", activebackground = "yellow", bg = "light blue", command = self.remotedel)
        self.localdel = Button(self.BtnFrm, text = "删除", fg = "black", activebackground = "yellow", bg = "light blue", command = self.localdel)
        self.Upfileloc = Button(self.BtnFrm, text="上传", fg="black", activebackground="yellow", bg="light blue",command=self.uplocfile)
        self.Downfileloc = Button(self.BtnFrm, text="下载", fg="black", activebackground="yellow", bg="light blue",command=self.downlocfile)

        self.LoginBtn.grid(row=0, column=8, padx=10, pady=10)
        self.Upfileloc.grid(row=1, column=0, padx=10, pady=10)
        self.LocalUpLvl.grid(row = 1, column = 1, padx = 10, pady = 10)
        self.LocalNewF.grid(row = 1, column = 2, padx = 10, pady = 10)
        self.localdel.grid(row = 1, column = 3, padx = 10, pady = 10)
        self.RemoteUpLvl.grid(row = 1, column = 6, padx = 10, pady = 10)
        self.RemoteNewF.grid(row = 1, column = 5, padx = 10, pady = 10)
        self.remotedel.grid(row = 1, column = 4, padx = 10, pady = 10)
        self.Downfileloc.grid(row=1, column=7, padx=10, pady=10)

    def addlistbox(self):
        self.LocalLst = Listbox(self.LstFrm, bd = 2, height = 18, width = 40, font = ("Calibri", 12), selectmode = EXTENDED)
        self.RemoteLst = Listbox(self.LstFrm, bd = 2, height = 18, width = 40, font = ("Calibri", 12), selectmode = EXTENDED)
        self.LocalLst.bind('<Double-Button-1>', self.forwarddir)
        self.RemoteLst.bind('<Double-Button-1>', self.remoteforwarddir)
        self.LocalLst.grid(row = 0, column = 0, padx = 30, pady = 10)
        self.RemoteLst.grid(row = 0, column = 1, padx = 30, pady = 10)

    def addlabel(self):
        # 添加标签
        self.HostLbl = Label(self.EntryFrm, text = "ftp地址: ", font = ("Calibri", 12))
        self.UserLbl = Label(self.EntryFrm, text = "用户名: ", font = ("Calibri", 12))
        self.PwdLbl = Label(self.EntryFrm, text = "密码: ", font = ("Calibri", 12))
        self.PortLbl = Label(self.EntryFrm, text = "端口号: ", font = ("Calibri", 12))
        self.HostLbl.grid(column = 0, row = 0, padx = 5, pady = 5)
        self.UserLbl.grid(column = 2, row = 0, padx = 5, pady = 5)
        self.PwdLbl.grid(column = 4, row = 0, padx = 5, pady = 5)
        self.PortLbl.grid(column = 6, row = 0, padx = 5, pady = 5)

    def addentrys(self):
        # 添加文本框
        self.HostEnt = Entry(self.EntryFrm, bd = 2, width = 17, font = ("Calibri", 10))
        self.UserEnt = Entry(self.EntryFrm, bd = 2, width = 17, font = ("Calibri", 10))
        self.PwdEnt = Entry(self.EntryFrm, bd = 2, width = 17, font = ("Calibri", 10), show = '*')
        # self.PortEnt = Entry(self.EntryFrm, bd = 2, width = 17, font = ("Calibri", 10))

        self.HostEnt.grid(column = 1, row = 0, padx = 10, pady = 10)
        self.UserEnt.grid(column = 3, row = 0, padx = 10, pady = 10)
        self.PwdEnt.grid(column = 5, row = 0, padx = 10, pady = 10)
        # self.PortEnt.grid(column = 7, row = 0, padx = 10, pady = 10)
        self.PortEnt=IntVar()
        Entry(self.EntryFrm, width=5, textvariable=self.PortEnt).grid(column = 7, row = 0, padx = 10, pady = 10)

    def localdel(self):
        # 删除本地文件
        self.Selection3 = self.LocalLst.curselection()
        self.Value3 = self.LocalLst.get(self.Selection3)
        self.Cdir3 = os.getcwd()
        self.NewDir3 = self.Cdir3 + "/" + self.Value3
        self.Question = messagebox.askyesno("Delete Query", "确定删除？")
        if self.Question:
            if '.' not in self.NewDir3:
                try:
                    # 删除目录文件夹
                    shutil.rmtree(self.NewDir3)
                    showinfo(title="showinfo", message="删除成功")
                except:
                    showerror(title="error", message="错误：删除失败！")
            else:
                try:
                    # 删除文件
                    os.remove(self.NewDir3)
                    showinfo(title="showinfo", message="删除成功")
                except:
                    showerror(title="error", message="错误：删除失败！")
            self.poppulatelocal()

    def remotedel(self):
        # 删除服务器文件
        # 用Listbox中的curselection()方法来捕捉鼠标选中的条目
        self.Selection4 = self.RemoteLst.curselection()
        self.Value4 = self.RemoteLst.get(self.Selection4)
        self.Question2 = messagebox.askyesno("Delete Query", "确定删除？")
        if self.Question2:
            if '.' in self.Value4:
                try:
                    # 删除服务器文件
                    self.ftp.delete(self.Value4)
                    showinfo(title="showinfo", message="删除成功")
                except:
                    showerror(title="error", message="错误：删除失败！")

            else:
                try:
                    #  删除服务器目录
                    self.ftp.rmd(self.Value4)
                    showinfo(title="showinfo", message="删除成功")
                except:
                    showerror(title="error", message="错误：删除失败！")
            self.poppulateremote()

    def uplocfile(self):
        # 从本地上传文件到服务器
        flag=0
        # os.getcwd()方法用于返回当前工作目录。
        self.Cdir5 = os.getcwd()
        # ftp.nlst() #获取服务器目录下的文件
        filelist= self.ftp.nlst()
        # 用Listbox中的curselection()方法来捕捉鼠标选中的条目
        selection=self.LocalLst.curselection()
        inputFileName = self.LocalLst.get(selection)
        if '.' in inputFileName:
            file_handler = open(self.Cdir5 + '/' + inputFileName, 'rb')
            filename=os.path.basename(inputFileName)#返回path最后的文件名
            for i in filelist:
                if i==filename:
                    flag=1
                    break
            if flag==1:
                showerror(title="error", message="有相同文件名，请检查！")

            else:
                try:
                    # file_handler = open(self.Cdir5 + '/' + inputFileName, 'rb')
                    self.ftp.storbinary('STOR %s' % filename, file_handler, 1224)
                    showinfo(title="showinfo" ,message= "上传成功")
                    self.poppulateremote()
                except ftplib.error_perm:
                    showerror(title="error" ,message= "上传失败，请检查!")
        else:
            showerror(title="error", message="抱歉，不支持上传文件夹！")

    def downlocfile(self):
        # 从服务器上下载文件到本地
        flag=0
        self.Cdir6 = os.getcwd()
        filelist = os.listdir(self.Cdir6)
        # 用Listbox中的curselection()方法来捕捉鼠标选中的条目
        choose=self.RemoteLst.curselection()
        inputFileName = self.RemoteLst.get(choose)
        if '.'  in inputFileName:
            filename=os.path.basename(inputFileName)
            for i in filelist:
                if i == filename:
                    flag=1
                    break

            if flag == 1:
                showerror(title="error", message="有相同文件名，请检查!将重新命名文件")
                # #以写模式在本地打开文件
                file_handler = open(self.Cdir6 + '/'  +"(1)"+inputFileName, 'wb').write
                try:
                    self.ftp.retrbinary('RETR %s' % filename, file_handler, 1224)  # 二进制传输模式
                    showinfo(title="showinfo" ,message= "下载成功")
                    self.poppulatelocal()

                except ftplib.error_perm:
                    showerror(title="error" ,message= "下载失败，请检查!")


            else:
                try:
                    file_handler = open(self.Cdir6 + '/' + inputFileName, 'wb').write
                    self.ftp.retrbinary('RETR %s' % filename, file_handler, 1224)  # 二进制传输模式
                    showinfo(title="showinfo" ,message= "下载成功")
                    self.poppulatelocal()

                except ftplib.error_perm:
                    showerror(title="error" ,message= "下载失败，请检查!")
        else:
            showerror(title="error", message="抱歉，不支持下载文件夹！")

    def uplocal(self):
        # 返回本地一层目录
        os.chdir("..")
        self.poppulatelocal()

    def upremote(self):
        # 返回服务器上一层目录
        self.ftp.cwd("..")
        self.poppulateremote()

    def newlocalfolder(self):
        # 新建本地文件夹
        x = True
        NewFolder(x)

    def newremotefolder(self):
        # 新建服务器文件夹
        x = False
        NewFolder(x)

    def poppulatelocal(self):
        # 更新本地目录
        self.LocalLst.delete(0, END)
        # os.getcwd()方法用于返回当前工作目录。
        self.Cdir = os.getcwd()
        # os.listdir() 方法用于返回指定的文件夹包含的文件或文件夹的名字的列表。
        self.LocalDirLst = os.listdir(self.Cdir)
        for i in range(len(self.LocalDirLst)):
            self.LocalLst.insert(i, self.LocalDirLst[i - 1])

    def poppulateremote(self):
        # 更新服务器目录
        self.RemoteLst.delete(0, END)
        # ftp.nlst() #获取服务器目录下的文件
        self.DirLst = self.ftp.nlst()
        for i in range(len(self.DirLst)):
            self.RemoteLst.insert(i, (self.DirLst[i - 1]))


    def forwarddir(self, event):
        # 双击进入选中本地文件目录
        self.Widget = event.widget
        # 用Listbox中的curselection()方法来捕捉鼠标选中的条目
        self.Selection = self.Widget.curselection()
        # 获取鼠标选中条目的值
        self.Value = self.Widget.get(self.Selection[0])
        # os.getcwd()方法用于返回当前工作目录。
        self.Cdir = os.getcwd()
        self.NewDir = self.Cdir + '/'+ self.Value
        if '.' not in self.Value:
            try:
                # os.chdir()方法用于改变当前工作目录到指定的路径。
                os.chdir(self.NewDir)
                self.poppulatelocal()
            except:
                showerror(title="error", message="错误：无法访问该文件夹，请检查！")
        else:
            showerror(title="error", message="错误：只能访问文件夹")

    def remoteforwarddir(self, event):
        # # 双击进入选中服务器文件目录
        self.Widget2 = event.widget
        # 用Listbox中的curselection()方法来捕捉鼠标选中的条目
        self.Selection2 = self.Widget2.curselection()
        self.Value2 = self.Widget2.get(self.Selection2[0])##获取鼠标选中条目的值
        if '.' not in self.Value2:
            try:
                self.ftp.cwd(self.Value2)#更改服务器目录
                self.poppulateremote()#刷新当前目录的文件列表
            except:
                showerror(title="error", message="错误：无法访问该文件夹，请检查！")
        else:
            showerror(title="error", message="错误：只能访问文件夹，请检查！")

    def quit(self):
        self.root.destroy()
        self.ftp.close()

    def help(self):
        showinfo(title='帮助', message='左边本地目录，右边服务器目录，双击打开文件夹！')
    def version(self):
        showinfo(title='版本信息', message='Ftp 1.0 版 2018')

    def login(self):
        # 登录并连接到服务器
        self.HostHold = self.HostEnt.get()
        self.UserHold = self.UserEnt.get()
        self.PwdHold = self.PwdEnt.get()
        self.PortHold = self.PortEnt.get()
        try:
            self.ftp.connect(self.HostHold,self.PortHold)
            showinfo("showinfo", "成功连接！欢迎 " + self.UserHold + ".")

        except socket.error as e:
            showerror(title="error", message="错误：无法访问FTP服务，请检查！")

        try:

            self.ftp.login(self.UserHold, self.PwdHold)
            showinfo(title="showinfo", message="已成功登录")
            self.poppulateremote()

        except ftplib.error_perm as e:
            showerror(title="error", message="用户名或密码不对")

    def newrm(self, new):
        try:
            self.ftp.mkd(new)#新建服务器目录
            showinfo(title="showinfo", message="创建成功！")
        except:
            messagebox.showerror("创建文件", "文件夹创建失败——权限被拒绝")


class NewFolder():
    def __init__(self,x):

        self.x = x
        #创建窗口
        self.root = Tk()
        self.root.title('文件名')
        self.root.geometry("250x250")
        self.root.configure()#窗口部件配置管理
        # 布局管理器会将控件放置到一个二维的表格里。
        # 主控件被分割成一系列的行和列，表格中的每个单元都可以放置一个控件。
        self.root.grid()#布局管理器
        self.root.resizable(0,0)
        self.root.configure()
        self.addstuff()

    def addstuff(self):
        # 添加控件
        self.Lbl = Label(self.root, text = "请输入文件名", font = ("Calibri", 12))
        self.Ent = Entry(self.root, bd = 2, width = 25, font = ("Calibri", 10))
        self.Btn = Button(self.root, text = "创建", height = 2, width = 10,
                          fg = "black", activebackground = "yellow",
                          bg = "light blue",command = self.create)
        self.Lbl.grid(row = 0, column = 0, padx = 20, pady = 20)
        self.Ent.grid(row = 1, column = 0, padx = 20, pady = 20)
        self.Btn.grid(row = 2, column = 0, padx = 20, pady = 20)

    def create(self):
        self.Breaker = True
        self.Ent=self.Ent.get()
        for x in self.Ent:
            if x in[' /', '?', '<', '>', ':,', '*', '|'] or x == chr(92):
                messagebox.showerror("User Error", "文件夹名称不能包含  / ? < > \ : * |")
                self.Breaker = False
                break

        if len(self.Ent) < 1:
            messagebox.showerror("User Error", "请输入文件夹名称!!")

        elif self.Breaker:
            if self.x:
                try:
                    os.makedirs(self.Ent)
                    showinfo(title="showinfo", message="创建成功！")
                    buildftp.poppulatelocal()
                except:
                    messagebox.showerror("创建文件", "文件夹创建失败——权限被拒绝")
            else:
                z = self.Ent
                buildftp.newrm(z)
                buildftp.poppulateremote()
            self.root.destroy()#销毁当前新建文件夹窗口




