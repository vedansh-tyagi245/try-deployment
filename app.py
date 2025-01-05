from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Get the MongoDB connection string from the environment variable
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Specify your database name (replace 'your_database_name' with your actual database name)
db = client['NameDB']  # Select the database by name
names_collection = db.names  # Select the collection where names will be stored

@app.route('/', methods=['GET'])
def home():
    # Fetch all names from the MongoDB collection
    names = [name['name'] for name in names_collection.find()]
    return render_template('index.html', names=names)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')  # Get the name from the form input
    if name:
        # Insert the name into the MongoDB collection
        names_collection.insert_one({'name': name})
    return redirect(url_for('home'))  # Redirect to the home page to display updated names

if __name__ == '__main__':
    app.run(debug=True)
