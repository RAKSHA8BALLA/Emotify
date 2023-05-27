import streamlit as st
from helpers.affect.scherer import Emotive2D
from helpers.music.tracks import decode_ms
import webbrowser
from helpers.visualization.plotting import DrawVectors
import requests
# import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_webrtc import webrtc_streamer
import av
import cv2
import numpy as np
import mediapipe as mp
from keras.models import load_model
# import webbrowser
import json

class Playlist():

    def __init__(self, features: dict, tracks: list):
        self._tracks: str      = tracks
        self.name: str         = features['name']
        self.description: str  = features['description']
        self.artists: str      = features['artists']
        self.artists_id: str   = features['artists_id']
        self.id: str           = features['id']
        self.num_tracks: float = len(tracks)
        self.url: str          = features['url']
        self.owner             = features['owner']
        self.owner_id          = features['owner_id'] 

        self.total_time_ms: float = 0
        for track in tracks:
            self.total_time_ms = self.total_time_ms + track.duration_ms

        emotions: list = self.getVectors()
        u_v: float = 0
        u_a: float = 0
        for emotive in emotions:
            u_v = u_v + emotive.getValence()
            u_a = u_a + emotive.getArousal()
        self.emotive = Emotive2D(u_v / self.num_tracks, u_a / self.num_tracks)
    
    def getVectors(self) -> list:
        return [ song.emotive for song in self._tracks]
    
    def __repr__(self, show_tracks: bool = True) -> str:
        emo_input = np.load("emotion.npy")[0]
        # emo_input = emo_input[0]
        val = 'PLAYLIST.meta\n'
        val = val + '  name       : {:>s}\n'.format(self.name)
        val = val + '  by         : {:>s}\n'.format(self.owner)
        val = val + '  num tracks : {:>d}\n'.format(self.num_tracks)
        val = val + '  length     : {:>s}\n'.format(decode_ms(self.total_time_ms))
        val = val + '  url        : {:>s}\n'.format(self.url)
        if show_tracks:
            val = val + '\nPLAYLIST.tracks\n'
            number = 1
            for track in self._tracks:
                emo = Emotive2D.getEmotion(track.emotive)
                
                if emo == emo_input:
                    n = str(number)
                    val = val + '{:s}.'.format(n)
                    val = val + '  {:s}\n'.format(track.name)
                    val = val + '    by {:s}\n'.format(track.artist)
                    val = val + '    on {:s}\n'.format(track.album)
                    # val = val + '  URL: {:s}\n'.format(track.url)
                    st.text(val)
                    st.write(f"URL: [{track.url}](%s)" % track.url)
                    val=''
                    val = val + '\nDetails:\n'
                    val = val + '    {}\n\n'.format(Emotive2D.__repr__(track.emotive).replace('\n', '\n    '))
                    # st.text(val)
                    st.text('\n')
                    val = ''
                    number = number + 1
        val = val + 'PLAYLIST.emotions\n'
        val = val + '  {}\n'.format(Emotive2D.__repr__(self.emotive).replace('\n', '\n  '))
        return val

    def plot(self, normalize:bool):
        DrawVectors('Playlist ' + self.name, self.getVectors(), self._tracks, normalize)

