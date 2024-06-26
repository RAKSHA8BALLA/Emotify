import streamlit as st
from argparse import Namespace
from parsers.feelsparser import FeelsParser
import tasks.index as BigBrain
import requests
from streamlit_lottie import st_lottie
from streamlit_webrtc import webrtc_streamer
import av
import cv2
import numpy as np
import mediapipe as mp
from keras.models import load_model
import webbrowser
import json

def main(args: Namespace):
    BigBrain.execute(args)

st.set_page_config(page_title="Emotify", layout="wide")
# st.header("Emotify")
# st.write("A emotion based music recommender")

m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: rgb(0, 82, 204);
}
</style>""", unsafe_allow_html=True)




def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
# lottie_hello = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_A6VCTi95cd.json")
lottie_hello = load_lottieurl("https://assets5.lottiefiles.com/private_files/lf30_fjln45y5.json")





lc,rc = st.columns(2)
with st.container():
    with rc:
        st_lottie(
            lottie_hello,
            speed=1,
            reverse=False,
            loop=True,
            quality="low", # medium ; high
            # renderer="svg", # canvas
            height=500,
            #
            width=600,
            # key=None,
        )
    with lc:
        # st.subheader("")
        st.header("Emotify")
        st.write("A emotion based Recommendation system")
        # url= st.text_input('Enter the link:')
        play_list = ['Select Option', 'Default Playlist', 'Enter your own playlist']
        pl_result = st.selectbox('Select Playlist', play_list)
        if pl_result == 'Enter your own playlist':
            url= st.text_input('Enter the link:')
        emotion_list = ['Select Emotion','Happy', 'Sad', 'Angry', 'Relaxed', 'Detect']
        result = st.selectbox('Select Emotion',emotion_list)
        # lang = st.text_input("Language")
        # singer = st.text_input("singer")


if pl_result == 'Select Option':
    url = ' '

if pl_result == 'Default Playlist':
    url = 'https://open.spotify.com/playlist/0k7kW5d0O1SLb2r77Fiq8f?si=8CobNodRTPS2338CJcBbjA'



# if __name__ == '__main__':
from parsers.feelsparser import FeelsParser
import sys




# emotion_list = ['Select Emotion','Happy', 'Sad', 'Angry', 'Neutral', 'Detect']
# result = st.selectbox('Select Emotion',emotion_list)


if result == 'Happy':
    pred = 'Happy'
    np.save("emotion.npy", np.array([pred]))

if result == 'Sad':
    pred = 'Sad'
    np.save("emotion.npy", np.array([pred]))

if result == 'Angry':
    pred = 'Angry'
    np.save("emotion.npy", np.array([pred]))

if result == 'Relaxed':
    pred = 'Relaxed'
    np.save("emotion.npy", np.array([pred]))



model = load_model("model.h5")
label = np.load("labels.npy")
holistic = mp.solutions.holistic
hands = mp.solutions.hands
holis = holistic.Holistic()
drawing = mp.solutions.drawing_utils



if "run" not in st.session_state:
    st.session_state["run"] = "true"

try:
    emotion = np.load("emotion.npy")[0]
except:
    emotion = ""

if result == 'Detect':
    if not (emotion):
        st.session_state["run"] = "true"
    else:
        st.session_state["run"] = "false"


    class EmotionProcessor:
        def recv(self, frame):
            frm = frame.to_ndarray(format="bgr24")

            ##############################
            frm = cv2.flip(frm, 1)

            res = holis.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

            lst = []

            if res.face_landmarks:
                for i in res.face_landmarks.landmark:
                    lst.append(i.x - res.face_landmarks.landmark[1].x)
                    lst.append(i.y - res.face_landmarks.landmark[1].y)

                if res.left_hand_landmarks:
                    for i in res.left_hand_landmarks.landmark:
                        lst.append(i.x - res.left_hand_landmarks.landmark[8].x)
                        lst.append(i.y - res.left_hand_landmarks.landmark[8].y)
                else:
                    for i in range(42):
                        lst.append(0.0)

                if res.right_hand_landmarks:
                    for i in res.right_hand_landmarks.landmark:
                        lst.append(i.x - res.right_hand_landmarks.landmark[8].x)
                        lst.append(i.y - res.right_hand_landmarks.landmark[8].y)
                else:
                    for i in range(42):
                        lst.append(0.0)

                lst = np.array(lst).reshape(1, -1)

                pred = label[np.argmax(model.predict(lst))]

                print(pred)
                cv2.putText(frm, pred, (50, 50), cv2.FONT_ITALIC, 1, (255, 0, 0), 2)

                np.save("emotion.npy", np.array([pred]))

            drawing.draw_landmarks(frm, res.face_landmarks, holistic.FACEMESH_TESSELATION,
                                landmark_drawing_spec=drawing.DrawingSpec(color=(0, 0, 255), thickness=-1,
                                                                            circle_radius=1),
                                connection_drawing_spec=drawing.DrawingSpec(thickness=1))
            drawing.draw_landmarks(frm, res.left_hand_landmarks, hands.HAND_CONNECTIONS)
            drawing.draw_landmarks(frm, res.right_hand_landmarks, hands.HAND_CONNECTIONS)

            ##############################

            return av.VideoFrame.from_ndarray(frm, format="bgr24")


with rc:
    btn = st.button("Recommend songs")
if url and result == 'Detect' and st.session_state["run"] != "false":
    with lc:
        webrtc_streamer(key="key", desired_playing_state=True,
                    video_processor_factory=EmotionProcessor)
if btn:
    if not (emotion):
        st.warning("Please let me capture your emotion first")
        st.session_state["run"] = "true"
    else:
        st.session_state["run"] = "false"
        main(args)
        np.save("emotion.npy", np.array([""]))
        # np.delete("emotion.npy", emotion)
        emotion = ''



