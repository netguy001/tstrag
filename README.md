# RAG Document System

A Retrieval-Augmented Generation (RAG) system that lets you upload documents and ask questions about them. The system uses AI to find relevant information from your documents and provides accurate answers with source citations.

## What It Does

- **Upload Documents**: Support for PDF, DOCX, TXT, and JSON files
- **Smart Search**: Uses vector embeddings to find relevant information
- **AI-Powered Answers**: Groq's Llama 3.3 model generates accurate responses
- **Source Tracking**: Shows which documents the answers came from
- **Persistent Storage**: Uploaded files are saved and indexed in a database

## How It Works

1. **Upload**: You upload a document (PDF, DOCX, TXT, or JSON)
2. **Processing**: The system extracts text and splits it into chunks
3. **Indexing**: Chunks are converted to vectors and stored in ChromaDB
4. **Query**: You ask a question about your documents
5. **Search**: The system finds the most relevant chunks using semantic search
6. **Answer**: Groq AI generates an answer based only on your documents

## Requirements

- Python 3.8 or higher
- Groq API key (free at https://console.groq.com)

## Installation

### Step 1: Clone or Download

```bash
cd path/to/your/folder
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your free API key from: https://console.groq.com/keys

## Project Structure

```
rag-system/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── database/
│   └── chroma_db/         # Vector database storage
├── uploads/               # Uploaded files stored here
├── templates/
│   └── index.html         # Web interface
├── static/
│   └── style.css          # Styling
└── utils/
    ├── __init__.py
    ├── extractor.py       # Text extraction from files
    ├── chunker.py         # Text splitting logic
    └── embeddings.py      # Vector database operations
```

## Running the System

### Start the Server

```bash
python app.py
```

The server will start at: **http://127.0.0.1:5001**

### Using the Web Interface

1. **Open your browser** and go to `http://127.0.0.1:5001`
2. **Upload a document** using the file picker
3. **Wait for processing** (you'll see "Success! X chunks created")
4. **Ask a question** in the text area
5. **View the answer** with source citations

## Configuration

Edit `config.py` to customize:

```python
CHUNK_SIZE = 800           # Characters per chunk
CHUNK_OVERLAP = 100        # Overlap between chunks
TOP_K_RESULTS = 5          # Number of chunks to retrieve
MODEL_NAME = "llama-3.3-70b-versatile"  # AI model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"    # Embedding model
```

## Supported File Types

- **PDF** (.pdf)
- **Word Documents** (.docx)
- **Text Files** (.txt)
- **JSON Files** (.json)

## Troubleshooting

### Port Already in Use

If port 5001 is occupied, change it in `app.py`:

```python
app.run(debug=True, port=5002)  # Use different port
```

### API Key Error

Make sure your `.env` file exists and contains:
```
GROQ_API_KEY=gsk_...
```

### Model Not Found

If you get a model error, update `config.py` with a working model:
```python
MODEL_NAME = "llama-3.1-8b-instant"
```

### Database Corruption

Delete and recreate the database:
```bash
# Windows PowerShell
Remove-Item -Recurse -Force database\chroma_db

# Mac/Linux
rm -rf database/chroma_db
```

## Technologies Used

- **Flask**: Web framework
- **ChromaDB**: Vector database for embeddings
- **Sentence Transformers**: Text embedding generation
- **Groq**: Fast AI inference
- **PyPDF2**: PDF text extraction
- **python-docx**: Word document processing

## API Endpoints

### POST /upload
Upload and process a document
- **Request**: multipart/form-data with file
- **Response**: `{"message": "...", "chunks": 17}`

### POST /query
Ask a question about uploaded documents
- **Request**: `{"query": "your question"}`
- **Response**: `{"answer": "...", "sources": ["file.pdf"]}`

## Performance Tips

- **Chunk Size**: Larger chunks = more context but slower search
- **Top K Results**: More results = better context but higher API costs
- **Model Choice**: Faster models (8b) vs more accurate (70b)

## Limitations

- Maximum file size: 16MB (Flask default)
- ChromaDB runs in-process (single user)
- No authentication or user management
- Files are not encrypted at rest

## Future Improvements

- [ ] Multi-user support with authentication
- [ ] File management (delete, re-index)
- [ ] Conversation history
- [ ] Support for images and tables
- [ ] Export answers to PDF/DOCX
- [ ] API rate limiting

## License

This project is open source and available for personal and commercial use.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review Groq documentation: https://console.groq.com/docs
3. Check ChromaDB docs: https://docs.trychroma.com

## Credits

Built with Flask, ChromaDB, Sentence Transformers, and Groq AI.