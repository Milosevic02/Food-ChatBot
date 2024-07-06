from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import db_helper
app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/favicon.ico")
async def read_favicon():
    return JSONResponse(content={"detail": "Not found"}, status_code=404)

@app.post("/")
async def handle_request(request: Request):
    payload = await request.json()
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    
    if intent == "track.order - context: ongoing-tracking":
        return track_order(parameters)

def track_order(parameters: dict, session_id: str):
    order_id = int(parameters['order_id'])
    order_status = db_helper.get_order_status(order_id)
    if order_status:
        fulfillment_text = f"The order status for order id: {order_id} is: {order_status}"
    else:
        fulfillment_text = f"No order found with order id: {order_id}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })