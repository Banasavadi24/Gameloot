from flask import Flask, jsonify, request
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATA_FILE = "data.json"

# Helper functions
def load_data():
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Get all items
@app.route('/items', methods=['GET'])
def get_items():
    data = load_data()
    return jsonify(data)

# Add new item
@app.route('/items', methods=['POST'])
def add_item():
    data = load_data()
    new_item = request.json
    data.append(new_item)
    save_data(data)
    return jsonify({"message": "Item added"}), 201

# Update item by ID
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = load_data()
    updated_item = request.json
    if item_id < 0 or item_id >= len(data):
        return jsonify({"error": "Item not found"}), 404
    data[item_id] = updated_item
    save_data(data)
    return jsonify({"message": "Item updated"})

# Delete item by ID
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    data = load_data()
    if item_id < 0 or item_id >= len(data):
        return jsonify({"error": "Item not found"}), 404
    data.pop(item_id)
    save_data(data)
    return jsonify({"message": "Item deleted"})

if __name__ == '__main__':
    app.run(debug=True)
