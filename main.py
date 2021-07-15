import streamlit as st
from streamlit import caching
import SessionState as ss
import datetime as dt
import pandas as pd
from PIL import Image
from class_funcs import ammends, checker
st.set_page_config(page_title='Friends Circle')

def write_dt(idx, data):
    gender=data.Gender[idx]
    st.markdown("***Your friendship details with Tuhin:***")
    if gender=='Male':
        st.write("Hello! Sir "+check.good_name(check.name))
    else:
        st.write("Hello! Madame "+check.good_name(check.name))
    st.write("E-mail ID: ", data.email[idx])
    st.write("Gender:", data.Gender[idx])
    st.write("Relationship:", data.Relationship[idx])
    st.write("Level:", data.Level[idx])
    st.write("School/College:", data['School/College'][idx])
    st.write("From Year:", data['From Year'][idx])
    st.write('You are Living in:', data['Living in'][idx])

@st.cache(show_spinner=True, suppress_st_warning=True)
def bday_wish(name):
    bday_list = editor.get_bday_list()
    if name.lower() in bday_list:
        st.markdown("# 🎉Happy birthday {name}! Many Many happy returns of the day.🥳🎉".format(name=name.split()[0].capitalize()))
        st.write("Play video below")
        st.balloons()
        video = open("bday\hbd_new.mp4", "rb")
        video = video.read()
        st.video(video, format='video/mp4', start_time=0)
    else:
        pass


st.title("Friends Circle")
img = Image.open("image.jpg")
st.image(img, width=300)
st.markdown("## *Hola amigos!!*")
st.header("You have landed here to have a glance of your friendship with Tuhin")
st.markdown("  \n")
st.subheader("The Web app doesn't have any commercial or social purpose, it is\
    to test some methods and processes for developing a better platform in future.")
st.write("How to use this? (*Read the instructions below*)")
with st.beta_expander("click here for instructions"):
    st.markdown("1.  **Add as Friend: ** To do that, Type your name in the Name box below.\
                    If it shows your details then you are already in friend. If it shows\
                         *No such person found*, then feel free to add yourself as a\
                     friend by going to the *sidebar* on the left. Enter you email and verify it.\
                     After verification, fill all details and click add as a friend. Woohoo! You're done.  \n\
                \n2.  **Register yourself**: To do that, Type your name in the Name box below & press enter\
                    if it shows your email then you are already registered\
                     registered & if not(*shows nan*) then add your email.  \n\
                 \n3.  **Login: ** To access any feature you need to login, scroll down\
                     to the dropdown bar saying *click here to login*. Click that to open Credentials\
                         Box, Enter yor name and passkey to login.  \n\
                 \n4.  **Changing details:(*after logging in*)** If you find any of your details wrong or missing\
                     you are free to change (**including changing passkey**) them under edit details dropdown.  \n\
                 \n5.  **Changing/adding Email(*after logging in*)**: You can also edit/add your\
                     email ID by going to edit/add email dropdown. Enter your new email and\
                         verify it by entering the code. Press enter and it will be updated.")

@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def fetch_data(): #loading data directly from github
    return (pd.read_csv("https://raw.githubusercontent.com/Gituhin/Friends-Data/main/database.csv"),
            pd.read_csv("https://raw.githubusercontent.com/Gituhin/Friends-Data/main/dob.csv", parse_dates=['dob']))

try:
    with st.spinner("Fetching Data..."):
        (data, dob_data) = fetch_data()
except:
    st.error("Failed to fetch from database, All further processes terminated.")
    st.stop()

editor = ammends(data, dob_data)
name = st.text_input("Enter Your Full name", "Type Here ...")
name=name.lower()
check = checker(data)
check.name = name

try:
    idx=data[data['Name']==check.name].index[0]
    bday_wish(name)
    write_dt(idx, data)
