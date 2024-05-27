import os
from dotenv import load_dotenv
import time

import google.generativeai as genai

class geminiInterface:
  def __init__(self):
    load_dotenv()
    api_key = os.getenv('API_KEY')
    genai.configure(api_key=api_key)
    generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 64,
      "max_output_tokens": 8192,
      "response_mime_type": "text/plain",
    }
    safety_settings = [
      {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
      },
      {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
      },
      {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
      },
      {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
      },
    ]

    self.model = genai.GenerativeModel(
      model_name="gemini-1.5-flash-latest",
      safety_settings=safety_settings,
      generation_config=generation_config,
    )

  def upload_to_gemini(self, path, mime_type=None):
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

  def wait_for_files_active(self, *files):
    print("Waiting for file processing...")
    for name in (file.name for file in files):
      file = genai.get_file(name)
      while file.state.name == "PROCESSING":
        print(".", end="", flush=True)
        time.sleep(10)
        file = genai.get_file(name)
      if file.state.name != "ACTIVE":
        raise Exception(f"File {file.name} failed to process")
    print("...all files ready")



# video_drive0 = upload_to_gemini("sportVideo.mp4", mime_type="video/mp4")

# wait_for_files_active(video_drive0)

# chat_session = model.start_chat(
#   history=[
#     {
#       "role": "user",
#       "parts": [
#         video_drive0,
#       ],
#     },
#   ]
# )

# response = chat_session.send_message("Describe what you see in this video")

# print(response.text)