# OpenAI Image Analysis Setup Guide

## Overview

A new image analysis feature has been added that uses OpenAI's GPT-4 Vision API instead of the local MobileNetV3 model. This provides more detailed analysis with natural language descriptions and recommendations.

## What Was Added

### 1. New Sidebar Menu Item
- **Location:** `app/templates/sidebar.html`
- **Route:** `/analyse_image_new`
- **Icon:** Robot icon (🤖) to distinguish from the original analysis tool

### 2. New API Endpoints
- **Single Image:** `POST /api/detection/crack-openai`
- **Batch Analysis:** `POST /api/detection/batch-analyze-openai`
- **Location:** `app/routes/api/detection_api.py`

### 3. New Page Route
- **Route:** `/analyse_image_new`
- **Handler:** `insurance_pages.analyse_image_new()`
- **Location:** `app/routes/pages/insurance_pages.py`

### 4. New Template
- **File:** `app/templates/analyse_image_new.html`
- **Features:**
  - Drag & drop image upload
  - Batch image processing
  - Detailed AI analysis with descriptions
  - Recommendations from OpenAI
  - Visual result cards

### 5. Configuration Updates
- **File:** `app/config.py`
- **New Variables:**
  - `OPENAI_API_KEY` - Your OpenAI API key
  - `OPENAI_MODEL` - Model to use (default: "gpt-4-vision-preview")

### 6. Dependencies
- **File:** `requirements.txt`
- **Added:** `openai` package

## Setup Instructions

### Step 1: Install Dependencies

```bash
pip install openai
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

### Step 2: Get OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (it starts with `sk-...`)

### Step 3: Configure Environment Variables

Add to your `.env` file:

```env
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4-vision-preview
```

**Note:** For newer models, you can use:
- `gpt-4o` (latest, recommended)
- `gpt-4-vision-preview` (legacy)
- `gpt-4-turbo` (if available)

### Step 4: Restart Application

After adding the API key, restart your Flask application:

```bash
python app.py
```

## How It Works

### API Flow

1. **Image Upload:** User uploads image(s) via the web interface
2. **Base64 Encoding:** Image is converted to base64 format
3. **OpenAI API Call:** Image and prompt are sent to GPT-4 Vision
4. **Response Parsing:** JSON response is parsed for:
   - Detection result (Positive/Negative)
   - Confidence level (0-100%)
   - Detailed description
   - Recommendations
5. **Result Display:** Formatted results shown to user

### Prompt Engineering

The system uses a carefully crafted prompt that:
- Asks for crack detection analysis
- Requests structured JSON response
- Includes confidence levels
- Requests detailed descriptions
- Asks for safety recommendations

## Features

### ✅ What's Included

- **Single Image Analysis:** Analyze one image at a time
- **Batch Processing:** Analyze up to 10 images at once
- **Detailed Descriptions:** Natural language analysis of damage
- **Recommendations:** Safety and repair suggestions
- **Confidence Scores:** Percentage-based confidence levels
- **Visual Results:** Clean, organized result cards
- **Error Handling:** Graceful error messages if API fails

### 🔄 Differences from Original Analysis

| Feature | Original (MobileNetV3) | New (OpenAI) |
|---------|----------------------|--------------|
| Model | Local PyTorch model | Cloud-based GPT-4 Vision |
| Speed | Fast (local) | Slower (API call) |
| Cost | Free | Pay-per-use |
| Accuracy | Binary classification | Detailed analysis |
| Output | Crack/No Crack | Detailed description + recommendations |
| Visualization | OpenCV crack overlay | Original image only |
| Measurements | Length, width, area | Description-based |

## API Response Format

### Success Response

```json
{
  "success": true,
  "predicted_class": "Positive (Crack Detected)",
  "confidence": 85.5,
  "probabilities": {
    "Positive (Crack Detected)": 85.5,
    "Negative (No Crack)": 14.5
  },
  "crack_detected": true,
  "description": "The image shows a vertical crack running along the wall...",
  "recommendations": "Immediate structural assessment recommended...",
  "original_image_url": "/static/upload_image/openai_1234567890_image.jpg",
  "analysis_model": "OpenAI GPT-4 Vision"
}
```

### Error Response

```json
{
  "success": false,
  "error": "OpenAI API key not configured..."
}
```

## Usage

### Access the Feature

1. Log in to the application
2. Click on **"Analyse Image New"** in the sidebar (robot icon)
3. Upload one or more images
4. Click **"Analyze All Images (OpenAI)"**
5. View detailed results with descriptions and recommendations

### Best Practices

1. **Image Quality:** Use clear, well-lit images for best results
2. **Image Size:** Keep images under 20MB (OpenAI limit)
3. **Batch Size:** Process 5-10 images at a time for optimal performance
4. **API Costs:** Monitor usage on OpenAI dashboard
5. **Error Handling:** Check API key configuration if errors occur

## Troubleshooting

### Common Issues

#### 1. "OpenAI API key not configured"
- **Solution:** Add `OPENAI_API_KEY` to your `.env` file
- **Check:** Ensure the key starts with `sk-`

#### 2. "OpenAI library not installed"
- **Solution:** Run `pip install openai`

#### 3. "Rate limit exceeded"
- **Solution:** Wait a few minutes or upgrade OpenAI plan
- **Check:** Your API usage limits on OpenAI dashboard

#### 4. "Invalid API key"
- **Solution:** Verify the key is correct and active
- **Check:** Key hasn't been revoked on OpenAI platform

#### 5. "Model not found"
- **Solution:** Update `OPENAI_MODEL` in `.env` to a valid model name
- **Try:** `gpt-4o` or `gpt-4-vision-preview`

## Cost Considerations

OpenAI API pricing (as of 2024):
- **GPT-4 Vision:** ~$0.01-0.03 per image (varies by size)
- **Batch Processing:** Costs multiply by number of images
- **Free Tier:** Limited credits available for new accounts

**Tip:** Monitor usage on [OpenAI Usage Dashboard](https://platform.openai.com/usage)

## Security Notes

1. **API Key Security:**
   - Never commit API keys to git
   - Use `.env` file (already in `.gitignore`)
   - Rotate keys periodically

2. **Image Privacy:**
   - Images are sent to OpenAI servers
   - Review OpenAI's data usage policy
   - Consider enterprise plan for data privacy

3. **Rate Limiting:**
   - Consider implementing rate limiting on your endpoints
   - Monitor API usage to prevent unexpected costs

## Future Enhancements

Potential improvements:
- [ ] Caching results to reduce API calls
- [ ] Image compression before sending
- [ ] Cost tracking dashboard
- [ ] Comparison view (OpenAI vs Local model)
- [ ] Export results to PDF/CSV
- [ ] Custom prompt templates
- [ ] Multi-language support

## Support

If you encounter issues:
1. Check the error message in the browser console
2. Verify API key is correctly set
3. Check OpenAI service status
4. Review application logs

---

**Status:** ✅ Fully Functional
**Last Updated:** 2024
**Version:** 1.0

