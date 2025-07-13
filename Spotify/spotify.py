import random

song_list = {"505": "Arctic Monkeys", "Do I Wanna Know?": "Arctic Monkeys", "After Hours": "Weekend", "Enter the Sandman": "Mettalica", "Diet Mountain Dew": "Lana Del Ray", "Sajde":"Faheem Abdullah", "11K":"Seedhe Maut"}
library = {}
profile_db = {}
song_keys = list(song_list.keys())
playlist_keys = library.values()
song_len = len(song_keys)
now_playing = 0
song_number = 0
volume =  100

class Profile:
   def __init__(self, name, age, followers, following):
      self.name = name
      self.age = age
      self.followers = followers
      self.following = following
   def __str__(self):
       return f"Profile(name={self.name}, age={self.age}, followers={self.followers}, following={self.following})"

def create_profile(name,age, followers, following):
      global Profile
      profile_db[name] = Profile(name, age, followers, following)
      print("Your profile has been created")

def open_profile(n):
   print(profile_db[n])

def create_playlist(playlist_name):
    library[playlist_name] = []
    print("Your playlist has been created:", playlist_name)

def add_song(playlist_name, song_keys,n):
    if playlist_name in library:
     library[playlist_name].append(song_keys[n])
     print(song_keys[n],"has been added to", playlist_name, "playlist.", "This is your updated playlist:", library[playlist_name])
    else:
       print(playlist_name,"Playlist does not exist")

def remove_song(playlist_name, song_keys,n):
    if playlist_name in library:
     library[playlist_name].remove(song_keys[n])
     print(song_keys[n],"has been removed from", playlist_name, "playlist.", "This is your updated playlist:", library[playlist_name])
    else:
       print(playlist_name,"Playlist does not exist")

def play_song(song_keys, n):
   global now_playing
   global song_number
   now_playing = song_keys[n]
   song_number = n
   print(now_playing, "is playing right now. Happy listening")
   
def play_playlist(library, playlist_name, n):
   global now_playing
   global song_number
   now_playing = library[playlist_name][n]
   song_number = n
   print(now_playing, "is playing right now, Happy listening")

def random_song(song_keys):
   global now_playing
   global song_number
   n = random.randint(0,song_len-1)
   now_playing = song_keys[n]
   song_number = n
   print(now_playing,"is playing right now.")

def pause_song(now_playing):
   print(now_playing, "has been paused")

def next_song(song_keys):
    global now_playing
    global song_number
    global song_len
    song_number = (song_number + 1) % song_len
    now_playing = song_keys[song_number]
    print(now_playing, "is playing right now. Happy listening")

def prev_song(song_keys):
    global now_playing
    global song_number
    global song_len
    song_number = song_number - 1
    now_playing = song_keys[song_number]
    print(now_playing, "is playing right now. Happy listening")

def volume_up():
   global volume
   if volume <=100:
      print("Your volume is at max")
   else:
    volume +=5
    print("Your volume has been increased by 5% to :", volume)

def volume_down():
   global volume
   if volume <=0:
      print("Your volume is at lowest")
   else:
    volume -=5
    print("Your volume has been decreased by 5% to :", volume)

def volume_set(n):
   global volume
   if n<0 or n>100:
     print("You can't set that value")
     return
   volume = n
   print("Your volume has been set to:", volume)

