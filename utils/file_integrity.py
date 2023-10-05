import streamlit as st
import hashlib


def hash_calculator():
    # Streamlit app title and description
    st.title("File Hasher")
    st.write("The hash produced by a file can be an indicator of integrity. It can be used to easily compare two files, after a download for example. Ensuring the file has not been tampered with in-transit.")

    # File upload
    uploaded_file = st.file_uploader("Choose a file...", type=["txt", "pdf", "png", "jpg", "jpeg", "gif"])

    if uploaded_file is not None:
        # Read the file
        file_contents = uploaded_file.read()

        # Hashing algorithms
        hash_algorithms = ["MD5", "sha1", "sha256", "sha512"]

        # # Dropdown for selecting the hashing algorithm
        # selected_algorithm = st.selectbox("Select a Hashing Algorithm:", hash_algorithms)

        # # Calculate and display the hash value
        # if st.button("Calculate Hash"):
        for algo in hash_algorithms:
            hasher = hashlib.new(algo)
            hasher.update(file_contents)
            hash_value = hasher.hexdigest()
            st.write(f"Hash ({algo}): {hash_value}")
