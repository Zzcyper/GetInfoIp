import customtkinter as ctk
import tkinter as tk
import requests

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

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

window = ctk.CTk()
window.title("IP Info Lookup")
window.geometry("400x300")

frame = ctk.CTkFrame(window)
frame.pack(pady=20, padx=20, fill="both", expand=True)

label = ctk.CTkLabel(frame, text="Enter an IP address:")
label.pack(pady=10)

entry = ctk.CTkEntry(frame, width=300)
entry.pack(pady=5)

lookup_button = ctk.CTkButton(frame, text="Lookup IP Info", command=get_ip_info)
lookup_button.pack(pady=10)

result_text = ctk.CTkLabel(frame, text="", wraplength=380, justify="left")
result_text.pack(pady=10)

window.mainloop()
