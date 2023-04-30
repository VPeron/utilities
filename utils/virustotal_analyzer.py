import requests
from io import StringIO

import streamlit as st
import pandas as pd
import vt

from utils.custom_logger import get_custom_logger


logger = get_custom_logger('api_call')
VT_API_KEY = st.secrets['vt_api_key']
VT_API_URL = "https://www.virustotal.com/vtapi/v2/file/scan"

st.cache(ttl=300)
def get_ip_scan_response(ip):
    logger.info('get_ip_scan')
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {"accept": "application/json", "x-apikey": VT_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json(), response.status_code
    else:
        return 'No results', response.status_code

def check_ip_addr():
    st.header('Scan IP Address')
    ip = st.text_input('Enter an IP Addr: ')
    if st.button('Start Scan'):
        # make api call
        response = get_ip_scan_response(ip)
        
        if response[1] == 200:
            result = dict(response[0])['data']['attributes']['last_analysis_stats']
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
    

def scan_file(client):
    logger.info('scan_file')
    st.header('Scan File')
    uploaded_file = st.file_uploader("Upload file", key="main_file")
    if uploaded_file is not None:
        st.info(f"file size: {uploaded_file.size} - file type: {uploaded_file.type}")
        file_obj = StringIO(uploaded_file.getvalue().decode("utf-8"))
        with st.spinner('Scanning File, this may take a while'):
            analysis = client.scan_file(file_obj, wait_for_completion=True)
        return analysis
    

def scan_url(client):
    logger.info('scan_url')
    st.header('Scan URL')
    target_url = st.text_input("Enter URL", key="main_url")
    if st.button('Scan URL', key='url scan confirm'):
        with st.spinner('Scanning URL, this may take a while'):
            analysis = client.scan_url(target_url, wait_for_completion=True)
            return analysis


def display_result(stats, result):
    st.write(pd.DataFrame(stats, index=['# of vendors']))
    if st.checkbox('full report'):
        st.write(result)


def vt_main():
    # page title
    st.title("VirusTotal Analyzer")
    st.info("""
The target ip, url or file will be scanned by around 70 AV vendors simultaneously.\n
This means the scan may take a while. Get a coffee.\n
You can hide the long version of the scans by clicking on the first blue arrow atop.
            """)
    
    with vt.Client(VT_API_KEY) as client:
        # scan file
        file_scan_report = scan_file(client)
        if file_scan_report:
            stats = file_scan_report.to_dict()['attributes']['stats']
            result = file_scan_report.to_dict()['attributes']['results']
            display_result(stats, result)
        
        st.divider()
        
        # scan url
        url_scan_report = scan_url(client)
        if url_scan_report:
            stats = url_scan_report.to_dict()['attributes']['stats']
            result = url_scan_report.to_dict()['attributes']['results']
            display_result(stats, result)
    st.divider()
    
    # scan ip addr
    check_ip_addr()
