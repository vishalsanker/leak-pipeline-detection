import sqlite3
from sklearn.ensemble import IsolationForest
import joblib

# Function to connect to the SQLite database and check count
def check_and_update_training_set():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('your_database.db')  # Replace with your actual database name
        cursor = conn.cursor()

        # Execute a query to get the count of records
        cursor.execute('SELECT COUNT(*) FROM your_table')  # Replace with your actual table name
        count = cursor.fetchone()[0]

        if count > 100000:
            # If count is greater than 100,000, fetch data and add to training set
            cursor.execute('SELECT * FROM your_table LIMIT 100000')  # Fetch first 100,000 records
            data = cursor.fetchall()

            # Assume 'features' is a list of feature vectors from your data
            features = [row[1:] for row in data]

            # Initialize or load the Isolation Forest model
            model = IsolationForest()
            # Assuming 'training_set.pkl' is the file to store the model
            model_file = 'training_set.pkl'

            try:
                # Load existing model if available
                model = joblib.load(model_file)
            except FileNotFoundError:
                # Train the model if it doesn't exist
                model.fit(features)
                joblib.dump(model, model_file)
            
    finally:
        # Close the database connection
        conn.close()

# Run the function
check_and_update_training_set()
