import tkinter as tk
from tkinter import END, WORD, ANCHOR, DISABLED, NORMAL, messagebox, LEFT, CENTER, TOP

from PIL import Image, ImageTk
import requests
import webbrowser
import os
from stat import S_IREAD

url_artist = "https://theaudiodb.p.rapidapi.com/search.php"
url_album = "https://theaudiodb.p.rapidapi.com/searchalbum.php"
url_track = "https://theaudiodb.p.rapidapi.com/track.php"
url_videos = "https://theaudiodb.p.rapidapi.com/mvid.php"
url_top_ten = "https://theaudiodb.p.rapidapi.com/track-top10.php"

headers = {
    "X-RapidAPI-Key": "76629d5f79msh7f105d831bd6767p140c96jsndc4e04ff6293",
    "X-RapidAPI-Host": "theaudiodb.p.rapidapi.com"
}

root = tk.Tk()
root.geometry("700x560")
root.title("Name That Album")
# logo
logo = Image.open("best albums.jpg")
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(padx=20, pady=20)

# information
artist_prompt = tk.Label(root, text="What artist are you interested in?")
artist_prompt.grid(column=0, row=1)
instructions = tk.Label(root, wraplength=350, width=50, text="What kind of music to you like?  Enter in your "
                                                             "favorite artist and "
                                                             "click the "
                                                             "submit button.  You will then see a list of "
                                                             "albums by that artist. "
                                                             "From there "
                                                             "you can see information about the artist and "
                                                             "each individual album. "
                                                             " Want to know "
                                                             "the top tracks by that artist?  Just click the "
                                                             "appropriate button. "
                                                             "You can even "
                                                             "see any available Youtube videos from that "
                                                             "artist.")
instructions.place(x=340, y=50)

artist_entry = tk.Entry(fg="black", bg='white', width=25)
artist_entry.grid(column=0, row=2, padx=20, pady=5)

global album_list
global video_link
global video_desc_list
global top_ten_list
global artist


def album_list_request(url):
    try:
        querystring = {"s": artist_entry.get()}
        response = requests.get(url_album, headers=headers, params=querystring)
        album_info = response.json()
        all_albums = album_info['album']
        global album_list
        album_list = tk.Listbox(root, height=18, width=50)
        album_list.place(x=360, y=170)
        for items in all_albums:
            album_name = items['strAlbum']
            album_year = items['intYearReleased']
            all_info = album_name + ' - ' + album_year
            album_list.insert(END, all_info)
        if len(all_albums) > 0:
            show_artist_info_button.config(state=NORMAL)
            show_top_ten_songs_button.config(state=NORMAL)
            show_album_info_button.config(state=NORMAL)
            show_track_list_button.config(state=NORMAL)
            show_music_videos_button.config(state=NORMAL)
            clear_form_button.config(state=NORMAL)
            artist_entry.config(state=DISABLED)
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

        album_title = album_list.get(ANCHOR)
        album_title_split = album_title.split(" -", 1)
        album_title_name = album_title_split[0]
        track_window.title("Track Listing for: " + album_title_name)
        track_window.geometry('310x397')
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


def top_ten_songs():
    global top_ten_window
    global top_ten_list
    global artist
    try:
        top_ten_window = tk.Toplevel(root)
        top_ten_window.geometry('310x397')
        querystring = {"s": artist_entry.get()}
        response = requests.request("GET", url_top_ten, headers=headers, params=querystring)
        top_tracks = response.json()
        tracks = top_tracks['track']
        top_ten_list = tk.Listbox(top_ten_window, height=14, width=50)
        top_ten_list.grid(ipadx=10, ipady=10, padx=10, pady=10)
        for items in tracks:
            track_name = items['strTrack']
            album_name = items['strAlbum']
            artist = items['strArtist']
            all_info = track_name + ' - ' + album_name
            top_ten_list.insert(END, all_info)
        top_ten_window.title("Top Tracks By: " + artist)

    except TypeError:
        tk.messagebox.showwarning(title="No tracks found for artist.", message="Sorry there are no top tracks listed "
                                                                               "for this artist.")
        track_window.destroy()


