import subprocess
import platform
import re
import pandas as pd
import streamlit as st
import random
import os
from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Function to generate a temporary MAC address
def generate_temp_mac():
    return "00:14:22:{:02x}:{:02x}:{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Function to detect rogue APs and send alert
def detect_rogue_aps(wifi_list):
    known_networks = {"trusted_ssid_1", "trusted_ssid_2"}  # Example trusted SSIDs
    rogue_aps = []

    for network in wifi_list:
        if network['SSID'] not in known_networks:
            rogue_aps.append(network)

    if rogue_aps:
        send_alert(rogue_aps)
        
    return rogue_aps

# Function to send email alert
def send_email_alert(rogue_aps):
    sender_email = "your_email@example.com"
    sender_password = "your_email_password"
    receiver_email = "receiver_email@example.com"
    subject = "Rogue AP Detected!"
    body = f"The following rogue APs were detected:\n\n{pd.DataFrame(rogue_aps)}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:  # Replace with your SMTP server
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            st.success("Email alert sent successfully!")
    except Exception as e:
        st.error(f"Failed to send email alert: {e}")

# Function to send SMS alert using Twilio
def send_sms_alert(rogue_aps):
    account_sid = 'your_account_sid'  # Replace with your Twilio account SID
    auth_token = 'your_auth_token'    # Replace with your Twilio Auth Token
    from_phone = 'your_twilio_phone_number'
    to_phone = 'receiver_phone_number'

    client = Client(account_sid, auth_token)

    message_body = f"Rogue APs detected:\n\n{pd.DataFrame(rogue_aps)}"

    try:
        message = client.messages.create(
            body=message_body,
            from_=from_phone,
            to=to_phone
        )
        st.success("SMS alert sent successfully!")
    except Exception as e:
        st.error(f"Failed to send SMS alert: {e}")

# Unified function to send both email and SMS alerts
def send_alert(rogue_aps):
    send_email_alert(rogue_aps)
    send_sms_alert(rogue_aps)

# Function to get Wi-Fi networks and return as a DataFrame
def get_nearby_wifi():
    wifi_list = []  # List to store Wi-Fi data
    os_name = platform.system()

    if os_name == "Windows":
        command = "netsh wlan show networks mode=bssid"
        try:
            networks = subprocess.check_output(command, shell=True, encoding="utf-8")
            if not networks.strip():
                st.error("No networks found. Ensure Wi-Fi is enabled.")
                return pd.DataFrame(columns=["SSID", "MAC Address", "RSSI", "Channel", "Security"])

            # Regex patterns for parsing command output
            ssid_regex = re.compile(r"SSID \d+ : (.+)")
            mac_regex = re.compile(r"BSSID \d+ : (.+)")
            rssi_regex = re.compile(r"Signal\s*:\s*(\d+)%")
            channel_regex = re.compile(r"Channel\s*:\s*(\d+)")
            security_regex = re.compile(r"Authentication\s*:\s*(.+)")

            ssids = ssid_regex.findall(networks)
            macs = mac_regex.findall(networks)
            signals = rssi_regex.findall(networks)
            channels = channel_regex.findall(networks)
            securities = security_regex.findall(networks)

            # Populate Wi-Fi data
            num_networks = len(ssids)
            for i in range(num_networks):
                mac = macs[i] if i < len(macs) else generate_temp_mac()
                signal = int(signals[i]) - 100 if i < len(signals) else "N/A"  # Approx dBm conversion
                channel = int(channels[i]) if i < len(channels) else "N/A"
                security = securities[i] if i < len(securities) else "Unknown"
                
                wifi_list.append({
                    "SSID": ssids[i],
                    "MAC Address": mac,
                    "RSSI": signal,
                    "Channel": channel,
                    "Security": security
                })

            return pd.DataFrame(wifi_list)

        except subprocess.CalledProcessError as e:
            st.error(f"An error occurred while scanning Wi-Fi networks: {e}")
            return pd.DataFrame(columns=["SSID", "MAC Address", "RSSI", "Channel", "Security"])

# Streamlit app with sidebar
st.sidebar.header("Wi-Fi Scanner Options")

# Sidebar buttons
scan_button = st.sidebar.button("Scan for Wi-Fi Networks")
show_rogue_aps = st.sidebar.checkbox("Show Only Rogue APs", value=False)
track_rssi_button = st.sidebar.button("Track Live RSSI")

# Main app title
st.title("Wi-Fi Network Scanner")

if scan_button:
    st.info("Scanning for Wi-Fi networks...")
    wifi_df = get_nearby_wifi()

    if wifi_df.empty:
        st.error("No networks found. Please ensure your Wi-Fi is enabled and try again.")
    else:
        if show_rogue_aps:
            rogue_aps = detect_rogue_aps(wifi_df.to_dict(orient='records'))
            rogue_df = pd.DataFrame(rogue_aps)

            if rogue_df.empty:
                st.success("No rogue APs detected.")
            else:
                st.warning("Rogue APs detected!")
                st.dataframe(rogue_df)
        else:
            st.success("Networks found:")
            st.dataframe(wifi_df)

# Live RSSI tracking
if track_rssi_button:
    st.info("Tracking live RSSI data...")
    placeholder = st.empty()  # Placeholder for updating charts

    try:
        for _ in range(10):  # Simulate tracking with updates (adjust as needed)
            wifi_df = get_nearby_wifi()
            if not wifi_df.empty:
                rssi_chart = wifi_df[["SSID", "RSSI"]].sort_values(by="RSSI", ascending=False)
                placeholder.bar_chart(rssi_chart.set_index("SSID"))
            time.sleep(5)  # Refresh rate (in seconds)
    except Exception as e:
        st.error(f"An error occurred during live tracking: {e}")
