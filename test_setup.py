"""
Simple test script to verify the application setup
"""

def test_imports():
    """Test that all required modules can be imported"""
    try:
        print("🧪 Testing imports...")
        
        # Test core imports
        from app.core.config import settings
        print("✅ Core config imported successfully")
        
        # Test models
        from app.models.document import Document, DocumentStatus, DocumentType
        print("✅ Document models imported successfully")
        
        # Test services
        from app.services.pdf_service import pdf_service
        print("✅ PDF service imported successfully")
        
        # Test API
        from app.api.documents import router
        print("✅ Document API imported successfully")
        
        print("\n🎉 All imports successful! Application is ready to run.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_config():
    """Test configuration loading"""
    try:
        print("\n🔧 Testing configuration...")
        
        from app.core.config import settings
        
        print(f"   App Name: {settings.app_name}")
        print(f"   Version: {settings.app_version}")
        print(f"   Host: {settings.host}")
        print(f"   Port: {settings.port}")
        print(f"   Debug: {settings.debug}")
        print(f"   Database: {settings.database_url}")
        print(f"   Max File Size: {settings.max_file_size} bytes")
        
        print("✅ Configuration loaded successfully")
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_pdf_service():
    """Test PDF service initialization"""
    try:
        print("\n📄 Testing PDF service...")
        
        from app.services.pdf_service import pdf_service
        
        print(f"   Supported extensions: {pdf_service.supported_extensions}")
        print(f"   Service type: {type(pdf_service).__name__}")
        
        print("✅ PDF service initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ PDF service error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 AI Legal Document Explainer - Setup Test")
    print("=" * 50)
    
    # Run tests
    tests = [
        test_imports,
        test_config,
        test_pdf_service
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your application is ready to run.")
        print("\nTo start the application, run:")
        print("   python main.py")
        print("\nOr with uvicorn:")
        print("   uvicorn main:app --reload")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("Make sure all dependencies are installed and the virtual environment is activated.")
