import random as rd

def encrypt(string):
    rkey=rd.randint(1,100)
    passkey=[ord(string[c])*(c+1)+rkey for c in range(len(string))]
    passkey.append(rkey)
    return str(passkey)

def decrypt(st):
    lis=[int(e) for e in st[1:len(st)-1].split(sep=', ')]
    dkey=lis.pop()
    st=[chr((lis[e]-dkey)//(e+1)) for e in range(len(lis))]
    return ''.join(st)
    