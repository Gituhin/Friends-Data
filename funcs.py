## only functions
from Levenshtein import distance as ds
from numpy.core.defchararray import decode
import pandas as pd
from Armor.enc_dcr import encrypt, decrypt

def fetch_database():
    return pd.read_csv('database.csv')

def good_name(name):
    lis=name.split()
    for i in range(len(lis)):
        lis[i]=lis[i].capitalize()
    return ' '.join(lis)

def display_friendlist(data):
    return pd.concat([data['Name'].apply(lambda x:good_name(x)), data['Relationship'], data['Level']], axis=1)

def mispell(name, data):
    min=ds(name, 'durga de')
    sugg='durga de'
    for n in data.Name:
        diff=ds(name, n)
        if diff<min:
            sugg=n
            min=diff
    return sugg if min<5 else "No name"

def authethicate(name, key, data):
    lname=name.lower()
    try:
        idx=data[data['Name']==lname].index[0]
    except:
        return (False, -1)
    return (True, idx) if decrypt(data.Passkey[idx])==key else (False, -1)

def make_edits(data, val_list, idx):
    cols=['Name', 'Gender', 'Relationship', 'Level','School/College', 'From Year', 'Living in']
    last_edit=val_list.pop()
    passkey=val_list.pop()

    for values, rows in zip(val_list, cols):
        if len(values)!=0:
            data.loc[idx, rows]=values

    if len(passkey)!=0:
        data.loc[idx, 'Passkey']=encrypt(passkey)
    data.loc[idx, 'Last edits']=last_edit
    data.to_csv("database.csv", index=False) #updating to local storage

    text=open('database.csv', 'r')
    text1=''.join([i for i in text])
    g = Github()

    user=g.get_user("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")
    repo = user.get_repo("Friends-Data")
    file = repo.get_contents("database.csv")
    #commiting to github
    repo.update_file(file.path, "Commit by Users", text1, file.sha, branch="main")
