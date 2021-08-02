from Levenshtein import distance as ds
import pandas as pd
from Armor.enc_dcr import encrypt, decrypt
from github import Github
from decouple import config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import datetime as dt

messenger = "zeng.gooseofshifu@gmail.com"
password = config("APP_PASSWORD")

class ammends:
    def __init__(self, data, dob_data):
        self.data = data
        self.dob_data = dob_data
    
    def push_to_github(self, by_name):
        mdb_text = open('database.csv', 'r')
        text1=''.join([i for i in mdb_text])
        token=config('TOKEN')
        g = Github(token)

        user=g.get_user()
        repo = user.get_repo("Friends-Data")
        main_db = repo.get_contents("database.csv")
        #commiting to github
        by_name = by_name.split()[0]
        repo.update_file(main_db.path, "Commit by "+str(by_name), text1, main_db.sha, branch="main")
        
        dob_text = open('dob.csv', 'r')
        text2=''.join([i for i in dob_text])
        dob_db = repo.get_contents("dob.csv")
        repo.update_file(dob_db.path, "Commit by "+str(by_name), text2, dob_db.sha, branch="main")

    def make_edits(self, val_list, idx):
        cols=['Name', 'Gender', 'Relationship', 'Level','School/College', 'From Year', 'Living in']
        passkey=val_list.pop()
        last_edits = val_list.pop()
        for values, rows in zip(val_list, cols):
            if len(values)!=0:
                self.data.loc[idx, rows]=values

        if len(passkey)!=0:
            self.data.loc[idx, 'Passkey']=encrypt(passkey)

        self.data.loc[idx, 'Last edits'] = last_edits
        self.dob_data.loc[idx, 'name'] = val_list[0]

        self.data.to_csv("database.csv", index=False)
        self.dob_data.to_csv("dob.csv", index=False) #updating to local storage
        by_name = self.data.loc[idx, 'Name']
        self.push_to_github(by_name)
    
    def push_new(self, val_list):
        cols=['Name', 'email','Gender', 'Relationship', 'Level','School/College', 'From Year', 'Living in', 'Last edits']
        dob = val_list.pop()
        passkey=val_list.pop()

        dob_list = [dob, val_list[0], val_list[1]]
        df_main={}
        df_dob={}
        for col, values in zip(cols, val_list):df_main[col]=values
        for col, values in zip(['dob','name', 'email'],dob_list):df_dob[col]=values
        df_main['Passkey']=encrypt(passkey)

        self.data = self.data.append(df_main, ignore_index=True)
        self.dob_data = self.dob_data.append(df_dob, ignore_index=True)

        self.data.to_csv("database.csv", index=False) #updating to local storage
        self.dob_data.to_csv("dob.csv", index=False)
        by_name = self.data.loc[len(self.data)-1, 'Name']
        self.push_to_github(by_name)

    def update_email(self, mail, idx):
        self.data.loc[idx, 'email']=mail
        self.dob_data.loc[idx, 'email']=mail

        self.data.to_csv('database.csv', index=False)
        self.dob_data.to_csv("dob.csv", index=False)
        by_name = self.data.loc[idx, 'Name']
        self.push_to_github(by_name)
    
    def get_bday_list(self):
        today = dt.datetime.today()
        yesterday = today-dt.timedelta(1)

        name_list = []
        for i in range(len(self.dob_data)):
            date = self.dob_data['dob'][i] 
            td, tm = today.day, today.month
            yd, ym = yesterday.day, yesterday.month
            dd, dm = date.day, date.month

            if (dd==td or dd==yd) and (dm==tm or dm==ym):
                name_list.append(self.dob_data['name'][i])
        
        return name_list



class checker:
    name = " "
    def __init__(self, data):
        self.data = data
    
    def mispell(self):
        min=ds(self.name, 'Random Name')
        sugg='Random Name'
        for n in self.data.Name:
            diff=ds(self.name, n)
            if diff<min:
                sugg=n
                min=diff
        return sugg if min<5 else "No name"

    def authethicate(self, key):
        lname=self.name.lower()
        try:
            idx=self.data[self.data['Name']==lname].index[0]
        except:
            return (False, -1)
        return (True, idx) if decrypt(self.data.Passkey[idx])==key else (False, -1)
    
    def good_name(self, name1):
        lis=name1.split()
        for i in range(len(lis)):
            lis[i]=lis[i].capitalize()
        return ' '.join(lis)
    
    def display_friendlist(self):
        df= pd.concat([self.data['Name'].apply(lambda x:self.good_name(x)), self.data['Relationship'], self.data['Level']], axis=1)
        return df.sort_values("Name", axis=0)
    
    def verify_mail(self, mail):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Verify your email for Friends-circle"
        message["From"] = messenger
        message["To"] = mail

        key=str(random.randint(1000,8000))

        html = """
            <html>
            <body>
            <div style="font-family:Trebuchet MS; font-size: 120%; font-weight: 600;">Hello! I am Zeng the messenger bird of Master Tuhin.</div>
            <p style="font-family:Segoe UI; font-size: large;">I carried you the verification code from email servers.
            <br><br>Here is your E-mail verification code: <b>{code}</b><br>
            Enter this code in the app's text space.</p>
            <br><br>
            <div style="font-family: cursive; font-weight: 540; font-size: large;"><i>From,<br>
            Zeng the Goose<br>
            (Context: Kung Fu Panda).</i>
            <a href="https://kungfupanda.fandom.com/wiki/Zeng">Why am I named Zeng?</a></div>
            <br><br>
            <div style="cursor: not-allowed; border: lightslategrey; border-style: groove; border-radius: 6px;
            background-color:darkgrey; padding: 20px; border-bottom: dimgray; width: 550px;">
            <b style="font-family: Verdana; font-size: medium;">THIS IS AN AUTOMATED EMAIL. PLEASE DON'T REPLY BACK.</b></div>
            <footer style="border: rgb(145, 157, 170); border-style: groove; border-radius: 6px; border-top: aliceblue;
            background-color: rgb(195, 199, 204); padding: 5px; font-family: Courier New; font-size:small; width: 582px;">
            <b>© tsd-friends-circle 2021</b></footer>
            </body>
            </html>"""

        message.attach(MIMEText(html, "html"))
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(messenger, password)  
        s.sendmail(messenger, mail, message.as_string().format(code=key))
        s.quit()

        return key
