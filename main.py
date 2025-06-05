from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import pickle
import json
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

try:
    fertilizer_model = pickle.load(open('MODELS/fertilizer_model.pkl', 'rb'))
    crop_model = pickle.load(open('MODELS/crop_recommendation_model.pkl', 'rb'))
    yield_model = pickle.load(open('MODELS/crop_yield_model.pkl', 'rb'))
except FileNotFoundError as e:
    raise RuntimeError(f"Model file not found: {str(e)}")
except Exception as e:
    raise RuntimeError(f"Error loading model: {str(e)}")

app = FastAPI()

request_limit_per_minute = 10
rate_limit_str = f"{request_limit_per_minute}/minute"
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda request, exc: JSONResponse(
    status_code=429, 
    content={"status": "error", "message": "Too Many Requests"}
))
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

class ModelInput(BaseModel): 
    temperature: int
    humidity: int
    moisture: int
    soil_type: int
    crop_type: int
    nitrogen: int
    potassium: int
    phosphorous: int

class CropModelInput(BaseModel): 
    nitrogen: int
    phosphorous: int
    potassium: int
    temperature: float
    humidity: float
    pH: float
    rainfall: float

class YieldModelInput(BaseModel):  
    state: int
    district: int
    crop_type: int
    season: int
    area: float

@app.get("/", response_class=HTMLResponse)
def read_root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🌾</text></svg>">
        <title>CropHawk | PUBLIC API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-image: url('https://images.unsplash.com/photo-1464226184884-fa280b87c399?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80');
                background-size: cover;
                background-position: center;
            }
            .container {
                text-align: center;
                background: rgba(255, 255, 255, 0.8);
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                font-size: 3rem;
                color: #2c3e50;
                margin-bottom: 20px;
            }
            p {
                font-size: 1.2rem;
                color: #34495e;
                margin-bottom: 30px;
            }
            .btn {
                background-color: #27ae60;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-size: 1rem;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            .btn:hover {
                background-color: #219653;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to CropHawk 🌾</h1>
            <p>Your one-stop solution for smart farming and crop recommendations.</p>
            <button class="btn" onclick="window.open('https://crophawk-app.vercel.app/', '_blank')">Explore our Web Application</button>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.post('/fertilizer_recommendation')
@limiter.limit(rate_limit_str)
async def fertilizer_recommendation(request: Request, input_parameters: ModelInput):  
    try:
        input_list = [
            input_parameters.temperature,
            input_parameters.humidity,
            input_parameters.moisture,
            input_parameters.soil_type,
            input_parameters.crop_type,
            input_parameters.nitrogen,
            input_parameters.potassium,
            input_parameters.phosphorous
        ]

        recommendation = fertilizer_model.predict([input_list])[0]
        return {"status": "success", "res": recommendation}  

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Internal Server Error: {str(e)}"}
        )

@app.post('/crop_recommendation')
@limiter.limit(rate_limit_str)
async def crop_recommendation(request: Request, input_parameters: CropModelInput):  
    try:
        input_list = [
            input_parameters.nitrogen,
            input_parameters.phosphorous,
            input_parameters.potassium,
            input_parameters.temperature,
            input_parameters.humidity,
            input_parameters.pH,
            input_parameters.rainfall
        ]

        recommendation = crop_model.predict([input_list])[0]
        return {"status": "success", "res": recommendation} 

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Internal Server Error: {str(e)}"}
        )

@app.post('/yield_prediction')
@limiter.limit(rate_limit_str)
async def yield_prediction(request: Request, input_parameters: YieldModelInput):  
    try:
        input_list = [
            input_parameters.state,
            input_parameters.district,
            input_parameters.crop_type,
            input_parameters.season,
            input_parameters.area
        ]

        prediction = yield_model.predict([input_list])[0]
        return {"status": "success", "res": prediction} 

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Internal Server Error: {str(e)}"}
        )

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Service is healthy"}

if __name__ == "__main__":
    nest_asyncio.apply()
    uvicorn.run(app, host="0.0.0.0", port=8000)