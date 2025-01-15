import pandas as pd

# Load the data
df = pd.read_csv('Books.csv', dtype=str)  # Read all columns as strings to avoid issues with mixed types
print("Initial data shape:", df.shape)

# Sample the dataset to 20000 rows randomly
df = df.sample(n=20000, random_state=1)  # Set random_state for reproducibility
print("Sampled data shape:", df.shape)

# Handle Missing Values
df.dropna(inplace=True)
print("After dropping missing values:", df.shape)

# Remove Duplicates
df.drop_duplicates(inplace=True)
print("After removing duplicates:", df.shape)

# Strip whitespace and lowercase column names
df.columns = df.columns.str.strip().str.lower().str.replace('-', '_')
print("Renamed columns:", df.columns.tolist())

# Validate and clean data (e.g., ISBN length, valid URLs, and numeric checks)
df = df[df['isbn'].str.match(r'^\d{10}|\d{13}$', na=False)]  # Keep only valid ISBN-10 or ISBN-13
print("After filtering valid ISBNs:", df.shape)

# Convert 'year_of_publication' to integer if valid, else set as NaN
df['year_of_publication'] = pd.to_numeric(df['year_of_publication'], errors='coerce')
df = df[df['year_of_publication'] > 0]  # Keep only valid years
print("After cleaning 'year_of_publication':", df.shape)

# Validate URLs (basic check)
url_columns = ['image_url_s', 'image_url_m', 'image_url_l']
for col in url_columns:
    df = df[df[col].str.startswith('http', na=False)]
print("After validating URLs:", df.shape)

# Save Cleaned Data
df.to_csv('Cleaned_Books.csv', index=False)
print("Cleaned data saved to 'Cleaned_Books.csv'")