except:
    if name=="": #blank name
        st.error("Please enter a name!")

    elif name!="type here ...": #same as default input
        if check.mispell()=="No name": #random name
            st.error("No such person found. Feel Free to add yourself as a friend.")
        else:
            check.name=check.mispell()
            warn="Did you mean "+check.good_name(check.name)+"?"
            st.warning(warn+" Here are the details of possible you.")
            idx=data[data['Name']==check.name].index[0]
            bday_wish(check.name)
            write_dt(idx, data)
            st.info("If you find any details wrong, edit it below.")
            
    else:
        st.info("Enter a name")

st.text('\n')

if st.button('Display Friend list'):
    with st.spinner("Displaying list..."):
        st.dataframe(check.display_friendlist())
        

st.markdown("***") # for line divider
st.text('\n\n')
log=st.empty()
auth_state=ss.get(login=False, idx=-7)
log.write("Login: "+str(auth_state.login))

with st.beta_expander("Click here to login"):
    form=st.form(key='my_form')
    en_name=form.text_input(label='Enter Your current Full Name:')
    en_passkey=form.text_input("Enter your passkey", type='password')
    submit_button = form.form_submit_button(label='Login')

    if submit_button:
        check.name = en_name
        (auth_state.login, auth_state.idx)=check.authethicate(en_passkey)
        if auth_state.login:
            log.empty()
            log.write("Login: "+str(auth_state.login))
            st.success("Verified as: "+check.good_name(check.name))
        else:
            st.error("The Name and Passkey doesn't match!")


with st.beta_expander("Edit your details:"):       # editing existing details     
    if auth_state.login:
        st.info("Go with your desired edits: (Leave blank if existing is correct)")
        forme=st.form(key="edit_form")
        edit_name=forme.text_input(label='Enter your correct name')
        edit_gender=forme.radio('Gender: ', ("Male", "Female"))
        edit_relation=forme.text_input(label='Enter your correct relationship')
        edit_level=forme.text_input(label='Enter your correct Level')
        edit_insti=forme.text_input(label='Enter School/College')
        edit_year=forme.text_input(label='Enter when you two met')
        edit_place=forme.text_input(label='Enter Place of living')
        edit_pass=forme.text_input(label='Enter new passkey')
        p_edit = forme.form_submit_button(label='Push Edits')

        if p_edit:
            val_list=[edit_name.lower(), edit_gender, edit_relation, edit_level, edit_insti, edit_year, edit_place, dt.datetime.now(),edit_pass]
            try:
                with st.spinner("Updating details..."):
                    editor.make_edits(val_list, auth_state.idx)
                st.success("Details Updated.")
            except:
                st.error("Can't Update right now. Update failed.")
                

        if st.button("click twice to logout"):
            auth_state.login=False
            auth_state.idx=-7
            st.info("Click once more")
    else:
        st.write("Not logged in")

edit_ver=ss.get(email="abc@sthm.com", state1=False, verified=False, v_code=str(1))

with st.beta_expander('Edit/Add your email:'): # editing email
    if auth_state.login:
        edit_ver.email=st.text_input("Enter your email:")

        if st.button("Verify email and update"):
            status=st.empty()
            if len(edit_ver.email)==0:
                st.error("email can't be blank")

            elif edit_ver.email in str(data['email']):
                st.error("The email is already associated with someone. Please check again.")
            else:
                with st.spinner("Sending Verification Code to your email... Wait for input code box to appear"):
                    edit_ver.v_code=check.verify_mail(edit_ver.email)
                    edit_ver.state1=True

                status.info("A verification code has been sent to your email. Check your inbox/spam\
                    for the name of Zeng.gooseofshifu.\
                        Your email will be automatically updated after verification.")

        with st.beta_container():
            try:
                if edit_ver.state1:       
                    u_code=st.text_input("Enter your verification code & Press Enter:")
                    if u_code==edit_ver.v_code:
                        with st.spinner("Updating Email..."):
                            editor.update_email(edit_ver.email, auth_state.idx)
                        st.success("email updated.")
                        edit_ver.state1=False
                    elif len(u_code)==0 :
                        st.info("Enter code")
                    elif u_code!=edit_ver.v_code:
                        st.error("wrong code! Please check again.")
            except:
                pass
            
            if st.button("Click twice to logout"):
                auth_state.login=False
                auth_state.idx=-7
                st.info("Click once more")
    else:
        st.write("Not logged in")



