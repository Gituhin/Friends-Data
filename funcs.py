## only functions
from Levenshtein import distance as ds
import pandas as pd
from Armor.enc_dcr import encrypt, decrypt
from github import Github
from decouple import config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

messenger = "zeng.gooseofshifu@gmail.com"
password = config("APP_PASSWORD")

def good_name(name):
    lis=name.split()
    for i in range(len(lis)):
        lis[i]=lis[i].capitalize()
    return ' '.join(lis)

def display_friendlist(data):
    df= pd.concat([data['Name'].apply(lambda x:good_name(x)), data['Relationship'], data['Level']], axis=1)
    return df.sort_values("Name", axis=0)

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

def verify_mail(mail):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Verify your email for Friends-circle"
    message["From"] = messenger
    message["To"] = mail

    key=str(random.randint(1000,8000))
    html="""\
    <html>
    <body>
    <p>Hello! I am Zeng the messenger bird of Master Tuhin.
    <br>I will be responsible for carrying to you the messages sent by your friends
    on my master's web Application tsd-friends-circle.</p>

    <p>Here is your E-mail verification code: <b>{code}</b><br>
    Enter this code in the app.<br><br>Regards,<br>
    Zeng Goose (Context: Kung Fu Panda).
    <a href="https://kungfupanda.fandom.com/wiki/Zeng">Why am I named Zeng?</a>
        <br><br><b>THIS IS AN AUTOMATED MAIL. PLEASE DON'T REPLY BACK.</b>
    </p>
    </body>
    </html>"""
    message.attach(MIMEText(html, "html"))

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(messenger, password)  
    s.sendmail(messenger, mail, message.as_string().format(code=key))
    s.quit()

    return key

def push_to_github():
    text=open('database.csv', 'r')
    text1=''.join([i for i in text])
    token=config('TOKEN')
    g = Github(token)

    user=g.get_user()
    repo = user.get_repo("Friends-Data")
    file = repo.get_contents("database.csv")
    #commiting to github
    repo.update_file(file.path, "Commit by Users", text1, file.sha, branch="main")

    
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
    push_to_github()


def update_email(data, mail, idx):
    data.loc[idx, 'email']=mail
    data.to_csv('database.csv', index=False)
    push_to_github()

def push_new(data, val_list):
    cols=['Name', 'email','Gender', 'Relationship', 'Level','School/College', 'From Year', 'Living in', 'Last edits']
    passkey=val_list.pop()

    df={}
    for col, values in zip(cols, val_list):df[col]=values
    df['Passkey']=encrypt(passkey)
    data=data.append(df, ignore_index=True)
    data.to_csv("database.csv", index=False) #updating to local storage
    push_to_github()