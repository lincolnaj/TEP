from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from pymongo import MongoClient
from bson import ObjectId
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from collections.abc import Mapping
from flask_cors import CORS, cross_origin
import pandas as pd

app=Flask(__name__)
CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key="secretkey"
app.config['MONGO_URI']="mongodb+srv://tep-warehouse:Gk7ILMaUdqj9NDA5@tep.wjl8agn.mongodb.net/Quiz"



mongo= PyMongo(app)


@app.route('/add-type',methods=['POST'])
@cross_origin()      
def add_quiz_type():
    _json= request.json
    _id=_json['id']
    _text=_json['text']
    _choices=_json['answers']
    _solutions=_json['solutions']
    if _id and _text and _solutions and  _choices and request.method =='POST':
        ids= mongo.db.question_answer.insert_one({'id':_id,'text':_text,'answers':_choices,'solutions':_solutions})
        resp=jsonify("Diffculty added")
        resp.status_code=200
        return resp
    else:
        return not_found()

@app.route('/get-type')
@cross_origin()      
def get_quiz_type():
    quiz= mongo.db.question_answer.find({})
    resp=dumps(quiz)
    
    
    return resp
@app.route('/get-type/<id>')
@cross_origin()      
def get_quiz_type_id(id):
    quiz= mongo.db.question_answer.find({'id':int(id)})
    resp=dumps(quiz)
    
    
    return resp
@app.route('/add-leader',methods=['POST'])
@cross_origin()      
def add_quiz_leader():
    _json= request.json
    _id=_json['studentID']
    _quizId=_json['quizID']
    _quiz=_json['quiz']
    ids= mongo.db.leaderboard.insert_one({'studentID':_id,'quizID':_quizId,'quiz':_quiz})
    resp=jsonify("leader added")
    resp.status_code=200
    return resp

@app.route('/get-leader')
@cross_origin()
def get_leader():
    quiz= mongo.db.leaderboard.aggregate([
            {"$group": 
            {

                "_id": "$studentID",
                    "total_score": {
                "$sum": "$quiz.score"
            },
            "total_stars":{
                "$sum": "$quiz.stars"
            },
                "completed": {
                    "$push": {
                    "quizID": "$quizID",
                    "quiz": "$quiz"
                    }
                }
                }
            }
    ])
    resp=dumps(quiz)
    
    
    return resp
@app.route('/add-mockQuiz',methods=['POST'])
@cross_origin()      
def add_mock_quiz():
    _json= request.json
    _id=_json['quizID']
    _title=_json['title']
    _quizId=_json['description']
    _quiz=_json['questions']
    ids= mongo.db.mockQuiz.insert_one({'quizID':_id,'title':_title, 'description':_quizId,'questions':_quiz})
    resp=jsonify("mock quiz added")
    resp.status_code=200
    return resp

@app.route('/get-mockQuiz/<id>')
@cross_origin()
def get_quiz(id):
    quiz= list(mongo.db.mockQuiz.find({"id" :id}))
    resp=dumps(quiz)
    
    
    return resp
@app.route('/get-mockQuiz')
@cross_origin()
def get_quiz_all():
    quiz= list(mongo.db.mockQuiz.find({}))
    resp=dumps(quiz)
    
    
    return resp

@app.route('/add-cred',methods=['POST'])
@cross_origin()      
def add_creds():
    _json= request.json
    _name=_json['name']
    _pwd=_json['password']
    ids= mongo.db.login.insert_one({'name':_name,'password':_pwd})
    resp=jsonify("Creds added")
    resp.status_code=200
    return resp

@app.route('/get-creds/<name>')
@cross_origin()
def get_creds(name):
    quiz= mongo.db.login.find({'name':name})
    resp=dumps(quiz)
    
    
    return resp

@app.route('/get-mockQuiz/<id>')
@cross_origin()
def get_mockQuiz(id):
    quiz= mongo.db.mockQuiz.find({"_id" : ObjectId(id)})
    resp=dumps(quiz)
    
    
    return resp
@app.errorhandler(404)
@cross_origin()
def not_found(error=None):
    message ={'status':404, 'message': 'NOt found'+ request.url}
    resp =jsonify(message)
    resp.status_code=404
    return resp

if __name__=="__main__":
    app.run(debug=True)
