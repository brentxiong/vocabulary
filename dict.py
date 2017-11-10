# -*- coding:utf-8 -*-
import sys
import random
import re
import requests
from bs4 import BeautifulSoup
import copy
import json
from Tkinter import *

def randHeader():
    head_connection = ['Keep-Alive', 'close']
    head_accept = ['text/html, application/xhtml+xml, */*']
    head_accept_language = ['zh-CN,fr-FR;q=0.5', 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']
    head_user_agent = ['Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                       'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11',
                       'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                       'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0'
                       ]
    header = {
        'Connection': head_connection[0],
        'Accept': head_accept[0],
        'Accept-Language': head_accept_language[1],
        'User-Agent': head_user_agent[random.randrange(0, len(head_user_agent))]
    }
    return header


def getCurrentTime():

    return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))


def getURL(url, tries_num=5, sleep_time=0, time_out=10, max_retry=5, isproxy=0, proxy=None, encoding='utf-8'):

    header = randHeader()
    try:
        res = requests.Session()
        if isproxy == 1:
            if proxy is None:
                print('===   proxy is empty     ====')
                return None
            res = requests.get(url, headers=header, timeout=time_out, proxies=proxy)
        else:
            res = requests.get(url, headers=header, timeout=time_out)
        res.raise_for_status()
    except requests.RequestException as e:
        if tries_num > 0:
            time.sleep(sleep_time)
            print(getCurrentTime(), url, 'URL Connection Error in ', max_retry - tries_num, ' try')
            return getURL(url, tries_num - 1, sleep_time + 10, time_out + 10, max_retry, isproxy, proxy)
        return None

    res.encoding = encoding
    return res