#adding new friend
ver=ss.get(mail_state1=False, mail_state2=False,email='abc@sth.com',v_code=str(1))
with st.sidebar:
    st.subheader("Add as a new Friend")
    ver.email=st.text_input("enter your email")

    if st.button("verify"):
        if len(ver.email)==0:
            st.error("Email can't be blank")

        elif not ver.email in str(data['email']):
            with st.spinner("Sending Verification Code to your email\
                ... Wait for input code box to appear."):
                ver.v_code=check.verify_mail(ver.email)
                ver.mail_state1=True
            st.info("A verification code has been sent to your email. Check your inbox/spam\
                for the name of Zeng.gooseof shifu.")
        
        else:
            st.error("Entered email already exists. Please check again")


with st.sidebar:
    try:
        if ver.mail_state1:       
            u_code=st.text_input("verification code:")
            code_check=st.empty()
            if u_code==ver.v_code and len(u_code)!=0:
                code_check.empty()
                code_check.success("Verified")
                ver.mail_state2=True
                ver.mail_state1=False
            elif len(u_code)==0 :
                code_check.info("Enter code")
            else:
                code_check.empty()
                code_check.error("wrong code! Please check again.")
    except:
        pass

with st.sidebar:
    try:
        if ver.mail_state2:
            today = dt.datetime.today()
            formn=st.form(key="edit_formnew")
            name=formn.text_input(label='Enter your full name: ')
            gender=formn.radio('Gender: ', ("Male", "Female"))
            relation=formn.text_input(label='Enter your relationship:')
            level=formn.text_input(label='Enter your relationship level(Eg.school friend/college friend etc.): ')
            insti=formn.text_input(label='Enter School/College where you met')
            year=formn.text_input(label='Enter the year you two met')
            place=formn.text_input(label='Enter your place of living')
            dob=formn.date_input("Date of birth(year isn't important. Can choose random year)", min_value=dt.datetime(1980, 1, 1), max_value=today, value=dt.datetime(2000, 1, 1))
            passk=formn.text_input(label='Enter new passkey for login(Remember this for later use)')
            new_friend = formn.form_submit_button(label='Create new friend')

            if new_friend:
                new_list=[name.lower(),ver.email, gender, relation, level, insti, year, place, dt.datetime.now(), passk, dob]
                try:
                    with st.spinner("Adding details... New Friend."):
                        editor.push_new(new_list)
                    st.success("Successfully added as new friend.")
                    st.text("Refresh page & check, may take time to update.")
                    ver.mail_state2=False
                    caching.clear_cache()
                except:
                    st.error("Failed to create a new friend.")
    except:
        pass

st.markdown("***") # for line divider
st.text('\n\n')
col1, col2= st.beta_columns((1,1.4))
col1.write("Visit my website for more projects: [Click here](https://www.tuhinsde.codes)")
#col1.write("[Click here](https://sites.google.com/view/tuhinsubhrade/home)")
col2.write("For Feedback/errors Fill out this Google Form: [Feedback/Error](https://forms.gle/NyguGsx9NFieJdyy6)")
st.write("*In view point of a developer, Visit working Github repo for this app: [Github Repo](https://github.com/Gituhin/Friends-Data)*")
st.markdown("***")
st.markdown("***")
st.subheader("This App got featured in Streamlit's Weekly AI podcast for second week of July 2021\
    [View Podcast](https://discuss.streamlit.io/t/weekly-roundup-ai-podcasts-visualizing-graph-embeddings-google-sheet-automations-and-more/14512)")
st.markdown("***") # for line divider
st.text('\n\n')
st.text("© tsd-friends-circle V 3.0 | Tuhin Subhra De 2021")
#end#
