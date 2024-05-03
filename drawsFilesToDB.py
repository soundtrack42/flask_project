import os
import mysql.connector

# Database connection parameters
db_config = {
    'host': 'localhost',
    'user': 'username',
    'password': 'password',
    'database': 'museum_db_mysql'
}

# Try connecting to the database
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION();")  # Simple query to check MySQL version
    version = cursor.fetchone()
    print("Database version:", version)
    conn.close()
except mysql.connector.Error as err:
    print("Database connection failed:", err)

# Connect to your MySQL database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()


# Function to find or insert an artist and return the artist ID
def find_or_insert_artist(name):
    # Special case substitution for "Albrecht_Du╠êrer"
    if name == "Albrecht_Du╠êrer":
        formatted_name = "Albrecht Dürer"
    else:
        # General replacement of underscores with spaces
        formatted_name = name.replace('_', ' ')
    
    cursor.execute('SELECT id FROM artists WHERE full_name = %s', (formatted_name,))
    result = cursor.fetchone()
    if result:
        return result[0]

    return ''

dir_path = "./images/images"
# List all subdirectories in 'images'
artists_dirs = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]

for artist_dir in artists_dirs:
    full_artist_dir_path = os.path.join(dir_path, artist_dir)
    # List all files in each artist directory
    files = [f for f in os.listdir(full_artist_dir_path) if os.path.isfile(os.path.join(full_artist_dir_path, f))]
    artist_id = find_or_insert_artist(artist_dir)
    for file_name in files:
        cursor.execute('INSERT INTO artworks (artist_id, painting_name) VALUES (%s, %s)', (artist_id, file_name))
    conn.commit()
    print("Files processed for artist:", artist_dir, "Files:", files)

conn.close()

print("Database has been updated with new artwork records.")