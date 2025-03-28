# CropHawk Public API

## Overview
This is the Public API of CropHawk, designed to enable developers to seamlessly integrate and utilize our machine learning models.

## Base URL
```
https://crophawk-api.onrender.com/
```

## Features
- **Fertilizer Recommendation**: Suggests optimal fertilizers based on the soil conditions.
- **Crop Recommendation**: Recommends the best crops based on the agricultural parameters.

## API Endpoints
### 1. Get Fertilizer Recommendation
```
POST /fertilizer_recommendation
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
    "status": "success",
    "recommendation": "Superphosphate"
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
    "potassium": 35,
    "phosphorous": 50,
    "temperature": 28,
    "humidity": 64.6,
    "rainfall": 214.4,
    "pH": 6.8
}
```
**Response:**
```json
{
    "status": "success",
    "recommendation": "mango"
}
```

## Usage in JavaScript
To use the API in a JavaScript applications, follow the example below:

```js
const fetchFertilizerRecommendation = async () => {
  try {
    const response = await fetch('https://crophawk-api.onrender.com/fertilizer_recommendation', {
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

### 2. API POSTMAN REQUEST
![Image](https://github.com/user-attachments/assets/19c19c5f-1e3d-443c-9fd5-7224e57ecc68)
