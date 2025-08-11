#!/usr/bin/env python3
"""
AI Legal Document Explainer - Startup Script
Simple script to start the application with different configurations
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("🚀 AI Legal Document Explainer")
    print("   Intelligent legal document analysis with AI")
    print("=" * 60)
    print()

def check_environment():
    """Check if virtual environment is activated"""
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Virtual environment not detected!")
        print("   Please activate your virtual environment first:")
        print("   Windows: legal_ai_env\\Scripts\\Activate.ps1")
        print("   macOS/Linux: source legal_ai_env/bin/activate")
        print()
        return False
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import pdfplumber
        import fitz
        print("✅ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("   Please install dependencies: pip install -r requirements.txt")
        return False

def create_env_file():
    """Create .env file from example if it doesn't exist"""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if not env_file.exists() and env_example.exists():
        print("📝 Creating .env file from env.example...")
        try:
            with open(env_example, 'r') as src, open(env_file, 'w') as dst:
                dst.write(src.read())
            print("✅ .env file created successfully")
            print("   Please edit .env file with your actual configuration values")
        except Exception as e:
            print(f"❌ Error creating .env file: {e}")
        print()

def start_development():
    """Start the application in development mode"""
    print("🚀 Starting AI Legal Document Explainer in development mode...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔄 Auto-reload enabled")
    print()
    
    try:
        # Import and run the application
        from main import app
        import uvicorn
        
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("   Please check the error messages above")

def start_production():
    """Start the application in production mode"""
    print("🚀 Starting AI Legal Document Explainer in production mode...")
    print("📍 Server will be available at: http://0.0.0.0:8000")
    print("📚 API Documentation: http://0.0.0.0:8000/docs")
    print("🔄 Auto-reload disabled")
    print()
    
    try:
        # Import and run the application
        from main import app
        import uvicorn
        
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("   Please check the error messages above")

def run_tests():
    """Run the test suite"""
    print("🧪 Running application tests...")
    try:
        result = subprocess.run([sys.executable, "test_setup.py"], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("❌ Tests failed:")
        print(e.stdout)
        print(e.stderr)
    except Exception as e:
        print(f"❌ Error running tests: {e}")

def show_help():
    """Show help information"""
    print("Usage: python start.py [option]")
    print()
    print("Options:")
    print("  dev, development    Start in development mode (default)")
    print("  prod, production    Start in production mode")
    print("  test                Run application tests")
    print("  help                Show this help message")
    print()
    print("Examples:")
    print("  python start.py           # Start in development mode")
    print("  python start.py dev       # Start in development mode")
    print("  python start.py prod      # Start in production mode")
    print("  python start.py test      # Run tests")

def main():
    """Main function"""
    print_banner()
    
    # Check environment
    if not check_environment():
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Create .env file if needed
    create_env_file()
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        option = sys.argv[1].lower()
        
        if option in ['dev', 'development']:
            start_development()
        elif option in ['prod', 'production']:
            start_production()
        elif option in ['test']:
            run_tests()
        elif option in ['help', '--help', '-h']:
            show_help()
        else:
            print(f"❌ Unknown option: {option}")
            show_help()
    else:
        # Default to development mode
        start_development()

if __name__ == "__main__":
    main()
