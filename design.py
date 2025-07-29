
import streamlit as st
import random


# add background image
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url('https://www.solidbackgrounds.com/images/3508x2480/3508x2480-bright-turquoise-solid-color-background.jpg');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
""", unsafe_allow_html=True)


#################################################################################

# changing display of final mood
st.markdown(f"""
    <h2 style='text-align: center; color: #FF7F50;'>
        Final Detected Mood: {final_mood.capitalize()} {mood_emojis.get(final_mood, '')}
    </h2>
""", unsafe_allow_html=True)



#################################################################################

#gifs or images based on mood
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


#################################################################################


# styled alers based on mood
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