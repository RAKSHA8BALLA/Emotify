import streamlit as st
from argparse import Namespace
from helpers.spotify.client import Client
from helpers.objects.playlist import Playlist

def execute(args:Namespace):
    playlist:Playlist = Client().getPlaylist(args.url, args.num)

    if args.print:
        st.text(playlist)
        # st.text('\n')
    else:
        st.text(playlist.name)
        st.text('\n')
        if len(playlist.description):
            st.text(playlist.description)
        st.text('by ' + playlist.owner )
        # st.text('\n')
        st.text(playlist.emotive.__repr__().replace('valence  ', 'valence μ').replace('arousal  ', 'arousal μ'))
        # st.text('\n')

    if args.plot:
        playlist.plot(args.normalize)

