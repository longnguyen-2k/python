import hashlib


with open('top1m.txt','r') as file:
    with open('top1m_hash.txt','w') as fileHash:
        list = set(file.readlines())
        for s in list :
            s=s.strip()
            fileHash.write(hashlib.md5(s.encode()).hexdigest()+"\n")