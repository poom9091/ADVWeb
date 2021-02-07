import os
import json
import redis
from flask import Flask,request,jsonify

app = Flask(__name__)

db=redis.StrictRedis(
    host='node9160-advweb-22.app.ruk-com.cloud',
    port=11015,
    password='TBNian15812',
    decode_responses=True
)

class Books():
    def __init__(self, id, book, price):
        self.id = id
        self.name = book
        self.price = price

# Get All 
@app.route('/', methods=['GET'])
def hello_world(): 
    # book = (db.hgetall("B001")) 
    b = db.keys()
    b.sort()
    result = []
    for id in b:
        result.append(db.hgetall(id))
    return jsonify(result)

# Set Book 
@app.route('/addBook', methods=['POST'])
def addBook():
    id = request.json['id']
    name = request.json['book']
    price = request.json['price']
    
    new_book = Books(id, name, price)
    jsonStr = json.dumps(new_book.__dict__)
    db.hset(id,"ID",new_book.id)
    db.hset(id,"name",new_book.name)
    db.hset(id,"price",new_book.price)
    print(jsonStr)
    return jsonify(jsonStr)

# Get Single Book 
@app.route('/book/<id>', methods=['GET'])
def get_book(id):
    book = db.hgetall(id)
    print(book)
    return book

# Del Book
@app.route('/delbook/<id>', methods=['DELETE'])
def delete_book(id):
    db.delete(id)
    return "Delete Success"
if __name__ == '__main__':
    app.run()