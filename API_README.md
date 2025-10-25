# API Documentation - README

Welcome to the Earthquake Damage Assessment Tool API documentation! This folder contains comprehensive documentation and resources for working with the API.

## 📚 Documentation Files

### 1. **API_DOCUMENTATION.md** 
The complete API reference documentation with:
- Detailed endpoint descriptions
- Request/response examples
- Authentication guide
- Data models
- Error handling
- Security considerations
- Configuration instructions

**👉 Start here for complete API understanding**

### 2. **API_QUICK_REFERENCE.md**
A condensed quick reference guide with:
- Quick endpoint lookup table
- Common request examples
- Response codes
- Essential cURL commands

**👉 Use this for quick lookups during development**

### 3. **Earthquake_API_Collection.postman_collection.json**
Postman collection file with:
- Pre-configured API requests
- Environment variables
- Auto token management
- Example payloads

**👉 Import this into Postman for easy API testing**

---

## 🚀 Quick Start

### 1. Setup Environment

Create a `.env` file in the project root:

```env
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=earthquake_db
SECRET_KEY=your_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Server

```bash
python app.py
```

The API will be available at `http://localhost:5000`

### 4. Test with cURL

```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'

# Get Dashboard Stats (replace TOKEN with your JWT token)
curl -X GET http://localhost:5000/api/dashboard/stats \
  -H "Authorization: Bearer TOKEN"
```

---

## 🧪 Using Postman Collection

### Import Collection

1. Open Postman
2. Click **Import** button
3. Select `Earthquake_API_Collection.postman_collection.json`
4. Collection will be imported with all endpoints

### Setup Variables

The collection uses two variables:

- **base_url**: Default is `http://localhost:5000`
- **jwt_token**: Auto-populated after login

To change base URL:
1. Right-click collection → Edit
2. Go to Variables tab
3. Update `base_url` value

### Workflow

1. **Login** - Run the login request first
   - Token is automatically saved to variables
   - All subsequent requests use this token

2. **Test Endpoints** - All endpoints are organized by category:
   - Authentication
   - Dashboard
   - AI Detection
   - Insurance
   - Claims
   - Page Routes

3. **Upload Files** - For image upload endpoints:
   - Click on Body → form-data
   - Select file from your computer
   - Send request

---

## 📋 API Categories

### 🔐 Authentication APIs
Handle user registration, login, logout, and token management.

**Key Endpoints:**
- `POST /api/auth/login` - Get JWT token
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/logout` - Logout user

### 📊 Dashboard APIs
Retrieve statistics and dashboard data.

**Key Endpoints:**
- `GET /api/dashboard/stats` - Get comprehensive stats

### 🤖 AI Detection APIs
Analyze images for crack detection using AI.

**Key Endpoints:**
- `POST /api/detection/crack` - Detect cracks in images

### 🏠 Insurance APIs
Manage insurance policies and claims.

**Key Endpoints:**
- `GET /api/insurance/policies` - Get all policies
- `GET /api/insurance/claims/all` - Get all claims
- `GET /api/insurance/reports` - Get reports

### 📋 Claims APIs
Handle claim creation and management.

**Key Endpoints:**
- `GET /api/insurance_claims_detail` - Get insurance codes
- `GET /api/get_policy` - Get policy numbers

---

## 🔑 Authentication Flow

1. **Register** (if new user):
```bash
POST /api/auth/signup
Body: { "name": "...", "email": "...", "username": "...", "password": "..." }
```

2. **Login**:
```bash
POST /api/auth/login
Body: { "username": "...", "password": "..." }
Response: { "token": "eyJ..." }
```

3. **Use Token** in subsequent requests:
```bash
Authorization: Bearer eyJ...
```

4. **Logout** when done:
```bash
POST /api/auth/logout
Header: Authorization: Bearer eyJ...
```

---

## 🎯 Common Use Cases

### Use Case 1: User Registration and Login

```python
import requests

# Register
response = requests.post('http://localhost:5000/api/auth/signup', json={
    'name': 'John Doe',
    'email': 'john@example.com',
    'username': 'johndoe',
    'password': 'securepass123'
})

# Login
response = requests.post('http://localhost:5000/api/auth/login', json={
    'username': 'johndoe',
    'password': 'securepass123'
})
token = response.json()['token']
```

### Use Case 2: Get Dashboard Statistics

```python
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:5000/api/dashboard/stats', headers=headers)
stats = response.json()
print(f"Total Claims: {stats['total_claims_count']}")
```

### Use Case 3: Detect Cracks in Image

```python
files = {'image': open('damage_photo.jpg', 'rb')}
response = requests.post('http://localhost:5000/api/detection/crack', files=files)
result = response.json()
print(f"Prediction: {result['predicted_class']}")
print(f"Confidence: {result['confidence']}%")
```

### Use Case 4: Get All Insurance Policies

```python
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:5000/api/insurance/policies', headers=headers)
policies = response.json()['insurance_policies']
for policy in policies:
    print(f"Policy: {policy['policy_number']} - {policy['insurance_type']}")
