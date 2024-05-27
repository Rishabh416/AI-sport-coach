from fastapi import FastAPI, Request
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

import videoCap
import gemini

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

templates = Jinja2Templates(directory="templates")

capture = videoCap.videoRecorder()
geminiInterface = gemini.geminiInterface()

@app.get('/')
async def root(request: Request):
  return templates.TemplateResponse("index.html", {"request": request})

@app.get('/recording.html')
async def recording(request: Request):
  print("working 2")
  capture.startRecording()
  print("working 3")
  return templates.TemplateResponse("recording.html", {"request": request})

@app.get('/aicoach.html')
async def aicoach(request: Request):
  videoSave = geminiInterface.upload_to_gemini("sportVideo.mp4", mime_type="video/mp4")
  geminiInterface.wait_for_files_active(videoSave)
  chat_session = geminiInterface.model.start_chat(
  history=[
      {
        "role": "user",
        "parts": [
          videoSave,
        ],
      },
    ]
  )
  response = chat_session.send_message("Identify the sport and skill present in this video. Provide 2 positives and 2 improvements in regards to the skill shown. Also provide a few ways in which the specific skill can be trained and improved.")
  print(response.text)
  
  return templates.TemplateResponse("aicoach.html", {"request": request, "response": response.text})


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)