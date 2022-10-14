# Importing all modules required
import tkinter as tk
from tkinter import font
import requests
from PIL import ImageTk, Image
import customtkinter
from dataclasses import dataclass
from tkinter.font import Font
import tkinter.font as tk_font
from emoji import emojize
import csv
import random


# Setting up the customtkinter window
window = customtkinter.CTk()
window.geometry('750x500')
window.title("Halloween Weather")
window.resizable(width=False, height=False)
customtkinter.set_default_color_theme("dark-blue")

################print(tk_font.families())



def resize_image(event):
    # Resises the image when required
    new_width = event.width
    new_height = event.height
    image = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    label.config(image = photo)
    label.image = photo

## Image created by anjarshevtian on Vecteezy
# Sets up the image
image = Image.open('img\halloween.jpg')
copy_of_image = image.copy()
photo = ImageTk.PhotoImage(image)
label = tk.Label(window, image = photo)
label.bind('<Configure>', resize_image)
label.pack(fill=tk.BOTH, expand = True)



def format_response(weather):
    # Function which formats the weather information 
    try:
        name = weather['resolvedAddress'] 
        date = weather['days'][0]['datetime'] # Format YYYY-MM-DD
        conditions = weather['days'][0]['conditions']
        maxtemp = weather['days'][0]['tempmax'] # In °C
        mintemp = weather['days'][0]['tempmin'] # In °C
        humidity = weather['days'][0]['humidity'] # In %
        windspeed = weather['days'][0]['windspeed'] # In mph

        icon = weather['days'][0]['icon']

        final_str = f'Location: {name}\nDate: {date} \nConditions: {conditions}\nMaximum Temperature: {maxtemp}°C \nMinimum Temperature: {mintemp}°C \nHumidity: {humidity}% \nWind speed: {windspeed} mph'
        label_below.configure(text=final_str)
    except:
        final_str = f'There was a problem retrieving that information'
        label_below.configure(text=final_str)


    return final_str

def get_weather(city, date):
    date = str(date)
    # Procedure which connects to the API (visual crossing) and stores the response in 'weather'
    if city != "":
        try:
            weather_key = 'KZWGYHQU6JZUJ6VTKLAUDH68W'
            url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'
            UnitGroup = 'uk'
            Location = city
            StartDate = date + "-10-31"
            ContentType = 'json'
            Include = "days"
            iconSet = "icons2"

            apiQuery = url + Location
            if (len(StartDate)):
                apiQuery+="/"+StartDate

            apiQuery+="?"

            if (len(UnitGroup)):
                apiQuery +="&unitGroup=" + UnitGroup
            if (len(ContentType)):
                apiQuery += "&contentType=" + ContentType 
            if (len(Include)):
                apiQuery += "&include=" + Include
            if (len(iconSet)):
                apiQuery += "&iconSet" + iconSet


            apiQuery += "&key=" + weather_key

            response = requests.get(apiQuery)
            weather = response.json()

            ##########print(weather)

            label_below['text'] = format_response(weather)
        except:
            label_below.configure(text="Sorry, what you have entered doesn't work!\nPlease try entering your values again.")


def supriseMeProcessing():
    countriesList = []
    countriesFile = open("countries of the world.csv", "r")
    rows = csv.reader(countriesFile)
    for row in rows:
        country = row[0]
        countriesList.append(country)

    randomCountry = random.choice(countriesList)
    randomDate = random.randint(1973, 2021)
    get_weather(randomCountry, randomDate)


def setup():
    # Function which sets up all of the entry boxes, buttons, frames, etc

    info_label = customtkinter.CTkLabel(window, text="Find the weather for any location, from 1973 onwards", text_font=("Comic Sans MS bold", 14), text_color="white", bg_color="#f2993f")
    info_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    city_entry = customtkinter.CTkEntry(window, placeholder_text="Location", placeholder_text_color="orange", text_font=("Comic Sans MS italic", 15), corner_radius=15, bg_color="#f2993f")
    city_entry.place(relx=0.20, rely=0.16, relwidth=0.18, relheight=0.1)

    date_entry = customtkinter.CTkEntry(window,  placeholder_text="Year", placeholder_text_color="orange", text_font=("Comic Sans MS italic", 15), corner_radius=15, bg_color="#f2993f")
    date_entry.place(relx=0.40, rely=0.16, relwidth=0.18, relheight=0.1)

    enter_button = customtkinter.CTkButton(window, text="Enter", command=lambda: get_weather(city_entry.get(), date_entry.get()), text_font=("Comic Sans MS bold", 15), corner_radius=15, bg_color="#f2993f", fg_color="#6c43cd")
    enter_button.place(relx=0.60, rely=0.16, relwidth=0.18, relheight=0.1)

    second_frame = customtkinter.CTkFrame(window, bg_color="#eb6835", bd=4)
    second_frame.place(relx=0.125, rely=0.35, relwidth=0.75, relheight=0.6)

    label_below = customtkinter.CTkLabel(second_frame, anchor="center", borderwidth=4, text="", text_font=("Comic Sans MS bold", 16))
    label_below.place(relwidth=1, relheight=1)

    supriseme_button = customtkinter.CTkButton(window, command=lambda: supriseMeProcessing(), corner_radius=15, bg_color="#f2993f", fg_color="#6c43cd", text="Suprise Me!", text_font=("Comic Sans MS bold", 10))
    supriseme_button.place(relx=0.42, rely=0.08, relwidth=0.14, relheight=0.07)

    ghostlabel1 = customtkinter.CTkLabel(window, text="\U0001F47B", anchor="nw", text_font=("Comic Sans MS bold", 20), bg_color="#292929")
    ghostlabel1.place(relx=0.135, rely=0.37)
    ghostlabel2 = customtkinter.CTkLabel(window, text="\U0001F47B", anchor="ne", text_font=("Comic Sans MS bold", 20), bg_color="#292929")
    ghostlabel2.place(relx=0.68, rely=0.37)
    ghostlabel3 = customtkinter.CTkLabel(window, text="\U0001F47B", anchor="sw", text_font=("Comic Sans MS bold", 20), bg_color="#292929")
    ghostlabel3.place(relx=0.135, rely=0.855)
    ghostlabel4 = customtkinter.CTkLabel(window, text="\U0001F47B", anchor="se", text_font=("Comic Sans MS bold", 20), bg_color="#292929")
    ghostlabel4.place(relx=0.68, rely=0.855)

    return label_below


# Calls the setup function
label_below = setup()
# Runs the program
window.mainloop()