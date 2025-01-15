from neo4j import GraphDatabase
import pandas as pd

# Connect to Neo4j
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

# Load dataset
books = pd.read_csv('data/Cleaned_Books.csv')

# Function to insert data into Neo4j
def insert_data(tx, title, isbn, year, author, publisher):
    query = """
    MERGE (b:Book {title: $title, isbn: $isbn, year: $year})
    MERGE (a:Author {name: $author})
    MERGE (p:Publisher {name: $publisher})
    MERGE (b)-[:WRITTEN_BY]->(a)
    MERGE (b)-[:PUBLISHED_BY]->(p)
    """
    tx.run(query, title=title, isbn=isbn, year=year, author=author, publisher=publisher)

with driver.session() as session:
    for _, row in books.iterrows():
        session.write_transaction(
            insert_data, row['book_title'], row['isbn'], row['year_of_publication'],
            row['book_author'], row['publisher']
        )
driver.close()