def show_music_videos():
    global video_window
    global video_desc_list
    try:
        video_window = tk.Toplevel(root)
        video_window.title("Music Videos")
        video_window.geometry('750x400')
        querystring = {"s": artist_entry.get()}
        response = requests.request("GET", url_artist, headers=headers, params=querystring)
        info = response.json()
        video_info = info['artists']
        for video in video_info:
            video_desc = video['idArtist']
        querystring2 = {"i": video_desc}
        response2 = requests.request("GET", url_videos, headers=headers, params=querystring2)
        info2 = response2.json()
        music_videos = info2['mvids']
        video_desc_list = tk.Listbox(video_window, height=20, width=80)
        video_desc_list.grid(ipadx=20, ipady=20, padx=20, pady=10)
        for videos in music_videos:
            video_name = videos['strTrack']
            video_link = videos['strMusicVid']
            all_video_info = video_name + ' - ' + video_link
            video_desc_list.insert(END, all_video_info)
    except TypeError:
        tk.messagebox.showwarning(title="No Artist Found", message="Please enter a valid artist name.")
        album_list.destroy()
        artist_entry.delete(0, END)
    play_video_button = tk.Button(video_window, text="Play Selected Video In Browser", command=play_music_video)
    play_video_button.grid(column=1, row=0)


def play_music_video():
    try:
        video_title = video_desc_list.get(ANCHOR)
        video_title_split = video_title.split(" - ", 1)
        video_title_name = video_title_split[1]
        webbrowser.open_new(video_title_name)
    except IndexError:
        tk.messagebox.showwarning(title="No Video Selected", message="Please select a video from the list.")


def clear_list():
    album_list.delete(0, END)
    album_list.destroy()
    artist_entry.delete(0, END)
    show_artist_info_button.config(state=DISABLED)
    show_top_ten_songs_button.config(state=DISABLED)
    show_album_info_button.config(state=DISABLED)
    show_track_list_button.config(state=DISABLED)
    show_music_videos_button.config(state=DISABLED)
    clear_form_button.config(state=DISABLED)
    artist_entry.config(state=NORMAL)


def help_window():
    os.chmod("help guide.txt", S_IREAD)
    webbrowser.open("help guide.txt")


# create menu
my_menu = tk.Menu(root)
root.config(menu=my_menu)

# add help menu item
main_menu = tk.Menu(my_menu)
my_menu.add_cascade(label="Application", menu=main_menu)
main_menu.add_command(label="Help", command=help_window)

# submit information

submit_button = tk.Button(root, text="Submit Artist", command=lambda: (album_list_request(url_track)))
submit_button.grid(padx=5, pady=5)

show_artist_info_button = tk.Button(root, text="Show Artist Information", command=show_artist_info, state=DISABLED)
show_artist_info_button.grid(padx=0, pady=5)

show_top_ten_songs_button = tk.Button(root, text="Show Top Tracks from Artist", command=top_ten_songs, state=DISABLED)
show_top_ten_songs_button.grid(padx=0, pady=5)

show_album_info_button = tk.Button(root, text="Show Album Information", command=open_album_info, state=DISABLED)
show_album_info_button.grid(padx=0, pady=5)

show_track_list_button = tk.Button(root, text="Show Tracks From Album", command=track_listing, state=DISABLED)
show_track_list_button.grid(padx=0, pady=5)

show_music_videos_button = tk.Button(root, text="Show Music Videos From Artist", command=show_music_videos,
                                     state=DISABLED)
show_music_videos_button.grid(padx=0, pady=5)

clear_form_button = tk.Button(root, text="Clear Album List", command=clear_list, state=DISABLED)
clear_form_button.place(x=460, y=480)

root.mainloop()
