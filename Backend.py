import json
import sqlite3
from argon2 import PasswordHasher

# Hashing passwords: https://www.geeksforgeeks.org/python/how-to-hash-passwords-in-python/
# SQLite3 Table Creation: https://www.sqlitetutorial.net/sqlite-python/creating-tables/
# SQLite3 Table Creation: https://sqlite.org/lang_createtable.html
# SQLite3 Table Creation: https://sqlite.org/withoutrowid.html


#TODO
# Might need to build a find user function
# Start understanding what data to put into the database and how to build a SQLite database for housing data. 
# Hash passwords for user logins
# Store all data in PT for now before creating CT storage

global lookup_db

#TODO Check if user already exists
def new_user(username: str, name: str, role: str):
    user = {
        "username": username, 
        "name": name,
        "password": hash_password("1234"),
        "role": role
    }

    with open("login.json", "r") as file:
        users = json.load(file)
        users["logins"].append(user)
    print(users)

    with open("login.json", "w") as file:
        json.dump(users, file, indent=4)
    return

def change_role(username: str, new_role: str):
    with open("login.json", "r") as file:
        users = json.load(file)

    for user in users["logins"]:
        if user["username"] == username:
            user["role"] = new_role
            
            with open("login.json", "w") as file:
                json.dump(users, file, indent=4)
            return True
        else:
            continue
    
    print("User not found in database. No changes made.")
    return False

def change_password():
    username = input("Please enter your username: ")
    current_password = input("Please enter your current password: ")

    ph = PasswordHasher()

    with open("login.json", "r") as file:
        users = json.load(file)

    for user in users["logins"]:
        try:
            if user["username"] == username and ph.verify(user["password"], current_password):
                new_password = input("Please enter your new password: ")
                user["password"] = hash_password(new_password)
                
                with open("login.json", "w") as file:
                    json.dump(users, file, indent=4)
                    print("Password successfully changed.")
                return True
            else:
                continue
        except Exception:
            print("User or password were incorrect. No changes made.")
            return False
    return

def reset_password(username):
    with open("login.json", "r") as file:
        users = json.load(file)

    for user in users["logins"]:
        if user["username"] == username:
            user["password"] = hash_password("1234")
            
            with open("login.json", "w") as file:
                json.dump(users, file, indent=4)
            print("Password successfully reset.")
            return True
        else:
            continue
    print("User not found in database. No changes made.")
    return False

def hash_password(password: str):
    ph = PasswordHasher()
    return ph.hash(password)    

#TODO Test Function
def login():
    ph = PasswordHasher()
    
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    with open("login.json", "r") as file:
        users = json.load(file)
    
    for user in users["logins"]:
        try:
            if user["username"] == username and ph.verify(user["password"], password):
                return True
            else:
                continue
        except Exception:
            return False

#TODO Transfer this to the SQL Database
def return_all_records():
    with open("records.json", "r") as file:
        records = json.load(file)
    print(records)

#TODO Transfer this to the SQL Database
def return_specialist_records(specialist_name: str):
    records_found = []
    with open("records.json", "r") as file:
        records = json.load(file)
    for record in records["record"]:
        if record["Specialist"].lower() == specialist_name.lower():
            records_found.append(record)
    return records_found


def create_db_tables(database):
    lookup_cursor = database.cursor()

    # Creates table if the database is brand new
    #TODO Add data types and confirm dateTime data type
    lookup_cursor.execute(
        """CREATE TABLE IF NOT EXISTS patients (
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name ,
        last_name ,
        date_of_birth ,
        address ,
        allergies 
        ); """)
    
    lookup_cursor.execute(
        """CREATE TABLE IF NOT EXISTS records (
        visit_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER, 
        date_of_visit ,
        visit_description ,
        specialist_appointed 
        );
        """
    )
    return

#TODO Need a way to check if patient already exists in database
def add_patient_record(first_name: str, last_name, date_of_birth, address, allergies):
    lookup_db = sqlite3.connect("lookup.db")
    lookup_cursor = lookup_db.cursor()

    create_db_tables(lookup_db)

    insert = """INSERT INTO patients(first_name, last_name, date_of_birth, address, allergies)
    VALUES(?,?,?,?,?)"""

    lookup_cursor.execute(insert, (first_name, last_name, date_of_birth, address, allergies))
    lookup_db.commit()
    
    lookup_db.close()

#TODO Implement this
def delete_patient_record():
    raise NotImplementedError

#TODO Implement this
def modify_patient_record():
    raise NotImplementedError

#TODO Need to set a default value of "" or whatever works for a NULL value when inputting the specialist.
#TODO Need to include encryption for values in here.  
#TODO Need to ensure that only patients who exist in the database can have a visit attached. 
def add_visit_record(patient_id: int, date_of_visit: str, description: str, specialist: str):
    lookup_db = sqlite3.connect("lookup.db")
    lookup_cursor = lookup_db.cursor()

    create_db_tables(lookup_db)
    
    insert = """INSERT INTO records(patient_id, date_of_visit, visit_description, specialist_appointed)
    VALUES(?,?,?,?)"""

    lookup_cursor.execute(insert, (patient_id, date_of_visit, description, specialist))
    lookup_db.commit()

    lookup_db.close()

    return

def main():
    #option = input("Press 1 to login: ")
    #while int(option) != 1:
    #    print("Invalid input!")
    #    option = input("Press 1 to login: ")

    #print("Enter Login Details")
    add_patient_record("Z", "J", "1", "2", "None")



if __name__ == "__main__":
    main()