# API Quick Reference Guide

## Base URL
```
http://localhost:5000
```

## Authentication
Include JWT token in header for protected endpoints:
```
Authorization: Bearer <token>
```

---

## Quick Endpoint Reference

### 🔐 Authentication

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/auth/login` | ❌ | Login and get JWT token |
| POST | `/api/auth/signup` | ❌ | Register new user |
| POST | `/api/auth/logout` | ✅ | Logout user |
| GET | `/api/auth/verify` | ✅ | Verify token validity |
| GET | `/api/auth/user` | ✅ | Get current user info |

### 📊 Dashboard

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/dashboard/stats` | ✅ | Get dashboard statistics |

### 🤖 AI Detection

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/detection/crack` | ❌ | Detect cracks in image |
| POST | `/api/detect-earthquake` | ❌ | Legacy crack detection |

### 🏠 Insurance

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/insurance/policies` | ✅ | Get all insurance policies |
| GET | `/api/insurance/policy-numbers` | ❌ | Get policy numbers by insurance code |
| GET | `/api/insurance/claims/all` | ✅ | Get all claims for user |
| GET | `/api/insurance/claims` | ❌ | Get claims by policy number |
| GET | `/api/insurance/assessment` | ❌ | Get assessment data by claims code |
| GET | `/api/insurance/reports` | ✅ | Get insurance reports |
| GET | `/api/insurance/damage-calculation` | ❌ | Get damage calculation |

### 📋 Claims

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/insurance_claims_detail` | ✅ | Get insurance codes for new claim |
| GET | `/api/get_policy` | ❌ | Get policy numbers by insurance code |

---

## Common Request Examples

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'
```

### Get Dashboard Stats
```bash
curl -X GET http://localhost:5000/api/dashboard/stats \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Detect Crack
```bash
curl -X POST http://localhost:5000/api/detection/crack \
  -F "image=@image.jpg"
```

### Get User Policies
```bash
curl -X GET http://localhost:5000/api/insurance/policies \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 302 | Redirect |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 500 | Server Error |

---

## Error Response Format
```json
{
  "success": false,
  "message": "Error description",
  "error": "Detailed error (optional)"
}
```

---

## Environment Variables
```env
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=earthquake_db
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

For detailed documentation, see [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

