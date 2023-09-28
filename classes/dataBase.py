import psycopg2

#ссылка на базу данных в виде 'postgresql://user:password@localhost/database'
#user="postgres", password="posTgress23", localhost = "127.0.0.1", database="rsoi_persons"
my_database = 'postgresql://postgres:posTgress23@127.0.0.1/rsoi_persons'

class Database:
    def __init__(self):
        self.my_database = my_database

    #создание таблицы в базе данных
    def DB_create_table(self):
        new_table = '''
                    CREATE TABLE IF NOT EXISTS Persons
                    (
                       id serial PRIMARY KEY,
                       name varchar(50) NOT NULL,
                       age integer,
                       address varchar(50),
                       work varchar(50)
                    );
                    '''
        #соединение с существующей базой данных и создание курсора
        conn = psycopg2.connect(self.my_database)
        cur = conn.cursor()

        #выполнение SQL-запроса к базе данных
        cur.execute(new_table)

        #сохранение изменений
        conn.commit()

        #закрытие соединений
        cur.close()
        conn.close()

    #получение информации о человеке по ID
    def DB_get_person(self, personId):
        conn = psycopg2.connect(self.my_database)
        cur = conn.cursor()

        cur.execute(f"SELECT * FROM Persons WHERE id={personId};")

        #возвращаем одну строку данных, информацию о человеке по ID
        person = cur.fetchone()

        cur.close()
        conn.close()

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

        return person[0]

    #изменение информации о человеке по ID
    def DB_update_person(self, new_info, personId):
        conn = psycopg2.connect(self.my_database)
        cur = conn.cursor()

        cur.execute(f"UPDATE Persons SET name = '{new_info['name']}', age = {new_info['age']}, address = '{new_info['address']}', work = '{new_info['work']}' WHERE id={personId} RETURNING id, name, age, address, work;")

        conn.commit()

        person = cur.fetchone()

        cur.close()
        conn.close()

        return person

    #удаление человека по ID
    def DB_delete_person(self, personId):
        conn = psycopg2.connect(self.my_database)
        cur = conn.cursor()

        cur.execute(f"DELETE FROM Persons WHERE id={personId};")

        #количество удалённых строк
        rows_deleted = cur.rowcount

        conn.commit()

        cur.close()
        conn.close()

        return rows_deleted
