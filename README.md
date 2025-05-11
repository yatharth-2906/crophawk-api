# CropHawk Public API

## Overview
This is the Public API of CropHawk, designed to enable developers to seamlessly integrate and utilize our machine learning models into their applications.

## Base URL
```
https://crophawk-api.onrender.com/
```

## Features
- **Fertilizer Recommendation**: Suggests optimal fertilizers based on the soil conditions.
- **Crop Recommendation**: Recommends the best crops based on the agricultural parameters.
- **Yield Prediction**: Predicts crop yield based on historical data and agricultural factirs to support efficient planning.

## API Endpoints
### 1. Fertilizer Recommendation
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
    "res": "Superphosphate"
}
```

### 2. Crop Recommendation
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
    "res": "mango"
}
```

### 3. Yield Prediction
```
POST /yield_prediction
```
**Request Body:**
```json
{
    "state": 4,
    "district": 88,
    "crop_year": 2003,
    "crop_type": 2,
    "season": 3,
    "area": 304.8
}
```
**Response:**
```json
{
    "status": "success",
    "res": "952.8"
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

## Contact
For any issues, reach out at [yatharth2906@gmail.com] or open an issue on GitHub.
