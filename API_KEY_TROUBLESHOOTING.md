# OpenAI API Key Troubleshooting Guide

## Error: 401 - Invalid API Key

If you're getting a 401 error with "Incorrect API key provided", follow these steps:

### Step 1: Verify Your API Key

1. **Go to OpenAI Platform:**
   - Visit: https://platform.openai.com/account/api-keys
   - Log in to your OpenAI account

2. **Check Your API Keys:**
   - Look for active API keys
   - Make sure the key starts with `sk-`
   - Check if the key has been revoked or expired

### Step 2: Get a New API Key

If your key is invalid or missing:

1. **Create a New Key:**
   - Click "Create new secret key"
   - Give it a name (e.g., "Earthquake Damage Assessment")
   - **IMPORTANT:** Copy the key immediately - you won't see it again!

2. **Copy the Complete Key:**
   - The key should be very long (100+ characters)
   - It starts with `sk-` or `sk-proj-`
   - Make sure you copy the ENTIRE key, no spaces before or after

### Step 3: Update Your .env File

1. **Open the `.env` file** in your project root directory

2. **Find this line:**
   ```
   OPENAI_API_KEY=sk-proj-...
   ```

3. **Replace with your new key:**
   ```
   OPENAI_API_KEY=your-new-complete-api-key-here
   ```

4. **Important:**
   - No spaces around the `=` sign
   - No quotes needed
   - No line breaks in the key
   - Save the file

### Step 4: Restart Your Application

After updating the `.env` file:

1. **Stop your Flask application** (Ctrl+C if running)

2. **Restart it:**
   ```bash
   python app.py
   ```

3. **Test again** by uploading an image

## Common Issues

### Issue 1: Key Format Looks Correct But Still Fails

**Possible Causes:**
- Key was revoked by OpenAI
- Key belongs to a different account
- Key doesn't have required permissions
- Key has expired

**Solution:** Create a new API key

### Issue 2: Key Has Extra Spaces

**Symptom:** Key looks correct but still fails

**Solution:** 
- Open `.env` file
- Remove any spaces before or after the key
- Make sure it's exactly: `OPENAI_API_KEY=sk-...` (no spaces)

### Issue 3: Key Not Being Read

**Symptom:** Error says "API key not configured"

**Solution:**
1. Check that `.env` file exists in project root
2. Check that the line is exactly: `OPENAI_API_KEY=...`
3. Restart the Flask application
4. Make sure you're using `python-dotenv` (already in requirements.txt)

### Issue 4: Wrong Model Name

**Symptom:** Error about model not found

**Solution:**
- Check your `.env` file for `OPENAI_MODEL`
- Valid models:
  - `gpt-4o` (latest, recommended)
  - `gpt-4-vision-preview` (legacy)
  - `gpt-4-turbo` (if available)

## Verification Steps

### Test Your API Key

Run this Python script to verify:

```python
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY", "").strip()

if not api_key:
    print("ERROR: API key not found in .env")
else:
    print(f"Key found: {api_key[:20]}...")
    try:
        client = OpenAI(api_key=api_key)
        print("SUCCESS: API key format is correct")
        print("Note: Full validation requires an actual API call")
    except Exception as e:
        print(f"ERROR: {e}")
```

## Still Having Issues?

1. **Double-check the key:**
   - Go to https://platform.openai.com/account/api-keys
   - Create a fresh key
   - Copy it completely
   - Paste it into `.env` file

2. **Check your OpenAI account:**
   - Make sure you have credits/balance
   - Check if there are any restrictions on your account
   - Verify billing is set up

3. **Check the error message:**
   - The improved error handling will now show more specific messages
   - Look for clues in the error text

4. **Try a simple test:**
   - Use OpenAI's API directly to test the key
   - Visit: https://platform.openai.com/playground

## Security Reminder

⚠️ **Never commit your `.env` file to git!**

- The `.env` file is already in `.gitignore`
- Never share your API key publicly
- If you accidentally committed it, revoke the key immediately and create a new one

---

**Last Updated:** 2024
**Need Help?** Check OpenAI documentation: https://platform.openai.com/docs

