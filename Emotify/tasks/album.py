import streamlit as st
from argparse import Namespace
from helpers.spotify.client import Client
from helpers.objects.album import Album

def execute(args: Namespace):
    album: Album = Client().getAlbum(args.url, args.num)
    if args.print:
        st.text(album)
    else:
        st.text(album.name)
        st.text('by ' + album.artist)
        # st.text('\n')
        st.text(album.emotive)
        # st.text('\n')

    if args.plot:
        album.plot(args.normalize)