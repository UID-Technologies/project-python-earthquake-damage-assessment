# Docker Deployment Guide

This guide explains how to build, run, and push the Earthquake Damage Assessment Tool Docker container.

## Prerequisites

- Docker installed on your system
- Docker Hub account (for pushing images)
- Docker Compose (optional, for local development with database)

## Quick Start

### Option 1: Using Docker Compose (Recommended for Local Development)

1. **Create environment file**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Build and run with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

3. **View logs**:
   ```bash
   docker-compose logs -f web
   ```

4. **Stop containers**:
   ```bash
   docker-compose down
   ```

### Option 2: Using Docker Directly

1. **Build the image**:
   ```bash
   docker build -t varungupta2809/earthquake-damage-assessment:latest .
   ```

2. **Run the container**:
   ```bash
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

3. **View logs**:
   ```bash
   docker logs -f earthquake-app
   ```

4. **Stop container**:
   ```bash
   docker stop earthquake-app
   docker rm earthquake-app
   ```

## Building and Pushing to Docker Hub

### Step 1: Build the Image

```bash
# Build for your platform
docker build -t varungupta2809/earthquake-damage-assessment:latest .

# Or build for multiple platforms (requires buildx)
docker buildx build --platform linux/amd64,linux/arm64 \
  -t varungupta2809/earthquake-damage-assessment:latest .
```

### Step 2: Tag the Image (Optional - for versioning)

```bash
# Tag with version number
docker tag varungupta2809/earthquake-damage-assessment:latest \
  varungupta2809/earthquake-damage-assessment:v1.0.0

# Tag with date
docker tag varungupta2809/earthquake-damage-assessment:latest \
  varungupta2809/earthquake-damage-assessment:$(date +%Y%m%d)
```

### Step 3: Login to Docker Hub

```bash
docker login
# Enter your Docker Hub username: varungupta2809
# Enter your Docker Hub password: ********
```

### Step 4: Push to Docker Hub

```bash
# Push latest tag
docker push varungupta2809/earthquake-damage-assessment:latest

# Push specific version (if tagged)
docker push varungupta2809/earthquake-damage-assessment:v1.0.0
```

### Step 5: Verify Push

Visit: https://hub.docker.com/r/varungupta2809/earthquake-damage-assessment

## Pull and Run from Docker Hub

Once pushed, anyone can pull and run your image:

```bash
# Pull the image
docker pull varungupta2809/earthquake-damage-assessment:latest

# Run the container
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

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key for sessions | `supersecretkey123` |
| `DB_USER` | Database username | `root` |
| `DB_PASSWORD` | Database password | `Bp32#12345` |
| `DB_HOST` | Database host | `localhost` |
| `DB_PORT` | Database port | `3306` |
| `DB_NAME` | Database name | `earthquake_db` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiry time | `60` |

## Image Optimization Features

This Dockerfile is optimized for size and security:

- ✅ Uses Python 3.11 slim base image
- ✅ PyTorch CPU-only version (reduces size by ~2GB)
- ✅ OpenCV headless version (no GUI dependencies)
- ✅ Multi-layer caching for faster builds
- ✅ Removes build dependencies after installation
- ✅ Runs as non-root user for security
- ✅ Health check included
- ✅ Production-ready with Gunicorn
- ✅ Proper signal handling

### Key Dependencies Included

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | Latest | Web framework |
| PyTorch | CPU-only | AI model inference |
| OpenCV | Headless | Image processing & crack detection |
| Gunicorn | Latest | WSGI HTTP server |
| MySQL | Client | Database connection |

## Image Size

Expected image size: **~1.5-2GB** (compared to ~4-5GB with full PyTorch)

Check your image size:
```bash
docker images varungupta2809/earthquake-damage-assessment:latest
```

## Troubleshooting

### Container won't start
```bash
# Check logs
docker logs earthquake-app

# Check if port is already in use
netstat -ano | findstr :5000  # Windows
lsof -i :5000                  # Linux/Mac
```

### Database connection issues
```bash
# Verify database is accessible
docker exec -it earthquake-app ping db

# Check environment variables
docker exec -it earthquake-app env | grep DB_
```

### Permission issues with uploads
```bash
# Fix permissions on upload directory
docker exec -it earthquake-app ls -la /app/app/static/upload_image
```

### Rebuild without cache
```bash
docker build --no-cache -t varungupta2809/earthquake-damage-assessment:latest .
```

## Production Deployment

For production deployment, consider:

1. **Use proper secrets management** (not environment variables)
2. **Set up reverse proxy** (Nginx/Traefik)
3. **Enable HTTPS** with SSL certificates
4. **Configure proper logging** and monitoring
5. **Set resource limits**:
   ```bash
   docker run -d \
     --memory="2g" \
     --cpus="2" \
     --name earthquake-app \
     varungupta2809/earthquake-damage-assessment:latest
   ```
6. **Use Docker Swarm or Kubernetes** for orchestration
7. **Implement health checks** and auto-restart policies

## Useful Commands

```bash
# View container stats
docker stats earthquake-app

# Execute commands inside container
docker exec -it earthquake-app /bin/bash

# View container resource usage
docker container inspect earthquake-app

# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune -a
```

## CI/CD Integration

Example GitHub Actions workflow snippet:

```yaml
- name: Build and Push Docker image
  uses: docker/build-push-action@v4
  with:
    context: .
    push: true
    tags: varungupta2809/earthquake-damage-assessment:latest
```

## Support

For issues or questions, please open an issue on the GitHub repository.

