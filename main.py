import streamlit as st
import funcs as fn
import SessionState as ss
import datetime as dt

def fetch_dt(idx, data):
    gender=data.Gender[idx]
    if gender=='Male':
        st.write("Hello! Sir "+fn.good_name(data.Name[idx]))
    else:
        st.write("Hello! Madame "+fn.good_name(data.Name[idx]))
    st.write("Gender:", data.Gender[idx])
    st.write("Relationship:", data.Relationship[idx])
    st.write("Level:", data.Level[idx])
    st.write("School/College:", data['School/College'][idx])
    st.write("From Year:", data['From Year'][idx])
    st.write('You are Living in:', data['Living in'][idx])


st.title("Friends Database")
st.header("Hola amigos!!")
st.write("You have landed here to have a glance of your friendship/relationship, with Tuhin. The purpose of this Web app is to keep a track of your friendship with Tuhin in a formal way.")
st.text("Kindly type your name & press enter to get details")

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
            st.error("No such person found")
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
    st.dataframe(fn.display_friendlist(data))
        

st.markdown("***") # for line divider
st.text('\n\n')
log=st.empty()
auth_state=ss.get(login=False, idx=-7)
log.write("Login: "+str(auth_state.login))

with st.beta_expander("click here to login"):
    form=st.form(key='my_form')
    en_name=form.text_input(label='Enter Your current Full Name:')
    en_passkey=form.text_input("Enter your passkey", type='password')
    submit_button = form.form_submit_button(label='Verify')

    if submit_button:
        (auth_state.login, auth_state.idx)=fn.authethicate(en_name, en_passkey, data)
        if auth_state.login:
            log.empty()
            log.write("Login: "+str(auth_state.login))
            st.success("Verified as: "+fn.good_name(en_name))
        else:
            st.error("The Name and Passkey doesn't match!")

with st.beta_container():            
    if auth_state.login:
        st.success("Identity Verified.")
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
                fn.make_edits(data, val_list, auth_state.idx)
                st.success("Details updated.")
            except:
                st.error("Database engaged, Please try after sometime")

        if st.button("Click twice to logout"):
            auth_state.login=False
            auth_state.idx=-7
            st.info("Click once more")
    else:
        st.write("Not logged in")

#sidebar
with st.sidebar:
    st.subheader("Click here to add a new Friend")
    clicked = st.button(" + ")
    if clicked:
        st.write("Feature yet to be added, coming soon..")

st.markdown("***") # for line divider
st.text('\n\n')
st.subheader("Feature of adding Personal Description paragraph coming soon with Natural Language Sentiment Capture...")

st.text('\n\n')
col1, col2= st.beta_columns((1,1.4))
col1.write("Visit my website for more projects: [Click here](https://sites.google.com/view/tuhinsubhrade/home)")
#col1.write("[Click here](https://sites.google.com/view/tuhinsubhrade/home)")
col2.write("For Feedback/errors Fill out this Google Form: [Feedback/Error](https://forms.gle/NyguGsx9NFieJdyy6)")
st.text("© Tuhin Subhra De 2021")
#end#