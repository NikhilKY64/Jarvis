
import os # Import os for file path handling
from dotenv import dotenv_values # Import dotenv for reading environment variables from a .env file

# Load environment variables from a .env file
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice") # Get the AssistantVoice from the environment variables

# Asynchronous function to convert text to an audio file
async def TextToAudioFile(text) -> None:
    file_path = r"Data\speech.mp3" # Define the path where the speech file will be save
    
    if os.path.exists(file_path): # Check if the file already exists
        os.remove(file_path) # If it exists, remove it to avoid overwriting errors

    # Create the communicate object to generate speech
    communicate = edge_tts. Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%' )
    await communicate.save(r'Data\speech.mp3') # Save the generated speech as an MP3 file

# Function to manage Text-to-Speech (TTS) functionality
def TTS(Text, func=lambda r=None: True):
    while True:
        try:
            # Convert text to an audio file asynchronously
            asyncio.run(TextToAudioFile(Text))

            # Initialize pygame mixer for audio playback
            pygame.mixer.init()
            
            # Load the generated speech file into pygame mixer