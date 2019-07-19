import spotipy
import spotipy.util as util
from urllib import request
import pprint
import math
from configparser import ConfigParser
import os

pp = pprint.PrettyPrinter(indent=4)

class Spotify_Device():
    id : str
    name : str
    is_active : bool
    is_restricted : bool

    def __init__(self,id=None,name=None,is_active=None, is_restricted=None):
        self.id = id
        self.name = name
        self.is_active = is_active
        self.is_restricted =  is_restricted

class Spotify:
    is_playing_music : bool
    
    def __init__(self):
        config = ConfigParser()
        if os.path.isfile('config.ini'):
            config.read('config.ini',encoding='utf-8-sig')

        self.token = util.prompt_for_user_token(config['SPOTIFY']['username'],'user-read-playback-state user-modify-playback-state',config['SPOTIFY']['client_id'],config['SPOTIFY']['client_secret'],config['SPOTIFY']['redirect_uri'])
        
        if self.token:
            #Spotify Login
            self.sp = spotipy.Spotify(auth=self.token)
            self.sp.trace = False
            self.login_successful = True
            self.active_device = Spotify_Device()
        else:
            self.login_successful = False

    def get_devices(self):
        return self.sp.devices()
    
    def get_active_device(self, devices):
        self.devices = []
        for device in devices['devices']:
            if device['is_active'] is True:
                self.active_device = Spotify_Device(id = device['id'], name = device['name'], is_active = device['is_active'], is_restricted = device['is_restricted'])
            self.devices.append(Spotify_Device(id = device['id'], name = device['name'], is_active = device['is_active'], is_restricted = device['is_restricted']))


    def get_album_art(self, album_url):
        return request.urlopen(album_url).read()
    
    #Playback Controls
    def next_track(self):
        self.sp.next_track(device_id=self.active_device.id)
    
    def previous_track(self):
        self.sp.previous_track(device_id=self.active_device.id)
    
    def pause_track(self):
        self.sp.pause_playback(device_id=self.active_device.id)
        self.is_playing_music = False
    
    def play_track(self):
        self.sp.start_playback(device_id=self.active_device.id)
        self.is_playing_music = True
            
    def get_song_info(self):
        try:
            current_song = self.sp.current_user_playing_track()
            if current_song is not None:
                self.is_playing_music = True
                song_info = current_song['item']
                album_info = current_song['item']['album']

                artist_name = album_info['artists'][0]['name']
                album_name = album_info['name']
                release_date = album_info['release_date']
                biggest_album_image = album_info['images'][0]['url']
                song_name = song_info['name']
                song_length_seconds = int(int(song_info['duration_ms']) / 1000)
                song_popularity = int(song_info['popularity'])

                return {
                    'artist_name' : artist_name, 
                    'album_name' : album_name,
                    'release_date' : release_date,
                    'album_art' : biggest_album_image,
                    'song_name' : song_name,
                    'song_length' : str(math.floor(song_length_seconds/60)) + ':' + str(song_length_seconds%60),
                    'song_popularity' : song_popularity}
            else:
                self.is_playing_music = False
                print("No music is playing")
        except Exception:
            self.sp = spotipy.Spotify(auth=self.token)
            self.get_song_info()