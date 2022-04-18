from unicodedata import name
from flask import Flask, Response, request, render_template, jsonify
import pymongo
import json
from bson.objectid import ObjectId

app=Flask(__name__)

try:
    mongo = pymongo.MongoClient(
        host = 'localhost',
        port = 27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo.Testing #connect to mongodb1
    mongo.server_info() #trigger exception if cannot connect to db
except:
    print("Error -connect to db")

@app.route('/api', methods=['POST'])
def insertdata():
  try:
    data = request.get_json()
    dbResponse = db.Student.insert_one(data)
    response = Response("New Record added",status=201,mimetype='application/json')
    return response
  except Exception as ex:
    response = Response("Insert New Record Error!!",status=500,mimetype='application/json')
    return response 

@app.route('/api', methods=['GET'])
def displayall():
  try:
    documents = db.Student.find()
    output = [{item: data[item] for item in data if item != '_id'} for data in documents]
    return jsonify(output)
  except Exception as ex:
    response = Response("Search Records Error!!",status=500,mimetype='application/json')
    return response

@app.route('/api/teachers', methods=['GET'])
def displayallteachers():
  try:
    documents = db.Teachers.find()
    output = [{item: data[item] for item in data if item != '_id'} for data in documents]
    return jsonify(output)
  except Exception as ex:
    response = Response("Search Records Error!!",status=500,mimetype='application/json')
    return response

@app.route('/api/<string:name>', methods=['GET'])
def searchbyname(name):
  try:
    documents = list(db.Student.find({"Lois":name}))
    output = [{item: data[item] for item in data if item != '_id'} for data in documents]
    return jsonify(output)
  except Exception as ex:
    response = Response("Search Records Error!!",status=500,mimetype='application/json')
    return response

@app.route('/api/<int:id>', methods=['GET'])
def searchbyid(id):
  try:
    documents = list(db.Teachers.find({"stid":id}))
    output = [{item: data[item] for item in data if item != '_id'} for data in documents]
    return jsonify(output)
  except Exception as ex:
    response = Response("Search Records Error!!",status=500,mimetype='application/json')
    return response

@app.route('/api/<int:id>', methods=['PATCH'])
def updatebyid(id):
  try:
    data=request.get_json()
    dataresp=db.Teachers.update_one({"stid":id},{'$set':{"tname":data["tname"],"tage":data["tage"]}})
    response = Response(" Records updated!!",status=500,mimetype='application/json')
    return response
  except Exception as ex:
    response = Response("Search Records Error!!",status=500,mimetype='application/json')
    return response


@app.route('/api/<int:id>', methods=['DELETE'])
def deletebyid(id):
  try:
    documents = list(db.Teachers.find({"stid":id}))
    if(documents):
      dataresp=db.Teachers.delete_one({"stid":id})
      response = Response(" Records deleted!!",status=500,mimetype='application/json')
    return response

 
  except Exception as ex:
    response = Response("Search Records Error!!",status=500,mimetype='application/json')
    return response
if __name__ == '__main__':
    app.run(port=5000, debug=True)

