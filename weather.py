import tkinter as tk
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

# Function to fetch weather data
def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name!")
        return
    
    # Replace with your actual API key
    api_key = "4aecc5a8770ee048a9c220cf5e4b2867"  
    base_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(base_url)
        data = response.json()
        
        if data.get("cod") != 200:
            error_message = data.get("message", "An error occurred").capitalize()
            messagebox.showerror("Error", error_message)
            return
        
        # Extracting weather details
        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"].capitalize()
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"] * 3.6  # Convert m/s to km/h

        # Displaying weather data
        result = (
            f"Weather in {city}:\n"
            f"Temperature: {temp}°C\n"
            f"Condition: {weather}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed:.2f} km/h"
        )
        result_label.config(text=result)
        
        # Send result via email
        send_email(city, result)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch weather data:\n{e}")

# Function to send email
def send_email(city, result):
    sender_email = "ashik09siraj@gmail.com"  # Replace with your email
    sender_password = "luje ovmj wtkc gcel"  # Replace with your email password
    recipient_email = recipient_entry.get()
    
    if not recipient_email:
        messagebox.showerror("Error", "Please enter a recipient email!")
        return

    try:
        # Set up email
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = f"Weather Report for {city}"
        message.attach(MIMEText(result, "plain"))
        
        # Send email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        
        messagebox.showinfo("Success", f"Weather report sent to {recipient_email}!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email:\n{e}")

# Setting up the GUI
root = tk.Tk()
root.title("Weather App")
root.geometry("400x500")
root.resizable(False, False)

# Set the background color to blue
root.config(bg="blue")

# Header
title_label = tk.Label(root, text="Weather App", font=("Helvetica", 18, "bold"), bg="blue", fg="white")
title_label.pack(pady=10)

# City entry
city_label = tk.Label(root, text="Enter city name:", font=("Helvetica", 12), bg="blue", fg="white")
city_label.pack(pady=5)
city_entry = tk.Entry(root, font=("Helvetica", 12), width=30)
city_entry.pack(pady=5)

# Recipient email entry
recipient_label = tk.Label(root, text="Enter recipient email:", font=("Helvetica", 12), bg="blue", fg="white")
recipient_label.pack(pady=5)
recipient_entry = tk.Entry(root, font=("Helvetica", 12), width=30)
recipient_entry.pack(pady=5)

# Search button
search_button = tk.Button(root, text="Get Weather and Send Email", font=("Helvetica", 12), command=get_weather)
search_button.pack(pady=10)

# Result display
result_label = tk.Label(root, text="", font=("Helvetica", 12), justify="left", bg="blue", fg="white")
result_label.pack(pady=20)

# Run the app
root.mainloop()
