from flask import Flask, request, make_response

from classes.personClass import Person

app = Flask(__name__)

#маршрут для обработки запроса "/"
@app.route("/")
def index():
    return "RSOI. Lab №1 (CI & CD) : PERSONS"

#маршрут для обработки GET-запроса на получение информации о человеке по ID
@app.route('/persons/<int:personId>', methods=["GET"])
def get_person(personId):
    person = Person()

    person_json = person.PC_get_person(personId)

    if person_json is None:
        return make_response(f"Not found Person for ID {personId}", 404)
    
    #создадим http-ответ с кодом состояния 200 (успешный запрос) и телом ответа в формате JSON
    response = make_response(person_json, 200)

    #установим значение заголовка "Content-Type" на "application/json" (т.е. сервер будет отправлять данные в формате JSON)
    response.headers['Content-Type'] = 'application/json'

    return response

#маршрут для обработки GET-запроса на получение информации о всех людях
@app.route('/persons', methods=["GET"])
def get_all_person():
    person = Person()

    persons_json = person.PC_get_all_persons()

    response = make_response(persons_json, 200)
    response.headers['Content-Type'] = 'application/json'

    return response

#маршрут для обработки POST-запроса на создание новой записи о человеке
@app.route('/persons', methods=["POST"])
def post_person():
    #присвоим переменной JSON-объект, который был передан в запросе с помощью метода "json()"
    new_person = request.json

    person = Person()

    person_id = person.PC_create_person(new_person)

    if person_id is None:
        return make_response('Invalid data', 400)
    #при успешном создании новой записи возвращается пустая строка, код состояния 201 Created и заголовок Location со значением, содержащим URL для доступа к новому ресурсу 
    return '', 201, {'location': f'{request.host_url}/persons/{int(person_id)}'}   

#маршрут для обработки PATCH-запроса на обновление существующей записи о человеке по ID
@app.route('/persons/<int:personId>', methods=["PATCH"])
def patch_person(personId):
    new_person = request.json

    person = Person()

    code = person.PC_update_person(new_person, personId)

    if code:   #т.е code == 1 (True)
        return make_response(f"Not found Person for ID {personId}", 404)

    person_json = person.PC_get_person(personId)

    response = make_response(person_json, 200)
    response.headers['Content-Type'] = 'application/json'

    return response

#маршрут для обработки DELETE-запроса на удаление записи о человеке по ID
@app.route('/persons/<int:personId>', methods=["DELETE"])
def delete_person(personId):
    person = Person()

    answer = person.PC_delete_person(personId)

    if answer == 0:
        return make_response(f"Not found Person for ID {personId}", 404)

    return make_response(f"Person for ID {personId} was removed", 204)

if __name__ == '__main__':
    app.run(host='localhost',port=5432)
