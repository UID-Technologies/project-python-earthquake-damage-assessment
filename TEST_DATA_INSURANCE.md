# Test Data for Add Insurance Form

## Overview
Sample test data for the insurance policy form to facilitate quick testing and development.

## Form Fields Required

### Policy Information
- **Insurance Code** (required)
- **Policy Number** (required)
- **Coverage Start Date** (required)
- **Coverage End Date** (required)
- **Insurance Type** (required): earthquake / flood / comprehensive
- **Status** (required): active / inactive

### Insured Person Details
- **Name of Insured** (required)
- **Occupation** (required)

### Additional Information
- **Policy Details / Notes** (optional)

---

## Test Data Sets

### Test Set 1: Earthquake Insurance - Active Policy
```
Insurance Code: INS-EQ-2024-001
Policy Number: POL-45678-2024
Coverage Start Date: 2024-01-01T00:00
Coverage End Date: 2025-12-31T23:59
Insurance Type: Earthquake Insurance
Status: Active
Name of Insured: John Michael Anderson
Occupation: Software Engineer
Policy Details: Premium earthquake coverage for residential property in California. 
Includes structural damage, contents coverage up to $500,000, 
and temporary housing assistance. Annual premium: $2,400.
```

### Test Set 2: Flood Insurance - Active Policy
```
Insurance Code: INS-FL-2024-002
Policy Number: POL-98765-2024
Coverage Start Date: 2024-03-15T08:00
Coverage End Date: 2026-03-14T23:59
Insurance Type: Flood Insurance
Status: Active
Name of Insured: Sarah Elizabeth Thompson
Occupation: Medical Doctor
Policy Details: Comprehensive flood insurance for coastal property. 
Coverage includes building and contents up to $750,000. 
Replacement cost coverage with no depreciation. Premium: $3,200/year.
```

### Test Set 3: Comprehensive Insurance - Active
```
Insurance Code: INS-COMP-2024-003
Policy Number: POL-11223-2024
Coverage Start Date: 2024-06-01T00:00
Coverage End Date: 2025-05-31T23:59
Insurance Type: Comprehensive
Status: Active
Name of Insured: Robert James Wilson
Occupation: Business Owner
Policy Details: All-risk comprehensive coverage for commercial building. 
Includes earthquake, flood, fire, and liability. 
Total coverage: $2,000,000. Monthly premium: $850.
```

### Test Set 4: Earthquake Insurance - Expired/Inactive
```
Insurance Code: INS-EQ-2023-004
Policy Number: POL-55444-2023
Coverage Start Date: 2023-01-01T00:00
Coverage End Date: 2023-12-31T23:59
Insurance Type: Earthquake Insurance
Status: Inactive
Name of Insured: Maria Elena Rodriguez
Occupation: Teacher
Policy Details: Basic earthquake coverage for residential property. 
Policy has expired and needs renewal. 
Previous annual premium: $1,800.
```

### Test Set 5: Flood Insurance - Recently Started
```
Insurance Code: INS-FL-2024-005
Policy Number: POL-77889-2024
Coverage Start Date: 2024-10-01T00:00
Coverage End Date: 2025-09-30T23:59
Insurance Type: Flood Insurance
Status: Active
Name of Insured: David Chen
Occupation: Architect
Policy Details: New flood insurance policy for newly constructed property 
near river zone. Includes basement coverage and sewer backup. 
Premium: $2,100/year with 10% new construction discount.
```

### Test Set 6: Comprehensive - Long Term
```
Insurance Code: INS-COMP-2024-006
Policy Number: POL-33221-2024
Coverage Start Date: 2024-01-01T00:00
Coverage End Date: 2029-12-31T23:59
Insurance Type: Comprehensive
Status: Active
Name of Insured: Jennifer Marie Foster
Occupation: Real Estate Agent
Policy Details: 5-year comprehensive insurance package with premium discount. 
Multi-property coverage for 3 residential units. 
Total coverage: $1,500,000. Prepaid for full term.
```

### Test Set 7: Earthquake - High Value Property
```
Insurance Code: INS-EQ-2024-007
Policy Number: POL-99001-2024
Coverage Start Date: 2024-07-01T09:00
Coverage End Date: 2025-06-30T23:59
Insurance Type: Earthquake Insurance
Status: Active
Name of Insured: William Alexander Scott
Occupation: Investment Banker
Policy Details: Premium earthquake insurance for luxury property. 
Includes rare art collection, wine cellar, and smart home systems. 
Total coverage: $5,000,000. Annual premium: $12,000.
```

### Test Set 8: Flood - Seasonal Property
```
Insurance Code: INS-FL-2024-008
Policy Number: POL-44556-2024
Coverage Start Date: 2024-04-01T00:00
Coverage End Date: 2024-10-31T23:59
Insurance Type: Flood Insurance
Status: Active
Name of Insured: Lisa Ann Martinez
Occupation: Retired
Policy Details: Seasonal flood coverage for vacation home. 
Coverage period aligns with rainy season. 
Basic structure and contents up to $300,000. Premium: $900.
```

