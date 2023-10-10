import os
#sys.path.append('C:\\Users\\ОЛЬГА\\Desktop\\rsoi\\rsoi_lab1_try\\classes')

import unittest
import requests

import sys
#sys.path.append('C:\\Users\\ОЛЬГА\\Desktop\\rsoi\\rsoi_lab1_try\\classes')
#sys.path.append(os.path.join(os.getcwd(), 'classes'))
#my_path = os.getcwd()
#if my_path == 'C:\\Users\\ОЛЬГА\\Desktop\\rsoi\\rsoi_lab1_try':
sys.path.append(os.path.join(os.getcwd(), 'classes'))
sys.path.append(os.path.dirname(os.getcwd()))

from dataBase import Database

database = Database()

class TestAPI(unittest.TestCase):

    #тестирование GET-запроса на получение информации о человеке по ID
    def test_get_person(self):
        person = database.DB_get_person(2)

        r = requests.get(url="http://127.0.0.1:8080/persons/2")
        self.assertEqual(r.status_code, 200)
            
        person_info = r.json()

        #проверим, является ли person_info словарём
        self.assertIsInstance(person_info, dict)

        self.assertEqual(person_info['id'], person[0])
        self.assertEqual(person_info['name'], person[1])
        self.assertEqual(person_info['age'], person[2])
        self.assertEqual(person_info['address'], person[3])
        self.assertEqual(person_info['work'], person[4])

    #тестирование GET-запроса на получение информации о всех людях   
    def test_get_all_persons(self):
        persons = database.DB_get_all_persons()

        r = requests.get(url="http://127.0.0.1:8080/persons")
        self.assertEqual(r.status_code, 200)

        persons_info = r.json()
        #проверим, является ли persons_info списком
        self.assertIsInstance(persons_info, list)

        for p_inf, pers in zip(persons_info, persons):
            with self.subTest(p_inf=p_inf, pers=pers):
                self.assertIsInstance(p_inf, dict)

                self.assertEqual(p_inf['id'], pers[0])
                self.assertEqual(p_inf['name'], pers[1])
                self.assertEqual(p_inf['age'], pers[2])
                self.assertEqual(p_inf['address'], pers[3])
                self.assertEqual(p_inf['work'], pers[4])
        
    #тестирование POST-запроса на создание новой записи о человеке
    def test_post_person(self):
        person = {
            "name" : "Vera",
            "age" : 31,
            "address" : "Moscow",
            "work" : "painter"
        }
        
        r = requests.post(url="http://127.0.0.1:8080/persons", json=person)
        self.assertEqual(r.status_code, 201)

        #извлекаем значение ключа 'Location' из заголовков ответа r
        redirected_url = r.headers['Location']

        #получим ID нового созданного человека 
        person_id_dict = {"id": int(redirected_url.split("/")[-1])}

        #выполненим GET-запроса к созданному ранее человеку для проверки корректности 
        r = requests.get(redirected_url)
        self.assertEqual(r.status_code, 200)
        
        #сравним объединение словарей person и person_id_dict с результатом json-запроса
        self.assertEqual(r.json(), {**person, **person_id_dict})

    #тестирование PATCH-запроса на обновление существующей записи о человеке по ID
    def test_patch_person(self):
        person = {
            "name" : "Tanya",
            "age" : 20,
            "address" : "Krasnodar",
            "work" : "writer"
        }

        patch_name = {"name" : "Ksenia"}
        patch_age = {"age" : 23}
        patch_address = {"address" : "Khimki"}
        patch_work = {"work" : "designer"}

        patch_vars = [patch_name, patch_age, patch_address, patch_work]

        for patch_var in patch_vars:
            with self.subTest(patch_var=patch_var):
                r = requests.post(url="http://127.0.0.1:8080/persons", json=person)
                redirected_url = r.headers['Location']

                person_id_dict = {"id": int(redirected_url.split("/")[-1])}

                r = requests.get(redirected_url)
                self.assertEqual(r.status_code, 200)

                r = requests.patch(url=redirected_url, json=patch_var)
                self.assertEqual(r.status_code, 200)
                
                self.assertEqual(r.json(), {**person, **patch_var, **person_id_dict})

    #тестирование DELETE-запроса на удаление записи о человеке по ID
    def test_delete_person(self):
        person = {
            "name" : "Tanya",
            "age" : 20,
            "address" : "Krasnodar",
            "work" : "writer"
        }
        
        r = requests.post(url="http://127.0.0.1:8080/persons", json=person)
        redirected_url = r.headers['Location']
                
        #удаляем объект с помощью DELETE-запроса
        r = requests.delete(redirected_url)
        self.assertEqual(r.status_code, 204)
                
        #проверяем корректность удаления с помощью GET-запроса
        r = requests.get(redirected_url)
        self.assertEqual(r.status_code, 404)             

if __name__ == '__main__':
    current_dir = os.getcwd()
    #print('~~~~~', current_dir)
    database_path = os.path.dirname(current_dir)
    #print('~~~~~', database_path)
    #unitest_path = os.path.join(os.getcwd(), 'classes', 'uniTest')
    #print('~~~~~', unitest_path)
    sys.path.append(database_path)
    #database_path = os.path.join(os.getcwd(), 'classes')
    #sys.path.append(database_path)
    
    unittest.main()

