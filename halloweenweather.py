# Importing all modules required
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
failureSounds = ["audio/failure/dundundun.mp3", "audio/failure/1.mp3", "audio/failure/2.mp3", "audio/failure/3.mp3", "audio/failure/4.mp3", "audio/failure/5.mp3", "audio/failure/6.mp3", "audio/failure/7.mp3"]
introSounds = ["audio/intro/dramaticintro.mp3", "audio/intro/halloweenimpact01.mp3", "audio/intro/halloweenimpact02.mp3", "audio/intro/halloweenimpact03.mp3", "audio/intro/halloweenimpact04.mp3", "audio/intro/halloweenimpact05.mp3", "audio/intro/bellofdeath.mp3"]

def resize_image(event):
    # Resises the image to fit the window
    new_width = event.width
    new_height = event.height
    image = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    label.config(image = photo)
    label.image = photo

def format_response(address, weather):
    # Procedure which formats and displays the weather information 
    try:
        name = weather['address']
        resolvedAddress = weather['resolvedAddress'] 
        date = weather['days'][0]['datetime'] # Format YYYY-MM-DD
        conditions = weather['days'][0]['conditions']
        maxtemp = weather['days'][0]['tempmax'] # In °C
        mintemp = weather['days'][0]['tempmin'] # In °C
        humidity = weather['days'][0]['humidity'] # In %
        windspeed = weather['days'][0]['windspeed'] # In mph

        # Ensuring that the text will fit on the screen.
        length = len(resolvedAddress)
        if length == 43 or length == 44:
            label_below.configure(font=("Comic Sans MS bold", 14))
        elif length ==45 or length == 46:
            label_below.configure(font=("Comic Sans MS bold", 13))
        elif length <= 43:
            label_below.configure(font=("Comic Sans MS bold", 16))
        elif length >= 47 and length <= 52:
            label_below.configure(font=("Comic Sans MS bold", 13))
        elif length >= 53:
            label_below.configure(font=("Comic Sans MS bold", 10))
        
        # Converting the first letter of the location name to a capital letter
        firstChar = ord(name[0:1])
        if firstChar > 97 and firstChar < 122:
            firstChar -= 32
            name = chr(firstChar) + name[1:]

        dateDay = date[8:]
        dateMonth = date[4:8]
        dateYear = date[0:4]
        # Converting the date format to DD-MM-YYYY
        dateFormatted = dateDay + dateMonth + dateYear

        # If these values return 0.0 or None then it will go to the except and display an error message to the user
        if maxtemp == 0.0 or maxtemp == None and mintemp == 0.0 or mintemp == None and humidity == None and windspeed == None:
            raise Exception 

        maxtemp = f'{maxtemp}°C'
        mintemp = f'{mintemp}°C'
        humidity = f'{humidity}%'
        windspeed = f'{windspeed} mph'

        # If there is no data available, changing the output to 'No data'
        if conditions == "":
            conditions = "No data"
        if maxtemp == '0.0°C' or maxtemp == 'None°C':
            maxtemp = "No data"
        if mintemp == '0.0°C' or mintemp == 'None°C':
            mintemp = "No data"
        if humidity == 'None%' or humidity == '0.0%':
            humidity = "No data"
        if windspeed == 'None mph' or windspeed == '0.0 mph':
            windspeed = "No data"

       
        if address == True:
            final_str = f'Location: {name}\nDate: {dateFormatted} \nConditions: {conditions}\nMaximum Temperature: {maxtemp} \nMinimum Temperature: {mintemp} \nHumidity: {humidity} \nWind speed: {windspeed}'
            
        elif address == False:
            final_str = f'Location: {resolvedAddress}\nDate: {dateFormatted} \nConditions: {conditions}\nMaximum Temperature: {maxtemp} \nMinimum Temperature: {mintemp} \nHumidity: {humidity} \nWind speed: {windspeed}' 

        # Setting the label to the final_str
        label_below.configure(text=final_str)
    except:
        # Displaying an error message to user and playing failure sounds
        final_str = 'Sorry, there was a problem retrieving that information'
        label_below.configure(font=("Comic Sans MS bold", 14))
        label_below.configure(text=final_str)
        pygame.mixer.music.load(random.choice(failureSounds))
        pygame.mixer.music.play(loops=0)

