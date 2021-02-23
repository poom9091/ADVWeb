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

# Get  All 
@app.route('/', methods=['GET'])
def getLeague(): 
    b = db.keys('*PokemonLeague*') #รับค่ามาจาก Redis
    b.sort() #รับค่ามาจาก Redis แล้วเรียง ID 
    result = [] # ประกาศตัวแปร result เป็น array
    for i in range(len(b)):
        if i%2 == 0 :
            info = db.hgetall(b[i])
        elif i%2 == 1 :
            listPokemon = db.smembers(b[i])
            pokemon = []
            for k in listPokemon:
                pokemon.append(db.hgetall('Pokemon:'+k))

            print(info["id"])
            Train = db.hgetall('Trainer:'+info["name"])
            print(Train)
            print(pokemon)
           
            result.append({
                "id":info["id"],
                "name":Train,
                "pokemon":pokemon
            })
    return  jsonify(result)

# Get pokedex All 
@app.route('/pokedex', methods=['GET'])
def hello_world(): 
    b = db.keys('*Pokemon:*') #รับค่ามาจาก Redis
    b.sort() #รับค่ามาจาก Redis แล้วเรียง ID 
    result = [] # ประกาศตัวแปร result เป็น array
    for id in b:
        result.append(db.hgetall(id)) # hgetall ใช้ในการเรียกข้อมูล HASH ตาม Id ที่ใส่ แล้วเพิ่มลง Array
    return jsonify(result)

# Set Pokemon 
@app.route('/pokedex', methods=['POST'])
def addPokemon():
    id = request.json['id'] 
    name = request.json['name']
    type = request.json['type']
    weaknesses = request.json['weaknesses']

    new_pokemon = Pokedex(id, name,type,weaknesses) # สร้าง OBJ ชื่อ new_pokemon ใส่ค่า พารามิเตอร์ที่รับเข้ามา
    jsonStr = json.dumps(new_pokemon.__dict__)
    # hset เป็นคำสั่งสร้าง Hash
    # db.hset(ชื่อ HASH,ชื่อ Field,Value)
    db.hset("Pokemon:"+id,"ID",new_pokemon.id) 
    db.hset("Pokemon:"+id,"Name",new_pokemon.name)
    db.hset("Pokemon:"+id,"Type",new_pokemon.type)
    db.hset("Pokemon:"+id,"Weaknesses",new_pokemon.weaknesses)
    print(jsonStr)
    return jsonify(jsonStr)

# Get Single Pokemon 
@app.route('/pokedex/<id>', methods=['GET'])
def get_book(id):
    pokemon = db.hgetall("Pokemon:"+id) # hgetall ใช้ในการเรียกข้อมูล HASH ตาม Id
    print(pokemon)
    return pokemon

# Del Pokemon
@app.route('/pokedex/<id>', methods=['DELETE'])
def delete_pokemon(id):
    db.delete("Pokemon:"+id) #delete เป็นคำสั่งลบข้อมูล
    return "Delete Success"

# Update a Pokemon
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
    db.hmset("Pokemon:"+id,pokemon) #hmset ต่างจาก hset : hset สามารถ set ได้ทีละ Field : hmset สามารถ set ได้หลาย Field
    print(jsonStr)
    return jsonify(jsonStr)


#####################Trainer#####################

class Trainer():
    def __init__(self, id, name, age, gender):
        self.id = id
        self.name = name
        self.age = age
        self.gender = gender

# Get All 
@app.route('/trainer', methods=['GET'])
def getTrainers(): 
    b = db.keys('*Trainer:*') #รับค่ามาจาก Redis
    print(b) #รับค่ามาจาก Redis แล้วเรียง ID 
    result = [] # ประกาศตัวแปร result เป็น array
    for id in b:
        result.append(db.hgetall(id)) # hgetall ใช้ในการเรียกข้อมูล HASH ตาม Id ที่ใส่ แล้วเพิ่มลง Array
    return jsonify(result)

# Set Pokemon 
@app.route('/trainer', methods=['POST'])
def addTrainer():
    id = request.json['id'] 
    name = request.json['name']
    age = request.json['age']
    gender = request.json['gender']

    new_Trainer = Trainer(id, name,age,gender) # สร้าง OBJ ชื่อ new_pokemon ใส่ค่า พารามิเตอร์ที่รับเข้ามา
    jsonStr = json.dumps(new_Trainer.__dict__)
    # hset เป็นคำสั่งสร้าง Hash
    # db.hset(ชื่อ HASH,ชื่อ Field,Value)
    db.hset("Trainer:"+id,"ID",new_Trainer.id) 
    db.hset("Trainer:"+id,"Name",new_Trainer.name)
    db.hset("Trainer:"+id,"Age",new_Trainer.age)
    db.hset("Trainer:"+id,"Gender",new_Trainer.gender)
    print(jsonStr)
    return jsonify(jsonStr)

# Get Single Pokemon 
@app.route('/trainer/<id>', methods=['GET'])
def get_Trainer(id):
    trainer = db.hgetall("Trainer:"+id) # hgetall ใช้ในการเรียกข้อมูล HASH ตาม Id
    print(trainer)
    return trainer

# Del Pokemon
@app.route('/trainer/<id>', methods=['DELETE'])
def delete_Trainer(id):
    db.delete("Trainer:"+id) #delete เป็นคำสั่งลบข้อมูล
    return "Delete Success"

# Update a Pokemon
@app.route('/trainer/<id>', methods=['PUT'])
def update_Trainer(id):
    name = request.json['name']
    age = request.json['age']
    gender = request.json['gender']

    update_trainer = Trainer(id, name,age,gender) # สร้าง OBJ ชื่อ new_pokemon ใส่ค่า พารามิเตอร์ที่รับเข้ามา
    jsonStr = json.dumps(update_trainer.__dict__)
    trainer = { 
                "ID":id,
                "Name":update_trainer.name,
                "Age":update_trainer.age,
                "Gender":update_trainer.gender
              }
    db.hmset("Trainer:"+id,trainer) #hmset ต่างจาก hset : hset สามารถ set ได้ทีละ Field : hmset สามารถ set ได้หลาย Field
    print(jsonStr)
    return jsonify(jsonStr)

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=80)