from fastapi import FastAPI, Body, Depends, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "*", #Also enough for webhooks
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/webhook/")
async def paypal_webhook(request: Request):
    request_data = await request.json()

    print(request_data)

    return {"status": "success"}