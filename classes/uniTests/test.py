import unittest
import requests

import sys
sys.path.append('C:/Users/ОЛЬГА/Desktop/rsoi/rsoi_lab1_try/classes/uniTests/test.py')

from classes.dataBase import Database
#from classes.personClass import Person

database = Database()

person1 = {
     "name" : "Vera",
     "age" : 31,
     "address" : "Moscow",
     "work" : "painter"
}

person2 = {
     "name" : "Tanya",
     "age" : 20,
     "address" : "Krasnodar",
     "work" : "writer"
}

patch_name = {"name" : "Ksenia"}
patch_age = {"age" : 23}
patch_address = {"address" : "Khimki"}
patch_work = {"designer"}

class TestAPI(unittest.TestCase):
    #тестирование GET-запроса для человека по ID
    def test_get_person(self):
        person = database.DB_get_person(1)

        with self.subTest(person=person):
            r = requests.get(url="http://127.0.0.1:8080/api/v1/persons/1")
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json(), person)
    
    #тестирование GET-запроса для всех людей

    #тестирование POST-запроса
    def test_post_person(self):
        persons = [person1, person2]

        for person in persons:
            with self.subTest(person=person):        #создание подтеста с параметром "person" для проверки определённого объекта "person"
                #отправка POST-запроса с информацией о человеке
                r = requests.post(url="http://127.0.0.1:8080/api/v1/persons", json=person)
                self.assertEqual(r.status_code, 201)

                #извлечение значения ключа 'Location' из заголовков ответа r
                redirected_url = r.headers['Location']

                #получение ID созданного человека 
                person_id_dict = {"id": int(redirected_url.split("/")[-1])}

                #выполнение GET-запроса к созданному ранее человеку для проверки корректности 
                r = requests.get(redirected_url)
                self.assertEqual(r.status_code, 200)

                #сравним объединение словарей person и person_id_dict с результатом json-запроса
                self.assertEqual(r.json(), {**person, **person_id_dict})
    
    """
    #тестирование PATCH-запроса
    def test_patch_person(self):
        persons = [person1, person2]
        patch_vars = [patch_name, patch_age, patch_address, patch_work]

        for person in persons:
            for patch_var in patch_vars:
                with self.subTest(person=person, patch_var=patch_var):
                    r = requests.post(url="http://127.0.0.1:8080/api/v1/persons", json=person)
                    redirected_url = r.headers['Location']
                    r = requests.patch(url=redirected_url, json=patch_var)
                    self.assertEqual(r.status_code, 200)
                    self.assertEqual(r.json(), patch_var)
    """
    
    #тестирование DELETE-запроса
    def test_delete_person(self):
        persons = [person1, person2]

        for person in persons:
            with self.subTest(person=person):
                r = requests.post(url="http://127.0.0.1:8080/api/v1/persons", json=person)

                redirected_url = r.headers['Location']
                
                #удаляем объект с помощью DELETE-запроса
                r = requests.delete(redirected_url)
                self.assertEqual(r.status_code, 204)
                
                #проверяем корректность удаления с помощью GET-запроса
                r = requests.get(redirected_url)
                self.assertEqual(r.status_code, 404)             

if __name__ == '__main__':
    unittest.main()