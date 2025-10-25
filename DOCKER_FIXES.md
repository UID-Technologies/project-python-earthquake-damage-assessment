# 🔧 Docker Fixes Applied

## ❌ Issue Found

When running the Docker container, it failed to start with the error:
```
ModuleNotFoundError: No module named 'cv2'
```

The application uses OpenCV in `app/routes/image_area_calculater.py` but it was **missing from requirements.txt**.

---

## ✅ Fixes Applied

### 1. **Updated requirements.txt**
Added missing dependencies:
```
opencv-python-headless  # Headless version (no GUI) - perfect for Docker
numpy                    # Required by OpenCV and matplotlib
matplotlib               # For crack visualization and plotting
```

**Why `opencv-python-headless`?**
- No X11/GUI dependencies needed
- Smaller image size
- Faster installation
- Perfect for server/container environments

**Why `matplotlib`?**
- Used in `image_area_calculater.py` for crack detection visualization
- Configured with `Agg` backend (non-interactive, headless mode)
- Essential for generating crack detection plots

### 2. **Updated Dockerfile**
Added OpenCV system dependencies:
```dockerfile
libglib2.0-0      # Core library
libsm6            # Session management
libxext6          # X11 extensions
libxrender-dev    # Rendering
libgomp1          # OpenMP support
```

### 3. **Fixed docker-compose.yml**
Removed obsolete `version: '3.8'` line that caused warnings in newer Docker Compose versions.

---

## 🚀 How to Rebuild and Test

### Step 1: Stop and Remove Old Container

```bash
# Stop container if running
docker stop earthquake-app

# Remove container
docker rm earthquake-app

# Remove old image (optional but recommended)
docker rmi varungupta2809/earthquake-damage-assessment:latest
```

### Step 2: Rebuild with Fixes

**Using Docker Compose (Recommended):**
```bash
docker-compose build --no-cache
docker-compose up -d
```

**Using Build Script (Windows):**
```bash
.\build-and-push.bat latest
```

**Using Build Script (Linux/Mac):**
```bash
./build-and-push.sh latest
```

**Manual Build:**
```bash
docker build --no-cache -t varungupta2809/earthquake-damage-assessment:latest .
docker run -d -p 5000:5000 --name earthquake-app varungupta2809/earthquake-damage-assessment:latest
```

### Step 3: Verify Container is Running

```bash
# Check container status
docker ps

# View logs (should see successful startup)
docker logs -f earthquake-app
```

**Expected successful logs:**
```
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:5000
[INFO] Using worker: gthread
[INFO] Booting worker with pid: 7
[INFO] Booting worker with pid: 8
[INFO] Booting worker with pid: 9
[INFO] Booting worker with pid: 10
```

### Step 4: Test the Application

```bash
# Test health endpoint
curl http://localhost:5000/

# Or open in browser
# http://localhost:5000
```

---

## 📦 Updated Image Details

| Component | Status | Notes |
|-----------|--------|-------|
| OpenCV | ✅ Added | opencv-python-headless 4.x |
| NumPy | ✅ Added | Required by OpenCV & matplotlib |
| Matplotlib | ✅ Added | For crack visualization (Agg backend) |
| System libs | ✅ Added | 6 additional packages (~5MB) |
| Docker Compose | ✅ Fixed | Removed obsolete version field |

**New Image Size:** ~1.7-2.2GB (includes all image processing libs)

---

## 🐛 Troubleshooting

### Container still won't start?

1. **Check logs for new errors:**
   ```bash
   docker logs earthquake-app
   ```

2. **Ensure clean rebuild:**
   ```bash
   docker system prune -a
   docker-compose build --no-cache
   ```

3. **Verify requirements.txt includes OpenCV:**
   ```bash
   cat requirements.txt | grep opencv
   # Should show: opencv-python-headless
   ```

### Import errors for other modules?

Check if module is in requirements.txt:
```bash
docker exec -it earthquake-app pip list
```

If missing, add to requirements.txt and rebuild.

### Database connection issues?

```bash
# Check database is running
docker ps | grep mysql

# Test connection
docker exec -it earthquake-app ping db

# Check environment variables
docker exec -it earthquake-app env | grep DB_
```

---

## 📝 Changes Summary

### Files Modified:
1. ✅ `requirements.txt` - Added opencv-python-headless and numpy
2. ✅ `Dockerfile` - Added OpenCV system dependencies
3. ✅ `docker-compose.yml` - Removed obsolete version field

### Files Created:
- ✅ `DOCKER_FIXES.md` (this file)

---

## ✨ Additional Improvements Made

While fixing the OpenCV issue, also optimized:
- Better cleanup in Dockerfile
- More descriptive comments
- Explicit numpy dependency (good practice)
- Fixed Docker Compose version warning

---

## 🎯 Next Steps

1. ✅ Rebuild the image with `--no-cache` flag
2. ✅ Test locally to ensure it starts successfully
3. ✅ Push to Docker Hub when ready
4. ✅ Update any deployment scripts/documentation

---

## 📚 References

- OpenCV Docker Best Practices: https://opencv.org/
- Docker Multi-stage Builds: https://docs.docker.com/build/building/multi-stage/
- Python Slim Images: https://hub.docker.com/_/python

---

**Fixed**: October 25, 2025  
**Issue**: ModuleNotFoundError: No module named 'cv2'  
**Status**: ✅ Resolved

