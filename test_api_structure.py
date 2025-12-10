"""
Quick Test Script for Restructured API
This script verifies that all new blueprints are properly registered
"""
import sys
sys.path.insert(0, '.')

from app import create_app

def test_blueprints():
    """Test that all blueprints are registered correctly"""
    app = create_app()
    
    print("🔍 Testing Blueprint Registration...\n")
    
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
    
    print("📋 Registered Blueprints:")
    for name in blueprints.keys():
        print(f"  ✅ {name}")
    
    print("\n🎯 Expected Blueprints:")
    all_found = True
    for expected in expected_blueprints:
        if expected in blueprints:
            print(f"  ✅ {expected}")
        else:
            print(f"  ❌ {expected} - MISSING!")
            all_found = False
    
    if all_found:
        print("\n✅ All blueprints registered successfully!")
    else:
        print("\n❌ Some blueprints are missing!")
        return False
    
    return True


def test_routes():
    """Test that key routes are accessible"""
    app = create_app()
    
    print("\n🔍 Testing Route Registration...\n")
    
    test_routes = [
        # API Routes
        ('POST', '/api/auth/login', 'Login API'),
        ('POST', '/api/auth/signup', 'Signup API'),
        ('POST', '/api/auth/logout', 'Logout API'),
        ('GET', '/api/auth/verify', 'Verify Token API'),
        ('GET', '/api/dashboard/stats', 'Dashboard Stats API'),
        ('POST', '/api/detection/crack', 'Crack Detection API'),
        ('GET', '/api/insurance/policies', 'Insurance Policies API'),
        
        # Page Routes
        ('GET', '/', 'Login Page'),
        ('GET', '/signup', 'Signup Page'),
        ('GET', '/dashboard', 'Dashboard Page'),
        ('GET', '/claim_insurance', 'Insurance Claim Form'),
    ]
    
    all_routes = []
    for rule in app.url_map.iter_rules():
        all_routes.append((rule.endpoint, list(rule.methods), rule.rule))
    
    print("📋 Testing Key Routes:")
    all_found = True
    for method, route, description in test_routes:
        found = any(route == r[2] and method in r[1] for r in all_routes)
        if found:
            print(f"  ✅ {method:6} {route:40} - {description}")
        else:
            print(f"  ❌ {method:6} {route:40} - {description} - NOT FOUND!")
            all_found = False
    
    if all_found:
        print("\n✅ All key routes registered successfully!")
    else:
        print("\n❌ Some routes are missing!")
        return False
    
    return True


def test_api_structure():
    """Test API URL prefixes"""
    app = create_app()
    
    print("\n🔍 Testing API Structure...\n")
    
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
    
    print("📋 API Endpoints by Prefix:")
    for prefix, description in api_prefixes.items():
        print(f"\n  {description} ({prefix}):")
        routes = routes_by_prefix[prefix]
        if routes:
            for route in sorted(routes):
                print(f"    ✅ {route}")
        else:
            print(f"    ⚠️  No routes found!")
    
    print("\n✅ API structure verified!")
    return True


if __name__ == '__main__':
    print("="*70)
    print("  RESTRUCTURED API TEST SUITE")
    print("="*70)
    
    results = []
    
    try:
        results.append(("Blueprint Registration", test_blueprints()))
        results.append(("Route Registration", test_routes()))
        results.append(("API Structure", test_api_structure()))
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n" + "="*70)
    print("  TEST SUMMARY")
    print("="*70)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {test_name:30} {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("="*70)
    
    if all_passed:
        print("\n🎉 All tests passed! The API restructuring is successful!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please review the output above.")
        sys.exit(1)

