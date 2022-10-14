from sqlite3 import SQLITE_DROP_TEMP_VIEW
import tkinter as tk
from tkinter import font
import requests
from PIL import ImageTk, Image
import customtkinter
from dataclasses import dataclass
import csv
import codecs
import urllib.request
import urllib.error
import sys
from tkinter.font import Font

window = customtkinter.CTk()
window.geometry('750x500')
window.title("Halloween Weather")
customtkinter.set_default_color_theme("dark-blue")

    
# Could EITHER use an API or download the data and read it from a CSV file.

def resize_image(event):
    new_width = event.width
    new_height = event.height
    image = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    label.config(image = photo)
    label.image = photo

## FIND A BETTER IMAGE
image = Image.open('img\halloween-ghost-hand-drawn-set_52683-46646.jpg')
copy_of_image = image.copy()
photo = ImageTk.PhotoImage(image)
label = tk.Label(window, image = photo)
label.bind('<Configure>', resize_image)
label.pack(fill=tk.BOTH, expand = True)


def get_weather(city, date):
    weather_key = 'KZWGYHQU6JZUJ6VTKLAUDH68W'
    url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'
    UnitGroup = 'metric'
    Location = city
    StartDate = date + "-10-31"
    ContentType = 'csv'
    Include = "days"

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

    apiQuery += "&key=" + weather_key

    try: 
        CSVBytes = urllib.request.urlopen(apiQuery)
    except urllib.error.HTTPError  as e:
        ErrorInfo= e.read().decode() 
        print('Error code: ', e.code, ErrorInfo)
        sys.exit()
    except  urllib.error.URLError as e:
        ErrorInfo= e.read().decode() 
        print('Error code: ', e.code,ErrorInfo)
        sys.exit()

    CSVText = csv.reader(codecs.iterdecode(CSVBytes, 'utf-8'))
    RowIndex = 0

    # The first row contain the headers and the additional rows each contain the weather metrics for a single day
    # To simply our code, we use the knowledge that column 0 contains the location and column 1 contains the date.  The data starts at column 4
    for Row in CSVText:
        if RowIndex == 0:
            FirstRow = Row
        else:
            print('Weather in ', Row[0], ' on ', Row[1])

            ColIndex = 0
            for Col in Row:
                if ColIndex >= 4:
                    print('   ', FirstRow[ColIndex], ' = ', Row[ColIndex])
                ColIndex += 1
        RowIndex += 1

def setup():
    # CHANGE FONTS

    tippyTop_frame = customtkinter.CTkFrame(window, bg_color="orange", bd=4)
    tippyTop_frame.place(relx=0.1, rely=0.01, relwidth=0.80, relheight=0.1)

    info_label = customtkinter.CTkLabel(tippyTop_frame, text="Enter a city and any year from 1975 onwards to see the weather on Halloween", text_font=("Arial", 10))
    info_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    top_frame = customtkinter.CTkFrame(window, bg_color="orange", bd=4)
    top_frame.place(relx=0.125, rely=0.15, relwidth=0.75, relheight=0.15)

    city_entry = customtkinter.CTkEntry(top_frame, placeholder_text="City")
    city_entry.place(relx=0.05, rely=0.05, relwidth=0.25, relheight=0.90)

    def slider_event():
        dateSlider = date_slider.get()
        date_label = customtkinter.CTkLabel(top_frame, text=dateSlider)
        date_label.place(relx=0.5, rely=0.5, relwidth=0.2)

    date_slider = customtkinter.CTkSlider(top_frame, from_=1975, to=2022, button_color="orange", command=slider_event)
    date_slider.place(relx=0.38, rely=0.5, relwidth=0.3)


    #date_entry = customtkinter.CTkEntry(top_frame,  placeholder_text="Year")
    #date_entry.place(relx=0.38, rely=0.05, relwidth=0.25, relheight=0.90)

    enter_button = customtkinter.CTkButton(top_frame, text="Enter", command=lambda: get_weather(city_entry.get(), date_entry.get()))
    enter_button.place(relx=0.75, relwidth=0.25, relheight=1)

    second_frame = customtkinter.CTkFrame(window, bg_color="orange", bd=4)
    second_frame.place(relx=0.125, rely=0.35, relwidth=0.75, relheight=0.6)

    label_below = customtkinter.CTkLabel(second_frame, anchor="nw", justify="left", borderwidth=4, text="")
    label_below.place(relwidth=1, relheight=1)



setup()
window.mainloop()