```

### Use Case 5: Submit Complete Claim Workflow

```python
# Step 1: Submit insurance claim
claim_data = {
    'user_id': 1,
    'claims_code': 'CLM-2024-001',
    'insurance_id': 'INS-2024-001',
    'policy_number': 'POL-123456',
    'claim_details': 'Earthquake damage',
    'time_of_loss': '2024-10-20 14:30:00'
}
response = requests.post('http://localhost:5000/submit_insurance_claims', data=claim_data)

# Step 2: Upload damage image
files = {'file_name': open('damage.jpg', 'rb')}
data = {'claims_id': 1, 'claims_code': 'CLM-2024-001'}
response = requests.post('http://localhost:5000/submit_damaged_property_image', 
                        files=files, data=data)

# Step 3: Submit property details
property_data = {
    'claims_id': 1,
    'claim_property_details_id': 1,
    'property_type': 'Residential',
    'damage_area': 150.75,
    'rate_per_sqft': 100.00
}
response = requests.post('http://localhost:5000/submit_damaged_property', data=property_data)
```

---

## 🛠️ Development Tips

### Enable Debug Mode

In `app.py`, debug mode is already enabled:
```python
app.run(host="0.0.0.0", port=5000, debug=True)
```

### Check Database Connection

Run the test script:
```bash
python test_db_connection.py
```

### View API Logs

Flask logs are printed to console. Watch for:
- Request methods and paths
- Response status codes
- Database queries
- Error messages

### Testing Error Cases

Test various error scenarios:
```bash
# Invalid credentials
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "invalid", "password": "wrong"}'

# Missing token
curl -X GET http://localhost:5000/api/dashboard/stats

# Invalid token
curl -X GET http://localhost:5000/api/dashboard/stats \
  -H "Authorization: Bearer invalid_token"
```

---

## 📊 Response Status Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Request successful |
| 302 | Redirect | Redirected (form submissions) |
| 400 | Bad Request | Invalid parameters |
| 401 | Unauthorized | Missing/invalid token |
| 403 | Forbidden | Account inactive |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Duplicate entry |
| 500 | Server Error | Internal error |

---

## 🔒 Security Notes

### In Development:
- JWT tokens expire after 60 minutes
- Passwords are hashed using bcrypt
- New users require admin approval (inactive status)

### For Production:
- ✅ Enable HTTPS
- ✅ Implement rate limiting
- ✅ Add CORS configuration
- ✅ Use environment-specific secrets
- ✅ Enable database connection pooling
- ✅ Add comprehensive logging
- ✅ Implement input validation
- ✅ Set file upload size limits

---

## 🐛 Troubleshooting

### "Database connection failed"
- Check MySQL is running
- Verify credentials in `.env`
- Test connection: `mysql -u root -p`

### "Token has expired"
- Login again to get new token
- Token lifetime: 60 minutes (default)

### "User not found"
- Verify username is correct
- Check if user exists in database

### "Account inactive"
- New accounts are inactive by default
- Admin must activate account in database

### "Image file missing"
- Ensure file field name is `image`
- Check file is selected
- Verify Content-Type is multipart/form-data

### "Module not found"
- Install dependencies: `pip install -r requirements.txt`
- Activate virtual environment

---

## 📝 Additional Resources

### Project Structure
```
earthquake-damage-assessment-tool-web/
├── app/
│   ├── models/         # AI models
│   ├── routes/         # API routes
│   │   ├── api/       # REST API endpoints
│   │   └── pages/     # Page routes
│   ├── static/        # Static files
│   └── templates/     # HTML templates
├── API_DOCUMENTATION.md
├── API_QUICK_REFERENCE.md
├── Earthquake_API_Collection.postman_collection.json
└── API_README.md (this file)
```

### Related Files
- `README.md` - Main project README
- `requirements.txt` - Python dependencies
- `app.py` - Application entry point
- `.env` - Environment configuration (create this)

---

## 🤝 Contributing

When adding new endpoints:
1. Update API_DOCUMENTATION.md with full details
2. Add endpoint to API_QUICK_REFERENCE.md
3. Add request to Postman collection
4. Update this README if needed

---

## 📞 Support

For questions or issues:
1. Check API_DOCUMENTATION.md for detailed info
2. Review troubleshooting section above
3. Check application logs for errors
4. Contact development team

---

## 📅 Version History

### Version 1.0.0 (October 24, 2025)
- Initial API documentation
- Complete endpoint coverage
- Postman collection
- Quick reference guide

---

**Happy coding! 🚀**

