from flask import Flask
from personClass import Persons 

app = Flask(__name__)

persons = Persons()

@app.route("/")
def index():
    return "Lab №1 PERSONS"

@app.route('/api/v1/persons/<int:personId>', methods=["GET"])
def get_person(personId):
    return persons.get_pers(personId)

@app.route('/api/v1/persons', methods=["GET"])
def get_all_persons():
    return persons.get_all_pers()

@app.route('/api/v1/persons', methods=["POST"])
def create_person():
    return persons.create_pers()

@app.route('/api/v1/persons/<int:personId>', methods=["PATCH"])
def update_person(personId):
    return persons.upd_pers(personId)

@app.route("/api/v1/persons/<int:personId>", methods=["DELETE"])
def delete_person(personId):
    return persons.del_pers(personId)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)
 
