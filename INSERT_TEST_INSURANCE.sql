-- ====================================================================
-- MySQL INSERT Commands for Test Insurance Data
-- ====================================================================
-- 
-- IMPORTANT: Replace 'YOUR_USER_ID' with the actual user_id from your users table
-- You can find your user_id by running: SELECT id FROM users WHERE username = 'your_username';
--
-- ====================================================================

-- Test Set 1: Earthquake Insurance - Active Policy
INSERT INTO insurance (
    user_id, 
    insurance_code, 
    policy_number,
    insurance_from, 
    insurance_to, 
    insurance_type, 
    insured, 
    occupation, 
    insurance_details, 
    is_active, 
    status, 
    created_by
) VALUES (
    1, -- Replace with your actual user_id
    'INS-EQ-2024-001',
    'POL-45678-2024',
    '2024-01-01 00:00:00',
    '2025-12-31 23:59:00',
    'earthquake',
    'John Michael Anderson',
    'Software Engineer',
    'Premium earthquake coverage for residential property in California. Includes structural damage, contents coverage up to $500,000, and temporary housing assistance. Annual premium: $2,400.',
    1,
    'active',
    1 -- Replace with your actual user_id
);

-- Test Set 2: Flood Insurance - Active Policy
INSERT INTO insurance (
    user_id, 
    insurance_code, 
    policy_number,
    insurance_from, 
    insurance_to, 
    insurance_type, 
    insured, 
    occupation, 
    insurance_details, 
    is_active, 
    status, 
    created_by
) VALUES (
    1, -- Replace with your actual user_id
    'INS-FL-2024-002',
    'POL-98765-2024',
    '2024-03-15 08:00:00',
    '2026-03-14 23:59:00',
    'flood',
    'Sarah Elizabeth Thompson',
    'Medical Doctor',
    'Comprehensive flood insurance for coastal property. Coverage includes building and contents up to $750,000. Replacement cost coverage with no depreciation. Premium: $3,200/year.',
    1,
    'active',
    1 -- Replace with your actual user_id
);

-- Test Set 3: Comprehensive Insurance - Active
INSERT INTO insurance (
    user_id, 
    insurance_code, 
    policy_number,
    insurance_from, 
    insurance_to, 
    insurance_type, 
    insured, 
    occupation, 
    insurance_details, 
    is_active, 
    status, 
    created_by
) VALUES (
    1, -- Replace with your actual user_id
    'INS-COMP-2024-003',
    'POL-11223-2024',
    '2024-06-01 00:00:00',
    '2025-05-31 23:59:00',
    'comprehensive',
    'Robert James Wilson',
    'Business Owner',
    'All-risk comprehensive coverage for commercial building. Includes earthquake, flood, fire, and liability. Total coverage: $2,000,000. Monthly premium: $850.',
    1,
    'active',
    1 -- Replace with your actual user_id
);

-- ====================================================================
-- VERIFICATION QUERIES
-- ====================================================================

-- Check if the records were inserted successfully
SELECT 
    id,
    insurance_code,
    policy_number,
    insurance_type,
    insured,
    status,
    created_at
FROM insurance
WHERE insurance_code IN ('INS-EQ-2024-001', 'INS-FL-2024-002', 'INS-COMP-2024-003')
ORDER BY created_at DESC;

-- ====================================================================
-- ALTERNATIVE: INSERT WITH VARIABLE (if you want to use a variable)
-- ====================================================================

-- First, get your user_id
-- SELECT @user_id := id FROM users WHERE username = 'your_username' LIMIT 1;

-- Then use the variable in inserts:
/*
SET @user_id = 1; -- Replace with actual user_id or use SELECT above

INSERT INTO insurance (user_id, insurance_code, policy_number, insurance_from, insurance_to, insurance_type, insured, occupation, insurance_details, is_active, status, created_by)
VALUES 
(@user_id, 'INS-EQ-2024-001', 'POL-45678-2024', '2024-01-01 00:00:00', '2025-12-31 23:59:00', 'earthquake', 'John Michael Anderson', 'Software Engineer', 'Premium earthquake coverage for residential property in California. Includes structural damage, contents coverage up to $500,000, and temporary housing assistance. Annual premium: $2,400.', 1, 'active', @user_id),
(@user_id, 'INS-FL-2024-002', 'POL-98765-2024', '2024-03-15 08:00:00', '2026-03-14 23:59:00', 'flood', 'Sarah Elizabeth Thompson', 'Medical Doctor', 'Comprehensive flood insurance for coastal property. Coverage includes building and contents up to $750,000. Replacement cost coverage with no depreciation. Premium: $3,200/year.', 1, 'active', @user_id),
(@user_id, 'INS-COMP-2024-003', 'POL-11223-2024', '2024-06-01 00:00:00', '2025-05-31 23:59:00', 'comprehensive', 'Robert James Wilson', 'Business Owner', 'All-risk comprehensive coverage for commercial building. Includes earthquake, flood, fire, and liability. Total coverage: $2,000,000. Monthly premium: $850.', 1, 'active', @user_id);
*/

-- ====================================================================
-- HELPFUL QUERIES
-- ====================================================================

-- Get your user_id
-- SELECT id, username, name, email FROM users;

-- Count insurance policies
-- SELECT COUNT(*) as total_policies FROM insurance WHERE user_id = 1;

-- View all insurance policies for a user
-- SELECT * FROM insurance WHERE user_id = 1 ORDER BY created_at DESC;

-- Delete test data (if needed)
-- DELETE FROM insurance WHERE insurance_code IN ('INS-EQ-2024-001', 'INS-FL-2024-002', 'INS-COMP-2024-003');

-- ====================================================================
-- NOTES:
-- ====================================================================
-- 1. The insurance_type values in the database should match what the form dropdown sends:
--    - 'earthquake' (not 'Earthquake Insurance')
--    - 'flood' (not 'Flood Insurance') 
--    - 'comprehensive' (not 'Comprehensive')
--
-- 2. Date format: 'YYYY-MM-DD HH:MM:SS' is standard MySQL datetime format
--
-- 3. The 'is_active' field is set to 1 (true) for active policies
--
-- 4. The 'status' field should be 'active' or 'inactive' (lowercase)
--
-- 5. The 'created_by' field typically contains the user_id of who created the record
--
-- 6. The 'created_at' field will be auto-populated if it has DEFAULT CURRENT_TIMESTAMP
-- ====================================================================

