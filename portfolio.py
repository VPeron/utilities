import streamlit as st
import streamlit_authenticator as stauth
from streamlit_player import st_player

from utils.custom_logger import get_custom_logger
from utils.file_encryption import encrypt_main
from utils.virustotal_analyzer import vt_main
from utils.about import profile


# Set Streamlit app UI config
st.set_page_config(page_title="V Peron", page_icon="🗝️", layout="wide")

# init logger
logger = get_custom_logger('login')

# hide pandas default table index in st
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

# insert footer app wide
hide_streamlit_style = """
    <style>
    
    footer {
        visibility:hidden;
    }
    footer:after {
        content: 'V Peron Utilities ®️';
        visibility: visible;
        display: block;
        position: relative;
        #background-color: red;
        padding: 5px;
        top: 2px;
    }
    </style>
"""
# Inject CSS with Markdown
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def front_door():
    # login widget via streamlit_authenticator 
    authenticator = stauth.Authenticate(
        dict(st.secrets["credentials"]),
        st.secrets["cookie"]["name"],
        st.secrets["cookie"]["key"],
        st.secrets["cookie"]["expiry_days"],
        st.secrets["preauthorized"],
    )
    
    placeholder = st.empty()
    placeholder.image('http://www.hummingbirds.net/images/vault.jpg', width=600)

    st.sidebar.header('Login Form')
    name, authentication_status, username = authenticator.login("Login", "sidebar")
    if authentication_status:
        authenticator.logout("Logout", "sidebar")
        st.sidebar.info(f"Welcome *{name}*")
        logger.info(f"{st.session_state['username']} logged in")
        placeholder.empty()
    elif authentication_status == False:
        st.sidebar.error("Username/password is incorrect")
        logger.info("Username/password is incorrect")
    elif authentication_status == None:
        st.sidebar.info("Please enter your username and password")


def main():
    st_player('https://soundcloud.com/vini-peron/sets/on-the-road')
    # run app
    if st.session_state['username']:
        page_choice = st.sidebar.radio('Pages', ('VirusTotal Analyzer', 'File Encryption', 'About'))
        if page_choice == 'VirusTotal Analyzer':
            vt_main()
        if page_choice == 'File Encryption':
            encrypt_main()
        if page_choice == 'About':
            profile()

if __name__ == "__main__":
    front_door()
    if st.session_state["authentication_status"]:
        
        main()
