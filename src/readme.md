# Rogue Wi-Fi Access Point Detection and Network Packet Analyzer for Intrusion Detection

This project aims to strengthen network security by combining rogue Wi-Fi access point detection and real-time network traffic analysis. The system is divided into three primary modules: a Streamlit-based visualization dashboard, a malware analysis model, and an ESP32-based intrusion detection system. 

## Project Structure

### 1. Dashboard (Streamlit)
   - **Overview**: 
     The dashboard serves as the central interface, providing real-time visualizations of network traffic, rogue AP detections, and system statistics. It allows administrators to review alerts, monitor security events, and visualize traffic patterns for enhanced situational awareness.
   - **Technologies Used**:
     - **Streamlit** for web-based data visualization.
     - **Matplotlib** and **Plotly** for interactive charts and graphs.
   - **Features**:
     - Real-time detection and flagging of rogue access points.
     - Visualizations of network traffic patterns and protocol distribution.
     - Dashboard alert notifications for detected threats and anomalies.
   - **Implementation Screenshots**:
       ![frontend](https://github.com/user-attachments/assets/65cf1f56-990e-477f-9f4c-7a6b9004ea07)
       ![front_end](https://github.com/user-attachments/assets/495a01ec-db8a-490f-a4c4-ec4f4ad7f9fa)


### 2. Malware Analysis Model
   - **Overview**: 
     This module includes a trained model that analyzes captured packets and flags malicious packets based on behavioral patterns. The model helps detect unusual packet activity, unauthorized data transfers, and protocol anomalies.
   - **Technologies Used**:
     - **Python** for packet capture and preprocessing.
     - **Scikit-Learn** or **TensorFlow** for machine learning model implementation.
     - **PyShark** or **Scapy** for packet capture and filtering.
   - **Features**:
     - Packet capture with protocol filtering.
     - Machine learning-based anomaly detection.
     - Detailed packet inspection for malware signatures.
   - **Implementation Screenshots**:
       ![malware_img](https://github.com/user-attachments/assets/f3c6e5f7-71d2-481f-87dd-72942a8a259a)


### 3. ESP32 Intrusion Detection System (Arduino)
   - **Overview**:
     This component involves the ESP32 microcontroller, programmed via the Arduino IDE, to scan for Wi-Fi networks and detect rogue access points. It sends alert notifications if unauthorized access points or suspicious activity is identified.
   - **Technologies Used**:
     - **ESP32 Microcontroller** for network scanning.
     - **Arduino IDE** for programming the ESP32.
     - **WiFi** library for access point scanning and monitoring.
   - **Features**:
     - Scans and identifies unauthorized Wi-Fi access points.
     - Flags access points with duplicated SSIDs or suspicious MAC addresses.
     - Sends alerts to the central dashboard for prompt response.
   - **Implementation Screenshots**:
       ![Screenshot 2024-11-09 014219](https://github.com/user-attachments/assets/c49ed4c2-d578-4a69-8715-8dc8121491c0)
