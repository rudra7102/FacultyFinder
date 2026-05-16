FacultyFinder

AI-powered semantic faculty search engine that helps users discover relevant professors based on research interests, teaching domains, and academic expertise using Natural Language Processing and Semantic Search.

Overview

FacultyFinder allows users to search faculty profiles using natural language queries such as:

machine learning,
professors working on cybersecurity,
NLP faculty,
deep learning researchers,
embedded systems,
computer vision professors

Instead of relying only on exact keyword matching, the system uses semantic embeddings to understand the meaning behind user queries and retrieve the most relevant faculty members.

Features
Semantic faculty search using Sentence Transformers
Natural language query understanding
Faculty profile scraping and preprocessing
Research-area based retrieval
Interactive frontend UI
FastAPI backend API
Real faculty profile dataset
Responsive faculty cards with:
Research Areas
Teaching Domains
Biography
Contact Information
Faculty Profile Links

Tech Stack
Frontend
HTML
CSS
JavaScript

Backend
FastAPI
Python
AI / NLP
Sentence Transformers
all-MiniLM-L6-v2
Cosine Similarity

Data Processing
Pandas
NumPy
BeautifulSoup
Requests

Project Architecture
User Query
     ↓
Frontend UI
     ↓
FastAPI Backend
     ↓
Semantic Embedding Search
     ↓
Cosine Similarity Matching
     ↓
Top Relevant Faculty Results

Project Structure
FacultyFinder/
│
├── api/
│   └── main.py
│
├── embeddings/
│   ├── generate_embeddings.py
│   └── semantic_search.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── scraper/
│   ├── fetch_faculty_links.py
│   ├── scrape_profiles.py
│   └── utils.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── requirements.txt
├── runtime.txt
└── README.mds


How It Works
1. Faculty Scraping

Faculty profile pages are scraped using BeautifulSoup and Requests.

The scraper extracts:

Faculty Name
Research Areas
Teaching Information
Biography
Email
Phone Number
Profile URL

2. Data Cleaning

Scraped content is cleaned to remove:

Navigation text
Footer content
Broken formatting
Duplicate information
Empty values
"Back to Top" artifacts

3. Embedding Generation

Faculty profiles are converted into dense vector embeddings using:

sentence-transformers/all-MiniLM-L6-v2

Embeddings are generated from:

Research Areas
Teaching Information
Biography

4. Semantic Search

User queries are:

normalized
embedded
compared against faculty embeddings

Similarity is computed using cosine similarity.

The system returns the most relevant faculty profiles based on semantic meaning rather than exact keyword matching.

Installation Guide
1. Clone Repository
git clone https://github.com/rudra7102/FacultyFinder.git
2. Navigate to Project Folder
cd FacultyFinder
3. Create Virtual Environment
Windows
python -m venv venv
venv\Scripts\activate
Mac/Linux
python3 -m venv venv
source venv/bin/activate
4. Install Dependencies
pip install -r requirements.txt
Generate Embeddings

Run the following command to generate faculty embeddings:

python embeddings/generate_embeddings.py
Run Backend Server
uvicorn api.main:app --reload

Backend runs at:

http://127.0.0.1:8000


Run Frontend

Open:

frontend/index.html

using:

VS Code Live Server
OR
any local static server

Frontend typically runs at:

http://127.0.0.1:5500

Example Queries
machine learning
cybersecurity
deep learning faculty
professors working on NLP
embedded systems
computer vision researchers
blockchain faculty
mathematics professors

Sample Search Workflow

User Query
    ↓
Query Embedding
    ↓
Cosine Similarity Search
    ↓
Top Matching Faculty
    ↓
Frontend Display

Key Highlights

Supports semantic understanding of queries
Handles research-domain based retrieval
Works with abbreviated and natural language inputs
Retrieves top relevant faculty profiles
Lightweight and modular project structure
Easy to extend for university-scale datasets