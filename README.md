# CropHawk Public API

## Overview
The CropHawk Public API provides developers with seamless access to our machine learning models for agriculture-related predictions and recommendations.

## Base URL
```
https://crophawk-api.onrender.com/
```

## Features
- **Fertilizer Recommendation**: Get the best-suited fertilizer based on soil parameters.
- **Crop Prediction**: Predict the best crops based on environmental factors.

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
  "ph": 6.8
}
```
**Response:**
```json
{
  "recommended_fertilizer": "Urea"
}
```

## Usage in React
To use the API in a React application, follow the example below:

```js
const fetchFertilizerRecommendation = async () => {
  try {
    const response = await fetch('https://crophawk-api.onrender.com/api/fertilizer-recommendation', {
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
        "ph": 6.8
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
![Image](https://github.com/user-attachments/assets/af842afe-5bc8-4819-8273-62fdf77a08f1)

### 2. API DOCS
![Image](https://github.com/user-attachments/assets/54dacdae-6132-45e6-9fba-bd897b9c6ad2)

