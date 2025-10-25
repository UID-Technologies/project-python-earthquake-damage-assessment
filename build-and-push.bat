@echo off
REM Build and Push Script for Earthquake Damage Assessment Tool (Windows)
REM Usage: build-and-push.bat [version]

setlocal enabledelayedexpansion

set DOCKER_USERNAME=varungupta2809
set IMAGE_NAME=earthquake-damage-assessment
set VERSION=%1
if "%VERSION%"=="" set VERSION=latest

echo 🔨 Building Docker image...
docker build -t %DOCKER_USERNAME%/%IMAGE_NAME%:%VERSION% .

if errorlevel 1 (
    echo ❌ Build failed!
    exit /b 1
)

if not "%VERSION%"=="latest" (
    echo 🏷️  Tagging as latest...
    docker tag %DOCKER_USERNAME%/%IMAGE_NAME%:%VERSION% %DOCKER_USERNAME%/%IMAGE_NAME%:latest
)

echo.
echo 📊 Image size:
docker images %DOCKER_USERNAME%/%IMAGE_NAME%:%VERSION%

echo.
set /p PUSH="🚀 Push to Docker Hub? (Y/N): "

if /i "%PUSH%"=="Y" (
    echo 🔐 Logging in to Docker Hub...
    docker login
    
    if errorlevel 1 (
        echo ❌ Login failed!
        exit /b 1
    )
    
    echo 📤 Pushing %DOCKER_USERNAME%/%IMAGE_NAME%:%VERSION%...
    docker push %DOCKER_USERNAME%/%IMAGE_NAME%:%VERSION%
    
    if not "%VERSION%"=="latest" (
        echo 📤 Pushing %DOCKER_USERNAME%/%IMAGE_NAME%:latest...
        docker push %DOCKER_USERNAME%/%IMAGE_NAME%:latest
    )
    
    echo.
    echo ✅ Successfully pushed to Docker Hub!
    echo 🔗 View at: https://hub.docker.com/r/%DOCKER_USERNAME%/%IMAGE_NAME%
) else (
    echo ⏭️  Skipping push to Docker Hub
)

echo.
echo 🎉 Done! You can now run:
echo    docker run -d -p 5000:5000 %DOCKER_USERNAME%/%IMAGE_NAME%:%VERSION%

endlocal

