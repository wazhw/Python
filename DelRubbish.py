mport tkinter
import tkinter.messagebox

import os,os.path
import threading

#垃圾文件常见后缀名
rubbishExt = ['.tmp','.bak','.old','.xlk','.log','.chk','.syd','.gid']
import tkinter.simpledialog
class Window:
    def __init__(self):
        self.root = tkinter.Tk()

        menu = tkinter.Menu(self.root)#创建菜单

        #创建"查找"子菜单
        submenu = tkinter.Menu(menu,tearoff = 0)
        submenu.add_command(label="搜索文件",command = self.MenuScanFile)
        submenu.add_separator()
        submenu.add_command(label="以文件名搜索",command = self.MenuSearchFile)
        menu.add_cascade(label="搜索",menu=submenu)
        self.root.config(menu=menu)

        # 创建"清理"子菜单
        submenu = tkinter.Menu(menu,tearoff = 0)
        submenu.add_command(label="扫描垃圾文件",command = self.MenuScanRubbish)
        submenu.add_separator()
        submenu.add_command(label="清理垃圾文件",command = self.MenuDelRubbish)
        menu.add_cascade(label="清理",menu=submenu)
        self.root.config(menu=menu)

        # 创建"系统"子菜单
        submenu = tkinter.Menu(menu,tearoff = 0)
        submenu.add_command(label="关于",command = self.MenuAbout)
        submenu.add_separator()
        submenu.add_command(label="退出",command = self.MenuExit)
        menu.add_cascade(label="系统",menu=submenu)

        self.root.config(menu=menu)

        #创建标签
        self.labell = tkinter.Label(self.root,anchor=tkinter.W,text='状态',bitmap='hourglass',compound='left')
        self.labell.place(x=10,y=430,width=480,height=15)

        #创建文本框
        self.entry = tkinter.Text(self.root,bg='gray')
        self.entry.place(x=10,y=10,width=380,height=400)

        #为文本框添加滚动滑轮
        self.vscroll = tkinter.Scrollbar(self.entry)
        self.vscroll.pack(side="right",fill='y')
        self.entry['yscrollcommand'] = self.vscroll.set
        self.vscroll['command']  = self.entry.yview

    #"关于"菜单
    def MenuAbout(self):
        tkinter.messagebox.showinfo("Findfat","记得给五星好评哦!")

    #"退出"菜单
    def MenuExit(self):
        result = tkinter.messagebox.askquestion("Findfat", "是否要退出?")
        if result == 'no':
            return
        self.root.quit()

    #"扫描垃圾文件"菜单
    def MenuScanRubbish(self):
        t = threading.Thread(target=self.ScanRubbishExt)
        t.start()

    #"删除垃圾文件"菜单
    def  MenuDelRubbish(self):
        result = tkinter.messagebox.askquestion("Findfat", "即将进行清理，是否继续？")
        if result == 'no':
            return
        t = threading.Thread(target=self.DeleteRubbish)
        t.start()

    #"按文件大小搜索文件"菜单
    def MenuScanFile(self):
        s = tkinter.simpledialog.askinteger('Findfat','请设置文件的大小(M)')
        t = threading.Thread(target=self.ScanFile,args=(s,))
        t.start()

    #"按名称搜索文件"菜单
    def MenuSearchFile(self):
        s = tkinter.simpledialog.askstring('Findfat', '请输入要搜索的文件名或部分字符')
        t = threading.Thread(target=self.SearchFile, args=(s,))
        t.start()

    #扫描垃圾文件
    def ScanRubbishExt(self):
        global rubbishExt
        total = 0
        filesize = 0
        for root,dirs,files in os.walk('D:'):
            try:
                for fil in files:
                    filesplit = os.path.splitext(fil)
                    if filesplit[1] =='':
                        continue
                    try:
                        if rubbishExt.index(filesplit[1]) >= 0:
                            fname = os.path.join(os.path.abspath(root),fil)
                            filesize += os.path.getsize(fname)
                            self.entry.insert(tkinter.END,fname + '\n') #在最后一个文件名插入一个文件名
                            l =len(fname)
                            if l > 60:
                                self.labell['text'] = fname[:30] + '...' + fname[l - 30:l]
                            else:
                                self.labell['text'] = fname
                            total += 1
                    except ValueError :
                        pass
            except Exception as e:
                print(e)
                pass
        self.labell['text'] = "找到 %s 个垃圾文件，共占用 %.2f M磁盘空间" %(total,filesize/1024/1024)

    #删除垃圾文件
    def DeleteRubbish(self):
        global rubbishExt
        total = 0
        beforesize = 0 #删除前垃圾文件大小
        aftersize = 0 #删除后垃圾文件大小
        filesize  = 0 #删除的垃圾文件大小
        self.entry.delete(0.0, tkinter.END)
        for root, dirs, files in os.walk("D:"):
            try:
                for fil in files:
                    filesplit = os.path.splitext(fil)
                    if filesplit[1] == '':
                        continue
                    try:
                        if rubbishExt.index(filesplit[1]) >= 0:
                            fname = os.path.join(os.path.abspath(root), fil)
                            beforesize += os.path.getsize(fname)
                            l = len(fname)

                            if l > 60:
                                self.labell['text'] = fname[:30] + '...' + fname[l - 30:l]
                            else:
                                self.labell['text'] = fname
                            try:
                                os.remove(fname)
                                total += 1
                            except:
                                aftersize += os.path.getsize(fname)
                                self.entry.insert(tkinter.END, fname + '\n')
                                pass
                    except ValueError:
                        pass
            except Exception as e:
                print(e)
                pass
        filesize = beforesize - aftersize
        self.labell['text'] = "删除了 %s 个垃圾文件，释放了 %.2f M磁盘空间" % (total, (filesize) / 1024 / 1024)

    #按文件大小搜索文件
    def ScanFile(self,filesize):
        total = 0
        filesize = filesize * 1024 * 1024
        self.entry.delete(0.0, tkinter.END)
        for root,dirs,files in os.walk('D:'):
            for fil in files:
                try:
                    fname = os.path.join(os.path.abspath(root), fil)#将父录名与当前连接
                    fsize = os.path.getsize(fname)
                    self.labell['text'] = fname
                    if fsize >= filesize:
                        total += 1
                        self.entry.insert(tkinter.END, '%s, [%.2f M]\n' %(fname,fsize/1024/1024))
                except:
                    pass

    #按名称搜索文件
    def SearchFile(self,fname):
        total = 0
        fname = fname.upper()
        self.entry.delete(0.0, tkinter.END)
        for root, dirs, files in os.walk('D:'):
            for fil in files:
                try:
                    fn = os.path.join(os.path.abspath(root), fil)
                    fsize = os.path.getsize(fn)
                    self.labell['text'] = fn
                    if fil.upper().find(fname) >= 0:
                        total += 1
                        self.entry.insert(tkinter.END, fn + '\n')
                except:
                    pass

    def MainLoop(self):
        self.root.title ("Findfat")
        self.root.minsize (410,450)
        self.root.maxsize (410,450)
        self.root.mainloop()

if __name__ == "__main__":
    window = Window()

