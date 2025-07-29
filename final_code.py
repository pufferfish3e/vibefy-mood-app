import streamlit as st
import random
from googleapiclient.discovery import build
import dotenv
import requests
import os
# from transformers import pipeline

# This was changed
# Load environment variables
YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
HF_TOKEN = st.secrets["HF_TOKEN"]

# Load environment variables from .env file
# dotenv.load_dotenv()  
# YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
# HF_TOKEN = os.getenv("HF_TOKEN")

#-------------------------

def search_youtube_video(query, api_key):
    youtube = build("youtube", "v3", developerKey=api_key) # create a YouTube API client
    request = youtube.search().list(
        q=query, # search term
        part="snippet", # request metadata
        type="video", # search only videos
        videoCategoryId="10",  # Music category
        maxResults=10, # no of results
        videoEmbeddable="true", # only return videos that can be embedded into app
    )
    response = request.execute() # send request to YouTube API
    videos = response.get("items", []) # get the list of videos from the response
    if videos: # check if video were found
        selected_video = random.choice(videos) # choose a random video
        video_id = selected_video["id"]["videoId"] # unique identifier(each video)
        video_title = selected_video["snippet"]["title"] # video title
        video_url = f"https://www.youtube.com/watch?v={video_id}" # full video URL

        return video_title, video_url 
    return None, None # if no videos found, return None


# This was changed
def get_emotion_label(text):
    api_url = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }
    response = requests.post(api_url, headers=headers, json={"inputs": text})

    try:
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            top_label = result[0][0]["label"].lower()
            return top_label
    except Exception as e:
        st.error("Error from HuggingFace API")
        print(e)

    return "unknown"
# ----------------------
st.title("Mood Detector App 😊")

input_method = st.radio(
    "How do you want to share your mood?",
    ("Type my feeling", "Select from dropdown")
)

final_mood = "unknown"

if input_method == "Type my feeling":
    user_input = st.text_input(
        "How are you feeling today? (Type your feeling)"
    )
    if user_input:
        # Use the pretrained model to classify emotions
        # results = mood_classifier(user_input)
        results = get_emotion_label(user_input)
        print("Results from HuggingFace API:", results)  # Debugging line to see the results
        if results:
            final_mood = results.lower()
        else:
            final_mood = "unknown"

elif input_method == "Select from dropdown":
    mood_option = st.selectbox("Select your mood:", ["Choose...", "joy", "sadness", "anger", "surprise", "fear", "disgust", "neutral"])
    if mood_option != "Choose...":
        final_mood = mood_option.lower()

# Emojis for moods
mood_emojis = {
    "joy": "😄",
    "sadness": "😢",
    "anger": "😡",
    "surprise": "😲",
    "fear": "😨",
    "disgust": "🤢",
    "neutral": "😐",
    "unknown": "❓"
}

# st.subheader(f"Final Detected Mood: {final_mood.capitalize()} {mood_emojis.get(final_mood, '')}")

st.markdown(f"""
    <h2 style='text-align: center; color: #FF7F50;'>
        Final Detected Mood: {final_mood.capitalize()} {mood_emojis.get(final_mood, '')}
    </h2>
""", unsafe_allow_html=True)

mood_gifs = {
    "joy": "https://media.tenor.com/WHC3_omNF-sAAAAM/joy-inside-out.gif",
    "sadness": "https://media.tenor.com/CV9KmvIEY_gAAAAM/sad-crying.gif",
    "anger": "https://media.tenor.com/u34-uQF3w08AAAAM/anger-scream.gif",
    "surprise": "https://media.tenor.com/KTFdL8YliMwAAAAM/surprised-happy.gif",
    "fear": "https://media4.giphy.com/media/v1.Y2lkPTZjMDliOTUyMThuMDU1cTBmejBtZTRmbHl1NXU0ZW9nOHJ6aDV0NmNmNWMwbzBneCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/14ut8PhnIwzros/source.gif",
    "disgust": "https://media.tenor.com/nmI8w4Urb4sAAAAM/superhero-the-boys.gif",
    "neutral": "https://media.tenor.com/BJZHOmTIJDMAAAAM/futurama-neutral.gif",
    "unknown": "https://media.tenor.com/LbaVZBTP-98AAAAM/frozen-elsa.gif"
}

# Center the image and set width to 300px (adjust as needed)
st.markdown(
    f"""
    <div style="display: flex; justify-content: center; margin: 50px;">
        <img src="{mood_gifs.get(final_mood, '')}" width="300">
    </div>
    """,
    unsafe_allow_html=True
)


# Suggestions
suggestions = {
    "joy": ["Enjoy your day and spread the positivity! 🌟", "Keep smiling and live life to your fullest!", "You're awesome, keep up the good work!"],
    "sadness": ["Take care! Things will get better 💛", "Sending virtual hugs, things will always get better", "You're not alone in this! Don't give up!"],
    "anger": ["Take a deep breath. You got this. 💨", "Step away and reset.", "Channel your energy positively!"],
    "fear": ["You are stronger than you think.", "Breathe. Face it one step at a time.", "Courage starts with showing up."],
    "surprise": ["Life is full of surprises!", "Embrace the unexpected!", "Wow, that was unexpected!"],
    "disgust": ["It's okay to feel that way sometimes.", "Try to focus on the positive aspects.", "Take a moment to breathe and reset."],
    "neutral": ["It's okay to have mixed feelings.", "Take a moment to reflect on your day.", "Sometimes it's good to just be present."],
    "unknown": ["Tell me more about how you're feeling."]
}

# msg_list = suggestions.get(final_mood, ["Tell me more."])
# random_message = random.choice(msg_list)

# st.write(random_message)

# Mood to Streamlit status function mapping
mood_to_display = {
    "joy": st.success,
    "sadness": st.info,
    "anger": st.error,
    "fear": st.warning,
    "surprise": st.info,
    "disgust": st.warning,
    "neutral": st.write,
    "unknown": st.write
}

# Pick a random message
msg_list = suggestions.get(final_mood, ["Tell me more."])
random_message = random.choice(msg_list)

# Get the display function based on mood
display_func = mood_to_display.get(final_mood, st.write)

# Show the styled message
display_func(random_message)


# ========== Search and Display YouTube Song ==========
st.markdown("### 🎵 Recommended Song for You")

recommended_song = None
if final_mood != "unknown": # if mood is found

    # Create query based on input method
    if input_method == "Type my feeling": 
        search_query = f"{final_mood} official music video for when you feel\"{user_input}\""
        # search_query = f"recommend me a official song where mood is {final_mood} when i m feeling \"{user_input}\""
    elif input_method == "Select from dropdown":
        search_query = f"{final_mood} official song audio lyrics"
    
    # Search for YouTube video
    video_title, recommended_song = search_youtube_video(search_query, YOUTUBE_API_KEY)

if recommended_song:
    st.markdown(f"#### Video Name: [{video_title}]({recommended_song})")
    st.video(recommended_song)
else:
    st.write("Sorry, no video found for your mood. Please write your feeling again.")



print("Recommended song URL:", recommended_song)  # Debugging line to see the recommended song URL



st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url('https://img.freepik.com/premium-photo/plain-light-pink-background_1174990-190152.jpg');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
""", unsafe_allow_html=True)



