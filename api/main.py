from fastapi import FastAPI, Body, Depends, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import os.path as osp
import json

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

templates = Jinja2Templates(directory="./templates")

@app.post("/webhook/")
async def paypal_webhook(request: Request):
    request_data = await request.json()
    event_type = request_data['event_type']
    resource = request_data['resource']

    print("Type: ", event_type)
    if event_type == 'PAYMENT.SALE.COMPLETED':
        '''
        Do nothing
        '''
        user_id = resource['billing_agreement_id'] # Matches subscriptionID in JS SDK
        event_time = resource['update_time']
    elif event_type == 'BILLING.SUBSCRIPTION.ACTIVATED':
        '''
        Set user to this plan
        CARE: Hopefully also when user changes plan
        '''
        user_id = resource['id'] # Matches subscriptionID in JS SDK
        plan_id = resource['plan_id']
        event_time = resource['update_time']
    elif event_type in ('BILLING.SUBSCRIPTION.PAYMENT.FAILED', 
                        'BILLING.SUBSCRIPTION.CANCELLED',
                        'BILLING.SUBSCRIPTION.EXPIRED',
                        'BILLING.SUBSCRIPTION.SUSPENDED'):
        '''
        If user is on this plan, set them to free plan, sent email
        '''
        user_id = resource['id'] # Matches subscriptionID in JS SDK
        plan_id = resource['plan_id']
        event_time = resource['update_time']     
    elif event_type == 'BILLING.SUBSCRIPTION.RE-ACTIVATED':
        '''
        Does not have plan id => Set user to last plan_id if any
        '''
        user_id = resource['id'] # Matches subscriptionID in JS SDK
        event_time = resource['update_time']   
    else:
        pass

    return {"status": "success"}

@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/{template_name}')
async def template(request: Request, template_name: str):
    if not template_name.endswith('.html'):
        template_name = f"{template_name}.html"
    if not osp.isfile('./templates/' + template_name):
        raise HTTPException(status_code=404, detail="Not found.")
    else:
        return templates.TemplateResponse(template_name, {"request": request})

'''
I-9WU1ETXFJAB2        
'''