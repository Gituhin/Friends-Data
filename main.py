import streamlit as st
import funcs as fn
import SessionState as ss
import datetime as dt

st.set_page_config(page_title='Friends Circle', page_icon=":smile:")
def fetch_dt(idx, data):
    gender=data.Gender[idx]
    st.markdown("***Your friendship details with Tuhin:***")
    if gender=='Male':
        st.write("Hello! Sir "+fn.good_name(data.Name[idx]))
    else:
        st.write("Hello! Madame "+fn.good_name(data.Name[idx]))
    st.write("E-mail ID: ", data.email[idx])
    st.write("Gender:", data.Gender[idx])
    st.write("Relationship:", data.Relationship[idx])
    st.write("Level:", data.Level[idx])
    st.write("School/College:", data['School/College'][idx])
    st.write("From Year:", data['From Year'][idx])
    st.write('You are Living in:', data['Living in'][idx])


st.title("Friends Circle")
st.header("Hola amigos!!")
st.subheader("You have landed here to have a glance of your friendship,\
     with Tuhin and mutual friends. The purpose of this Web app is to keep a track of your exchanged notes with\
          others in a social way.")
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

data=fn.fetch_database()
name = st.text_input("Enter Your Full name", "Type Here ...")
name=name.lower()

try:
    idx=data[data['Name']==name].index[0]
    fetch_dt(idx, data)
except:
    if name=="": #blank name
        st.error("Please enter a name!")

    elif name!="type here ...": #same as default input
        if fn.mispell(name, data)=="No name": #random name
            st.error("No such person found. Feel Free to add yourself as a friend.")
        else:
            name=fn.mispell(name, data)
            warn="Did you mean "+fn.good_name(name)+"?"
            st.warning(warn+" Here are the details of the possible you.")
            idx=data[data['Name']==name].index[0]
            fetch_dt(idx, data)
            st.info("If you find any details wrong, edit it below.")
    else:
        st.info("Enter a name")

st.text('\n')

if st.button('Display Friend list'):
    with st.spinner("Displaying list..."):
        st.dataframe(fn.display_friendlist(data))
        

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
        (auth_state.login, auth_state.idx)=fn.authethicate(en_name, en_passkey, data)
        if auth_state.login:
            log.empty()
            log.write("Login: "+str(auth_state.login))
            st.success("Verified as: "+fn.good_name(en_name))
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
            val_list=[edit_name.lower(), edit_gender, edit_relation, edit_level, edit_insti, edit_year, edit_place, edit_pass, dt.datetime.now()]
            try:
                with st.spinner("Updating details..."):
                    fn.make_edits(data, val_list, auth_state.idx)
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
            with st.spinner("Sending Verification Code to your email... Wait for input code box to appear"):
                edit_ver.v_code=fn.verify_mail(edit_ver.email)
                edit_ver.state1=True

            status.info("A verification code has been sent to your email. Check your inbox/spam\
                for the name of Zeng.gooseofshifu.\
                    Your email will be automatically updated after verification.")
        with st.beta_container():
            try:
                if edit_ver.state1:       
                    u_code=st.text_input("Enter your verification code & Press Enter:")
                    if u_code==edit_ver.v_code and len(u_code)!=0:
                        with st.spinner("Updating Email..."):
                            fn.update_email(data, edit_ver.mail, auth_state.idx)
                        st.success("email updated.")
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
        with st.spinner("Sending Verification Code to your email\
            ... Wait for input code box to appear."):
            ver.v_code=fn.verify_mail(ver.email)
            ver.mail_state1=True
        st.info("A verification code has been sent to your email. Check your inbox/spam\
            for the name of Zeng.gooseof shifu.")


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
            formn=st.form(key="edit_formnew")
            name=formn.text_input(label='Enter your full name: ')
            gender=formn.radio('Gender: ', ("Male", "Female"))
            relation=formn.text_input(label='Enter your relationship:')
            level=formn.text_input(label='Enter your relationship level(Eg.school friend/college friend etc.): ')
            insti=formn.text_input(label='Enter School/College')
            year=formn.text_input(label='Enter year you two met')
            place=formn.text_input(label='Enter your place of living')
            passk=formn.text_input(label='Enter new passkey for login(Remember this for later use)')
            new_friend = formn.form_submit_button(label='Create new friend')

            if new_friend:
                new_list=[name.lower(),ver.email, gender, relation, level, insti, year, place, dt.datetime.now(), passk]
                try:
                    with st.spinner("Adding details... New Friend."):
                        fn.push_new(data, new_list)
                    st.success("Successfully added as new friend.")
                    st.text("Click friend list for your name")
                    ver.mail_state2=False
                except:
                    st.error("Failed to create a new friend.")
    except:
        pass

st.markdown("***") # for line divider
st.text('\n\n')
st.subheader("Feature of leaving notes for your friends coming soon...")

st.text('\n\n')
col1, col2= st.beta_columns((1,1.4))
col1.write("Visit my website for more projects: [Click here](https://sites.google.com/view/tuhinsubhrade/home)")
#col1.write("[Click here](https://sites.google.com/view/tuhinsubhrade/home)")
col2.write("For Feedback/errors Fill out this Google Form: [Feedback/Error](https://forms.gle/NyguGsx9NFieJdyy6)")
st.write("*In view point of a developer, Visit working Github repo for this app: [Github Repo](https://github.com/Gituhin/Friends-Data)*")
st.markdown("***") # for line divider
st.text('\n\n')
st.text("© Tuhin Subhra De 2021")
#end#