from flask import request, jsonify
#from dataBase import Person

class Persons:
    def __init__(self):
        self.persons = [
            { "id" : 1, "name": "Kate", "age": 19, "address": "Moscow", "work": "student" },
            { "id" : 2, "name": "Elena", "age": 25, "address": "St. Peterburg", "work": "musician" },
            { "id" : 3, "name": "Ann", "age": 21, "address": "Voronegh", "work": "teacher of Math" }
        ]
    
    def get_pers(self, personId):
        for person in self.persons:
            if person["id"] == personId:
                return jsonify(person)
        return jsonify({"error": "Person not found"}), 404
    
    def get_all_pers(self):
        return jsonify(self.persons)
    
    def create_pers(self):
        data = request.get_json()
        new_person = {
            "id" : len(self.persons) + 1,
            "name": data["name"],
            "age": data["age"],
            "address": data["address"],
            "work": data["work"]
        }
        self.persons.append(new_person)
        return jsonify(new_person), 201
    
    def upd_pers(self, personId):
        data = request.get_json()
        for person in self.persons:
            if person["id"] == personId:
                person["name"] = data.get("name", person["name"])
                person["age"] = data.get("age", person["age"])
                person["address"] = data.get("address", person["address"])
                person["work"] = data.get("work", person["work"])
                return jsonify(person)
        return jsonify({"error": "Person not found"}), 404
    
    def del_pers(self, personId):
        for person in self.persons:
            if person["id"] == personId:
                self.persons.remove(person)
                return jsonify({"message": "Person deleted"})
        return jsonify({"error": "Person not found"}), 404
 
