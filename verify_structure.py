"""
Verification Script for Restructured API
Tests that all new blueprints and routes are properly registered
"""
import sys
sys.path.insert(0, '.')

from app import create_app

def test_blueprints():
    """Test that all blueprints are registered correctly"""
    app = create_app()
    
    print("="*70)
    print("TESTING BLUEPRINT REGISTRATION")
    print("="*70)
    
    blueprints = app.blueprints
    
    expected_blueprints = [
        'auth_api',
        'dashboard_api', 
        'detection_api',
        'insurance_api',
        'auth_pages',
        'dashboard_pages',
        'insurance_pages'
    ]
    
    print("\nRegistered Blueprints:")
    for name in blueprints.keys():
        print(f"  [OK] {name}")
    
    print("\nExpected Blueprints:")
    all_found = True
    for expected in expected_blueprints:
        if expected in blueprints:
            print(f"  [OK] {expected}")
        else:
            print(f"  [FAIL] {expected} - MISSING!")
            all_found = False
    
    if all_found:
        print("\n[SUCCESS] All blueprints registered successfully!\n")
    else:
        print("\n[FAILURE] Some blueprints are missing!\n")
    
    return all_found


def test_routes():
    """Test that key routes are accessible"""
    app = create_app()
    
    print("="*70)
    print("TESTING ROUTE REGISTRATION")
    print("="*70)
    
    test_routes = [
        # API Routes
        ('POST', '/api/auth/login', 'Login API'),
        ('POST', '/api/auth/signup', 'Signup API'),
        ('POST', '/api/auth/logout', 'Logout API'),
        ('GET', '/api/auth/verify', 'Verify Token API'),
        ('GET', '/api/auth/user', 'Get User API'),
        ('GET', '/api/dashboard/stats', 'Dashboard Stats API'),
        ('POST', '/api/detection/crack', 'Crack Detection API'),
        ('GET', '/api/insurance/policies', 'Insurance Policies API'),
        ('GET', '/api/insurance/policy-numbers', 'Policy Numbers API'),
        ('GET', '/api/insurance/claims', 'Claims API'),
        ('GET', '/api/insurance/assessment', 'Assessment API'),
        ('GET', '/api/insurance/reports', 'Reports API'),
        
        # Page Routes
        ('GET', '/', 'Login Page'),
        ('GET', '/signup', 'Signup Page'),
        ('GET', '/dashboard', 'Dashboard Page'),
        ('GET', '/claim_insurance', 'Insurance Claim Form'),
        ('GET', '/insurance_claims_detail', 'Claims Detail Page'),
        ('GET', '/damaged_property_image', 'Property Image Page'),
        ('GET', '/new_report', 'New Report Page'),
        ('GET', '/insurance_report', 'Insurance Report Page'),
    ]
    
    all_routes = []
    for rule in app.url_map.iter_rules():
        all_routes.append((rule.endpoint, list(rule.methods), rule.rule))
    
    print("\nTesting Key Routes:")
    all_found = True
    for method, route, description in test_routes:
        found = any(route == r[2] and method in r[1] for r in all_routes)
        if found:
            print(f"  [OK] {method:6} {route:40} - {description}")
        else:
            print(f"  [FAIL] {method:6} {route:40} - {description}")
            all_found = False
    
    if all_found:
        print("\n[SUCCESS] All key routes registered successfully!\n")
    else:
        print("\n[FAILURE] Some routes are missing!\n")
    
    return all_found


def test_api_structure():
    """Test API URL prefixes"""
    app = create_app()
    
    print("="*70)
    print("TESTING API STRUCTURE")
    print("="*70)
    
    api_prefixes = {
        '/api/auth': 'Authentication API',
        '/api/dashboard': 'Dashboard API',
        '/api/detection': 'Detection API',
        '/api/insurance': 'Insurance API'
    }
    
    routes_by_prefix = {prefix: [] for prefix in api_prefixes.keys()}
    
    for rule in app.url_map.iter_rules():
        for prefix in api_prefixes.keys():
            if rule.rule.startswith(prefix):
                routes_by_prefix[prefix].append(rule.rule)
    
    print("\nAPI Endpoints by Prefix:")
    for prefix, description in api_prefixes.items():
        print(f"\n  {description} ({prefix}):")
        routes = routes_by_prefix[prefix]
        if routes:
            for route in sorted(routes):
                print(f"    [OK] {route}")
        else:
            print(f"    [WARNING] No routes found!")
    
    print("\n[SUCCESS] API structure verified!\n")
    return True


def verify_file_structure():
    """Verify that all expected files exist"""
    import os
    
    print("="*70)
    print("VERIFYING FILE STRUCTURE")
    print("="*70)
    
    expected_files = [
        'app/routes/api/__init__.py',
        'app/routes/api/auth_api.py',
        'app/routes/api/dashboard_api.py',
        'app/routes/api/detection_api.py',
        'app/routes/api/insurance_api.py',
        'app/routes/pages/__init__.py',
        'app/routes/pages/auth_pages.py',
        'app/routes/pages/dashboard_pages.py',
        'app/routes/pages/insurance_pages.py',
        'API_STRUCTURE.md',
        'MIGRATION_GUIDE.md'
    ]
    
    print("\nChecking Expected Files:")
    all_exist = True
    for filepath in expected_files:
        if os.path.exists(filepath):
            print(f"  [OK] {filepath}")
        else:
            print(f"  [FAIL] {filepath} - NOT FOUND!")
            all_exist = False
    
    if all_exist:
        print("\n[SUCCESS] All expected files exist!\n")
    else:
        print("\n[FAILURE] Some files are missing!\n")
    
    return all_exist


if __name__ == '__main__':
    print("\n" + "="*70)
    print("  RESTRUCTURED APPLICATION VERIFICATION")
    print("="*70 + "\n")
    
    results = []
    
    try:
        results.append(("File Structure", verify_file_structure()))
        results.append(("Blueprint Registration", test_blueprints()))
        results.append(("Route Registration", test_routes()))
        results.append(("API Structure", test_api_structure()))
    except Exception as e:
        print(f"\n[ERROR] Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n" + "="*70)
    print("  VERIFICATION SUMMARY")
    print("="*70)
    
    for test_name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {test_name:30} {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("="*70)
    
    if all_passed:
        print("\n[SUCCESS] All verifications passed!")
        print("The API restructuring is complete and functional.\n")
        sys.exit(0)
    else:
        print("\n[WARNING] Some verifications failed.")
        print("Please review the output above.\n")
        sys.exit(1)