def get_weather(surprise, city, date):
    # Procedure which connects to the Visual Crossing Timeline API and stores the response in 'weather'

    try:
        dateInt = int(date) # Making sure the user enters an integer for the date
    except:
        label_below.configure(font=("Comic Sans MS bold", 16))
        label_below.configure(text="Sorry, what you have entered doesn't work!\nPlease try entering different values.")
        pygame.mixer.music.load(random.choice(failureSounds))
        pygame.mixer.music.play(loops=0)

    date = str(date)

    if city != "":
        try:
            if dateInt < 1973 or dateInt > 2021: # Validation on date
                raise Exception

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

            apiQuery += "&key=" + weather_key # Finished api query

            response = requests.get(apiQuery)
            weather = response.json() # Storing API response

            if surprise == False:
                address = False
                label_below['text'] = format_response(address, weather)
            elif surprise == True:
                address = True
                label_below['text'] = format_response(address, weather)

            # Ghosts will move in an anti-clockwise direction
            def anticlockwise():
                def one(y=0.37, x=0.135):
                    if y < 0.862:
                        ghostlabel1.place(relx=x, rely=y)
                        window.after(30, one, y+0.01)
                def two(x=0.815, y=0.36):
                    if x > 0.13:
                        ghostlabel2.configure(anchor="nw")
                        ghostlabel2.place(relx=x, rely=y)
                        window.after(22, two, x-0.01)

                def three(x=0.135, y=0.855):
                    if x <= 0.82:
                        ghostlabel3.configure(anchor="se")
                        ghostlabel3.place(relx=x, rely=y)
                        window.after(22, three, x+0.01)

                def four(y=0.855, x=0.815):
                    if y > 0.36:
                        ghostlabel4.configure(anchor="ne")
                        ghostlabel4.place(relx=x, rely=y)
                        window.after(30, four, y-0.01)
                        
                one()
                two()
                three()
                four()

            # Ghosts will move in a clockwise direction
            def clockwise():
                def one( x=0.135, y=0.36):
                    if x < 0.82:
                        ghostlabel1.place(relx=x, rely=y)
                        window.after(22, one, x+0.01)
                    
                def two(y=0.36, x=0.815):
                    if y < 0.865:
                        ghostlabel2.place(relx=x, rely=y)
                        window.after(30, two, y+0.01)

                def three(y=0.855, x=0.135):
                    if y > 0.36:
                        ghostlabel3.place(relx=x, rely=y)
                        window.after(30, three, y-0.01)


                def four(x=0.815, y=0.855):
                    if x > 0.13:
                        ghostlabel4.place(relx=x, rely=y)
                        window.after(22, four, x-0.01)
                        
                one()
                two()
                three()
                four()

            # Randomly picks whether the ghosts go in a clockwise or anticlockwise direction
            chooseDirection = [clockwise, anticlockwise]
            random.choice(chooseDirection)()

            pygame.mixer.music.load(random.choice(screamingSounds)) # Loading sounds
            pygame.mixer.music.play(loops=0) # Playing sound

        except:
            label_below.configure(font=("Comic Sans MS bold", 16))
            label_below.configure(text="Sorry, what you have entered doesn't work!\nPlease try entering different values.")
            pygame.mixer.music.load(random.choice(failureSounds))
            pygame.mixer.music.play(loops=0)
    
    elif city == "":
            label_below.configure(font=("Comic Sans MS bold", 16))
            label_below.configure(text="Sorry, what you have entered doesn't work!\nPlease try entering different values.")
            pygame.mixer.music.load(random.choice(failureSounds))
            pygame.mixer.music.play(loops=0)  

def supriseMeProcessing():
    # This procedure  reads in all the countries from the 'countries of the world.csv' file and then picks and stores a random country and date

    location_entry.delete(0, 'end') # Removing user entered text from location entry box
    date_entry.delete(0, 'end') # Removing user entered text from date entry box
    window.focus()
    pygame.mixer.music.load("audio/button/goreblood.mp3") # Load music
    pygame.mixer.music.play(loops=0) # Play music
    countriesList = []
    countriesFile = open("countries of the world.csv", "r")
    rows = csv.reader(countriesFile)
    for row in rows:
        country = row[0] 
        countriesList.append(country) # Storing the data in countriesList

    randomCountry = random.choice(countriesList) # Randomly choosing a country
    randomDate = random.randint(1973, 2021) # Choosing a random date
    surprise = True
    get_weather(surprise, randomCountry, randomDate)

def mute_switch():
    # If the switch is checked the sounds will be muted if it is unchecked the sound effects will be hearable
    text = audiobutton.text

    if text == "Audio on":
        pygame.mixer.music.set_volume(0)
        audiobutton.configure(text="Audio off")
    
    elif text == "Audio off":
        pygame.mixer.music.set_volume(1)
        audiobutton.configure(text="Audio on")

