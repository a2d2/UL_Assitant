# uvicorn main:app
# uvicorn main:app --reload

#Main imports
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai 

# Custom function imports
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.database import store_messages, reset_messages
from functions.text_to_speech import convert_text_to_speech


# Initiate App
app = FastAPI()

# CORS - Origins
origins =["http://localhost:5173", 
          "http://localhost:5174", 
          "http://localhost:4173", 
          "http://localhost:4174",
          "http://localhost:3000", 
         ]

# CORS -Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chack health
@app.get("/health")
async def check_health():
    return {"message": "healthy"}

# Reset Conversation
@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"response": "conversation reset"}

# Check audio
@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):

    # # Get saved audio
    # audio_input = open("voice.mp3", "rb")

    # Save the frontend file 
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")

    #Decode Audio
    message_decoded = convert_audio_to_text(audio_input)

    # print(message_decoded)

    # Guard: Ensure output
    if not message_decoded:
        return HTTPException(status_code=400, detail="Failed to decode audio")
    
    # Get chatGPT response
    chat_response = get_chat_response(message_decoded)

    # Guard: Ensure output
    if not chat_response:
        return HTTPException(status_code=400, detail="Failed chat response")
    
    # Store messages
    store_messages(message_decoded, chat_response)

    # Convert chat response to audio
    print(chat_response)
    audio_output = convert_text_to_speech(chat_response)

    # Guard: Ensure output
    if not audio_output:
       raise HTTPException(status_code=400, detail="Failed to get Eleven Labs audio output")

    # Create a generator that yields chunks of data
    def iterfile():
       yield audio_output

    # Use for Post: Return output audio
    return StreamingResponse(iterfile(), media_type="application/octet-stream")
    
    # return "Done"


