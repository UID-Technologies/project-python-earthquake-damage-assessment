# Troubleshooting: Insurance Policies Not Showing

## Common Issues and Solutions

### Issue 1: Wrong User ID in Database ⚠️
**Most Common Problem!**

The insurance records were inserted with `user_id = 1`, but your logged-in user might have a different ID.

#### Solution:

**Step 1: Find Your Actual User ID**
```sql
-- Run this query to see all users
SELECT id, username, name, email FROM users;
```

**Step 2: Check What User Is Logged In**
1. Open browser console (F12)
2. Go to Application/Storage → Local Storage
3. Look for the `token` value
4. Or run this in console:
```javascript
console.log('Token:', localStorage.getItem('token'));
```

**Step 3: Update the Insurance Records**

Option A: Update existing records to match your user_id
```sql
-- First, find your user_id (replace 'your_username' with actual username)
SELECT id FROM users WHERE username = 'your_username';

-- Let's say your user_id is 5, update the records:
UPDATE insurance 
SET user_id = 5, created_by = 5
WHERE insurance_code IN ('INS-EQ-2024-001', 'INS-FL-2024-002', 'INS-COMP-2024-003');
```

Option B: Delete and re-insert with correct user_id
```sql
-- Delete test records
DELETE FROM insurance 
WHERE insurance_code IN ('INS-EQ-2024-001', 'INS-FL-2024-002', 'INS-COMP-2024-003');

-- Find your user_id
SELECT @user_id := id FROM users WHERE username = 'your_username' LIMIT 1;

-- Re-insert with correct user_id
INSERT INTO insurance (user_id, insurance_code, policy_number, insurance_from, insurance_to, insurance_type, insured, occupation, insurance_details, is_active, status, created_by)
VALUES 
(@user_id, 'INS-EQ-2024-001', 'POL-45678-2024', '2024-01-01 00:00:00', '2025-12-31 23:59:00', 'earthquake', 'John Michael Anderson', 'Software Engineer', 'Premium earthquake coverage.', 1, 'active', @user_id),
(@user_id, 'INS-FL-2024-002', 'POL-98765-2024', '2024-03-15 08:00:00', '2026-03-14 23:59:00', 'flood', 'Sarah Elizabeth Thompson', 'Medical Doctor', 'Comprehensive flood insurance.', 1, 'active', @user_id),
(@user_id, 'INS-COMP-2024-003', 'POL-11223-2024', '2024-06-01 00:00:00', '2025-05-31 23:59:00', 'comprehensive', 'Robert James Wilson', 'Business Owner', 'All-risk comprehensive coverage.', 1, 'active', @user_id);
```

---

### Issue 2: Authentication Problem 🔐

#### Check if JWT Token is Valid

**Browser Console Test:**
```javascript
// Test the API endpoint
const token = localStorage.getItem('token');
fetch('/api/insurance/policies', {
  headers: {
    'Authorization': 'Bearer ' + token
  }
})
.then(res => res.json())
.then(data => console.log('API Response:', data))
.catch(err => console.error('Error:', err));
```

**Expected Response:**
```json
{
  "success": true,
  "user_id": 1,
  "insurance_policies": [...]
}
```

**If you get an error:**
- Token might be expired → Log out and log in again
- Token might be invalid → Clear localStorage and log in again

```javascript
// Clear token and reload
localStorage.clear();
window.location.href = '/login';
```

---

### Issue 3: Database Query Issue 🔍

#### Verify Data Exists in Database
```sql
-- Check if records exist
SELECT * FROM insurance 
WHERE insurance_code IN ('INS-EQ-2024-001', 'INS-FL-2024-002', 'INS-COMP-2024-003');

-- Check which user_id the records belong to
SELECT user_id, insurance_code, policy_number, insured, status 
FROM insurance 
WHERE insurance_code IN ('INS-EQ-2024-001', 'INS-FL-2024-002', 'INS-COMP-2024-003');

-- Check what user_id your logged-in user has
SELECT id, username FROM users;
```

---

### Issue 4: API Not Returning Data 📡

#### Debug the API Response

Add this temporary debugging to the insurance list page (already in the HTML):

1. Open browser console (F12)
2. Refresh the insurance policies page
3. Look for console errors
4. Check Network tab for the `/api/insurance/policies` request

