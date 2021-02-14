import os
import json
import redis
from flask import Flask,request,jsonify

app = Flask(__name__)

# เชื่มมต่อ Redis ผ่าน Local
# db=redis.StrictRedis(
#     host='node9160-advweb-22.app.ruk-com.cloud',
#     port=11015,
#     password='TBNian15812',
#     decode_responses=True
# )

# เชื่มมต่อ Redis ผ่าน Cloud 
db=redis.StrictRedis(
    host='10.100.2.137', 
    port=6379,
    password='TBNian15812',
    decode_responses=True
)


class Pokedex():
    def __init__(self, id, name, type, weaknesses):
        self.id = id
        self.name = name
        self.type = type
        self.weaknesses = weaknesses

# Get All 
@app.route('/', methods=['GET'])
def hello_world(): 
    b = db.keys() #รับค่ามาจาก Redis
    b.sort() #รับค่ามาจาก Redis แล้วเรียง ID 
    result = [] # ประกาศตัวแปร result เป็น array
    for id in b:
        result.append(db.hgetall(id)) # hgetall ใช้ในการเรียกข้อมูล HASH ตาม Id ที่ใส่ แล้วเพิ่มลง Array
    return jsonify(result)

# Set Pokemon 
@app.route('/addPokemon', methods=['POST'])
def addPokemon():
    id = request.json['id'] 
    name = request.json['name']
    type = request.json['type']
    weaknesses = request.json['weaknesses']

    new_pokemon = Pokedex(id, name,type,weaknesses) # สร้าง OBJ ชื่อ new_pokemon ใส่ค่า พารามิเตอร์ที่รับเข้ามา
    jsonStr = json.dumps(new_pokemon.__dict__)
    # hset เป็นคำสั่งสร้าง Hash
    # db.hset(ชื่อ HASH,ชื่อ Field,Value)
    db.hset(id,"ID",new_pokemon.id) 
    db.hset(id,"Name",new_pokemon.name)
    db.hset(id,"Type",new_pokemon.type)
    db.hset(id,"Weaknesses",new_pokemon.weaknesses)
    print(jsonStr)
    return jsonify(jsonStr)

# Get Single Pokemon 
@app.route('/pokedex/<id>', methods=['GET'])
def get_book(id):
    pokemon = db.hgetall(id) # hgetall ใช้ในการเรียกข้อมูล HASH ตาม Id
    print(pokemon)
    return pokemon

# Del Pokemon
@app.route('/delpokemon/<id>', methods=['DELETE'])
def delete_pokemon(id):
    db.delete(id) #delete เป็นคำสั่งลบข้อมูล
    return "Delete Success"

# Update a Staff
@app.route('/pokedex/<id>', methods=['PUT'])
def update_staff(id):
    name = request.json['name']
    type = request.json['type']
    weaknesses = request.json['weaknesses']

    update_pokemon = Pokedex(id, name,type,weaknesses) # สร้าง OBJ ชื่อ new_pokemon ใส่ค่า พารามิเตอร์ที่รับเข้ามา
    jsonStr = json.dumps(update_pokemon.__dict__)
    pokemon = { 
                "ID":id,
                "Name":update_pokemon.name,
                "Type":update_pokemon.type,
                "Weaknesses":update_pokemon.weaknesses
              }
    db.hmset(id,pokemon)
    print(jsonStr)
    return jsonify(jsonStr)

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=80)