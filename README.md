# Earthquake Damage Assessment Tool - Web Application

A Flask-based web application that uses AI to assess earthquake damage from building images, process insurance claims, and generate comprehensive damage reports.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Folder Structure](#folder-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Usage](#usage)
- [Testing](#testing)
- [Security](#security)
- [Deployment](#deployment)

---

## 🎯 Overview

This application combines AI-powered crack detection with insurance claim management to streamline the earthquake damage assessment process. Users can upload images of damaged properties, receive AI-based damage assessments, calculate repair costs, and generate insurance claim reports.

### Key Capabilities
- **AI Crack Detection**: MobileNetV3-based binary classifier for crack identification
- **Image Analysis**: OpenCV-based crack measurement and area calculation
- **Insurance Management**: Complete workflow from policy creation to claim submission
- **Report Generation**: Automated damage assessment reports with AI recommendations
- **User Authentication**: JWT-based secure authentication with role management

---

## ✨ Features

### 🔐 Authentication & Authorization
- User registration with admin approval workflow
- JWT token-based authentication
- Password hashing with Bcrypt
- Token blocklist for logout management
- Protected routes with role-based access

### 🏠 Insurance Management
- Create and manage insurance policies
- Submit insurance claims with detailed information
- Track claim status and history
- Policy number and code management

### 🖼️ Damage Assessment
- Upload property damage images
- AI-powered crack detection with confidence scores
- Automatic crack measurement (length, width, area)
- Visual comparison with detected crack overlay
- Multiple image support per claim

### 📊 Reporting & Analytics
- User dashboard with statistics
- Damage calculation based on area and rates
- AI recommendation vs user inference comparison
- Comprehensive claim reports
- Export-ready data format

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 3.1.3
- **Database**: MySQL 8.0 (AWS RDS)
- **Authentication**: Flask-JWT-Extended, Flask-Bcrypt
- **WSGI Server**: Gunicorn

### AI & Machine Learning
- **Deep Learning**: PyTorch
- **Model**: MobileNetV3 Large (lightweight, efficient)
- **Image Processing**: OpenCV (cv2), Pillow
- **Model Library**: timm (PyTorch Image Models)

### Frontend
- **Templates**: Jinja2
- **JavaScript**: Vanilla JS with Fetch API
- **CSS**: Custom responsive design
- **Icons**: Font Awesome

### Development Tools
- **Environment**: Python 3.11+
- **Virtual Environment**: venv
- **Package Manager**: pip
- **Environment Variables**: python-dotenv

---

## 🏗️ Architecture

### Application Structure

The application follows a **modular blueprint architecture** with clear separation between API endpoints and page routes:

```
┌─────────────────────────────────────────────────────────┐
│                     Flask Application                    │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────┐         ┌──────────────────┐     │
│  │   API Routes     │         │   Page Routes    │     │
│  │   (JSON)         │         │   (HTML)         │     │
│  ├──────────────────┤         ├──────────────────┤     │
│  │ • Auth API       │         │ • Auth Pages     │     │
│  │ • Dashboard API  │         │ • Dashboard View │     │
│  │ • Detection API  │         │ • Insurance Forms│     │
│  │ • Insurance API  │         │                  │     │
│  └──────────────────┘         └──────────────────┘     │
│           │                            │                 │
│           └────────────┬───────────────┘                │
│                        │                                 │
│              ┌─────────▼─────────┐                      │
│              │   Core Services   │                      │
│              ├───────────────────┤                      │
│              │ • Database (MySQL)│                      │
│              │ • AI Model (PyTorch)│                    │
│              │ • Image Processing│                      │
│              │ • JWT Manager     │                      │
│              └───────────────────┘                      │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### Request Flow

#### 1. Authentication Flow
```
User → Login Page → API (/api/auth/login) → JWT Token → localStorage → Protected Routes
```

#### 2. Insurance Claim Flow
```
User → Insurance Form → API → Dashboard → 
Upload Image → AI Detection + Area Calculation → 
Damage Details → Report Generation → Submission
```

#### 3. AI Detection Pipeline
```
Image Upload → Preprocessing → MobileNetV3 Model → 
Confidence Score → Crack/No Crack Classification → 
OpenCV Analysis → Area Calculation → Visual Overlay → 
Database Storage → Report Display
```

---

## 📁 Folder Structure

```
earthquake-damage-assessment-tool-web/
│
├── app/                                    # Main application package
│   ├── __init__.py                        # App factory, blueprint registration
│   ├── config.py                          # Configuration management
│   ├── db.py                              # Database connection helper
│   ├── blocklist.py                       # JWT token blocklist
│   │
│   ├── models/                            # AI Models
│   │   ├── __init__.py
│   │   ├── crack_classifier.py           # MobileNetV3 crack detection model
│   │   └── models/
│   │       └── best_model.pth            # Trained model weights
│   │
│   ├── routes/                            # Application routes
│   │   ├── __init__.py
│   │   │
│   │   ├── api/                          # API Endpoints (JSON responses)
│   │   │   ├── __init__.py
│   │   │   ├── auth_api.py              # Authentication APIs
│   │   │   ├── dashboard_api.py         # Dashboard data APIs
│   │   │   ├── detection_api.py         # AI crack detection API
│   │   │   └── insurance_api.py         # Insurance & claims APIs
│   │   │
│   │   ├── pages/                        # Page Routes (HTML responses)
│   │   │   ├── __init__.py
│   │   │   ├── auth_pages.py            # Login/signup pages
│   │   │   ├── dashboard_pages.py       # Dashboard view
│   │   │   └── insurance_pages.py       # Insurance forms & pages
│   │   │
│   │   ├── earthquake_detection.py       # Detection helper functions
│   │   └── image_area_calculater.py      # Image processing utilities
│   │
│   ├── static/                           # Static assets
│   │   ├── css/                         # Stylesheets
│   │   │   ├── login.css
│   │   │   ├── dashboard.css
│   │   │   ├── sidebar.css
│   │   │   ├── insurance_form.css
│   │   │   └── ...
│   │   ├── js/                          # JavaScript files
│   │   │   ├── auth_check.js           # Token verification
│   │   │   ├── login.js                # Login handler
│   │   │   ├── signup.js               # Signup handler
│   │   │   └── logout.js               # Logout handler
│   │   ├── images/                      # Images & assets
│   │   │   └── logo.png
│   │   └── upload_image/                # User uploaded images
│   │
│   └── templates/                        # Jinja2 HTML templates
│       ├── base.html                    # Base template
│       ├── header.html                  # Header component
│       ├── footer.html                  # Footer component
│       ├── sidebar.html                 # Sidebar navigation
│       ├── login.html
│       ├── signup.html
│       ├── dashboard.html
│       ├── insurance_form.html
│       ├── insurance_claims_detail.html
│       ├── damaged_property_image.html
│       ├── damaged_property_details.html
│       ├── new_report.html
│       └── report.html
│
├── venv/                                 # Virtual environment (not in git)
│
├── app.py                                # Application entry point
├── wsgi.py                               # WSGI configuration for production
├── requirements.txt                      # Python dependencies
├── .env                                  # Environment variables (not in git)
├── .gitignore                            # Git ignore rules
├── verify_structure.py                   # Application structure verification
├── test_db_connection.py                 # Database connection tester
└── README.md                             # This file
```

---

## 🚀 Installation

### Prerequisites
- Python 3.11+
- MySQL 8.0+ (or access to AWS RDS)
- pip package manager
- Virtual environment support

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd earthquake-damage-assessment-tool-web
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment**
   - **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```
   - **Linux/Mac**:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Environment Variables**
   Create a `.env` file in the root directory:
   ```env
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   DB_PORT=3306
   DB_NAME=your_db_name
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ```

6. **Test Database Connection**
   ```bash
   python test_db_connection.py
   ```

7. **Run the Application**
   ```bash
   python app.py
   ```

8. **Access the Application**
   Open browser and navigate to: `http://localhost:5000`

---

## 🐳 Docker Deployment

### Quick Start with Docker

#### Option 1: Using Docker Compose (Recommended)

1. **Build and run with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

2. **Access the application**:
   Open browser and navigate to: `http://localhost:5000`

#### Option 2: Build and Push to Docker Hub

**For Windows:**
```bash
.\build-and-push.bat latest
```

**For Linux/Mac:**
```bash
chmod +x build-and-push.sh
./build-and-push.sh latest
```

#### Option 3: Pull from Docker Hub

```bash
docker pull varungupta2809/earthquake-damage-assessment:latest

docker run -d \
  --name earthquake-app \
  -p 5000:5000 \
  -e SECRET_KEY=your-secret-key \
  -e DB_HOST=your-db-host \
  -e DB_USER=root \
  -e DB_PASSWORD=your-password \
  -e DB_NAME=earthquake_db \
  varungupta2809/earthquake-damage-assessment:latest
```

### Docker Image Features

- ✅ **Lightweight**: ~1.5-2GB (PyTorch CPU-only)
- ✅ **Security**: Runs as non-root user
- ✅ **Production Ready**: Uses Gunicorn with 4 workers
- ✅ **Health Checks**: Built-in health monitoring
- ✅ **Optimized**: Multi-layer caching for faster builds

📖 **Detailed Docker Guide**: See [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for complete instructions.

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DB_HOST` | Database host address | localhost | Yes |
| `DB_USER` | Database username | root | Yes |
| `DB_PASSWORD` | Database password | - | Yes |
| `DB_NAME` | Database name | earthquake_db | Yes |
| `DB_PORT` | Database port | 3306 | No |
| `SECRET_KEY` | JWT secret key | supersecretkey123 | Yes |
| `ALGORITHM` | JWT algorithm | HS256 | No |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry time | 60 | No |

### Database Configuration

**Current Setup**: AWS RDS (Production)
```
Region: Asia Pacific (Mumbai - ap-south-1)
MySQL Version: 8.0.43
SSL: Supported
```

### AI Model Configuration

**Model**: MobileNetV3 Large
```python
CONFIG = {
    'img_size': 224,
    'num_classes': 2,
    'dropout': 0.2
}
```

**Classes**:
- 0: Negative (No Crack)
- 1: Positive (Crack Detected)

---

## 📡 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Authentication APIs

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "password123"
}

Response:
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Signup
```http
POST /api/auth/signup
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "mobile": "+1234567890",
  "address": "123 Main St",
  "username": "john_doe",
  "password": "password123"
}

Response:
{
  "success": true,
  "message": "User registered successfully"
}
```

#### Logout
```http
POST /api/auth/logout
Authorization: Bearer <token>

Response:
{
  "success": true,
  "message": "Successfully logged out"
}
```

#### Verify Token
```http
GET /api/auth/verify
Authorization: Bearer <token>

Response:
{
  "success": true,
  "logged_in_as": "john_doe"
}
```

### Dashboard API

#### Get Statistics
```http
GET /api/dashboard/stats
Authorization: Bearer <token>

Response:
{
  "success": true,
  "total_insurance_count": 5,
  "total_claims_count": 3,
  "total_picture_tests": 8,
  "total_claim_you_get": 15000.50,
  "total_policy_number": 5,
  "name": "John Doe",
  "email": "john@example.com",
  "mobile": "+1234567890",
  "address": "123 Main St"
}
```

### Detection API

#### Detect Crack
```http
POST /api/detection/crack
Content-Type: multipart/form-data

image: [binary file]

Response:
{
  "success": true,
  "predicted_class": "Positive (Crack Detected)",
  "confidence": 95.67,
  "probabilities": {
    "Negative (No Crack)": 4.33,
    "Positive (Crack Detected)": 95.67
  }
}
```

### Insurance APIs

#### Get Policies
```http
GET /api/insurance/policies
Authorization: Bearer <token>

Response:
{
  "success": true,
  "user_id": 1,
  "insurance_policies": [
    {
      "insurance_code": "INS001",
      "policy_number": "POL123456"
    }
  ]
}
```

#### Get Policy Numbers
```http
GET /api/insurance/policy-numbers?insurance_code=INS001

Response:
{
  "success": true,
  "policy_numbers": ["POL123456", "POL789012"]
}
```

#### Get Claims
```http
GET /api/insurance/claims?policy_number=POL123456

Response:
{
  "success": true,
  "claims_codes": ["CLM001", "CLM002"]
}
```

#### Get Assessment Data
```http
GET /api/insurance/assessment?claims_code=CLM001

Response:
{
  "success": true,
  "data": {
    "file_name": "crack_image.jpg",
    "ai_decision": "Positive (Crack Detected)",
    "confidence": 95.67,
    "crack_percent": 95.67,
    "damage_area": 25.5,
    "damage_length": 5.2,
    "damage_breadth": 4.9,
    "claim_recommended": 2550.00,
    "cpa_id": 1
  }
}
```

#### Get Reports
```http
GET /api/insurance/reports
Authorization: Bearer <token>

Response:
{
  "success": true,
  "reports": [
    {
      "name": "John Doe",
      "email": "john@example.com",
      "insurance_code": "INS001",
      "insurance_type": "Property",
      "policy_number": "POL123456",
      "claims_code": "CLM001",
      "property_type": "Residential",
      "wall_type": "Brick",
      "damage_area": 25.5,
      "rate_per_sqft": 100,
      "confidence": 95.67,
      "crack_percent": 95.67,
      "ai_decision": "Positive (Crack Detected)",
      "file_name": "crack_image.jpg"
    }
  ]
}
```

---

## 🗄️ Database Schema

### Tables Overview

#### users
Stores user account information
```sql
- id (PK)
- name
- email
- mobile
- address
- username (unique)
- password (hashed)
- role (user/admin)
- organization_id
- status (active/inactive)
- created_at
- updated_at
```

#### insurance
Insurance policy records
```sql
- id (PK)
- user_id (FK)
- insurance_code
- policy_number
- insurance_from
- insurance_to
- insurance_type
- insured
- occupation
- insurance_details
- is_active
- status
- created_by
- created_at
```

#### claims
Insurance claim submissions
```sql
- id (PK)
- user_id (FK)
- claims_code
- insurance_id
- policy_number
- claim_details
- time_of_loss
- situation_of_loss
- cause_of_loss
- is_active
- status
- created_by
- created_at
```

#### claim_property_details
Property damage specifications
```sql
- id (PK)
- claims_id (FK)
- property_type
- wall_type
- damage_area
- damage_length
- damage_breadth
- damage_height
- rate_per_sqft
- is_active
- status
```

#### claim_property_image
Uploaded damage images
```sql
- id (PK)
- claim_property_details_id (FK)
- file_name
- file_location
- file_format
- file_desc
- is_active
- status
```

#### claim_property_assessment
AI assessment results
```sql
- id (PK)
- claims_id (FK)
- confidence
- crack_percent
- non_crack_percent
- ai_decision
- user_inference
- final_damage_area
- final_damage_cost
```

#### claims_value
Claim amount calculations
```sql
- id (PK)
- claims_id (FK)
- claim_recommended
```

---

## 💻 Usage

### User Workflow

#### 1. Registration & Login
1. Navigate to signup page
2. Fill registration form
3. Wait for admin approval (status: inactive → active)
4. Login with credentials
5. JWT token stored in localStorage

#### 2. Create Insurance Policy
1. Navigate to "Add Insurance"
2. Fill insurance details:
   - Insurance code
   - Policy number
   - Coverage period
   - Type and insured details
3. Submit insurance form

#### 3. Submit Claim
1. Navigate to "Add Claim"
2. Select insurance code and policy
3. Fill claim details:
   - Time of loss
   - Situation and cause
4. Proceed to image upload

#### 4. Upload Damage Images
1. Upload property damage image
2. System automatically:
   - Runs AI crack detection
   - Calculates crack area
   - Measures dimensions
   - Generates visual overlay
3. Review AI assessment results

#### 5. Enter Damage Details
1. Confirm or adjust damage area
2. Enter property details:
   - Property type
   - Wall type
   - Rate per square foot
3. System calculates claim amount

#### 6. Generate Report
1. Review AI decision and confidence
2. Add user inference (if different)
3. Enter final damage assessment
4. Submit claim report

#### 7. View Reports
1. Navigate to "Report"
2. View all submitted claims
3. Review assessment details
4. Export data if needed

---

## 🧪 Testing

### Automated Tests

#### Verify Application Structure
```bash
python verify_structure.py
```

Checks:
- File structure integrity
- Blueprint registration
- Route registration
- API structure

#### Test Database Connection
```bash
python test_db_connection.py
```

Verifies:
- Database connectivity
- MySQL version
- Required tables existence

### Manual Testing Checklist

#### Authentication
- [ ] User can register
- [ ] User can login
- [ ] JWT token is generated
- [ ] Protected routes require token
- [ ] User can logout
- [ ] Token verification works

#### Insurance Management
- [ ] Can create insurance policy
- [ ] Can view insurance list
- [ ] Dropdowns populate correctly

#### Claim Workflow
- [ ] Can create new claim
- [ ] Can upload images
- [ ] AI detection runs successfully
- [ ] Image analysis completes
- [ ] Can enter damage details
- [ ] Can generate report

#### Dashboard
- [ ] Statistics display correctly
- [ ] User information shows
- [ ] Navigation works

#### Reports
- [ ] Reports list displays
- [ ] Data is accurate
- [ ] Images load correctly

---

## 🔒 Security

### Implemented Security Measures

#### Authentication & Authorization
- ✅ JWT token-based authentication
- ✅ Password hashing with Bcrypt
- ✅ Token blocklist for revoked tokens
- ✅ Token expiration (60 minutes)
- ✅ Protected routes with `@jwt_required()`

#### Data Protection
- ✅ Environment variables for sensitive data
- ✅ `.env` file excluded from git
- ✅ SQL injection protection (parameterized queries)
- ✅ CORS considerations

#### User Management
- ✅ Admin approval workflow
- ✅ Account status management (active/inactive)
- ✅ Role-based access control

### Security Recommendations

#### Critical (Implement Immediately)
1. **Change Default Secret Key**
   - Current: `supersecretkey123`
   - Action: Generate strong random key

2. **Enable HTTPS**
   - Use SSL/TLS in production
   - Force HTTPS redirects

3. **Implement Rate Limiting**
   ```bash
   pip install Flask-Limiter
   ```

4. **Add Input Validation**
   - Validate file uploads (type, size)
   - Sanitize user inputs
   - Implement file size limits

#### Important
1. **Enable Database SSL**
   - AWS RDS supports SSL
   - Update connection to use SSL

2. **Add CORS Protection**
   ```bash
   pip install flask-cors
   ```

3. **Implement CSP Headers**
   - Prevent XSS attacks
   - Content Security Policy

4. **Add Request Logging**
   - Monitor suspicious activity
   - Log authentication attempts

#### Recommended
1. **Two-Factor Authentication**
2. **Password Strength Requirements**
3. **Session Management**
4. **API Rate Limiting per User**
5. **Automated Security Scanning**

---

## 🚢 Deployment

### Production Deployment with Gunicorn

1. **Install Gunicorn** (already in requirements.txt)
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
   ```

3. **With Environment Variables**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 --env-file .env wsgi:app
   ```

### Docker Deployment

**Dockerfile** (create this):
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]
```

**Build and Run**:
```bash
docker build -t earthquake-assessment .
docker run -p 5000:5000 --env-file .env earthquake-assessment
```

### AWS Deployment Options

#### Option 1: AWS EC2
1. Launch EC2 instance (Ubuntu/Amazon Linux)
2. Install Python and dependencies
3. Configure security groups (port 5000)
4. Use systemd for process management
5. Setup Nginx as reverse proxy

#### Option 2: AWS Elastic Beanstalk
1. Create Elastic Beanstalk application
2. Configure environment variables
3. Deploy using EB CLI or web console
4. Auto-scaling enabled

#### Option 3: AWS ECS (Docker)
1. Push Docker image to ECR
2. Create ECS cluster
3. Define task definition
4. Deploy service with load balancer

### Environment-Specific Configuration

**Development**:
```python
DEBUG = True
```

**Production**:
```python
DEBUG = False
TESTING = False
```

---

## 📊 Performance Considerations

### Database Optimization
- Implement connection pooling
- Add database indexes
- Cache frequently accessed data
- Consider SQLAlchemy ORM

### AI Model Optimization
- Model is loaded once at startup
- Uses CPU or GPU (if available)
- Inference on single images < 1 second
- Consider model quantization for faster inference

### Image Processing
- Optimize image resize operations
- Implement async processing for large files
- Consider image compression

### API Performance
- Implement request caching
- Use CDN for static assets
- Enable gzip compression
- Monitor slow queries

---

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

### Code Style
- Follow PEP 8 for Python
- Use meaningful variable names
- Add docstrings to functions
- Comment complex logic

### Commit Messages
```
feat: Add new feature
fix: Fix bug
docs: Update documentation
style: Format code
refactor: Refactor code
test: Add tests
```

---

## 📝 License

[Add your license information here]

---

## 👥 Authors

[Add author information here]

---

## 📞 Support

For issues and questions:
- GitHub Issues: [Repository Issues URL]
- Email: [Support Email]
- Documentation: This README

---

## 🗺️ Roadmap

### Version 1.1 (Planned)
- [ ] API versioning (/api/v1/)
- [ ] Swagger/OpenAPI documentation
- [ ] Rate limiting implementation
- [ ] Enhanced error handling

### Version 1.2 (Planned)
- [ ] Multi-language support
- [ ] Email notifications
- [ ] PDF report generation
- [ ] Advanced analytics dashboard

### Version 2.0 (Future)
- [ ] Mobile app (React Native)
- [ ] Real-time notifications
- [ ] Video damage assessment
- [ ] Advanced AI models

---

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [PyTorch Documentation](https://pytorch.org/docs/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [JWT Best Practices](https://jwt.io/)
- [AWS RDS Documentation](https://docs.aws.amazon.com/rds/)

---

**Last Updated**: October 22, 2025  
**Version**: 1.0  
**Status**: Production Ready ✅
