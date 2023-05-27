import streamlit as st
from argparse import Namespace
from helpers.spotify.client import Client
from helpers.objects.track import Track

def execute(args: Namespace):
    song: Track = Client().getTrack(args.url)
    if args.print:
        st.text(song)
        # st.text('\n')
    else:
        st.text(song.name)
        st.text('by ' + song.artist)
        # st.text('\n')
        st.text(song.emotiv)
        # st.text('\n')
    
    if args.plot:
        st.write('WARNING: plotting for individual tracks is currently not supported\n')
