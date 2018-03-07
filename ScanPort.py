import tkinter
import tkinter.messagebox
import tkinter.simpledialog
import socket
import threading
import time
socket.setdefaulttimeout(3)#设置全局时长(分钟)

class Window:

    def __init__(self):
        self.root = tkinter.Tk()
        menu = tkinter.Menu(self.root)  # 创建菜单

        submenu = tkinter.Menu(menu, tearoff=0)
        submenu.add_command(label="全面扫描",command=self.IP_port)
        submenu.add_separator()
        submenu.add_command(label="快速扫描",command=self.SearchPort)
        menu.add_cascade(label="扫描", menu=submenu)
        self.root.config(menu=menu)

        # 创建"系统"子菜单
        submenu = tkinter.Menu(menu, tearoff=0)
        submenu.add_command(label="关于", command=self.MenuAbout)
        submenu.add_separator()
        submenu.add_command(label="退出", command=self.MenuExit)
        menu.add_cascade(label="系统", menu=submenu)
        self.root.config(menu=menu)

        # 创建标签
        self.labell = tkinter.Label(self.root, anchor=tkinter.W, text='状态', bitmap='hourglass', compound='left')
        self.labell.place(x=10, y=380, width=400, height=15)

        # 创建文本框
        self.entry = tkinter.Text(self.root, bg='gray')
        self.entry.place(x=10, y=10, width=290, height=370)

        # 为文本框添加滚动滑轮
        self.vscroll = tkinter.Scrollbar(self.entry)
        self.vscroll.pack(side="right", fill='y')
        self.entry['yscrollcommand'] = self.vscroll.set
        self.vscroll['command'] = self.entry.yview#"关于"菜单

    #按端口搜索
    def SearchPort(self):
        p = tkinter.simpledialog.askinteger('Port', '请输入所要搜索的端口')
        t = threading.Thread(target=self.Port, args=(p,))
        t.start()

    #端口搜索
    def Port(self,port):
        self.entry.delete(0.0, tkinter.END)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex(('127.0.0.1', port))
        if (result == 0):
            self.entry.insert(tkinter.END, str(port) + '端口开放\n')
        else:
            self.entry.insert(tkinter.END, str(port) + '端口未开放\n')

    #"关于"子菜单
    def MenuAbout(self):
        tkinter.messagebox.showinfo("Findfat","记得给五星好评哦!")

    #"退出"子菜单
    def MenuExit(self):
        result = tkinter.messagebox.askquestion("Findfat", "是否要退出?")
        if result == 'no':
            return
        self.root.quit()

    def socket_port(self, port):
        count = 0
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex(('127.0.0.1', port))
        if (result == 0):
            count += 1
            self.entry.insert(tkinter.END, str(port) + '端口开放\n')
        else:
            pass

    def IP_port(self):
        self.entry.delete(0.0, tkinter.END)
        self.labell['text'] = "正在扫描中,请耐心等候..."
        for port in range(0,2000):
            t = threading.Thread(target=self.socket_port, args=(port,))
            t.start()
            time.sleep(0.001)
        self.labell['text'] = "扫描结束!"

    def MainLoop(self):
        self.root.title ("端口扫描")
        self.root.minsize (310,400)
        self.root.maxsize (310,400)
        self.root.mainloop()

if __name__ == "__main__":
    window = Window()
    window.MainLoop()
