from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import pickle
import json
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio

fertilizer_model = pickle.load(open('MODELS/fertilizer_model.pkl', 'rb'))
crop_model = pickle.load(open('MODELS/crop_recommendation_model.pkl', 'rb'))
yield_model = pickle.load(open('MODELS/crop_yield_model.pkl', 'rb'))

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

class model_input(BaseModel):
    temperature: int
    humidity: int
    moisture: int
    soil_type: int
    crop_type: int
    nitrogen: int
    potassium: int
    phosphorous: int

class crop_model_input(BaseModel):
    nitrogen : int
    phosphorous : int
    potassium : int
    temperature : float
    humidity : float
    pH : float
    rainfall : float

class yield_model_input(BaseModel):
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
async def fertilizer_recommendation(input_parameters: model_input):
    try:
        input_data = input_parameters.json()
        input_dictionary = json.loads(input_data)

        temperature = input_dictionary['temperature']
        humidity = input_dictionary['humidity']
        moisture = input_dictionary['moisture']
        soil_type = input_dictionary['soil_type']
        crop_type = input_dictionary['crop_type']
        nitrogen = input_dictionary['nitrogen']
        potassium = input_dictionary['potassium']
        phosphorous = input_dictionary['phosphorous']

        input_list = [temperature, humidity, moisture, soil_type, crop_type, nitrogen, potassium, phosphorous]

        recommendation = fertilizer_model.predict([input_list])[0]

        return {"status": "success", "res": recommendation}

    except KeyError as e:
        return {"status": "error", "message": f"Missing key: {str(e)}"}
    except json.JSONDecodeError:
        return {"status": "error", "message": "Invalid JSON format"}
    except Exception as e:
        return {"status": "error", "message": f"Internal Server Error: {str(e)}"}


@app.post('/crop_recommendation')
async def crop_recommendation(input_parameters: crop_model_input):
    try:
        input_data = input_parameters.json()
        input_dictionary = json.loads(input_data)

        nitrogen = input_dictionary['nitrogen']
        phosphorous = input_dictionary['phosphorous']
        potassium = input_dictionary['potassium']
        temperature = input_dictionary['temperature']
        humidity = input_dictionary['humidity']
        pH = input_dictionary['pH']
        rainfall = input_dictionary['rainfall']

        input_list = [nitrogen, phosphorous, potassium, temperature, humidity, pH, rainfall]

        recommendation = crop_model.predict([input_list])[0]

        return {"status": "success", "res": recommendation}

    except KeyError as e:
        return {"status": "error", "message": f"Missing key: {str(e)}"}
    except json.JSONDecodeError:
        return {"status": "error", "message": "Invalid JSON format"}
    except Exception as e:
        return {"status": "error", "message": f"Internal Server Error: {str(e)}"}

@app.post('/yield_prediction')
async def yield_prediction(input_parameters: yield_model_input):
    try:
        input_data = input_parameters.json()
        input_dict = json.loads(input_data)

        input_list = [
            input_dict['state'],
            input_dict['district'],
            input_dict['crop_type'],
            input_dict['season'],
            input_dict['area']
        ]

        prediction = yield_model.predict([input_list])[0]

        return {"status": "success", "res": prediction}

    except KeyError as e:
        return {"status": "error", "message": f"Missing key: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Internal Server Error: {str(e)}"}


if __name__ == "__main__":
    nest_asyncio.apply()
    uvicorn.run(app, host="0.0.0.0", port=8000)
