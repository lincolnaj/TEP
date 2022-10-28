from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from pymongo import MongoClient
from bson import ObjectId
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from collections.abc import Mapping
import pandas as pd
app=Flask(__name__)

app.secret_key="secretkey"
app.config['MONGO_URI']="mongodb+srv://tep-warehouse:Gk7ILMaUdqj9NDA5@tep.wjl8agn.mongodb.net/Quiz"



mongo= PyMongo(app)

@app.route('/add',methods=['POST'])
def add_quiz():
    _json= request.json
    _easy=_json['EASY']
    _moderate=_json['MODERATE']
    _difficult=_json['DIFFICULT']
    if _easy and _moderate and _difficult and request.method =='POST':
        ids= mongo.db.quiz.insert_one({'EASY':_easy,'MODERATE':_moderate,'DIFFICULT':_difficult})
        resp=jsonify("Diffculty added")
        resp.status_code=200
        return resp
    else:
        return not_found()
@app.route('/get-quiz/<id>')
def get_quiz(id):
    quiz= list(mongo.db.question_answer.find({'id':id}))
    resp=dumps(quiz)
    
    
    return resp
@app.route('/get-quiz')
def get_quiz_all():
    quiz= list(mongo.db.question_answer.find({}))
    resp=dumps(quiz)
    
    
    return resp


@app.route('/add-type',methods=['POST'])      
def add_quiz_type():
    _json= request.json
    _id=_json['id']
    _text=_json['text']
    _choices=_json['choices']
    _solutions=_json['solutions']
    if _id and _text and _solutions and  _choices and request.method =='POST':
        ids= mongo.db.question_answer.insert_one({'id':_id,'text':_text,'chocies':_choices,'solutions':_solutions})
        resp=jsonify("Diffculty added")
        resp.status_code=200
        return resp
    else:
        return not_found()


@app.route('/add-leader',methods=['POST'])      
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
def add_mock_quiz():
    _json= request.json
    _id=_json['quizID']
    _quizId=_json['description']
    _quiz=_json['questions']
    ids= mongo.db.mockQuiz.insert_one({'quizID':_id,'description':_quizId,'questions':_quiz})
    resp=jsonify("mock quiz added")
    resp.status_code=200
    return resp

@app.route('/add-cred',methods=['POST'])      
def add_creds():
    _json= request.json
    _name=_json['name']
    _pwd=_json['password']
    ids= mongo.db.login.insert_one({'name':_name,'password':_pwd})
    resp=jsonify("Creds added")
    resp.status_code=200
    return resp

@app.route('/get-creds/<name>')
def get_creds(name):
    quiz= mongo.db.login.find({'name':name})
    resp=dumps(quiz)
    
    
    return resp

@app.errorhandler(404)
def not_found(error=None):
    message ={'status':404, 'message': 'NOt found'+ request.url}
    resp =jsonify(message)
    resp.status_code=404
    return resp

if __name__=="__main__":
    app.run(debug=True)