**What to look for:**
- 401 Unauthorized → Token issue, log in again
- 404 Not Found → User not found in database
- 500 Server Error → Check Flask console logs
- Empty array `[]` → Data exists but user_id mismatch

---

### Issue 5: Browser Cache 🔄

Sometimes the browser caches the old page.

**Solutions:**
1. Hard refresh: `Ctrl + Shift + R` (Windows/Linux) or `Cmd + Shift + R` (Mac)
2. Clear browser cache
3. Open in incognito/private window

---

## Quick Fix Commands (Copy & Paste)

### Option 1: If you know your username
```sql
-- Replace 'your_username' with your actual username
SET @my_user_id = (SELECT id FROM users WHERE username = 'your_username' LIMIT 1);

-- Update existing test records
UPDATE insurance 
SET user_id = @my_user_id, created_by = @my_user_id
WHERE insurance_code IN ('INS-EQ-2024-001', 'INS-FL-2024-002', 'INS-COMP-2024-003');

-- Verify
SELECT user_id, insurance_code, policy_number, insured 
FROM insurance 
WHERE user_id = @my_user_id;
```

### Option 2: If you want to use user_id = 1
```sql
-- Make sure user with id=1 exists
SELECT * FROM users WHERE id = 1;

-- If not, find the first user
SELECT * FROM users ORDER BY id LIMIT 1;

-- Use that user's ID for the insurance records
```

---

## Complete Debugging Checklist

### Step-by-Step Debugging:

1. **Verify you're logged in**
   - Check if you can access the dashboard
   - Check browser console for authentication errors

2. **Check your user_id**
   ```sql
   SELECT id, username FROM users;
   ```

3. **Check insurance records**
   ```sql
   SELECT user_id, insurance_code, policy_number FROM insurance;
   ```

4. **Do the user_ids match?**
   - If NO → Update insurance records with correct user_id
   - If YES → Check API response in browser console

5. **Test API directly**
   - Open browser console
   - Run the fetch test (provided above)
   - Check response

6. **Check browser console for errors**
   - Press F12
   - Go to Console tab
   - Look for red error messages

7. **Check Network requests**
   - Press F12
   - Go to Network tab
   - Refresh page
   - Look for `/api/insurance/policies` request
   - Check if it returns data

---

## Most Likely Solution (90% of cases)

```sql
-- 1. Find your username from the login page or dashboard
-- 2. Run this (replace 'your_actual_username'):

UPDATE insurance 
SET user_id = (SELECT id FROM users WHERE username = 'your_actual_username' LIMIT 1),
    created_by = (SELECT id FROM users WHERE username = 'your_actual_username' LIMIT 1)
WHERE insurance_code IN ('INS-EQ-2024-001', 'INS-FL-2024-002', 'INS-COMP-2024-003');

-- 3. Refresh the insurance policies page
-- 4. You should now see the 3 policies!
```

---

## Alternative: Add Data Through The Form

If SQL debugging is too complex, just use the form:

1. Go to: `/insurance_form` or click "Add Insurance Policy"
2. Fill in the form with test data from `TEST_DATA_INSURANCE.md`
3. Submit
4. It will automatically use the correct user_id from your login session!

---

## Still Not Working?

### Check Flask Application Logs

Look at the terminal where Flask is running for any error messages.

### Enable Debug Mode

In `app.py` or `wsgi.py`, check if debug mode is enabled:
```python
app.run(debug=True)
```

### Check Database Connection

```sql
-- Test database connection
SELECT 'Database connection OK' as status;

-- Check if insurance table exists
SHOW TABLES LIKE 'insurance';

-- Check insurance table structure
DESCRIBE insurance;
```

---

## Success Indicators

You'll know it's working when:
1. ✅ No console errors in browser (F12)
2. ✅ Statistics cards show count > 0
3. ✅ Table displays your insurance policies
4. ✅ Policy count badge shows "3 Policies"

---

## Need More Help?

If none of these solutions work, provide:
1. Your username from the database
2. Result of: `SELECT id, username FROM users;`
3. Result of: `SELECT user_id, insurance_code FROM insurance;`
4. Browser console errors (F12 → Console)
5. Flask application error logs

