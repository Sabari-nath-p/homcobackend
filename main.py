from bson import ObjectId
from flask import Flask, jsonify, request
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

uri = "mongodb+srv://homco:homco.admin@cluster0.vygyw1q.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['Homco'] # Replace with your own database name
 # Replace with your own collection name
@app.route('/packingmaterial', methods=['GET'])
def getpackingData():
    # Retrieve all data in the collection
    collection = db['packingMaterial']
    data = collection.find({})
    # Convert the data to a list and convert ObjectId instances to strings
    data_list = [item for item in data]
    for item in data_list:
        item['_id'] = str(item['_id'])
    # Return the data as a JSON response
    return jsonify(data_list)

@app.route('/products', methods=['GET'])
def getproductData():
    collection = db['productList']
    # Retrieve all data in the collection
    data = collection.find({})
    # Convert the data to a list and convert ObjectId instances to strings
    data_list = [item for item in data]
    for item in data_list:
        item['_id'] = str(item['_id'])
    # Return the data as a JSON response
    return jsonify(data_list)

@app.route('/addpackMaterial', methods=['POST'])
def insert_one_packData():
    collection = db['packingMaterial']
    # Parse the JSON data from the request body
    data = request.get_json()
    # Insert the data into the collection
    result = collection.insert_one(data)
    # Return the ID of the inserted document as a JSON response
    return jsonify({'_id': str(result.inserted_id)})

@app.route('/addmanypackMaterial', methods=['POST'])
def insert_many_packData():
    # Get the data to insert from the request body
    collection = db['packingMaterial']
    data = request.json
    # Insert the data into the collection
    result = collection.insert_many(data)
    # Return the IDs of the inserted documents as a JSON response
    return jsonify({'inserted_ids': result.inserted_ids})

if __name__ == '__main__':
    app.run(debug=True)
