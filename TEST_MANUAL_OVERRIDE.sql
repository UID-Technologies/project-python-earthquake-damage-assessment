-- =====================================================
-- TEST MANUAL OVERRIDE FEATURE
-- SQL Queries to verify manual override functionality
-- =====================================================

-- Replace with your actual claims code
SET @test_claims_code = 'CLM-20241025-001';

-- =====================================================
-- 1. VIEW ALL OVERRIDES FOR A CLAIM
-- =====================================================

SELECT 
    cpio.id AS override_id,
    c.claims_code,
    cpio.image_index,
    cpio.image_filename,
    cpio.ai_decision,
    cpio.confidence,
    cpio.length_ft,
    cpio.width_ft,
    cpio.area_sqft,
    cpio.claim_recommended,
    cpio.crack_detected,
    cpio.created_at,
    cpio.updated_at,
    TIMESTAMPDIFF(SECOND, cpio.created_at, cpio.updated_at) AS seconds_to_update
FROM claim_property_image_override cpio
JOIN claims c ON cpio.claims_id = c.id
WHERE c.claims_code = @test_claims_code
ORDER BY cpio.image_index;

-- =====================================================
-- 2. COUNT OVERRIDES PER CLAIM
-- =====================================================

SELECT 
    c.claims_code,
    c.status,
    COUNT(cpio.id) AS total_overrides,
    SUM(CASE WHEN cpio.crack_detected = 1 THEN 1 ELSE 0 END) AS cracks_detected,
    SUM(CASE WHEN cpio.crack_detected = 0 THEN 1 ELSE 0 END) AS no_cracks,
    SUM(cpio.claim_recommended) AS total_override_amount
FROM claims c
LEFT JOIN claim_property_image_override cpio ON c.id = cpio.claims_id
WHERE c.claims_code = @test_claims_code
GROUP BY c.claims_code, c.status;

-- =====================================================
-- 3. COMPARE: Number of Images vs Overrides
-- =====================================================

SELECT 
    c.claims_code,
    COUNT(DISTINCT cpi.id) AS total_images_uploaded,
    COUNT(DISTINCT cpio.id) AS total_overrides,
    (COUNT(DISTINCT cpi.id) - COUNT(DISTINCT cpio.id)) AS images_without_override
FROM claims c
LEFT JOIN claim_property_details cpd ON c.id = cpd.claims_id
LEFT JOIN claim_property_image cpi ON cpd.id = cpi.claim_property_details_id
LEFT JOIN claim_property_image_override cpio ON c.id = cpio.claims_id
WHERE c.claims_code = @test_claims_code
GROUP BY c.claims_code;

-- =====================================================
-- 4. DETAILED OVERRIDE REPORT
-- =====================================================

SELECT 
    cpio.image_index + 1 AS 'Image #',
    cpio.image_filename AS 'Filename',
    cpio.ai_decision AS 'Decision',
    CONCAT(cpio.confidence, '%') AS 'Confidence',
    CONCAT(cpio.length_ft, ' ft') AS 'Length',
    CONCAT(cpio.width_ft, ' ft') AS 'Breadth',
    CONCAT(cpio.area_sqft, ' sq ft') AS 'Area',
    CONCAT('$', FORMAT(cpio.claim_recommended, 2)) AS 'Claim Amount',
    CASE 
        WHEN cpio.crack_detected = 1 THEN '✓ Yes'
        ELSE '✗ No'
    END AS 'Crack?',
    DATE_FORMAT(cpio.created_at, '%Y-%m-%d %H:%i:%s') AS 'Created',
    DATE_FORMAT(cpio.updated_at, '%Y-%m-%d %H:%i:%s') AS 'Last Modified'
FROM claim_property_image_override cpio
JOIN claims c ON cpio.claims_id = c.id
WHERE c.claims_code = @test_claims_code
ORDER BY cpio.image_index;

-- =====================================================
-- 5. FIND RECENTLY MODIFIED OVERRIDES (Last 24 Hours)
-- =====================================================

