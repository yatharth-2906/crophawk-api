from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import json
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio

# Load the model
fertilizer_model = pickle.load(open('fertilizer_model.pkl', 'rb'))

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

@app.get("/")
def read_root():
    return {"message": "Swagat hai aapka CropHawk ki duniya mei :)"}

@app.post('/fertilizer_prediction')
async def fertilizer_predd(input_parameters: model_input):
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

    prediction = fertilizer_model.predict([input_list])

    return {"prediction": prediction.tolist()}

if __name__ == "__main__":
    nest_asyncio.apply()
    uvicorn.run(app, host="0.0.0.0", port=8000)