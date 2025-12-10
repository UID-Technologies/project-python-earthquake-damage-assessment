-- =====================================================
-- SQL QUERIES TO TEST FINAL CLAIM SUBMISSION
-- =====================================================

-- Replace 'YOUR_CLAIMS_CODE' with the actual claims code from your test
SET @test_claims_code = 'CLM-20241025-001';

-- =====================================================
-- 1. VERIFY CLAIM WAS CREATED (Step 1)
-- =====================================================

SELECT 
    id AS claims_id,
    user_id,
    claims_code,
    insurance_id,
    policy_number,
    claim_details,
    time_of_loss,
    situation_of_loss,
    cause_of_loss,
    status,  -- Should be 'active' after final submission
    created_at
FROM claims 
WHERE claims_code = @test_claims_code;

-- =====================================================
-- 2. VERIFY PROPERTY DETAILS SAVED (Step 3)
-- =====================================================

SELECT 
    cpd.id AS property_details_id,
    cpd.claims_id,
    cpd.property_type,
    cpd.wall_type,
    cpd.damage_area,
    cpd.damage_length,
    cpd.damage_breadth,
    cpd.damage_height,
    cpd.rate_per_sqft,
    cpd.is_active,
    cpd.status,
    cpd.created_at
FROM claim_property_details cpd
JOIN claims c ON cpd.claims_id = c.id
WHERE c.claims_code = @test_claims_code;

-- =====================================================
-- 3. VERIFY IMAGES UPLOADED (Step 2)
-- =====================================================

SELECT 
    cpi.id AS image_id,
    cpi.claim_property_details_id,
    cpi.file_name,
    cpi.file_format,
    cpi.file_desc,
    cpi.created_at
FROM claim_property_image cpi
JOIN claim_property_details cpd ON cpi.claim_property_details_id = cpd.id
JOIN claims c ON cpd.claims_id = c.id
WHERE c.claims_code = @test_claims_code
ORDER BY cpi.created_at;

-- =====================================================
-- 4. VERIFY AI ANALYSIS SAVED (Step 4)
-- =====================================================

SELECT 
    cpa.id AS assessment_id,
    cpa.claims_id,
    cpa.confidence,
    cpa.crack_percent,
    cpa.non_crack_percent,
    cpa.ai_decision,
    cpa.created_at
FROM claim_property_assessment cpa
JOIN claims c ON cpa.claims_id = c.id
WHERE c.claims_code = @test_claims_code;

-- =====================================================
-- 5. VERIFY CLAIM VALUE CALCULATED (Step 5)
-- =====================================================

SELECT 
    cv.id AS value_id,
    cv.claims_id,
    cv.claims_code,
    cv.claim_recommended,
    cv.created_at,
    -- Show calculation
    cpd.damage_area,
    cpd.rate_per_sqft,
    (cpd.damage_area * cpd.rate_per_sqft) AS expected_value
FROM claims_value cv
JOIN claims c ON cv.claims_id = c.id
JOIN claim_property_details cpd ON cpd.claims_id = c.id
WHERE cv.claims_code = @test_claims_code;

-- =====================================================
-- 6. COMPLETE CLAIM SUMMARY
-- =====================================================

SELECT 
    c.claims_code,
    c.status AS claim_status,
    c.insurance_id,
    c.policy_number,
    c.time_of_loss,
    cpd.property_type,
    cpd.wall_type,
    cpd.damage_area,
    cpd.rate_per_sqft,
    cv.claim_recommended,
    cpa.confidence AS ai_confidence,
    cpa.ai_decision,
    COUNT(DISTINCT cpi.id) AS total_images_uploaded,
    c.created_at AS claim_created,
    cv.created_at AS claim_submitted
FROM claims c
LEFT JOIN claim_property_details cpd ON cpd.claims_id = c.id
LEFT JOIN claims_value cv ON cv.claims_id = c.id
LEFT JOIN claim_property_assessment cpa ON cpa.claims_id = c.id
LEFT JOIN claim_property_image cpi ON cpi.claim_property_details_id = cpd.id
WHERE c.claims_code = @test_claims_code
GROUP BY c.id;

-- =====================================================
-- 7. CHECK FOR MISSING DATA (Troubleshooting)
-- =====================================================

-- Claims that have no property details
SELECT c.claims_code, 'Missing property details' AS issue
FROM claims c
LEFT JOIN claim_property_details cpd ON cpd.claims_id = c.id
WHERE c.claims_code = @test_claims_code AND cpd.id IS NULL

UNION ALL

-- Claims that have no images
SELECT c.claims_code, 'Missing images' AS issue
FROM claims c
LEFT JOIN claim_property_details cpd ON cpd.claims_id = c.id
LEFT JOIN claim_property_image cpi ON cpi.claim_property_details_id = cpd.id
WHERE c.claims_code = @test_claims_code AND cpi.id IS NULL

