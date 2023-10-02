import requests
from decouple import config

ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")

# Eleven Labs
# Convert text to speech
def convert_text_to_speech(message):
  
  # Define data
  body = {
    "text": message,
    # "model_id": "eleven_multilingual_v1",
    "voice_settings": {
        "stability": 0,
        "similarity_boost": 0,
        "style": 0,
    }
  }

  # Define voice
  # voice_charlotte = "XB0fDUnXU5powFXDhCwa"
  voice_rachel = "21m00Tcm4TlvDq8ikWAM"

  # Construct request headers and url
  headers = { "xi-api-key": ELEVEN_LABS_API_KEY, "Content-Type": "application/json", "accept": "audio/mpeg" }
  endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_rachel}"

  # Send request
  try:
    response = requests.post(endpoint, json=body, headers=headers)
  except Exception as e:
     return

  # Handle response
  if response.status_code == 200:
      # with open("output.wav", "wb") as f:
      #     f.write(audio_data)
      return response.content
  else:
    return