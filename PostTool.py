#!/usr/bin/env python
#encoding:utf-8

from ptGUI import PostToolGUI
import urllib
import httplib
import tkMessageBox
import threading
import chardet

class PostTool(PostToolGUI):
    def cmd_click(self, event):
        url = self.txtURL.get().lower().strip()
        if url=='':
            tkMessageBox.showinfo('Emptry URL', 'Please input a valid URL.')
            return
        
        self.protocol = 'http'
        if url.find('https://') >= 0:
            self.protocol = 'https'
        url = url.replace('https://', '').replace('http://', '')
        if url.find('/') >= 0:
            self.host = url[:url.find('/')]
            self.path = url[url.find('/') :]
        else:
            self.host = url
            self.path = '/'

        self.headers = {}
        str_headers = self.txtHeaders.get(1.0, 'end').replace('\r', '')
        try:
            encoding = chardet.detect(str_headers)['encoding']    #detect encoding
            if not encoding is None:
                str_headers = str_headers.decode(encoding, 'ignore')
        except:
            pass
        for line in str_headers.split('\n'):
            array = line.split(':')
            if len(array) > 1:
                self.headers[ array[0] ] = ''.join(array[1:])

        str_data = self.txtData.get(1.0, 'end').replace('\r', '')
        #encode unicode to utf8
        if isinstance(str_data, unicode):
            str_data = str_data.encode('utf8', 'ignore')
        elif isinstance(str_data, str):    #utf8 str
            pass
        else:    #not unicode nor utf8, decode first, and then encode utf8
            try:
                encoding = chardet.detect(str_data)['encoding']    #detect encoding
                if not encoding is None:
                    str_data = str_data.decode(encoding, 'ignore')
                str_data = str_data.encode('utf8', 'ignore')
            except:
                pass
        if str_data.find(':') < 0:
            data_type = 'str'
        elif str_data.find('=') < 0:
            data_type = 'dict'
        elif str_data.find(':') < str_data.find('='):
            data_type = 'str'
        else:
            data_type = 'dict'
        if data_type == 'str':
            self.params = str_data
        else:
            data = {}
            for line in str_data.split('\n'):
                array = line.split(':')
                if len(array) > 1:
                    data[ array[0] ] = ''.join(array[1:])
            self.params = urllib.urlencode(data)
        
        threading.Thread(target=post, args=(self,)).start()
            

def post(self):
    self.cmdPost.config(text='Posting...', state='disabled')
    self.txtHTML.delete('1.0', 'end')    #clear txtHTML
    try:
        if self.protocol == 'http':
            conn = httplib.HTTPConnection(self.host)
        else:
            conn = httplib.HTTPSConnection(self.host)
        self.cmdPost.config(state='disabled')    #disable the button
        conn.request(method='POST', url=self.path, body=self.params, headers=self.headers)
        response = conn.getresponse()
        self.txtHTML.insert('end', response.getheaders())
        self.txtHTML.insert('end', '\n\n')
        self.txtHTML.tag_add('headers', '1.0', 'current')    #add tag to headers
        html_doc = response.read()
        try:
            encoding = chardet.detect(html_doc)['encoding']
            if not encoding is None:
                html_doc = html_doc.decode(encoding, 'ignore')
        except:
            pass
        self.txtHTML.insert('end', html_doc.replace('\r', ''))
        self.txtHTML.tag_configure('headers', foreground='blue')
        
    except Exception, e:
        self.txtHTML.insert('end', unicode(e))
        self.txtHTML.tag_add("errmsg", '1.0', 'end')
        self.txtHTML.tag_configure('errmsg', foreground='red')
        
    self.cmdPost.config(text='Post', state='normal')
    return


app = PostTool()
app.root.mainloop()
