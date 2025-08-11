# AI Legal Document Explainer

An intelligent AI-powered system for analyzing, explaining, and extracting insights from legal documents using advanced natural language processing and machine learning techniques.

## 🚀 Features

- **PDF Document Processing**: Extract text and metadata from legal PDFs
- **AI-Powered Analysis**: Leverage OpenAI and other LLMs for document understanding
- **Smart Text Chunking**: Intelligent document segmentation for better processing
- **Legal Entity Recognition**: Identify and extract key legal terms and concepts
- **Document Summarization**: Generate concise summaries of complex legal documents
- **Interactive Visualizations**: Charts and graphs for document insights
- **RESTful API**: FastAPI backend for easy integration
- **Database Storage**: SQLite and MongoDB support for document management

## 🛠️ Technology Stack

### Backend Framework
- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - Lightning-fast ASGI server
- **Pydantic** - Data validation using Python type annotations

### PDF Processing
- **pdfplumber** - Accurate text extraction from PDFs
- **PyMuPDF** - Advanced PDF manipulation and text coordinates
- **pdf2image** - PDF to image conversion capabilities

### AI & Machine Learning
- **OpenAI** - GPT models for document analysis
- **LangChain** - Framework for developing applications with LLMs
- **LlamaIndex** - Data framework for LLM applications
- **Transformers** - Hugging Face models for offline processing
- **Sentence Transformers** - State-of-the-art sentence embeddings
- **Tiktoken** - Fast BPE tokenizer for OpenAI models

### Data & Storage
- **SQLAlchemy** - SQL toolkit and Object-Relational Mapping
- **SQLite** - Lightweight database for development
- **MongoDB** - NoSQL database for scalable document storage

### Visualization
- **Matplotlib** - Comprehensive plotting library
- **Seaborn** - Statistical data visualization
- **Plotly** - Interactive plotting and dashboards
- **Pandas** - Data manipulation and analysis

### Utilities
- **Python-dotenv** - Environment variable management
- **Requests** - HTTP library for API calls
- **Aiofiles** - Asynchronous file operations

## 📋 Prerequisites

- Python 3.8 or higher
- Git
- OpenAI API key (for AI features)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/shajishali/AI-powered-legal-Document-Explainer.git
cd AI-powered-legal-Document-Explainer
```

### 2. Create Virtual Environment
```bash
python -m venv legal_ai_env
```

### 3. Activate Virtual Environment
**Windows:**
```bash
legal_ai_env\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source legal_ai_env/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Set Environment Variables
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./legal_docs.db
MONGODB_URL=mongodb://localhost:27017/
```

### 6. Run the Application
```bash
uvicorn main:app --reload
```

## 📁 Project Structure

```
AI-powered-legal-Document-Explainer/
├── legal_ai_env/          # Virtual environment (not in git)
├── requirements.txt        # Python dependencies
├── .gitignore            # Git ignore rules
├── README.md             # Project documentation
├── main.py               # FastAPI application entry point
├── app/                  # Application modules
│   ├── api/             # API endpoints
│   ├── core/            # Core functionality
│   ├── models/          # Data models
│   ├── services/        # Business logic
│   └── utils/           # Utility functions
├── tests/                # Test suite
├── docs/                 # Documentation
└── examples/             # Usage examples
```

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `DATABASE_URL`: Database connection string
- `MONGODB_URL`: MongoDB connection string
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `MAX_FILE_SIZE`: Maximum file upload size in bytes

### API Configuration
- Default port: 8000
- API documentation: http://localhost:8000/docs
- Interactive API explorer: http://localhost:8000/redoc

## 📚 API Endpoints

### Document Management
- `POST /api/documents/upload` - Upload legal documents
- `GET /api/documents/` - List all documents
- `GET /api/documents/{id}` - Get document details
- `DELETE /api/documents/{id}` - Delete document

### Document Analysis
- `POST /api/documents/{id}/analyze` - Analyze document content
- `GET /api/documents/{id}/summary` - Get document summary
- `POST /api/documents/{id}/extract-entities` - Extract legal entities
- `GET /api/documents/{id}/insights` - Get document insights

### AI Features
- `POST /api/ai/explain` - AI-powered document explanation
- `POST /api/ai/qa` - Question-answering on documents
- `POST /api/ai/compare` - Compare multiple documents

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=app tests/
```

## 📊 Usage Examples

### Basic Document Upload
```python
import requests

# Upload a legal document
with open('contract.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/documents/upload',
        files={'file': f}
    )
    document_id = response.json()['id']

# Analyze the document
analysis = requests.post(
    f'http://localhost:8000/api/documents/{document_id}/analyze'
)
```

### AI-Powered Explanation
```python
# Get AI explanation of a document section
explanation = requests.post(
    f'http://localhost:8000/api/ai/explain',
    json={
        'document_id': document_id,
        'text': 'Section text to explain',
        'context': 'Legal context'
    }
)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing powerful language models
- The FastAPI community for the excellent web framework
- Contributors and users of this project

## 📞 Support

If you have any questions or need help:
- Open an issue on GitHub
- Check the documentation
- Review the examples

## 🔮 Roadmap

- [ ] Multi-language support
- [ ] Advanced legal entity recognition
- [ ] Document comparison tools
- [ ] Integration with legal databases
- [ ] Mobile application
- [ ] Advanced analytics dashboard
- [ ] Batch processing capabilities
- [ ] API rate limiting and authentication

---

**Built with ❤️ for the legal community**
