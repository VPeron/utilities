import streamlit as st


def profile():
    st.title('About')
    st.info("""
Some of the music I listen to, you can sample above, if you haven't already.\n 
The tools assembled in this portfolio, although current, should be considered for education and entertainment only.\n
They have been created for my personal use and to showcase some of my programs.
""")
    st.write('[My Github account](https://github.com/VPeron)')
    st.write('[My Linkedin](https://www.linkedin.com/in/vinicius-p-9a9197270/)')
    st.write('Here you can watch my presentation for the Lewagon Data Science Bootcamp Capstone project: Chess Engine Detection')
    st.video('https://www.youtube.com/watch?v=d_SOksxtVzs&t=2197s', start_time=2197)
    st.markdown("[Here's my Ironhack CyberSecurity Course Deliverable](https://ironhackdeliverable-group5.streamlit.app/)")
    st.markdown("""
# Holopin Badges
[![@vperon's Holopin badges full Holopin profile](https://holopin.me/vperon)](https://holopin.io/@vperon)
                """)