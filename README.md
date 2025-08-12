# AI Legal Document Explainer

An intelligent system for analyzing, understanding, and explaining legal documents using advanced AI and natural language processing techniques.

## 🚀 Features

- **Document Processing**: Support for PDF, DOCX, and various document formats
- **AI-Powered Analysis**: Advanced language models for legal document comprehension
- **Smart Summarization**: Intelligent extraction of key legal concepts and terms
- **Interactive Interface**: User-friendly web interface for document upload and analysis
- **Legal Knowledge Base**: Comprehensive understanding of legal terminology and concepts

## 🛠️ Technology Stack

- **Backend**: FastAPI, Python 3.13+
- **AI/ML**: LangChain, OpenAI, LlamaIndex, Sentence Transformers
- **Document Processing**: PyMuPDF, PDFMiner, Pytesseract, Pillow
- **Vector Database**: ChromaDB for document embeddings
- **Frontend**: Modern web interface with visualization capabilities
- **Data Visualization**: Matplotlib, Seaborn for insights and charts

## 📋 Prerequisites

- Python 3.13 or higher
- Windows 10/11 (current setup)
- Git for version control

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd "AI Legal Doc Explainer"
```

### 2. Create and Activate Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

### 4. Environment Setup
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
CHROMA_DB_PATH=./chroma_db
LOG_LEVEL=INFO
```

### 5. Run the Application
```bash
# Start the FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📁 Project Structure

```
AI Legal Doc Explainer/
├── venv/                    # Virtual environment
├── requirements.txt         # Python dependencies
├── .env                    # Environment variables (create this)
├── main.py                 # FastAPI application entry point
├── src/                    # Source code directory
│   ├── models/            # Data models and schemas
│   ├── services/          # Business logic services
│   ├── api/               # API endpoints
│   ├── utils/             # Utility functions
│   └── config/            # Configuration management
├── tests/                  # Test files
├── docs/                   # Documentation
└── README.md              # This file
```

## 🔧 Development

### Code Formatting
```bash
# Format code with Black
black .

# Sort imports with isort
isort .
```

### Running Tests
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src
```

### Adding New Dependencies
```bash
# Install new package
pip install package_name

# Update requirements.txt
pip freeze > requirements.txt
```

## 📚 API Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation in the `docs/` folder

## 🔮 Roadmap

- [x] Phase 1: Core document processing and analysis ✅ **COMPLETED**
- [ ] Phase 2: Advanced AI features and legal knowledge base
- [ ] Phase 3: User management and collaboration features
- [ ] Phase 4: Mobile application and API integrations

---

**Note**: This project has completed Phase 1 development. Advanced features will be added in subsequent phases.
