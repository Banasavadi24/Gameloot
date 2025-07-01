from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
# import uuid # Not strictly needed if using simple index-based delete for proof of concept, but good practice if you implement IDs later.

app = Flask(__name__)
CORS(app) # Enable CORS for all origins during development

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')

# --- Helper functions for data management ---

def read_data():
    """Reads data from the JSON file."""
    if not os.path.exists(DATA_FILE):
        # Initialize with empty list if file doesn't exist
        with open(DATA_FILE, 'w') as f:
            json.dump({"items": []}, f, indent=2) # Initialize with 'items'
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def write_data(data):
    """Writes data to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# --- API Endpoints for generic 'items' ---

@app.route('/items', methods=['GET'])
def get_all_items():
    """Reads all items."""
    data = read_data()
    return jsonify(data['items'])

@app.route('/items', methods=['POST'])
def add_item():
    """Creates a new item."""
    new_item_data = request.json
    if not new_item_data:
        return jsonify({"message": "No input data provided"}), 400

    data = read_data()
    
    # Basic validation and type conversion for price
    try:
        new_item_data['price'] = float(new_item_data['price'])
    except (ValueError, TypeError):
        return jsonify({"message": "Price must be a valid number"}), 400

    # For a proof-of-concept with simple index deletion, we might not assign an ID here.
    # If you later switch to ID-based deletion (recommended), you'd add:
    # new_item_data['id'] = str(uuid.uuid4()) # Example for unique ID

    data['items'].append(new_item_data)
    write_data(data)
    return jsonify(new_item_data), 201 # 201 Created

# WARNING: Deleting by index is highly discouraged for real APIs.
# It's fragile and can lead to incorrect deletions if the list changes.
# A robust solution requires a unique ID for each item.
@app.route('/items/<int:index>', methods=['DELETE'])
def delete_item(index):
    """Deletes an item by its index."""
    data = read_data()
    
    if 0 <= index < len(data['items']):
        deleted_item = data['items'].pop(index)
        write_data(data)
        return jsonify({"message": "Item deleted successfully", "item": deleted_item}), 200
    return jsonify({"message": "Item not found at that index"}), 404

# You might also need a PUT/UPDATE method for items, but your JS doesn't have it yet.

if __name__ == '__main__':
    # Ensure data.json exists on first run and has 'items' key
    if not os.path.exists(DATA_FILE):
        write_data({"items": []})
    else:
        # Ensure 'items' key exists if file exists but might be empty or missing it
        data = read_data()
        if "items" not in data:
            data["items"] = []
            write_data(data)

    app.run(debug=True, port=5000)