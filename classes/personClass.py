from classes.dataBase import Database

class Person:
    def __init__(self):
        self.database = Database()
        self.person = {
            "id": None,
            "name": None,
            "age": None,
            "address": None,
            "work": None
        }

    def PC_person_info(self, info_db):
        if len(info_db) != 5:
            raise Exception("Info doesn't contain 5 positions")

        self.person = {
            "id": int(info_db[0]),
            "name": str(info_db[1]),
            "age": int(info_db[2]),
            "address": str(info_db[3]),
            "work": str(info_db[4])
        }

    def PC_get_person(self, personId):
        info_db = self.database.DB_get_person(personId)

        #проверка наличия данных в базе данных info_db
        if not info_db:
            return None

        self.PC_person_info(info_db)

        return self.person

    def PC_get_all_persons(self):
        info_db = self.database.DB_get_all_persons()
        persons = []

        if not info_db:
            return None

        for i in info_db:
            self.PC_person_info(i)
            persons.append(self.person)

        return persons

    def PC_create_person(self, person):
        personId = self.database.DB_add_person(person)
        info_db = self.database.DB_get_person(personId)

        if not info_db:
            return None

        return personId

    def PC_update_person(self, new_person, personId):
        info_db = self.database.DB_get_person(personId)

        if not info_db:
            return 1

        self.PC_person_info(info_db)
        self.person.update(new_person)

        person = self.database.DB_update_person(self.person, personId)
        self.PC_person_info(person)

        return 0

    def PC_delete_person(self, personId):
        info_db = self.database.DB_get_person(personId)

        if not info_db:
            return 0

        self.database.DB_delete_person(personId)

        return personId
