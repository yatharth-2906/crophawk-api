# CropHawk Public API

## Overview
The CropHawk Public API provides developers with seamless access to our machine learning models for agriculture-related predictions and recommendations.

## Base URL
```
https://crophawk-api.onrender.com/
```

## Features
- **Fertilizer Recommendation**: Get the best-suited fertilizer based on soil parameters.
- **Crop Recommendation**: Get the best-suited crop based on soil parameters.

## API Endpoints
### 1. Get Fertilizer Recommendation
```
POST /api/fertilizer-recommendation
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
  "phosphorous": 50,
}
```
**Response:**
```json
{
  "recommended_fertilizer": "Urea"
}
```

### 2. Get Crop Recommendation
```
POST /api/fertilizer-recommendation
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
  "recommended_crop": "Rice"
}
```

## Usage in React
To use the API in a React application, follow the example below:

```js
const fetchFertilizerRecommendation = async () => {
  try {
    const response = await fetch('https://crophawk-api.onrender.com/fertilizer-recommendation', {
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
        "phosphorous": 50,
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

### 2. API DOCS
![Image](https://github.com/user-attachments/assets/6034ee1c-9243-4ee4-8f0c-5395e6e661ce)

