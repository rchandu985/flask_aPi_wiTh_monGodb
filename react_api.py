import json
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
from mongoengine import EmailField 
from mongoengine import connect
from flask import app
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'local',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

class User(db.Document):
    
    meta = {'collection': 'admin'}
    username = db.StringField()
    password = db.StringField()
    email=EmailField()
    '''def to_json(self):
        return {"name": self.name,
                "email": self.email}'''


@app.route('/', methods=['GET'])
def query_records():
    data = request.get_json()
    
    user = User.objects(username=data['username'])
    print(data)
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(user)

@app.route('/', methods=['PUT'])
def create_record():
    data = request.get_json()
    
    user = User.objects(username=data['username']).update(password=data['password'])
    
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        return {"status":"successfully updated"}

@app.route('/', methods=['POST'])
def update_record():
    data = json.loads(request.data)
    
    user = User.objects.create(username=data['username'],password=data['password'],email=data['email'])
    return jsonify(data)

@app.route('/', methods=['DELETE'])
def delete_record():
    data=request.get_json()
    
    d=User.objects(username=data['username']).first()
    d.delete()
    return {"status":"succesfull_deleted"}
    

if __name__ == "__main__":
    app.run(debug=True)