SELECT 
    c.claims_code,
    cpio.image_index,
    cpio.image_filename,
    cpio.ai_decision,
    cpio.updated_at,
    TIMESTAMPDIFF(MINUTE, cpio.updated_at, NOW()) AS minutes_ago
FROM claim_property_image_override cpio
JOIN claims c ON cpio.claims_id = c.id
WHERE cpio.updated_at >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
ORDER BY cpio.updated_at DESC;

-- =====================================================
-- 6. OVERRIDES WITH HIGH CLAIM AMOUNTS (> $5,000)
-- =====================================================

SELECT 
    c.claims_code,
    cpio.image_index,
    cpio.image_filename,
    cpio.ai_decision,
    cpio.area_sqft,
    cpio.claim_recommended,
    cpio.crack_detected
FROM claim_property_image_override cpio
JOIN claims c ON cpio.claims_id = c.id
WHERE cpio.claim_recommended > 5000
ORDER BY cpio.claim_recommended DESC;

-- =====================================================
-- 7. STATISTICS BY DECISION TYPE
-- =====================================================

SELECT 
    cpio.ai_decision,
    COUNT(*) AS total_count,
    AVG(cpio.confidence) AS avg_confidence,
    AVG(cpio.area_sqft) AS avg_area,
    SUM(cpio.claim_recommended) AS total_claim_amount,
    MIN(cpio.claim_recommended) AS min_claim,
    MAX(cpio.claim_recommended) AS max_claim
FROM claim_property_image_override cpio
GROUP BY cpio.ai_decision;

-- =====================================================
-- 8. FIND OVERRIDES WITH LOW CONFIDENCE (< 70%)
-- =====================================================

SELECT 
    c.claims_code,
    cpio.image_index,
    cpio.image_filename,
    cpio.ai_decision,
    cpio.confidence,
    cpio.claim_recommended
FROM claim_property_image_override cpio
JOIN claims c ON cpio.claims_id = c.id
WHERE cpio.confidence < 70
ORDER BY cpio.confidence ASC;

-- =====================================================
-- 9. CHECK IF TABLE EXISTS AND STRUCTURE
-- =====================================================

-- Check if table exists
SHOW TABLES LIKE 'claim_property_image_override';

-- View table structure
DESCRIBE claim_property_image_override;

-- View indexes
SHOW INDEXES FROM claim_property_image_override;

-- Count total records
SELECT COUNT(*) AS total_overrides FROM claim_property_image_override;

-- =====================================================
-- 10. USER'S OVERRIDE ACTIVITY
-- =====================================================

SELECT 
    u.username,
    u.name,
    COUNT(DISTINCT c.id) AS claims_with_overrides,
    COUNT(cpio.id) AS total_overrides,
    AVG(cpio.confidence) AS avg_confidence,
    SUM(cpio.claim_recommended) AS total_override_amounts
FROM users u
JOIN claims c ON u.id = c.user_id
JOIN claim_property_image_override cpio ON c.id = cpio.claims_id
GROUP BY u.username, u.name
ORDER BY total_overrides DESC;

-- =====================================================
-- 11. CLAIMS WITHOUT ANY OVERRIDES
-- =====================================================

SELECT 
    c.claims_code,
    c.status,
    c.created_at,
    COUNT(DISTINCT cpi.id) AS total_images
FROM claims c
LEFT JOIN claim_property_details cpd ON c.id = cpd.claims_id
LEFT JOIN claim_property_image cpi ON cpd.id = cpi.claim_property_details_id
LEFT JOIN claim_property_image_override cpio ON c.id = cpio.claims_id
WHERE cpio.id IS NULL
  AND cpi.id IS NOT NULL  -- Has images but no overrides
GROUP BY c.claims_code, c.status, c.created_at
ORDER BY c.created_at DESC;

-- =====================================================
-- 12. AUDIT TRAIL: Modified Overrides
-- =====================================================

