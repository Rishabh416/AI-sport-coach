from fastapi import FastAPI, Form, Request
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

templates = Jinja2Templates(directory="templates")

@app.get('/')
async def root(request: Request):
  return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)