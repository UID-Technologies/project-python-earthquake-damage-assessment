# 🔧 Container Rebuild Instructions

## Issue Summary

Your Docker container failed to start with **2 missing Python packages**:
1. ❌ `opencv-python-headless` (cv2)
2. ❌ `matplotlib`

Both have now been added to `requirements.txt`.

---

## ✅ All Fixes Applied

| Fix | Status |
|-----|--------|
| Added opencv-python-headless | ✅ Complete |
| Added matplotlib | ✅ Complete |
| Added numpy | ✅ Complete |
| Added OpenCV system libraries to Dockerfile | ✅ Complete |
| Fixed docker-compose.yml version warning | ✅ Complete |
| Verified all dependencies | ✅ Complete |

---

## 🚀 Quick Rebuild (Choose One Method)

### Method 1: Docker Compose (Recommended) ⭐

```bash
# Stop and remove everything
docker-compose down

# Rebuild from scratch
docker-compose build --no-cache

# Start containers
docker-compose up -d

# Watch logs to verify success
docker-compose logs -f web
```

### Method 2: Windows Build Script

```bash
# Clean up old container
docker stop earthquake-app 2>$null
docker rm earthquake-app 2>$null
docker rmi varungupta2809/earthquake-damage-assessment:latest 2>$null

# Rebuild
.\build-and-push.bat latest
```

### Method 3: Manual Docker Build

```bash
# Clean up
docker stop earthquake-app
docker rm earthquake-app
docker rmi varungupta2809/earthquake-damage-assessment:latest

# Rebuild (important: use --no-cache)
docker build --no-cache -t varungupta2809/earthquake-damage-assessment:latest .

# Run
docker run -d \
  --name earthquake-app \
  -p 5000:5000 \
  -e DB_HOST=your-db-host \
  -e DB_USER=root \
  -e DB_PASSWORD=your-password \
  -e DB_NAME=earthquake_db \
  varungupta2809/earthquake-damage-assessment:latest
```

---

## ✅ Expected Success Output

After rebuild, logs should show:

```
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:5000 (1)
[INFO] Using worker: gthread
[INFO] Booting worker with pid: 7
[INFO] Booting worker with pid: 8
[INFO] Booting worker with pid: 9
[INFO] Booting worker with pid: 10
```

**NO ModuleNotFoundError** should appear! ✅

---

## 🧪 Verify It's Working

```bash
# 1. Check container is running
docker ps

# 2. Check health status
docker inspect earthquake-app --format='{{.State.Health.Status}}'

# 3. Test the endpoint
curl http://localhost:5000/

# 4. Open in browser
# Navigate to: http://localhost:5000
```

---

## 📦 Complete Dependency List

Your `requirements.txt` now includes:

```txt
Flask                      # Web framework
requests                   # HTTP client
gunicorn                   # WSGI server
pymysql                    # MySQL database
python-dotenv              # Environment variables
Werkzeug                   # WSGI utilities
Flask-JWT-Extended         # JWT authentication
flask-bcrypt               # Password hashing
torch                      # PyTorch (CPU-only)
torchvision                # PyTorch vision
timm                       # Timm models
pillow                     # Image processing
opencv-python-headless     # OpenCV (no GUI) ✨ NEW
numpy                      # NumPy arrays ✨ NEW
matplotlib                 # Plotting ✨ NEW
```

---

## 🐛 If It Still Fails

### 1. Check for NEW errors in logs:
```bash
docker logs earthquake-app
```

### 2. Verify requirements.txt has all packages:
```bash
python verify_dependencies.py
```

### 3. Ensure clean rebuild:
```bash
# Remove ALL Docker build cache
docker builder prune -a -f

# Rebuild
docker-compose build --no-cache
```

### 4. Check system resources:
```bash
# Ensure enough disk space
docker system df

# Clean if needed
docker system prune -a
```

---

## 📊 Build Statistics

| Metric | Value |
|--------|-------|
| Expected build time (first) | 5-10 minutes |
| Expected build time (cached) | 1-2 minutes |
| Final image size | ~1.7-2.2 GB |
| Dependencies installed | 15 packages |
| System libraries added | 6 packages |

---

## 🎯 Post-Deployment

Once container is running successfully:

1. ✅ Test all API endpoints
2. ✅ Upload a test image for crack detection
3. ✅ Verify database connectivity
4. ✅ Push to Docker Hub (if ready):
   ```bash
   docker push varungupta2809/earthquake-damage-assessment:latest
   ```

---

## 📚 Additional Resources

- **Full Docker Guide**: [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)
- **Quick Start**: [QUICK_START_DOCKER.md](QUICK_START_DOCKER.md)
- **Fix Details**: [DOCKER_FIXES.md](DOCKER_FIXES.md)
- **Dependency Verification**: `python verify_dependencies.py`

---

## 💡 Pro Tips

1. **Always use `--no-cache`** for the first rebuild after dependency changes
2. **Watch logs in real-time** during startup: `docker logs -f earthquake-app`
3. **Use Docker Compose** for local dev - it's easier!
4. **Verify dependencies** before building: `python verify_dependencies.py`
5. **Tag your builds** with versions: `v1.0.0`, `v1.0.1`, etc.

---

**Status**: ✅ Ready to rebuild  
**Last Updated**: October 25, 2025  
**All dependencies**: VERIFIED ✅

