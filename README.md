# CropHawk Public API

## Overview
The CropHawk Public API provides developers with seamless access to our machine learning models for agriculture related predictions and recommendations.

## Base URL
```
https://crophawk-api.onrender.com/
```

## Features
- **Fertilizer Recommendation**: Get the best-suited fertilizer based on soil parameters.
- **Crop Recommendation**: Get the best-suited crop to grow based on soil parameters.

## API Endpoints
### 1. Get Fertilizer Recommendation
```
POST /fertilizer_prediction
```
**Request Body:**
```json
{
  "temperature": 28,
  "humidity": 65,
  "moisture": 30,
  "soil_type": 1,
  "crop_type": 2,
  "nitrogen": 40,
  "potassium": 35,
  "phosphorous": 50
}
```
**Response:**
```json
{
    "prediction": [ "Superphosphate" ]
}
```

### 2. Get Crop Recommendation
```
POST /crop_recommendation
```
**Request Body:**
```json
{
  "nitrogen": 40,
  "phosphorous": 50,
  "potassium": 35,
  "temperature": 28,
  "humidity": 64.6,
  "rainfall": 214.4,
  "pH": 6.8
}
```
**Response:**
```json
{
    "prediction": "mango"
}
```

## Usage in JavaScript
To use the API in a JavaScript application, follow the example below:

```js
const fetchFertilizerRecommendation = async () => {
  try {
    const response = await fetch('https://crophawk-api.onrender.com/fertilizer_prediction', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        "temperature": 28,
        "humidity": 65,
        "moisture": 30,
        "soil_type": 1,
        "crop_type": 2,
        "nitrogen": 40,
        "potassium": 35,
        "phosphorous": 50
      })
    });
    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};
```

## Screenshots
### 1. API
![Image](https://github.com/user-attachments/assets/0b69744e-1922-4e86-8bf4-43fb37849922)

### 2. POSTMAN REQUEST
![Image](https://github.com/user-attachments/assets/9771509c-8f36-451d-9a52-e62e59c0b40e)

