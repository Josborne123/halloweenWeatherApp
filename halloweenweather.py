# Importing all modules required
from datetime import date
import tkinter as tk
import customtkinter
import requests
from PIL import ImageTk, Image
import csv
import random
import pygame

# Defining sounds arrays
buttonSounds = ["audio/button/breezeofblood.mp3", "audio/button/goreblood.mp3", "audio/button/riptear.mp3", "audio/button/veryloudsplat.mp3"]
screamingSounds = ["audio\screamingsounds\demonic-woman-scream-6333.mp3", "audio\screamingsounds\evil-shreik-45560.mp3", "audio\screamingsounds\girl_scream_shortwav-14510.mp3", "audio\screamingsounds\man-scream-memes-121085.mp3", "audio\screamingsounds\panic-stricken-screaming-1-6880.mp3", "audio\screamingsounds\witch-laugh-95203.mp3", "audio\screamingsounds\witchlaughter-1-100652.mp3"]
failureSounds = []
introSounds = ["audio/intro/dramaticintro.mp3", "audio/intro/halloweenimpact01.mp3", "audio/intro/halloweenimpact02.mp3", "audio/intro/halloweenimpact03.mp3", "audio/intro/halloweenimpact04.mp3", "audio/intro/halloweenimpact05.mp3", "audio/intro/bellofdeath.mp3"]

def resize_image(event):
    # Resises the image when required
    new_width = event.width
    new_height = event.height
    image = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    label.config(image = photo)
    label.image = photo

def format_response(address, weather):
    # Function which formats the weather information 
    try:
        name = weather['address']
        resolvedAddress = weather['resolvedAddress'] 
        date = weather['days'][0]['datetime'] # Format YYYY-MM-DD
        conditions = weather['days'][0]['conditions']
        maxtemp = weather['days'][0]['tempmax'] # In °C
        mintemp = weather['days'][0]['tempmin'] # In °C
        humidity = weather['days'][0]['humidity'] # In %
        windspeed = weather['days'][0]['windspeed'] # In mph
        icon = weather['days'][0]['icon']

        # Converting the first letter of the location name to a capital letter
        firstChar = ord(name[0:1])
        if firstChar > 97 and firstChar < 122:
            firstChar -= 32
            name = chr(firstChar) + name[1:]

        dateDay = date[8:]
        dateMonth = date[4:8]
        dateYear = date[0:4]
        # Converting the date format to DD-MM-YYYY
        date = dateDay + dateMonth + dateYear

        if address == True:
            final_str = f'Location: {name}\nDate: {date} \nConditions: {conditions}\nMaximum Temperature: {maxtemp}°C \nMinimum Temperature: {mintemp}°C \nHumidity: {humidity}% \nWind speed: {windspeed} mph'
        elif address == False:
            final_str = f'Location: {resolvedAddress}\nDate: {date} \nConditions: {conditions}\nMaximum Temperature: {maxtemp}°C \nMinimum Temperature: {mintemp}°C \nHumidity: {humidity}% \nWind speed: {windspeed} mph'

        # Setting the label to the final_str
        label_below.configure(text=final_str)
    except:
        final_str = f'There was a problem retrieving that information'
        label_below.configure(text=final_str)
        pygame.mixer.music.load(random.choice(failureSounds))
        pygame.mixer.music.play(loops=0)

def get_weather(surprise, city, date):
    print(city)
    # Procedure which connects to the API (visual crossing) and stores the response in 'weather'
    date = str(date)

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
            language = "en"
            
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
                apiQuery += "&iconSet=" + iconSet
            if (len(language)):
                apiQuery += "&lang=" + language

            apiQuery += "&key=" + weather_key

            response = requests.get(apiQuery)
            weather = response.json()
            if surprise == False:
                address = False
                label_below['text'] = format_response(address, weather)
            elif surprise == True:
                address = True
                label_below['text'] = format_response(address, weather)

            pygame.mixer.music.load(random.choice(screamingSounds)) # Loading sounds
            pygame.mixer.music.play(loops=0) # Playing sound

        except:
            label_below.configure(text="Sorry, what you have entered doesn't work!\nPlease try entering your values again.")
            pygame.mixer.music.load(random.choice(failureSounds))
            pygame.mixer.music.play(loops=0)

def supriseMeProcessing():
    pygame.mixer.music.load("audio/button/goreblood.mp3") # Load music
    pygame.mixer.music.play(loops=0) # Play music
    # Function which reads in all the countries form the 'countries of the world.csv' file and then picks and stores a random country and date
    countriesList = []
    countriesFile = open("countries of the world.csv", "r")
    rows = csv.reader(countriesFile)
    for row in rows:
        country = row[0]
        countriesList.append(country)

    randomCountry = random.choice(countriesList)
    randomDate = random.randint(1973, 2021)
    surprise = True
    get_weather(surprise, randomCountry, randomDate)

def setup():
    # Function which sets up all of the entry boxes, buttons, frames, etc

    surprise = False

    info_label = customtkinter.CTkLabel(window, text="Find the weather for any location, from 1973 onwards", text_font=("Comic Sans MS bold", 14), text_color="white", bg_color="#f2993f")
    info_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    location_entry = customtkinter.CTkEntry(window, placeholder_text="Location", placeholder_text_color="orange", text_font=("Comic Sans MS italic", 15), corner_radius=15, bg_color="#f2993f")
    location_entry.place(relx=0.20, rely=0.16, relwidth=0.18, relheight=0.1)
    location_entry.bind("<Return>", (lambda event: get_weather(surprise, location_entry.get(), date_entry.get())))

    date_entry = customtkinter.CTkEntry(window,  placeholder_text="Year", placeholder_text_color="orange", text_font=("Comic Sans MS italic", 15), corner_radius=15, bg_color="#f2993f")
    date_entry.place(relx=0.40, rely=0.16, relwidth=0.18, relheight=0.1)
    date_entry.bind("<Return>", (lambda event: get_weather(surprise, location_entry.get(), date_entry.get())))


    enter_button = customtkinter.CTkButton(window, text="Enter", command=lambda: get_weather(surprise, location_entry.get(), date_entry.get()), text_font=("Comic Sans MS bold", 15), corner_radius=15, bg_color="#f2993f", fg_color="#6c43cd")
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

    return label_below, second_frame, surprise, location_entry, date_entry


# Main Program

pygame.mixer.init()

# ADD an audio file if i wan't something to play on startup
pygame.mixer.music.load(random.choice(introSounds))
pygame.mixer.music.play(loops=0)

# Setting up the customtkinter window
window = customtkinter.CTk()
window.geometry('750x500')
window.title("Halloween Weather")
window.resizable(width=False, height=False)
customtkinter.set_default_color_theme("dark-blue")

## Image created by anjarshevtian on Vecteezy
# Sets up the image
image = Image.open('img\halloween.jpg')
copy_of_image = image.copy()
photo = ImageTk.PhotoImage(image)
label = tk.Label(window, image = photo)
label.bind('<Configure>', resize_image)
label.pack(fill=tk.BOTH, expand = True)

################print(tk_font.families())

# Calls the setup function
label_below, second_frame, surprise, location_entry, date_entry = setup()



# Starts the program
window.mainloop()