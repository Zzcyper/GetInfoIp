# Description of the IP Info Lookup Application
The provided Python code creates a graphical user interface (UI) application using the customtkinter (ctk) library. The application allows users to enter an IP address and fetches information related to that IP address from the ipinfo.io service.

1. Import Libraries
- import customtkinter as ctk
- import tkinter as tk
- import requests

2. Define the Function to Get IP Information

```
def get_ip_info():
    ip_address = entry.get()
    try:
        url = f"https://ipinfo.io/{ip_address}/json"
        response = requests.get(url)
        
        if response.status_code == 200:
            ip_data = response.json()
            result_text.configure(text=f"IP Information:\n\nIP Address: {ip_data['ip']}\nHostname: {ip_data['hostname']}\nCity: {ip_data['city']}\nRegion: {ip_data['region']}\nCountry: {ip_data['country']}\nLocation: {ip_data['loc']}\nOrganization: {ip_data['org']}")
        else:
            result_text.configure(text=f"Failed to retrieve data. Status code: {response.status_code}")
    except Exception as e:
        result_text.configure(text=str(e))
```
