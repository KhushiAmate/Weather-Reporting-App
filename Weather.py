import requests
import json
import tkinter as tk
from PIL import ImageTk, Image
import io
from datetime import datetime

api_key = "5b03bea293adb401388678566d36eefd"

def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    response = requests.get(complete_url)
    return json.loads(response.content) if response.status_code == 200 else None

def get_weather_icon(icon_id):
    icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
    response = requests.get(icon_url)
    if response.status_code == 200:
        image = Image.open(io.BytesIO(response.content))
        return ImageTk.PhotoImage(image)
    return None

def update_weather(city_entry, weather_label, weather_image_label):
    city = city_entry.get()
    weather_data = get_weather(city)
    if weather_data:
        city_name = weather_data["name"]
        temperature = weather_data["main"]["temp"] - 273.15
        description = weather_data["weather"][0]["description"]
        weather_icon_id = weather_data["weather"][0]["icon"]
        weather_icon = get_weather_icon(weather_icon_id)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if weather_icon:
            weather_image_label.config(image=weather_icon)
            weather_image_label.image = weather_icon

        weather_label.config(text=f"Weather in {city_name}:\nDate & Time: {current_time}\nTemperature: {temperature:.2f} °C\nDescription: {description}")
    else:
        weather_image_label.config(image="")
        weather_label.config(text="Error: Could not retrieve weather data.")

def main():
    window = tk.Tk()
    window.title("Weather App")
    window.configure(bg="#87CEEB", padx=20, pady=20)

    tk.Label(window, text="Enter City:", font=("Arial", 14), bg="#87CEEB").pack(pady=5)
    city_entry = tk.Entry(window, font=("Arial", 14), width=30)
    city_entry.pack(pady=5)

    tk.Button(window, text="Get Weather", font=("Arial", 12), bg="#4682B4", fg="white",
              command=lambda: update_weather(city_entry, weather_label, weather_image_label)).pack(pady=10)

    weather_image_label = tk.Label(window, bg="#87CEEB")
    weather_image_label.pack(pady=5)

    weather_label = tk.Label(window, text="", font=("Arial", 14), bg="#87CEEB")
    weather_label.pack(pady=5)

    window.mainloop()

if __name__ == "__main__":
    main()
