import requests


url = "https://theaudiodb.p.rapidapi.com/searchalbum.php"
headers = {
    "X-RapidAPI-Key": "76629d5f79msh7f105d831bd6767p140c96jsndc4e04ff6293",
    "X-RapidAPI-Host": "theaudiodb.p.rapidapi.com"
}

entry_question = input("Are you interested in an artist's album list(l) or an album's information(i)? ")


def album_list_request(url):
    artist = input("What artist albums are you interested in? ")
    querystring = {"s": artist}
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()


def album_info_request(url):
    artist = input("Who is the artist you are looking for? ")
    album = input("What album are you interested in? ")
    querystring = {"s": artist, "a": album}
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()


def parse_json_list(response):
    print("Here is a list of the albums and the year it was released.")
    for item in response['album']:
        print(item['strAlbum'] + " - " + item['intYearReleased'])
    return


def parse_json_album(response):
    print("Here is the information for that album.")
    for item in response['album']:
        print(item['strDescriptionEN'])
    return


if entry_question == "l":
    band_data = album_list_request(url)
    parse_json_list(band_data)
elif entry_question == "i":
    band_data = album_info_request(url)
    parse_json_album(band_data)
else:
    print("I am sorry, you have entered invalid data.")




