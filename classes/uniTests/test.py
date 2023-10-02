import unittest
import requests

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

    def test_post_get(self):
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
    def test_post_patch(self):
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
    def test_post_delete(self):
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