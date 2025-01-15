from flask import Flask, request, render_template, jsonify
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import redis
from neo4j import GraphDatabase
import pickle

# Initialize Flask app
app = Flask(__name__)

# Load and preprocess dataset
books = pd.read_csv('data/Cleaned_Books.csv')
print("Starting to combine features for the books...")
books['combined_features'] = books['book_title'] + ' ' + books['book_author'] + ' ' + books['publisher']
print("Combining features completed.")

# Compute embeddings for all books
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Starting to compute embeddings for the books...")
data_embeddings = model.encode(books['combined_features'].tolist(), convert_to_tensor=True)
print("Embeddings computation completed.")

# Initialize Neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

# Initialize Redis for caching
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# Extract unique values for filtering options
unique_authors = books['book_author'].unique()
unique_publishers = books['publisher'].unique()
unique_years = books['year_of_publication'].unique()

@app.route('/')
def index():
    return render_template('index.html', 
                           authors=unique_authors, 
                           publishers=unique_publishers, 
                           years=unique_years)

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        query = data.get('query')
        selected_author = data.get('author')
        selected_publisher = data.get('publisher')
        selected_year = data.get('year')

        if not query and not selected_author and not selected_publisher and not selected_year:
            return jsonify({"error": "Please provide at least one search method (query, author, publisher, or year)."}), 400

        # Knowledge graph query expansion
        expanded_query_terms = []
        if query:
            with driver.session() as session:
                kg_result = session.run(
                    """
                    MATCH (b:Book)-[:WRITTEN_BY]->(a:Author)
                    MATCH (b)-[:PUBLISHED_BY]->(p:Publisher)
                    WHERE b.title CONTAINS $query OR a.name CONTAINS $query
                    RETURN b.title AS Book, a.name AS Author, b.publisher AS Publisher
                    """,
                    {"query": query}
                )
                for record in kg_result:
                    expanded_query_terms.extend([record["Book"], record["Author"], record["Publisher"]])
        
        # Remove duplicates and filter None values
        expanded_query_terms = list(filter(None, set(expanded_query_terms)))

        # Integrate expanded terms into the query embedding
        combined_query = query + ' ' + ' '.join(expanded_query_terms) if query else ' '.join(expanded_query_terms)
        query_embedding = None

        if combined_query:
            if redis_client.exists(combined_query):
                query_embedding = pickle.loads(redis_client.get(combined_query))
            else:
                query_embedding = model.encode([combined_query], convert_to_tensor=True)
                redis_client.set(combined_query, pickle.dumps(query_embedding))

        # Compute similarities and rank books
        top_books = books
        if query_embedding is not None:
            similarities = util.cos_sim(query_embedding, data_embeddings)
            top_results = similarities.argsort(descending=True)
            top_books = books.iloc[top_results[0][:10]]

        # Apply filters
        if selected_author:
            top_books = top_books[top_books['book_author'] == selected_author]
        if selected_publisher:
            top_books = top_books[top_books['publisher'] == selected_publisher]
        if selected_year:
            top_books = top_books[top_books['year_of_publication'] == int(selected_year)]

        # Prepare final results
        results = top_books[['book_title', 'book_author', 'publisher', 'year_of_publication', 'image_url_m']].to_dict('records')

        return jsonify({"embedding_results": results})

    except Exception as e:
        app.logger.error(f"Error during search: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
