# Semantic Search for Book Store

## Overview

This project implements a semantic search engine for a book store ecommerce. Users can search for books by title, author, publisher, or year of publication. The project features a Flask-based backend, Neo4j for Knowledge Graph Integration, Redis for caching, and a responsive frontend built with HTML, CSS, and JavaScript.

---

## Setup and Installation

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Musiemhy/Book_Store_Ecommerce.git
   cd Book_Store_Ecommerce
   ```
2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set Up Neo4j:

   Start Neo4j by running: neo4j desktop

   And importing the database located in the database folder.

   Or, you can run the provided load_data.py script to generate the data:

   ```bash
    python load_data.py
   ```

4. Start the Redis server:
   redis is not included in the requirements.txt so you have to install it separately
   To install redis:

   #### On Linux:

   ```bash
   sudo apt update
   sudo apt install redis
   sudo systemctl start redis
   ```

   #### On windows install wsl and follow the linux installation

   #### On macOS:

   ```bash
   brew install redis
   brew services start redis
   ```

   To start the server:

   ```bash
   redis-server
   ```

   Ensure Redis is running on port `6379` or update the configuration in the Flask app.

5. Run the Flask server:

   ```bash
   python app.py
   ```

6. Open your browser and navigate to:
   ```
   http://127.0.0.1:5001
   ```

---

## Model Details

### Model Used

I used **Sentence Transformers (SBERT)**, which is a transformer model fine-tuned for semantic similarity tasks. It converts textual data into vector embeddings that can be compared using cosine similarity.

### Why SBERT?

1. **Semantic Understanding**: SBERT captures the contextual meaning of text, making it ideal for semantic search.
2. **Efficiency**: It is computationally efficient for generating embeddings and comparing them using cosine similarity.
3. **Pretrained Models**: Access to pretrained models on diverse datasets reduces the need for extensive training.

The application uses the all-MiniLM-L6-v2 model from the SentenceTransformer library. This model is highly efficient and designed for semantic similarity tasks, It provides a good balance between speed and accuracy, allowing for fast responses without compromising the quality of search results.

---