def queryWords(word):

    url = 'http://dict.youdao.com/w/{}/'.format(word)
    html = getURL(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    trans_container = soup.find(class_='trans-container')

    if not trans_container:
        ''' not found the translation '''
        return [word]

    trans_li = trans_container.find_all('li')
    trans_data = [li.text.strip() for li in trans_li]
    return trans_data

class learning_statistics():
    def __init__(self):
        pass
    
class App(object):
    '''
    '''
    def __init__(self, master=None, **kwargs):
        
        #Frame.__init__(self, master)
        self.root = master
        w, h = self.root.maxsize()
        self.root.geometry("{}x{}".format(w, h)) 
        
        self.frame = Frame(self.root)
        self.frame.pack(expand=1, fill=BOTH)
        
        #self.state = False
        #self.root.bind("<F10>", self.toggle_fullscreen)
        #self.root.bind("<Escape>", self.end_fullscreen)
        
        self.init_variables()
        self.prepare_vocabulary()
        self.init_ui()
        
    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.root.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.root.attributes("-fullscreen", False)
        return "break"
    
    def init_variables(self):
        self.word_current = StringVar()
        
        self.word_opt_1 = StringVar() 
        self.word_opt_2 = StringVar()
        self.word_opt_3 = StringVar()
        self.word_opt_4 = StringVar()
        self.word_opt_5 = StringVar()
        self.word_opt_1.set('option 1')
        self.word_opt_2.set('option 2')
        self.word_opt_3.set('option 3')
        self.word_opt_4.set('option 4') 
        self.word_opt_5.set('option 5')
        
    def init_ui(self):
        '''
        '''
        self.lab_word = Label(self.frame, textvariable=self.word_current, height=2, fg="light green", bg="dark green", anchor='center', font = "Helvetica 72 bold")
        self.lab_word.pack(side=TOP,fill=BOTH,expand=1)
        self.lab_word.bind("<Button-1>",self.change_case)
        
        self.lab_opt_1 = Label(self.frame, textvariable=self.word_opt_1, relief='solid',justify='left',bg='lightgray',wraplength=180, width=20, height=20, anchor='nw')
        self.lab_opt_1.pack(side=LEFT,expand=1, fill=BOTH)
        self.lab_opt_1.bind("<Button-1>",self.change_case)
        
        self.lab_opt_2 = Label(self.frame, textvariable=self.word_opt_2, relief='solid',justify='left', bg='lightgray',wraplength=180, width=20, height=20, anchor='nw')
        self.lab_opt_2.pack(side=LEFT, fill=BOTH, expand=1)
        self.lab_opt_2.bind("<Button-1>",self.change_case)
        
        self.lab_opt_3 = Label(self.frame, textvariable=self.word_opt_3, relief='solid',justify='left', bg='lightgray',wraplength=180, width=20, height=20, anchor='nw')
        self.lab_opt_3.pack(side=LEFT, fill=BOTH, expand=1)
        self.lab_opt_3.bind("<Button-1>",self.change_case)
        
        self.lab_opt_4 = Label(self.frame, textvariable=self.word_opt_4,relief='solid',justify='left', bg='lightgray',wraplength=180, width=20, height=20, anchor='nw')
        self.lab_opt_4.pack(side=LEFT, fill=BOTH, expand=1)
        self.lab_opt_4.bind("<Button-1>",self.change_case)
        
        self.lab_opt_5 = Label(self.frame, textvariable=self.word_opt_5,relief='solid',justify='left', bg='lightgray',wraplength=180, width=20, height=20, anchor='nw')
        self.lab_opt_5.pack(side=LEFT, fill=BOTH, expand=1)
        self.lab_opt_5.bind("<Button-1>",self.change_case)
        
        self.display_options(self.get_temp_group(self.index_current))
    def prepare_vocabulary(self):
        '''
        '''
        fp = file('lesson_1.json','r')  
        vul = json.loads(fp.read())
        '''
        for k, v in vul.items():
            print
            print k
            for j in v:
                #print j.encode('utf-8')
                print j
            print
            print '==========='
        '''
        self.index_max = len(vul)
        self.index_current = 0
        self.words = vul.keys()
        self.translations = vul.values()
        self.word_current.set( self.words[self.index_current])
        

  
  
        #print random.sample(vul.keys(),5)
        #print random.sample(vul.values(),5)
        #self.word_opt_2.set(''.join([s.strip()+'\r\n' for s in random.choice(self.translations)]))
    def display_options(self, temp_group_translations):
        self.word_opt_1.set(''.join([s.strip()+'\r\n' for s in temp_group_translations[0]]))
        self.word_opt_2.set(''.join([s.strip()+'\r\n' for s in temp_group_translations[1]]))
        self.word_opt_3.set(''.join([s.strip()+'\r\n' for s in temp_group_translations[2]]))
        self.word_opt_4.set(''.join([s.strip()+'\r\n' for s in temp_group_translations[3]]))
        self.word_opt_5.set(''.join([s.strip()+'\r\n' for s in temp_group_translations[4]]))
        self.lab_opt_1["bg"] = 'gray'
        self.lab_opt_2["bg"] = 'gray'
        self.lab_opt_3["bg"] = 'gray'
        self.lab_opt_4["bg"] = 'gray'
        self.lab_opt_5["bg"] = 'gray'
    def get_temp_group(self, index_current):
        temp_words = copy.deepcopy(self.words)
        temp_word = temp_words.pop(index_current)
        temp_translations = copy.deepcopy(self.translations)
        temp_translation = temp_translations.pop(index_current)

        temp_group_translations = random.sample(temp_translations,4)
        temp_group_translations.append(temp_translation)
        random.shuffle(temp_group_translations)
        return temp_group_translations
    def convert_vocabulary(self,filename):
        '''
        fobj = open('lesson_1','r')
        dic = {}
        for line in fobj:
            print
            print line
            li = queryWords(line)
            
            li2=[]
            for l in li:
                l.encode('utf-8')
                print l
                li2.append(l)
            print
            dic[line] = li2
            #i = raw_input("===================")
            #if i == 'q':
                #break
        fobj.close()
        #js = json.dumps(dic)
        jsfile = open('lesson_1.json','w')
        jsfile.write(json.dumps(dic))
        jsfile.close()
        '''
        
    def change_case(self, event=None):
        '''
        '''
        if event.widget == self.lab_word:
            if self.index_current < self.index_max - 1:
                self.index_current = self.index_current + 1
            else:
                self.index_current = 0
            print self.index_current               
            self.word_current.set( self.words[self.index_current])
            self.display_options(self.get_temp_group(self.index_current))
            #self.lab_word.config(text=new_text)
        if event.widget == self.lab_opt_1:
            if self.word_opt_1.get() == ''.join([s.strip()+'\r\n' for s in self.translations[self.index_current]]):
                self.lab_opt_1["bg"] = 'darkgreen'
            else:
                self.lab_opt_1["bg"] = 'darkred'
        if event.widget == self.lab_opt_2:
            if self.word_opt_2.get() == ''.join([s.strip()+'\r\n' for s in self.translations[self.index_current]]):
                self.lab_opt_2["bg"] = 'darkgreen'
            else:
                self.lab_opt_2["bg"] = 'darkred'
        if event.widget == self.lab_opt_3:
            if self.word_opt_3.get() == ''.join([s.strip()+'\r\n' for s in self.translations[self.index_current]]):
                self.lab_opt_3["bg"] = 'darkgreen'
            else:
                self.lab_opt_3["bg"] = 'darkred'
        if event.widget == self.lab_opt_4:
            if self.word_opt_4.get() == ''.join([s.strip()+'\r\n' for s in self.translations[self.index_current]]):
                self.lab_opt_4["bg"] = 'darkgreen'
            else:
                self.lab_opt_4["bg"] = 'darkred'
        if event.widget == self.lab_opt_5:
            if self.word_opt_5.get() == ''.join([s.strip()+'\r\n' for s in self.translations[self.index_current]]):
                self.lab_opt_5["bg"] = 'darkgreen'
            else:
                self.lab_opt_5["bg"] = 'darkred'
        
if __name__ == '__main__':
    # create the application
    root=Tk()
    myapp = App(root)

    #
    # here are method calls to the window manager class
    #
    #myapp.master.title("My Vocabulary Application")
    #myapp.master.maxsize(1000, 600)

    # start the program
    #myapp.mainloop()
    root.mainloop()

