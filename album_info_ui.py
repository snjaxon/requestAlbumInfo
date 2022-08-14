import tkinter as tk
from tkinter import END, WORD, ANCHOR, DISABLED, NORMAL, messagebox

from PIL import Image, ImageTk
import requests

url_artist = "https://theaudiodb.p.rapidapi.com/search.php"
url_album = "https://theaudiodb.p.rapidapi.com/searchalbum.php"
url_track = url = "https://theaudiodb.p.rapidapi.com/track.php"
headers = {
    "X-RapidAPI-Key": "76629d5f79msh7f105d831bd6767p140c96jsndc4e04ff6293",
    "X-RapidAPI-Host": "theaudiodb.p.rapidapi.com"
}

root = tk.Tk()
root.geometry("340x690")
root.title("Name that Album")
# logo
logo = Image.open("best albums.jpg")
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(padx=20, pady=20)

# information
artist_prompt = tk.Label(root, text="What artist are you interested in?")
artist_prompt.grid(padx=20, pady=5)

artist_entry = tk.Entry(fg="black", bg='white', width=25)
artist_entry.grid(padx=20, pady=5)

global album_list


def album_list_request(url):
    try:
        querystring = {"s": artist_entry.get()}
        response = requests.get(url_album, headers=headers, params=querystring)
        album_info = response.json()
        all_albums = album_info['album']
        global album_list
        album_list = tk.Listbox(root, height=14, width=50)
        album_list.grid(ipadx=10, ipady=10, padx=10, pady=10)
        for items in all_albums:
            album_name = items['strAlbum']
            album_year = items['intYearReleased']
            all_info = album_name + ' - ' + album_year
            album_list.insert(END, all_info)
        if len(all_albums) > 0:
            show_artist_info_button.config(state=NORMAL)
            show_album_info_button.config(state=NORMAL)
            show_track_list_button.config(state=NORMAL)
            clear_form_button.config(state=NORMAL)
    except TypeError:
        tk.messagebox.showwarning(title="No Artist Found", message="Please enter a valid artist name.")
        album_list.destroy()
        artist_entry.delete(0, END)


def show_artist_info():
    global artist_window
    try:
        artist_window = tk.Toplevel(root)
        artist_window.title("Artist Information")
        artist_window.geometry('750x400')
        querystring = {"s": artist_entry.get()}
        response = requests.request("GET", url_artist, headers=headers, params=querystring)
        info = response.json()
        artist_info = info['artists']
        artist_desc_text = tk.Text(artist_window, height=20, width=80, wrap=WORD)
        artist_desc_text.grid(ipadx=20, ipady=20, padx=20, pady=10)
        for artist in artist_info:
            artist_desc = artist['strBiographyEN']
            artist_desc_text.insert(END, artist_desc)
    except TypeError:
        tk.messagebox.showwarning(title="No Artist Found", message="Please enter a valid artist name.")
        album_list.destroy()
        artist_entry.delete(0, END)


def open_album_info():
    global info_window
    try:
        info_window = tk.Toplevel(root)
        info_window.title("Album Information")
        info_window.geometry('750x400')
        album_title = album_list.get(ANCHOR)
        album_title_split = album_title.split(" -", 1)
        album_title_name = album_title_split[0]
        querystring = {"s": artist_entry.get(), "a": album_title_name}
        response = requests.request("GET", url_album, headers=headers, params=querystring)
        info = response.json()
        all_albums = info['album']
        album_desc_text = tk.Text(info_window, height=20, width=80, wrap=WORD)
        album_desc_text.grid(ipadx=20, ipady=20, padx=20, pady=10)
        for items in all_albums:
            album_desc = items['strDescriptionEN']
            album_desc_text.insert(END, album_desc)
    except KeyError:
        tk.messagebox.showwarning(title="No Album Info", message="Sorry, there appears to be no information for this "
                                                                 "album")
        info_window.destroy()


def track_listing():
    global track_window
    global album_id
    try:
        track_window = tk.Toplevel(root)
        track_window.title("Track Listing")
        track_window.geometry('310x397')
        album_title = album_list.get(ANCHOR)
        album_title_split = album_title.split(" -", 1)
        album_title_name = album_title_split[0]
        querystring = {"s": artist_entry.get(), "a": album_title_name}
        response = requests.request("GET", url_album, headers=headers, params=querystring)
        info = response.json()
        all_albums = info['album']
        for items in all_albums:
            album_id = items['idAlbum']
        querystring2 = {"m": album_id}
        response2 = requests.request("GET", url_track, headers=headers, params=querystring2)
        info2 = response2.json()
        album_tracks = info2['track']
        album_track_list_list = tk.Listbox(track_window, height=20, width=35)
        album_track_list_list.grid(ipadx=20, ipady=20, padx=30, pady=10)
        for items2 in album_tracks:
            album_track_list = items2['strTrack']
            album_track_list_list.insert(END, album_track_list)
    except KeyError:
        tk.messagebox.showwarning(title="No Track Information", message="Sorry, there appears to be no information "
                                                                        "for this "
                                                                        "album")
        track_window.destroy()


def clear_list():
    album_list.delete(0, END)
    album_list.destroy()
    artist_entry.delete(0, END)
    show_artist_info_button.config(state=DISABLED)
    show_album_info_button.config(state=DISABLED)
    show_track_list_button.config(state=DISABLED)
    clear_form_button.config(state=DISABLED)


# submit information

submit_button = tk.Button(root, text="Submit Artist", command=lambda: (album_list_request(url)))
submit_button.grid(padx=5, pady=5)

show_artist_info_button = tk.Button(root, text="Show Artist Information", command=show_artist_info, state=DISABLED)
show_artist_info_button.grid(padx=0, pady=0)

show_album_info_button = tk.Button(root, text="Show Album Information", command=open_album_info, state=DISABLED)
show_album_info_button.grid(padx=0, pady=0)

show_track_list_button = tk.Button(root, text="Show Tracks from album", command=track_listing, state=DISABLED)
show_track_list_button.grid(padx=0, pady=0)

clear_form_button = tk.Button(root, text="Clear album list", command=clear_list, state=DISABLED)
clear_form_button.grid(padx=5, pady=5)

root.mainloop()