### Test Set 9: Comprehensive - Small Business
```
Insurance Code: INS-COMP-2024-009
Policy Number: POL-66778-2024
Coverage Start Date: 2024-05-15T00:00
Coverage End Date: 2025-05-14T23:59
Insurance Type: Comprehensive
Status: Active
Name of Insured: Michael Patrick O'Brien
Occupation: Restaurant Owner
Policy Details: Small business comprehensive insurance. 
Includes property, equipment, inventory, and business interruption. 
Total coverage: $800,000. Monthly premium: $650.
```

### Test Set 10: Earthquake - Condo Unit
```
Insurance Code: INS-EQ-2024-010
Policy Number: POL-22334-2024
Coverage Start Date: 2024-08-01T00:00
Coverage End Date: 2025-07-31T23:59
Insurance Type: Earthquake Insurance
Status: Active
Name of Insured: Amanda Grace Peterson
Occupation: Graphic Designer
Policy Details: Earthquake insurance for condominium unit. 
Covers interior improvements and personal property. 
Deductible: 10% of coverage. Total coverage: $250,000. Premium: $1,200/year.
```

---

## Quick Copy Test Data (Minimal)

### Quick Test 1 (Copy & Paste Ready)
```
INS-TEST-001
POL-10001-2024
2024-01-01T00:00
2025-12-31T23:59
Earthquake Insurance
Active
John Doe
Engineer
Standard earthquake coverage policy for residential property.
```

### Quick Test 2 (Copy & Paste Ready)
```
INS-TEST-002
POL-10002-2024
2024-06-01T00:00
2025-05-31T23:59
Flood Insurance
Active
Jane Smith
Accountant
Basic flood insurance with contents coverage.
```

### Quick Test 3 (Copy & Paste Ready)
```
INS-TEST-003
POL-10003-2024
2024-03-01T00:00
2026-02-28T23:59
Comprehensive
Active
Bob Johnson
Contractor
Comprehensive coverage for commercial property.
```

---

## Common Testing Scenarios

### Scenario 1: Creating Multiple Active Policies
Use Test Sets 1, 2, 3 to create multiple active policies for the same user.

### Scenario 2: Testing Expired Policies
Use Test Set 4 to test how system handles inactive/expired policies.

### Scenario 3: Testing Date Validations
- Try Coverage End Date before Start Date (should fail)
- Try past Start Dates with future End Dates
- Try very long policy periods (5+ years)

### Scenario 4: Testing Required Fields
Leave fields blank one by one to verify validation:
- Insurance Code
- Policy Number
- Coverage dates
- Name of Insured
- Occupation

### Scenario 5: Testing Different Insurance Types
Use different test sets to ensure all insurance types work:
- Earthquake (Sets 1, 4, 7, 10)
- Flood (Sets 2, 5, 8)
- Comprehensive (Sets 3, 6, 9)

### Scenario 6: Testing Optional Fields
- Submit with empty "Policy Details / Notes"
- Submit with very long text in notes field
- Submit with special characters in notes

---

## Date Format Guidelines

The form uses `datetime-local` format:
- Format: `YYYY-MM-DDTHH:mm`
- Example: `2024-10-25T14:30`
- Midnight: `2024-01-01T00:00`
- End of day: `2024-12-31T23:59`

---

## Tips for Testing

1. **Insurance Codes**: Keep them unique for each test
2. **Policy Numbers**: Should also be unique
3. **Dates**: 
   - Use current or future dates for active policies
   - Use past end dates for testing inactive policies
4. **Names**: Use realistic full names (first + middle/last)
5. **Occupations**: Use common professional titles
6. **Notes**: Optional but helpful for identifying test data

---

## Auto-Fill JavaScript (Optional Enhancement)

You could add this to the form for quick testing (add a button to trigger it):

```javascript
function fillTestData() {
  document.getElementById('insuranceCode').value = 'INS-TEST-' + Date.now();
  document.getElementById('policyNumber').value = 'POL-' + Math.floor(Math.random() * 90000 + 10000);
  document.getElementById('insuredFrom').value = '2024-01-01T00:00';
  document.getElementById('insuredTill').value = '2025-12-31T23:59';
  document.getElementById('insuranceType').value = 'earthquake';
  document.getElementById('status').value = 'active';
  document.getElementById('nameOfInsured').value = 'John Test User';
  document.getElementById('occupationOfInsured').value = 'Software Tester';
  document.getElementById('insuranceDetails').value = 'Test insurance policy created for development and testing purposes.';
}
```

---

## Database Validation

After adding insurance policies, verify:
1. Policy appears in insurance list
2. Policy can be selected when creating claims
3. Policy number appears after selecting insurance code
4. All fields are saved correctly
5. User_id is properly linked

---

## Notes

- All test data is fictional and for testing purposes only
- Insurance codes follow format: `INS-{TYPE}-{YEAR}-{NUMBER}`
- Policy numbers follow format: `POL-{NUMBER}-{YEAR}`
- Premium amounts and coverage details are sample values
- Adjust dates to current/future dates as needed for testing

