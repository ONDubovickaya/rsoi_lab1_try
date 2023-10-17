import psycopg2

#ссылка на базу данных в виде 'postgresql://user:password@localhost/database'
#user="postgres", password="posTgress23", localhost = "127.0.0.1", database="rsoi_persons"
#my_database = ${{ secrets.DB_POSTGRES_URL }}

my_database = 'postgres://rsoi_persons_6qmq_user:WXXjkvg7vd3q1AE4ycIoTIOS9tlq7s8V@dpg-ckin5qse1qns738opfc0-a.oregon-postgres.render.com/rsoi_persons_6qmq'

#my_database = 'postgresql://postgres:posTgress23@127.0.0.1/rsoi_persons'
#my_database = 'postgres://rsoi_persons_6qmq_user:WXXjkvg7vd3q1AE4ycIoTIOS9tlq7s8V@dpg-ckin5qse1qns738opfc0-a.oregon-postgres.render.com/rsoi_persons_6qmq'
#my_database = psycopg2.connect(
       #host="127.0.0.1",
       #port="5432",
       #database="rsoi_persons",
       #user="postgres",
       #password="poTgress23"
   #)
   

class Database:
    def __init__(self):
        self.my_database = my_database

    #получение информации о человеке по его ID
    def DB_get_person(self, personId):
        conn = psycopg2.connect(self.my_database)
        cur = conn.cursor()

        cur.execute(f"SELECT * FROM Persons WHERE id={personId};")

        #возвращаем одну строку данных, информацию о человеке по ID
        person = cur.fetchone()

        cur.close()
        conn.close()

        if person is None:
            return None
        else:
            return person

    #информация о всех людях
    def DB_get_all_persons(self):
        conn = psycopg2.connect(self.my_database)
        cur = conn.cursor()

        cur.execute("SELECT * FROM Persons;")

        #возвращаем все строки данных в виде списка
        persons = cur.fetchall()

        cur.close()
        conn.close()

        if persons is None:
            return None
        else:
            return persons

    #добавление нового человека в таблицу
    def DB_add_person(self, new_person):
        conn = psycopg2.connect(self.my_database)
        cur = conn.cursor()

        cur.execute(f"INSERT INTO Persons (name, age, address, work) VALUES ('{new_person['name']}', {new_person['age']}, '{new_person['address']}', '{new_person['work']}') RETURNING id;")

        conn.commit()

        person = cur.fetchone()

        cur.close()
        conn.close()

        if person is None:
            return None
        else:
            return person[0]

    #изменение информации о человеке по его ID
    def DB_update_person(self, new_info, personId):
        conn = psycopg2.connect(self.my_database)
        cur = conn.cursor()

        cur.execute(f"UPDATE Persons SET name = '{new_info['name']}', age = {new_info['age']}, address = '{new_info['address']}', work = '{new_info['work']}' WHERE id={personId} RETURNING id, name, age, address, work;")

        conn.commit()

        person = cur.fetchone()

        cur.close()
        conn.close()

        if person is None:
            return None
        else:
            return person

    #удаление человека из таблицы по его ID
    def DB_delete_person(self, personId):
        conn = psycopg2.connect(self.my_database)
        cur = conn.cursor()

        cur.execute(f"SELECT id FROM Persons WHERE id={personId};")

        person_exists = cur.fetchone()

        if person_exists is None:
            cur.close()
            conn.close()
        else:
            cur.execute(f"DELETE FROM Persons WHERE id={personId} RETURNING *;")

            conn.commit()

            cur.close()
            conn.close()
            
