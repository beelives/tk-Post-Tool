#!/usr/bin/env python
#encoding:utf-8

from Tkinter import *

headers ='''Cookie:
Referer:http://www.lijiejie.com/
User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0'''

copyright = '''A Simple Post Tool build with Tk GUI

1. Headers must be key:value format string
2. Form data can be either key:value format string or a url encoded string

LiJieJie     my@lijiejie.com    http://www.lijiejie.com
'''

class PostToolGUI():
    def __init__(self):
        self.root = root = Tk()
        root.withdraw()    #hide window
        root.title('Tk Post Tool')
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight() - 100    #a taskbar may lie under the screen
        root.resizable(False,False)

        from ImageTk import PhotoImage
        icon = PhotoImage(file='icon.gif')
        root.tk.call('wm', 'iconphoto', root._w, icon)

        Label(root, text='URL').grid(row=0, column=0, sticky=NW, padx=10, pady=10)
        self.txtURL = txtURL = Entry(root)
        txtURL.grid(row=0, column=1, sticky=EW)
        txtURL.focus_set()
        
        Label(root, text='Headers').grid(row=1, column=0, sticky=NW, padx=10)
        headers_bar = Scrollbar()
        self.txtHeaders = txtHeaders = Text(root, bg='#F5F5DC', yscrollcommand=headers_bar.set)
        txtHeaders.grid(row=1, column=1, sticky=W)
        txtHeaders.config(width=60, height=4)
        headers_bar.grid(row=1, column=2, sticky=NS)
        headers_bar.config(command=txtHeaders.yview)
        txtHeaders.insert(END,headers)
        txtHeaders.grid_columnconfigure(2, weight=1)
        
        Label(root, text='Form Data').grid(row=2, column=0, sticky=NW, padx=10, pady=10)
        data_bar = Scrollbar()
        self.txtData = txtData = Text(root, bg='#FAEBD7', yscrollcommand=data_bar.set)
        txtData.grid(row=2, column=1, sticky=W, pady=15)
        txtData.config(width=60, height=3)
        data_bar.grid(row=2, column=2, sticky=NS, pady=15)
        data_bar.config(command=txtData.yview)

        self.cmdPost = cmdPost = Button(root, text='Post', bg='#FFDEAD', width=15, command=lambda: self.cmd_click(self))
        cmdPost.grid(row=3, column=1, sticky=W)
        
        Label(root, text='Reponse').grid(row=4, column=0, sticky=NW, padx=10, pady=10)
        html_bar = Scrollbar()
        self.txtHTML = txtHTML = Text(root, yscrollcommand=html_bar.set)
        txtHTML.grid(row=4, column=1, pady=10)
        txtHTML.config(width=60, height=9)
        txtHTML.insert('end', copyright)
        txtHTML.tag_add("title", '1.0', txtHTML.index("1.0 lineend"))    #set font weight bold for title
        txtHTML.tag_configure('title', font='helvetica 12 bold')
        html_bar.grid(row=4, column=2, sticky=NS, pady=10)
        html_bar.config(command=txtHTML.yview)

        root.update_idletasks()
        root.deiconify()    #calculate window size
        root.withdraw()     #hide it
        #put it on screen center
        root.geometry('%sx%s+%s+%s' % (root.winfo_width() + 10, root.winfo_height(),
                                       (screen_width - root.winfo_width())/2, (screen_height - root.winfo_height())/2) )
        root.deiconify()

    def cmd_click(self, event):
        pass
    
        
if __name__ == '__main__':
    testapp = PostToolGUI()
    testapp.root.mainloop()