UNION ALL

-- Claims that have no assessment
SELECT c.claims_code, 'Missing AI assessment' AS issue
FROM claims c
LEFT JOIN claim_property_assessment cpa ON cpa.claims_id = c.id
WHERE c.claims_code = @test_claims_code AND cpa.id IS NULL

UNION ALL

-- Claims that have no value
SELECT c.claims_code, 'Missing claim value' AS issue
FROM claims c
LEFT JOIN claims_value cv ON cv.claims_id = c.id
WHERE c.claims_code = @test_claims_code AND cv.id IS NULL;

-- =====================================================
-- 8. CHECK STATUS TRANSITION
-- =====================================================

-- Claim should have status 'active' after submission
-- If status is still 'inactive', submission didn't complete
SELECT 
    claims_code,
    status,
    CASE 
        WHEN status = 'active' THEN '✅ Submission completed'
        WHEN status = 'inactive' THEN '❌ Submission not completed'
        ELSE '⚠️ Unknown status'
    END AS submission_status
FROM claims
WHERE claims_code = @test_claims_code;

-- =====================================================
-- 9. LIST ALL CLAIMS FOR USER
-- =====================================================

-- Get all claims for a specific user (replace user_id)
SET @test_user_id = 1;

SELECT 
    c.id,
    c.claims_code,
    c.status,
    c.insurance_id,
    c.policy_number,
    cv.claim_recommended,
    cpa.ai_decision,
    COUNT(DISTINCT cpi.id) AS image_count,
    c.created_at
FROM claims c
LEFT JOIN claim_property_details cpd ON cpd.claims_id = c.id
LEFT JOIN claims_value cv ON cv.claims_id = c.id
LEFT JOIN claim_property_assessment cpa ON cpa.claims_id = c.id
LEFT JOIN claim_property_image cpi ON cpi.claim_property_details_id = cpd.id
WHERE c.user_id = @test_user_id
GROUP BY c.id
ORDER BY c.created_at DESC;

-- =====================================================
-- 10. CLEANUP TEST DATA (USE WITH CAUTION!)
-- =====================================================

-- ⚠️ WARNING: This will delete the test claim and all related data
-- Uncomment and run only if you want to remove test data

/*
SET @cleanup_claims_code = 'CLM-20241025-001';

-- Get the claims_id first
SET @cleanup_claims_id = (SELECT id FROM claims WHERE claims_code = @cleanup_claims_code);
SET @cleanup_property_id = (SELECT id FROM claim_property_details WHERE claims_id = @cleanup_claims_id);

-- Delete in reverse order (respect foreign keys)
DELETE FROM claims_value WHERE claims_id = @cleanup_claims_id;
DELETE FROM claim_property_assessment WHERE claims_id = @cleanup_claims_id;
DELETE FROM claim_property_image WHERE claim_property_details_id = @cleanup_property_id;
DELETE FROM claim_property_details WHERE claims_id = @cleanup_claims_id;
DELETE FROM claims WHERE id = @cleanup_claims_id;

-- Verify deletion
SELECT 'Cleanup complete' AS status;
*/

-- =====================================================
-- 11. PERFORMANCE CHECK
-- =====================================================

-- Check how long submissions are taking
SELECT 
    DATE(cv.created_at) AS submission_date,
    COUNT(*) AS total_submissions,
    AVG(TIMESTAMPDIFF(SECOND, c.created_at, cv.created_at)) AS avg_completion_time_seconds,
    MIN(TIMESTAMPDIFF(SECOND, c.created_at, cv.created_at)) AS fastest_time_seconds,
    MAX(TIMESTAMPDIFF(SECOND, c.created_at, cv.created_at)) AS slowest_time_seconds
FROM claims c
JOIN claims_value cv ON cv.claims_id = c.id
GROUP BY DATE(cv.created_at)
ORDER BY submission_date DESC;

-- =====================================================
-- 12. DATA INTEGRITY CHECK
-- =====================================================

-- Verify claim_recommended calculation is correct
SELECT 
    c.claims_code,
    cpd.damage_area,
    cpd.rate_per_sqft,
    cv.claim_recommended AS saved_value,
    (cpd.damage_area * cpd.rate_per_sqft) AS calculated_value,
    CASE 
        WHEN ABS(cv.claim_recommended - (cpd.damage_area * cpd.rate_per_sqft)) < 0.01 
        THEN '✅ Correct'
        ELSE '❌ Mismatch'
    END AS validation_status
FROM claims c
JOIN claim_property_details cpd ON cpd.claims_id = c.id
JOIN claims_value cv ON cv.claims_id = c.id
WHERE c.claims_code = @test_claims_code;

-- =====================================================
-- END OF TESTING QUERIES
-- =====================================================