def setup():
    # Procedure which sets up all of the entry boxes, buttons, frames, etc

    surprise = False

    info_label = customtkinter.CTkLabel(window, text="Find the weather on Halloween for any location, from 1973 onwards", text_font=("Comic Sans MS bold", 13), text_color="white", bg_color="#f2993f")
    info_label.place(relx=0.495, rely=0.3, anchor=tk.CENTER)

    location_entry = customtkinter.CTkEntry(window, placeholder_text="Location", placeholder_text_color="orange", text_font=("Comic Sans MS italic", 15), corner_radius=15, bg_color="#f2993f")
    location_entry.place(relx=0.20, rely=0.16, relwidth=0.18, relheight=0.1)
    location_entry.bind("<Return>", (lambda event: get_weather(surprise, location_entry.get(), date_entry.get())))

    date_entry = customtkinter.CTkEntry(window,  placeholder_text="Year", placeholder_text_color="orange", text_font=("Comic Sans MS italic", 15), corner_radius=15, bg_color="#f2993f")
    date_entry.place(relx=0.40, rely=0.16, relwidth=0.18, relheight=0.1)
    date_entry.bind("<Return>", (lambda event: get_weather(surprise, location_entry.get(), date_entry.get())))


    enter_button = customtkinter.CTkButton(window, text="Enter", command=lambda: get_weather(surprise, location_entry.get(), date_entry.get()), text_font=("Comic Sans MS bold", 15), corner_radius=15, bg_color="#f2993f", fg_color="#6c43cd", hover_color="#a589e8", border_width=2)
    enter_button.place(relx=0.60, rely=0.16, relwidth=0.18, relheight=0.1)

    second_frame = customtkinter.CTkFrame(window, bg_color="#eb6835", bd=4)
    second_frame.place(relx=0.125, rely=0.35, relwidth=0.75, relheight=0.6)

    label_below = customtkinter.CTkLabel(second_frame, anchor="center", borderwidth=4, text="", text_font=("Comic Sans MS bold", 16))
    label_below.place(relwidth=1, relheight=1)

    supriseme_button = customtkinter.CTkButton(window, command=lambda: supriseMeProcessing(), corner_radius=15, bg_color="#f2993f", fg_color="#6c43cd", text="Suprise Me!", text_font=("Comic Sans MS bold", 10), hover_color="#a589e8", border_width=2, height=1, width=1)
    supriseme_button.place(relx=0.56, rely=0.115, relwidth=0.14, relheight=0.07, anchor="center")


    ghostlabel1 = customtkinter.CTkLabel(window, text="\U0001F47B", anchor="nw", text_font=("Comic Sans MS bold", 20), bg_color="#292929", width=5)
    ghostlabel1.place(relx=0.135, rely=0.36) # Top left
    ghostlabel2 = customtkinter.CTkLabel(window, text="\U0001F47B", anchor="ne", text_font=("Comic Sans MS bold", 20), bg_color="#292929", width=5)
    ghostlabel2.place(relx=0.815, rely=0.36) # Top right
    ghostlabel3 = customtkinter.CTkLabel(window, text="\U0001F47B", anchor="sw", text_font=("Comic Sans MS bold", 20), bg_color="#292929", width=5)
    ghostlabel3.place(relx=0.135, rely=0.855) # Bottom left
    ghostlabel4 = customtkinter.CTkLabel(window, text="\U0001F47B", anchor="se", text_font=("Comic Sans MS bold", 20), bg_color="#292929", width=5)
    ghostlabel4.place(relx=0.815, rely=0.855) # Bottom right

    audiobutton = customtkinter.CTkButton(window, text="Audio on", command=mute_switch, text_font=("Comic Sans MS bold", 10), corner_radius=15, bg_color="#f2993f", fg_color="#6c43cd", hover_color="#a589e8", border_width=2, width=1, height=1)
    audiobutton.place(relx=0.41, rely=0.115, anchor="center", relwidth=0.14, relheight=0.07)

    return label_below, second_frame, surprise, location_entry, date_entry, ghostlabel1, ghostlabel2, ghostlabel3, ghostlabel4, audiobutton

# Main Program
pygame.mixer.init()

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

# Changes the icon of the window
image50 = Image.open('img\ghost.png')
photo50 = ImageTk.PhotoImage(image50)
window.iconphoto(False,photo50)

# Calls the setup procedure
label_below, second_frame, surprise, location_entry, date_entry, ghostlabel1, ghostlabel2, ghostlabel3, ghostlabel4, audiobutton = setup()

# Starts the program / tkinter window
window.mainloop()