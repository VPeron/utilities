import streamlit as st


def profile():
    st.title('About')
    st.info('My Github account: https://github.com/VPeron')
    st.write('Here you can watch my presentation for the Lewagon Data Science Capstone project: Chess Engine Detection')

    st.video('https://www.youtube.com/watch?v=d_SOksxtVzs&t=2197s', start_time=2197)