# Earthquake Damage Assessment Tool - API Documentation

## Table of Contents
1. [Overview](#overview)
2. [Authentication](#authentication)
3. [API Endpoints](#api-endpoints)
   - [Authentication APIs](#authentication-apis)
   - [Dashboard APIs](#dashboard-apis)
   - [Detection APIs](#detection-apis)
   - [Insurance APIs](#insurance-apis)
   - [Claims APIs](#claims-apis)
   - [Page Routes](#page-routes)
4. [Data Models](#data-models)
5. [Error Handling](#error-handling)

---

## Overview

**Base URL:** `http://localhost:5000`

**API Version:** 1.0

This API provides endpoints for managing earthquake damage assessments, insurance claims, and AI-powered crack detection. The system uses JWT (JSON Web Token) for authentication and MySQL for data persistence.

### Technology Stack
- **Framework:** Flask (Python)
- **Authentication:** JWT (Flask-JWT-Extended)
- **Database:** MySQL (PyMySQL)
- **AI/ML:** PyTorch, Timm (for crack detection)
- **Image Processing:** OpenCV, PIL, Matplotlib

---

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```http
Authorization: Bearer <your_jwt_token>
```

### Token Configuration
- **Expiration:** 60 minutes (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`)
- **Algorithm:** HS256

---

## API Endpoints

### Authentication APIs

Base URL: `/api/auth`

#### 1. Login
**POST** `/api/auth/login`

Authenticate user and receive JWT token.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Status Codes:**
- `200` - Success
- `400` - Missing username or password
- `401` - Invalid credentials
- `403` - Account inactive
- `404` - User not found

---

#### 2. Signup
**POST** `/api/auth/signup`

Register a new user. New users are created with 'inactive' status and require admin approval.

**Request Body:**
```json
{
  "name": "string",
  "email": "string",
  "mobile": "string (optional)",
  "address": "string (optional)",
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully"
}
```

**Status Codes:**
- `200` - Success
- `400` - Missing required fields
- `409` - Username or email already exists

---

#### 3. Logout
**POST** `/api/auth/logout`

🔒 **Requires Authentication**

Logout user and add JWT token to blocklist.

**Response:**
```json
{
  "success": true,
  "message": "Successfully logged out"
}
```

**Status Codes:**
- `200` - Success
- `401` - Invalid/expired token

---

#### 4. Verify Token
**GET** `/api/auth/verify`

🔒 **Requires Authentication**

Verify if the current JWT token is valid.

**Response:**
```json
{
  "success": true,
  "logged_in_as": "username"
}
```

**Status Codes:**
- `200` - Token valid
- `401` - Token invalid/expired

---

#### 5. Get Current User
**GET** `/api/auth/user`

🔒 **Requires Authentication**

Get information about the currently authenticated user.

**Response:**
```json
{
  "success": true,
  "user_id": "username"
}
```

**Status Codes:**
- `200` - Success
- `401` - Unauthorized

---

### Dashboard APIs

Base URL: `/api/dashboard`

#### 1. Get Dashboard Statistics
**GET** `/api/dashboard/stats`

🔒 **Requires Authentication**

Get comprehensive dashboard statistics for the current user.

**Response:**
```json
{
  "success": true,
  "total_insurance_count": 5,
  "total_claims_count": 12,
  "total_picture_tests": 25,
  "total_claim_you_get": 15000.50,
  "total_policy_number": 3,
  "name": "John Doe",
  "email": "john@example.com",
  "mobile": "+1234567890",
  "address": "123 Main St"
}
```

**Status Codes:**
- `200` - Success
- `401` - Unauthorized
- `404` - User not found
- `500` - Server error

---

### Detection APIs

Base URL: `/api/detection`

#### 1. Detect Cracks
**POST** `/api/detection/crack`

Analyze uploaded image using AI model to detect cracks and structural damage.

**Request:**
- Content-Type: `multipart/form-data`
- File field name: `image`
- Accepted formats: JPG, PNG, GIF

**Response:**
```json
{
  "success": true,
  "predicted_class": "Positive (Crack Detected)",
  "confidence": 94.52,
  "probabilities": {
    "Positive (Crack Detected)": 94.52,
    "Negative (No Crack)": 5.48
  }
}
```

**Status Codes:**
- `200` - Success
- `400` - Image file missing or invalid
- `500` - Processing error

**AI Model Details:**
- **Model Type:** Convolutional Neural Network (CNN)
- **Framework:** PyTorch with Timm
- **Classes:** 2 (Crack Detected / No Crack)
- **Output:** Binary classification with confidence scores

---

### Insurance APIs

Base URL: `/api/insurance`

#### 1. Get User Insurance Policies
**GET** `/api/insurance/policies`

🔒 **Requires Authentication**

Get all insurance policies for the current user with full details.

**Response:**
```json
{
  "success": true,
  "user_id": 123,
  "insurance_policies": [
    {
      "id": 1,
      "insurance_code": "INS-2024-001",
      "policy_number": "POL-123456",
      "insurance_from": "2024-01-01",
      "insurance_to": "2025-01-01",
      "insurance_type": "Property",
      "insured": "John Doe",
      "occupation": "Engineer",
      "status": "active",
      "created_at": "2024-01-01 10:00:00"
    }
  ]
}
```

**Status Codes:**
- `200` - Success
- `401` - Unauthorized
- `404` - User not found
- `500` - Server error

---

#### 2. Get Policy Numbers
**GET** `/api/insurance/policy-numbers?insurance_code=INS-2024-001`

Get all policy numbers associated with a specific insurance code.

**Query Parameters:**
- `insurance_code` (required): The insurance code

**Response:**
```json
{
  "success": true,
  "policy_numbers": ["POL-123456", "POL-123457"]
}
```

**Status Codes:**
- `200` - Success
- `400` - Missing insurance_code parameter
- `500` - Server error

---

#### 3. Get All User Claims
**GET** `/api/insurance/claims/all`

🔒 **Requires Authentication**

Get all claims for the current user with complete details.

**Response:**
```json
{
  "success": true,
  "user_id": 123,
  "claims": [
    {
      "id": 1,
      "claims_code": "CLM-2024-001",
      "policy_number": "POL-123456",
      "insurance_id": "INS-2024-001",
      "time_of_loss": "2024-10-20 14:30:00",
      "claim_details": "Earthquake damage to property",
      "situation_of_loss": "Main building, ground floor",
      "cause_of_loss": "Earthquake magnitude 6.5",
      "status": "pending",
      "created_at": "2024-10-21 09:00:00",
      "insured": "John Doe",
      "insurance_type": "Property",
      "insurance_code": "INS-2024-001",
      "claim_recommended": 15000.50
    }
  ]
}
```

**Status Codes:**
- `200` - Success
- `401` - Unauthorized
- `404` - User not found
- `500` - Server error

---

#### 4. Get Claims by Policy
**GET** `/api/insurance/claims?policy_number=POL-123456`

Get all claims codes for a specific policy number.

**Query Parameters:**
- `policy_number` (required): The policy number

**Response:**
```json
{
  "success": true,
  "claims_codes": ["CLM-2024-001", "CLM-2024-002"]
}
```

**Status Codes:**
- `200` - Success
- `400` - Missing policy_number parameter
- `500` - Server error

---

#### 5. Get Assessment Data
**GET** `/api/insurance/assessment?claims_code=CLM-2024-001`

Get detailed assessment data for a specific claim.

**Query Parameters:**
- `claims_code` (required): The claim code

**Response:**
```json
{
  "success": true,
  "data": {
    "file_name": "crack_detection_result_small_1234.png",
    "ai_decision": "Positive (Crack Detected)",
    "confidence": 94.52,
    "crack_percent": 94.52,
    "claim_recommended": 15000.50,
    "damage_area": 150.75,
    "damage_length": 12.5,
    "damage_breadth": 10.3,
    "cpa_id": 456
  }
}
```

**Status Codes:**
- `200` - Success
- `400` - Missing claims_code parameter
- `500` - Server error

---

#### 6. Get Insurance Reports
**GET** `/api/insurance/reports`

🔒 **Requires Authentication**

Get all insurance reports for the current user.

**Response:**
```json
{
  "success": true,
  "reports": [
    {
      "name": "John Doe",
      "email": "john@example.com",
      "insurance_code": "INS-2024-001",
      "insurance_type": "Property",
      "policy_number": "POL-123456",
      "claims_code": "CLM-2024-001",
      "property_type": "Residential",
      "wall_type": "Brick",
      "damage_area": 150.75,
      "rate_per_sqft": 100.00,
      "confidence": 94.52,
      "crack_percent": 94.52,
      "non_crack_percent": 5.48,
      "ai_decision": "Positive (Crack Detected)",
      "file_name": "crack_detection_result_small_1234.png"
    }
  ]
}
```

**Status Codes:**
- `200` - Success
- `401` - Unauthorized
- `500` - Server error

---

#### 7. Get Damage Calculation
**GET** `/api/insurance/damage-calculation?claims_id=1`

Get damage calculation details for a specific claim.

**Query Parameters:**
- `claims_id` (required): The claim ID

**Response:**
```json
{
  "success": true,
  "calculations": [
    {
      "name": "John Doe",
      "insurance_id": "INS-2024-001",
      "policy_number": "POL-123456",
      "claim_id": "CLM-2024-001",
      "file_name": "crack_detection_result_small_1234.png",
      "ai_decision": "Positive (Crack Detected)",
      "confidence": 94.52,
      "crack_percent": 94.52,
      "non_crack_percent": 5.48,
      "claim_recommended": 15000.50
    }
  ]
}
```

**Status Codes:**
- `200` - Success
- `400` - Missing claims_id parameter
- `404` - Claim not found
- `500` - Server error

---

### Claims APIs

Base URL: `/api`

#### 1. Get Insurance Claims Detail
**GET** `/api/insurance_claims_detail`

🔒 **Requires Authentication**

Get insurance codes for the current user to start a new claim.

**Response:**
```json
{
  "success": true,
  "user_id": 123,
  "insurance_codes": [
    {
      "insurance_code": "INS-2024-001"
    },
    {
      "insurance_code": "INS-2024-002"
    }
  ]
}
```

**Status Codes:**
- `200` - Success
- `401` - Unauthorized
- `404` - User not found
- `500` - Server error

---

#### 2. Get Policy Numbers
**GET** `/api/get_policy?insurance_code=INS-2024-001`

Get policy numbers for a specific insurance code.

**Query Parameters:**
- `insurance_code` (required): The insurance code

**Response:**
```json
{
  "success": true,
  "policy_number_all": ["POL-123456", "POL-123457"]
}
```

**Status Codes:**
- `200` - Success
- `400` - Missing insurance_code parameter
- `500` - Server error

---

### Legacy Detection Endpoint

#### Detect Earthquake (Legacy)
**POST** `/api/detect-earthquake`

⚠️ **Legacy Endpoint** - Use `/api/detection/crack` instead.

Analyze uploaded image for crack detection.

**Request:**
- Content-Type: `multipart/form-data`
- File field name: `image`

**Response:**
```json
{
  "predicted_class": "Positive (Crack Detected)",
  "confidence": 94.52,
  "probabilities": {
    "Positive (Crack Detected)": 94.52,
    "Negative (No Crack)": 5.48
  }
}
```

**Status Codes:**
- `200` - Success
- `400` - Image file missing
- `500` - Processing error

---

## Page Routes

### Authentication Pages

#### Login Page
**GET** `/`

Render the login page.

**Response:** HTML page

---

#### Signup Page
**GET** `/signup`

Render the signup page.

**Response:** HTML page

---

### Dashboard Pages

#### Dashboard
**GET** `/dashboard`

Render the main dashboard page.

**Response:** HTML page

---

### Insurance & Claims Pages

#### Insurance Policies List
**GET** `/insurances`

Render the insurance policies list page.

**Response:** HTML page

---

#### Claims List
**GET** `/claims`

Render the claims list page.

**Response:** HTML page

---

#### Claim Insurance Form
**GET** `/claim_insurance`

Render the insurance claim form.

**Response:** HTML page

---

#### Submit Insurance Detail
**POST** `/submit_insurance_detail`

Handle insurance detail form submission.

**Request Body (Form Data):**
```
username: string
insurance_code: string
policy_number: string
insurance_from: date
insurance_to: date
insurance_type: string
insured: string
occupation: string
insurance_details: string
status: string
```

**Response:** Redirect to `/insurance_claims_detail?user_id={user_id}`

**Status Codes:**
- `302` - Redirect on success
- `400` - Missing required fields
- `404` - User not found
- `500` - Server error

---

#### Insurance Claims Detail (Wizard)
**GET** `/insurance_claims_detail`

Render the insurance claims wizard (3-step process for creating claims).

**Response:** HTML page

---

#### Submit Insurance Claims
**POST** `/submit_insurance_claims`

Handle insurance claims form submission.

**Request Body (Form Data):**
```
user_id: integer
claims_code: string
insurance_id: string
claim_details: string
time_of_loss: datetime
situation_of_loss: string
cause_of_loss: string
policy_number: string
```

**Response:** Redirect to `/damaged_property_image?claims_id={id}&claims_code={code}`

**Status Codes:**
- `302` - Redirect on success
- `400` - Missing required fields
- `500` - Server error

---

#### Damaged Property Image
**GET** `/damaged_property_image?claims_id={id}&claims_code={code}`

Render the damaged property image upload page.

**Query Parameters:**
- `claims_id`: Claim ID
- `claims_code`: Claim code

**Response:** HTML page

---

#### Submit Damaged Property Image
**POST** `/submit_damaged_property_image`

Handle damaged property image submission with AI analysis.

**Request:**
- Content-Type: `multipart/form-data`
- File field name: `file_name`
- Additional fields:
  - `claims_id`: Claim ID
  - `claims_code`: Claim code
  - `file_format`: File format
  - `file_desc`: File description

**Processing Steps:**
1. Save uploaded image
2. Calculate crack area using OpenCV
3. Run AI crack detection
4. Save results to database

**Response:** Redirect to `/damaged_property_details?claims_id={id}&claim_property_details_id={details_id}&claims_code={code}`

**Status Codes:**
- `302` - Redirect on success
- `400` - No file uploaded
- `500` - Processing or database error

---

#### Damaged Property Details
**GET** `/damaged_property_details?claims_id={id}&claims_code={code}&claim_property_details_id={details_id}`

Render the damaged property details form.

**Query Parameters:**
- `claims_id`: Claim ID
- `claims_code`: Claim code
- `claim_property_details_id`: Property details ID

**Response:** HTML page with damage area data

---

#### Submit Damaged Property
**POST** `/submit_damaged_property`

Handle damaged property details form submission.

**Request Body (Form Data):**
```
claims_id: integer
claim_property_details_id: integer
claims_code: string
property_type: string
wall_type: string
damage_area: float
rate_per_sqft: float
```

**Calculation:**
```
claim_recommended = damage_area × rate_per_sqft
claim_recommended_usd = claim_recommended / 88 (exchange rate)
```

**Response:** Redirect to `/new_report?claims_id={id}&claim_property_details_id={details_id}&claims_code={code}`

**Status Codes:**
- `302` - Redirect on success
- `400` - Missing required fields
- `500` - Server error

---

#### New Report
**GET** `/new_report?claims_id={id}&claims_code={code}&claim_property_details_id={details_id}`

Render the new report page with claim summary.

**Query Parameters:**
- `claims_id` (required): Claim ID
- `claims_code` (required): Claim code
- `claim_property_details_id`: Property details ID

**Response:** HTML page with report data

**Status Codes:**
- `200` - Success
- `400` - Missing required parameters
- `404` - Claim not found
- `500` - Database error

---

#### Submit Claim Report
**POST** `/submit_claim_report`

Handle claim report submission with user inference.

**Request Body (Form Data):**
```
claims_id: integer
claim_property_details_id: integer
claims_code: string
cpa_id: integer
user_inference: string
final_damage_area: float
final_damage_cost: float
```

**Response:** Redirect to `/new_report` with updated parameters

**Status Codes:**
- `302` - Redirect on success
- `500` - Server error

---

#### Damaged Property Calculation
**GET** `/damaged_property_calculation?claims_id={id}`

Render the damaged property calculation summary page.

**Query Parameters:**
- `claims_id`: Claim ID

**Response:** HTML page with calculation records

---

#### Insurance Report
**GET** `/insurance_report`

Render the insurance report page.

**Response:** HTML page

---

## Data Models

### User
```json
{
  "id": "integer",
  "name": "string",
  "email": "string",
  "mobile": "string",
  "address": "string",
  "username": "string",
  "password": "string (hashed)",
  "role": "string (user/admin)",
  "organization_id": "integer",
  "status": "string (active/inactive)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Insurance
```json
{
  "id": "integer",
  "user_id": "integer",
  "insurance_code": "string",
  "policy_number": "string",
  "insurance_from": "date",
  "insurance_to": "date",
  "insurance_type": "string",
  "insured": "string",
  "occupation": "string",
  "insurance_details": "text",
  "is_active": "boolean",
  "status": "string",
  "created_by": "integer",
  "created_at": "datetime"
}
```

### Claim
```json
{
  "id": "integer",
  "user_id": "integer",
  "claims_code": "string",
  "policy_number": "string",
  "insurance_id": "string",
  "claim_details": "text",
  "time_of_loss": "datetime",
  "situation_of_loss": "text",
  "cause_of_loss": "text",
  "is_active": "boolean",
  "status": "string",
  "created_by": "integer",
  "created_at": "datetime"
}
```

### Claim Property Details
```json
{
  "id": "integer",
  "claims_id": "integer",
  "property_type": "string",
  "wall_type": "string",
  "damage_area": "float",
  "damage_length": "float",
  "damage_breadth": "float",
  "damage_height": "float",
  "rate_per_sqft": "float",
  "is_active": "boolean",
  "status": "string"
}
```

### Claim Property Assessment
```json
{
  "id": "integer",
  "claims_id": "integer",
  "confidence": "float",
  "crack_percent": "float",
  "non_crack_percent": "float",
  "ai_decision": "string",
  "user_inference": "text",
  "final_damage_area": "float",
  "final_damage_cost": "float"
}
```

### Claim Property Image
```json
{
  "id": "integer",
  "claim_property_details_id": "integer",
  "file_name": "string",
  "file_location": "string",
  "file_format": "string",
  "file_desc": "text",
  "is_active": "boolean",
  "status": "string"
}
```

### Claims Value
```json
{
  "id": "integer",
  "claims_id": "integer",
  "claim_recommended": "float (USD)"
}
```

---

## Error Handling

### Standard Error Response
```json
{
  "success": false,
  "message": "Error description",
  "error": "Detailed error message (optional)"
}
```

### Common HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 302 | Redirect (for form submissions) |
| 400 | Bad Request - Missing or invalid parameters |
| 401 | Unauthorized - Invalid or expired token |
| 403 | Forbidden - Account inactive or insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 409 | Conflict - Duplicate entry (e.g., username exists) |
| 500 | Internal Server Error |

### JWT Authentication Errors

**Invalid Token:**
```json
{
  "msg": "Token has been revoked"
}
```

**Expired Token:**
```json
{
  "msg": "Token has expired"
}
```

**Missing Token:**
```json
{
  "msg": "Missing Authorization Header"
}
```

---

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=earthquake_db

# JWT Configuration
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# File Upload
UPLOAD_FOLDER=app/static/upload_image
```

### Database Setup

The application uses MySQL with the following main tables:
- `users` - User accounts
- `insurance` - Insurance policies
- `claims` - Insurance claims
- `claim_property_details` - Property damage details
- `claim_property_assessment` - AI assessment results
- `claim_property_image` - Uploaded images
- `claims_value` - Claim valuation

---

## AI Model Information

### Crack Detection Model

**Model Architecture:** Convolutional Neural Network (CNN) using Timm library

**Model File:** `app/models/models/best_model.pth`

**Input:**
- Image format: RGB
- Preprocessing: Resize and normalize using inference transforms

**Output:**
- Binary classification: Crack Detected / No Crack
- Confidence score (0-100%)
- Probability distribution for both classes

**Class Labels:**
1. `Positive (Crack Detected)` - Structural damage detected
2. `Negative (No Crack)` - No structural damage detected

---

## Image Processing

### Crack Area Calculation

The system uses OpenCV to calculate crack dimensions:

**Process:**
1. Convert image to grayscale
2. Enhance contrast using histogram equalization
3. Apply Gaussian blur
4. Edge detection using Canny algorithm
5. Dilate edges to connect crack patterns
6. Find contours and calculate bounding box
7. Convert pixel measurements to feet

**Output:**
- `length_ft`: Length in feet
- `width_ft`: Width in feet
- `crack_area`: Area in square feet
- `plot_path`: Path to visualization image

**Conversion Rate:**
- Default: 96 pixels per inch
- Adjustable based on camera calibration

---

## Rate Limiting

Currently, there is no rate limiting implemented. For production deployment, consider implementing rate limiting using Flask-Limiter.

---

## API Testing

### Using cURL

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'
```

**Get Dashboard Stats:**
```bash
curl -X GET http://localhost:5000/api/dashboard/stats \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Upload Image for Detection:**
```bash
curl -X POST http://localhost:5000/api/detection/crack \
  -F "image=@/path/to/image.jpg"
```

### Using Python Requests

```python
import requests

# Login
response = requests.post('http://localhost:5000/api/auth/login', 
    json={'username': 'testuser', 'password': 'testpass'})
token = response.json()['token']

# Get dashboard stats
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:5000/api/dashboard/stats', 
    headers=headers)
stats = response.json()

# Upload image for detection
files = {'image': open('damage.jpg', 'rb')}
response = requests.post('http://localhost:5000/api/detection/crack', 
    files=files)
detection_result = response.json()
```

---

## Security Considerations

1. **Password Security:** Passwords are hashed using Flask-Bcrypt before storage
2. **JWT Security:** Tokens expire after 60 minutes by default
3. **Token Blocklist:** Logged out tokens are added to a blocklist
4. **SQL Injection Prevention:** Uses parameterized queries via PyMySQL
5. **File Upload Security:** Uses `secure_filename()` to sanitize uploaded filenames
6. **Account Approval:** New users require admin approval (inactive status by default)

### Recommendations for Production:
- Enable HTTPS
- Implement rate limiting
- Add CORS configuration if needed
- Use environment-specific secrets
- Enable database connection pooling
- Implement comprehensive logging
- Add input validation middleware
- Set up file upload size limits
- Implement CSRF protection for form submissions

---

## Changelog

### Version 1.0.0 (Current)
- Initial API implementation
- JWT authentication
- AI-powered crack detection
- Insurance and claims management
- Dashboard statistics
- Image upload and analysis

---

## Support

For issues or questions, please contact the development team or create an issue in the project repository.

---

**Last Updated:** October 24, 2025
**API Version:** 1.0.0
**Documentation Version:** 1.0.0

