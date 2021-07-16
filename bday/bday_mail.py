#This code run every day and sends mail to people who have birthdays that day.
#hosted on wayscript https://wayscript.com/script/4sL1Tzzd

#mail for wishing birthday
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config
import pandas as pd
import datetime as dt

def get_bday_list(dob_data):
    today = dt.datetime.today()

    name_list = []
    for i in range(len(dob_data)):
        date = dob_data['dob'][i] 
        if (today.day==date.day and today.month==date.month):
            name_list.append((dob_data['name'][i].split()[0].capitalize(), dob_data['email'][i]))
        
    return name_list

dob = pd.read_csv("https://raw.githubusercontent.com/Gituhin/Friends-Data/main/dob.csv", parse_dates=['dob'])

bdays = get_bday_list(dob)
print(bdays)
messenger = "zeng.gooseofshifu@gmail.com"
password = config("APP_PASSWORD")

if not len(bdays) == 0:
    
    for details in bdays:

        to = details[1]
        message = MIMEMultipart("alternative")
        message["From"] = messenger
        message["To"] = to
        message["Subject"] = "HAPPY BIRTHDAY "+details[0]+"!"


        html = """
        <html>
            <body>
                <div style="border:rgba(12, 108, 233, 0.719); border-style:double;
                padding: 8px; width: 315px; border-width: 6px; border-radius: 25px; background: rgb(255, 207, 189);font-family:cursive; font-size: 145%;
                font-weight: 600; font-style: italic; color: rgb(180, 57, 57);">
                <span style="font-style: normal;">🎁</span> Happy birthday to you! <span style="font-style: normal">🎉</span></div><br>
                <div style="font-family:Georgia; font-stretch:extra-expanded; font-size: 22px; color: rgb(5, 5, 219);"><b>Cheer up❗❗</b></div>
                <p style="font-family:sans-serif; color: rgb(25, 58, 58); font-size:17px;">Hey!, I am Zeng the goose of Master Tuhin and I am here to wish you many many happy returns of this joyful day
                    on behalf of my master. Along with this we have prepared a small gift for you on this auspicious occasion.
                <br><br>To access the gift go to the friends-circle app <a href="https://tsd-friends-circle.herokuapp.com">Go to app</a> and <b>type your name in search bar.</b>
                Gift will be available till tomorrow. So visit ASAP. <big>😉</big>
                <br><br>Hope you will like it with a big <big>💚</big>. Wish you all success in life🎇.<br> For now have a pleasant day ahead. </p>
                <div style="font-family: Cambria; font-weight: 580; font-size: medium;"><br>From,<br>
                    Tuhin Subhra De, <span style="color: rgb(88, 87, 87); font-weight: 500;">via Zeng the Goose</span><br>
                    (Context: Kung Fu Panda).
                    <a href="https://kungfupanda.fandom.com/wiki/Zeng">Why am I named Zeng?</a></div>
                    <br><br>
                    <div style="border: lightslategrey; border-style:hidden; border-radius: 6px;
                        background-color:darkgrey; padding: 20px; border-bottom: dimgray; width: 460px;">
                        <b style="font-family: Verdana; font-size: medium;">I AM A ROBOT SO PLEASE DON'T REPLY BACK.🚫</b></div>
                    <footer style="border: rgb(145, 157, 170); border-style:hidden; border-radius: 6px; border-top: aliceblue;
                                background-color: rgb(195, 199, 204); padding: 8px; font-family: Courier New; font-size:small; width: 485px;">
                        <b>© tsd-friends-circle 2021</b></footer>
            </body>
        </html>"""

        print("Attaching mail...")
        message.attach(MIMEText(html, "html"))
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        print("Logging in...")
        s.login(messenger, password) 
        print("sending mail...") 
        s.sendmail(messenger, to, message.as_string())
        s.quit()
        print("mail sent to", details[0], "\n")

else:
    pass
