import json
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
from mongoengine import EmailField 
from mongoengine import connect
from mongoengine.errors import NotUniqueError
from mongoengine.errors import ValidationError
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
    _id = db.StringField()
    password = db.StringField()
    email=EmailField()
    '''def to_json(self):
        return {"name": self.name,
                "email": self.email}'''


@app.route('/', methods=['GET'])
def query_records():
    data = request.get_json()
    
    user = User.objects(_id=data['username'])
    #print(data)
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(user)

@app.route('/', methods=['PUT'])
def create_record():
    data = request.get_json()
    
    user = User.objects(_id=data['username']).update(password=data['password'])
    
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        return {"status":"successfully updated"}

@app.route('/', methods=['POST'])
def update_record():
    data = json.loads(request.data)
    
    try:
        get_data=User.objects(email=data['email'])
        #print(get_data.first())
        if get_data.first() is not None:
        
            return {"Status":"Entered Email All Ready Exists"}
        
        else:
            user = User.objects.create(_id=data['username'],password=data['password'],email=data['email'])

            return {"Status":"User Created Succesfully"}
        
    except NotUniqueError:
        return {"Status":"Entered Username All ready Exists"}
    except ValidationError:
        return {"Status":"Enter The Valid Email Id"}
@app.route('/', methods=['DELETE'])
def delete_record():
    data=request.get_json()
    
    d=User.objects(_id=data['username']).first()
    d.delete()
    return {"status":"succesfully_deleted"}
    

if __name__ == "__main__":
    app.run(debug=True)