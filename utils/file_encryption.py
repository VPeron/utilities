from datetime import datetime
import pathlib

import streamlit as st
from cryptography.fernet import Fernet


def validate_file(filename):
    supported_extentions = [".csv", ".txt", ".pdf"]
    file_extension = pathlib.Path(filename).suffix
    if file_extension in supported_extentions:
        return True
    return False

def generate_new_key():
    # GENERATE AND SAVE KEY
    st.info(f"Your keyfile will be named: {st.session_state['username']}.key")
    st.download_button('Download key file', Fernet.generate_key(), file_name=f"{st.session_state['username']}.key")

def decript_file_content(contents, ext):
    """Takes in the encrypted content of file and the file extension. Requires a key in the form of a binary file
    to decrypt the contents.
    Offers a download of the decrypted contents in the form of a file with the original extension.
    """
    uploaded_key = st.file_uploader("Upload keyfile", key="key_file_decrypt")
    if uploaded_key is not None:
        user_key = uploaded_key.getvalue()  # get file bytes data
        # DENCRYPT FILE CONTENT
        contents_decrypted = Fernet(user_key).decrypt(contents)
        st.write(contents_decrypted)
        file_date = datetime.date(datetime.today())
        st.download_button('Download decrypted file', contents_decrypted, file_name=f"deccfile_{file_date}{ext}")

def encrypt_main():
    st.sidebar.image("https://blogs.lse.ac.uk/lti/files/2014/12/binary-155685_1280.png")
    ### HEADERS
    head_col_1, head_col_2, head_col_3 = st.columns(3)
    with head_col_1:
        st.write("")
    with head_col_2:
        st.header("🔒 Cryptography 🔑")
    with head_col_3:
        st.write("")

    ### BODY
    body_col1, body_col2 = st.columns(2)
    with body_col1:
        ### col 1
        st.title('ENCRYPT FILE')
        get_new_key = st.checkbox('I need a new keyfile')
        if get_new_key:
            st.warning("Keep your key safe, you will need it to encrypt and decrypt files. Warning: I am unable to decrypt files encrypted with lost keys.")
            generate_new_key()

        placeholder = st.empty()
        uploaded_file = placeholder.file_uploader("Upload file to lock", key="main_file")
        if uploaded_file is not None and validate_file(uploaded_file.name):
            # only simple file formats for now
            input_file_name = uploaded_file.name
            input_file_type = uploaded_file.type
            input_file_size = uploaded_file.size
            st.info(f"""Type: {input_file_type} | Size: {input_file_size} -> Upload your key above""")
            bytes_data = uploaded_file.getvalue()  # get file bytes data
            # get user key
            uploaded_key = placeholder.file_uploader("Upload keyfile. You will need one to lock and unlock your files", key="key_file_enc")
            if uploaded_key is not None:
                # ENCRYPT CONTENT
                #TODO guard mismatch key
                contents_encrypted = Fernet(uploaded_key.getvalue()).encrypt(bytes_data)
                st.write(contents_encrypted)
                
                # DOWNLOAD
                # to keep this very simple we preserve the original file name and extension.
                # decrypting the file should also reformat it properly with the correct extention in place.
                st.download_button('Download encrypted file', contents_encrypted, file_name=f"enc_{input_file_name}_file_date")
    
    with body_col2:
        # col 2
        st.title('DECRYPT FILE')
        st.write("Get your keyfile ready.")
        uploaded_file = st.file_uploader("Upload file to unlock", key="dec_file")
        if uploaded_file is not None and validate_file(uploaded_file.name):
            bytes_data = uploaded_file.getvalue()  # get file bytes data
            file_extension = pathlib.Path(uploaded_file.name).suffix
            decript_file_content(bytes_data, file_extension)
    st.info("""
In order to use this application, a downloadable key is writen to a file. 
Keep it safe, you will need it to decrypt any files you encrypt with it.
To keep this simple, we will only be working with simple .csv and .txt files for now.\n
---
The routine:\n
Download a keyfile, if you haven't done so yet, to be able to encrypt and decrypt files. 
Upload a file to have its contents encrypted. 
Download a new file with the encrypted contents from the original file.
Decrypt the encrypted file using the same key it has been encrypted with.
             """)