-- Overrides that have been modified (updated_at > created_at)
SELECT 
    c.claims_code,
    cpio.image_index,
    cpio.image_filename,
    cpio.ai_decision,
    cpio.created_at AS original_time,
    cpio.updated_at AS modified_time,
    TIMESTAMPDIFF(MINUTE, cpio.created_at, cpio.updated_at) AS minutes_between_changes,
    CASE 
        WHEN cpio.updated_at > cpio.created_at THEN '✓ Modified'
        ELSE 'Original'
    END AS modification_status
FROM claim_property_image_override cpio
JOIN claims c ON cpio.claims_id = c.id
WHERE cpio.updated_at > cpio.created_at
ORDER BY cpio.updated_at DESC;

-- =====================================================
-- 13. DELETE TEST OVERRIDES (USE WITH CAUTION!)
-- =====================================================

-- ⚠️ WARNING: This will delete override data
-- Uncomment only if you want to remove test overrides

/*
-- Delete overrides for a specific claim
DELETE FROM claim_property_image_override 
WHERE claims_id = (SELECT id FROM claims WHERE claims_code = 'CLM-20241025-001');

-- Verify deletion
SELECT COUNT(*) AS remaining_overrides 
FROM claim_property_image_override
WHERE claims_id = (SELECT id FROM claims WHERE claims_code = 'CLM-20241025-001');
*/

-- =====================================================
-- 14. INSERT SAMPLE TEST DATA (Optional)
-- =====================================================

/*
-- Insert sample override data for testing
SET @test_claim_id = (SELECT id FROM claims WHERE claims_code = @test_claims_code);

INSERT INTO claim_property_image_override 
(claims_id, image_index, image_filename, ai_decision, confidence, 
 length_ft, width_ft, area_sqft, claim_recommended, crack_detected)
VALUES 
(@test_claim_id, 0, 'test_damage1.jpg', 'Positive (Crack Detected)', 95.67, 5.20, 4.90, 25.48, 8918.00, 1),
(@test_claim_id, 1, 'test_damage2.jpg', 'Negative (No Crack)', 87.34, 0.00, 0.00, 0.00, 0.00, 0),
(@test_claim_id, 2, 'test_damage3.jpg', 'Positive (Crack Detected)', 92.15, 6.50, 5.80, 37.70, 13195.00, 1);

-- Verify insertion
SELECT * FROM claim_property_image_override 
WHERE claims_id = @test_claim_id;
*/

-- =====================================================
-- 15. EXPORT DATA FOR REPORTING
-- =====================================================

-- Complete export of all override data with claim details
SELECT 
    u.username AS 'User',
    c.claims_code AS 'Claim Code',
    c.insurance_id AS 'Insurance',
    cpio.image_index + 1 AS 'Image Number',
    cpio.image_filename AS 'Filename',
    cpio.ai_decision AS 'AI Decision',
    CONCAT(ROUND(cpio.confidence, 2), '%') AS 'Confidence',
    CONCAT(ROUND(cpio.length_ft, 2), ' ft') AS 'Length',
    CONCAT(ROUND(cpio.width_ft, 2), ' ft') AS 'Breadth',
    CONCAT(ROUND(cpio.area_sqft, 2), ' sq ft') AS 'Area',
    CONCAT('$', FORMAT(cpio.claim_recommended, 2)) AS 'Claim Amount',
    IF(cpio.crack_detected, 'Yes', 'No') AS 'Crack Detected',
    DATE_FORMAT(cpio.created_at, '%Y-%m-%d %H:%i') AS 'Created Date',
    DATE_FORMAT(cpio.updated_at, '%Y-%m-%d %H:%i') AS 'Last Modified'
FROM claim_property_image_override cpio
JOIN claims c ON cpio.claims_id = c.id
JOIN users u ON c.user_id = u.id
ORDER BY c.claims_code, cpio.image_index;

-- =====================================================
-- END OF QUERIES
-- =====================================================

