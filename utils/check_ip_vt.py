import requests

import streamlit as st
import pandas as pd

from utils.custom_logger import get_custom_logger


logger = get_custom_logger('suspicious_connections')
VT_API_KEY = st.secrets['vt_api_key']
VT_API_URL = "https://www.virustotal.com/vtapi/v2/file/scan"

st.cache(ttl=300)
def get_ip_scan_response(ip):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {"accept": "application/json", "x-apikey": VT_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {'status code': response.status_code}

def check_ip_addr():
    st.header('Enter an Ip Address for Analysis')
    ip = st.text_input('Enter an IP Addr: ')
    if st.button('Start Scan'):
        # make api call
        response = get_ip_scan_response(ip)
        result = dict(response)['data']['attributes']['last_analysis_stats']
        if result:
            st.info('A number of companies have cross checked this IP address. See the result summary below or check the full report.')
            res_df = pd.DataFrame(result, index=[0])
            res_df.reset_index(inplace=True, drop=True)
            st.write(res_df[['harmless', 'malicious', 'suspicious', 'undetected', 'timeout']])
            
            if result['malicious'] > 3 or result['suspicious'] > 5:
                st.warning('### IP Alert ###', ip)
                st.write('malicious or suspicious IP Addr')
                logger.info(f"{ip} {result}") 
        else:
            st.write('No results for this IP address')
    

def analyze_file():
    st.header('Drop a file for Analysis')
    # Display an upload widget
    file = st.file_uploader("Upload a file")
    # Check if a file has been uploaded
    if file is not None:
        # Read the contents of the file
        content = file.read()
        # Send the file to VirusTotal for analysis
        params = {"apikey": VT_API_KEY}
        files = {"file": content}
        response = requests.post(VT_API_URL, params=params, files=files)
        # Display the result of the analysis
        st.subheader("Analysis result:")
        if st.button("View Full report"):
            st.write(response.json())
        link = response.json()['permalink']
        st.write(f"[Link to results]({link})")


def vt_main():
    # Display a title
    st.title("VirusTotal Analyzer")
    
    analyze_file()
    
    check_ip_addr()
