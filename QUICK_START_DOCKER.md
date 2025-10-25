# 🐳 Docker Quick Start Guide

Get the Earthquake Damage Assessment Tool running in 3 simple steps!

---

## 🚀 Method 1: Pull and Run (Fastest)

Perfect if you just want to use the application:

```bash
# Pull the image
docker pull varungupta2809/earthquake-damage-assessment:latest

# Run the container
docker run -d \
  --name earthquake-app \
  -p 5000:5000 \
  -e DB_HOST=your-db-host \
  -e DB_USER=root \
  -e DB_PASSWORD=your-password \
  -e DB_NAME=earthquake_db \
  varungupta2809/earthquake-damage-assessment:latest

# View logs
docker logs -f earthquake-app
```

**Access**: Open http://localhost:5000 in your browser 🎉

---

## 🛠️ Method 2: Build and Run Locally

Perfect for development or customization:

### Using Docker Compose (Includes Database)

```bash
# Start everything (app + database)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down
```

### Using Docker Only

```bash
# Build the image
docker build -t varungupta2809/earthquake-damage-assessment:latest .

# Run the container
docker run -d -p 5000:5000 varungupta2809/earthquake-damage-assessment:latest
```

**Access**: Open http://localhost:5000 in your browser 🎉

---

## 📤 Method 3: Build and Push to Docker Hub

Perfect for deployment and sharing:

### Windows:
```bash
.\build-and-push.bat v1.0.0
```

### Linux/Mac:
```bash
chmod +x build-and-push.sh
./build-and-push.sh v1.0.0
```

The script will:
1. ✅ Build the Docker image
2. ✅ Show image size
3. ✅ Ask if you want to push to Docker Hub
4. ✅ Login to Docker Hub (if pushing)
5. ✅ Push the image with version tag and latest tag

---

## 🔧 Essential Commands

```bash
# View running containers
docker ps

# View logs
docker logs -f earthquake-app

# Stop container
docker stop earthquake-app

# Remove container
docker rm earthquake-app

# View image size
docker images varungupta2809/earthquake-damage-assessment

# Execute commands inside container
docker exec -it earthquake-app /bin/bash

# View container stats
docker stats earthquake-app
```

---

## 🌍 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `supersecretkey123` |
| `DB_HOST` | Database host | `localhost` |
| `DB_USER` | Database username | `root` |
| `DB_PASSWORD` | Database password | Required |
| `DB_NAME` | Database name | `earthquake_db` |
| `DB_PORT` | Database port | `3306` |

---

## 🐛 Troubleshooting

### Container won't start?
```bash
docker logs earthquake-app
```

### Port already in use?
```bash
# Windows
netstat -ano | findstr :5000

# Linux/Mac
lsof -i :5000
```

### Database connection issues?
```bash
# Make sure your database is accessible
docker exec -it earthquake-app ping your-db-host
```

### Need to rebuild?
```bash
docker build --no-cache -t varungupta2809/earthquake-damage-assessment:latest .
```

---

## 📊 Image Information

- **Base Image**: Python 3.11 Slim
- **Size**: ~1.5-2GB (optimized with CPU-only PyTorch)
- **Architecture**: linux/amd64
- **Web Server**: Gunicorn (4 workers, 2 threads each)
- **Security**: Non-root user
- **Health Check**: Built-in

---

## 🎯 Next Steps

1. **Development**: See [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for detailed info
2. **API Usage**: See [API_QUICK_REFERENCE.md](API_QUICK_REFERENCE.md)
3. **Full Documentation**: See [README.md](README.md)

---

## 💡 Pro Tips

✨ **Use Docker Compose** for local development - it includes the database!

✨ **Tag your builds** with version numbers: `./build-and-push.sh v1.0.0`

✨ **Volume mount uploads** to persist user uploads:
```bash
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/uploads:/app/app/static/upload_image \
  varungupta2809/earthquake-damage-assessment:latest
```

✨ **Resource limits** for production:
```bash
docker run -d \
  --memory="2g" \
  --cpus="2" \
  -p 5000:5000 \
  varungupta2809/earthquake-damage-assessment:latest
```

---

**Need Help?** Open an issue on GitHub or check [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for more details.

**Docker Hub**: https://hub.docker.com/r/varungupta2809/earthquake-damage-assessment

