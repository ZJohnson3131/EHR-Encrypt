import json
import sqlite3
from argon2 import PasswordHasher

# Hashing passwords: https://www.geeksforgeeks.org/python/how-to-hash-passwords-in-python/
# SQLite3 Table Creation: https://www.sqlitetutorial.net/sqlite-python/creating-tables/
# SQLite3 Table Creation: https://sqlite.org/lang_createtable.html
# SQLite3 Table Creation: https://sqlite.org/withoutrowid.html


#TODO
# Work on searching for individuals. Once found, work out how best to pass them back to the frontend functions and display.
# Work on role-based logins to limit information allowed for users to access when they login.
# Login function needs to also return the role of the user, this can then be saved in a global variable in the frontend for restricting access to files 
# Make sure all staff functions are updated for SQLite database

# TODO Create Database load script to build an initial database for an external user including patients, staff and visit records.

# Might need to build a find user function
# Start understanding what data to put into the database and how to build a SQLite database for housing data. 
# Store all data in PT for now before creating CT storage
# Work out how to store records of who modifies data and what was modified.

global lookup_db

#FIXME Make sure all SQL lookups are closing the database prior to returning the function.

# TODO Build Test
def new_user(username: str, f_name: str, l_name: str, role: str):
    """_summary_

    Args:
        username (str): _description_
        f_name (str): _description_
        l_name (str): _description_
        role (str): _description_
    """
    if lookup_user(username):
        lookup_db = sqlite3.connect("Lookup.db")
        lookup_cursor = lookup_db.cursor()
        # FIXME Need to create a unique username or find a way of generating this within the SQL Database.
        lookup_cursor.execute("INSERT INTO staff VALUES (?,?,?,?)", (username, f_name, l_name, role))
        lookup_db.close()
        return True
    else:
        return False
#TODO Build Test
def change_role(username: str, new_role: str):
    """_summary_

    Args:
        username (str): _description_
        new_role (str): _description_

    Returns:
        _type_: _description_
    """
    if lookup_user(username):
        lookup_db = sqlite3.connect("Lookup.db")
        lookup_cursor = lookup_db.cursor()
        lookup_cursor.execute("UPDATE staff SET role = ? WHERE user_name = ?", (new_role, username))
        lookup_db.close()
        return True
    else:
        return False        

#TODO Build Test
def change_password(username, current_password, new_password, confirm_password):
    """_summary_

    Args:
        username (_type_): _description_
        current_password (_type_): _description_
        new_password (_type_): _description_
        confirm_password (_type_): _description_

    Returns:
        _type_: _description_
    """
    ph = PasswordHasher()

    if lookup_user(username):
        lookup_db = sqlite3.connect("Lookup.db")
        lookup_cursor = lookup_db.cursor()
        
        password_check = lookup_cursor.execute("SELECT password FROM staff WHERE user_name = ?", (username,))
        
        if ph.verify(password_check, current_password) and new_password == confirm_password:
            lookup_cursor.execute("UPDATE staff SET password = ? WHERE user_name = ?", (hash_password(new_password), username))
            lookup_db.close()
            return True
        else:
            return False
    else:
        return False        

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
    
# TODO Build Test
def reset_password(username):
    """_summary_

    Args:
        username (_type_): _description_

    Returns:
        _type_: _description_
    """
    lookup_db = sqlite3.connect("Lookup.db")
    lookup_cursor = lookup_db.cursor()
    
    if lookup_user(username):
        lookup_cursor.execute("UPDATE staff SET password = ? WHERE user_name = ?", (hash_password("1234"), username))
        lookup_db.close()
        return True
    else:
        lookup_db.close()
        return False
   
# TODO Build Test    
def lookup_user(username):
    """_summary_

    Args:
        username (_type_): _description_

    Returns:
        _type_: _description_
    """
    lookup_db = sqlite3.connect("Lookup.db")
    lookup_cursor = lookup_db.cursor()
    create_db_tables(lookup_db)
    
    # If username is in datatable, the reset the password.
    user_lookup = lookup_cursor.execute("SELECT * FROM staff WHERE user_name = ?", (username,))
    if len(user_lookup.fetchall()) == 0:
        lookup_db.close()
        return False
    else:
        return True

# TODO Build Test
def check_staff_exists(username):
    """_summary_

    Args:
        username (_type_): _description_

    Returns:
        _type_: _description_
    """
    lookup_db = sqlite3.connect("Lookup.db")
    lookup_cursor = lookup_db.cursor()
    create_db_tables(lookup_db)
    
    # If username is in datatable, the reset the password.
    user_lookup = lookup_cursor.execute("SELECT * FROM staff WHERE user_name = ?", (username,))
    if len(user_lookup.fetchall()) == 0:
        return False
    else:    
        return True

# TODO Build Test
def hash_password(password: str):
    """_summary_

    Args:
        password (str): _description_

    Returns:
        _type_: _description_
    """
    ph = PasswordHasher()
    return ph.hash(password)    

# TODO Build Test
def login(username: str, password: str):
    """_summary_

    Args:
        username (str): _description_
        password (str): _description_

    Returns:
        _type_: _description_
    """
    if lookup_user(username):
        ph = PasswordHasher()
        lookup_db = sqlite3.connect("Lookup.db")
        lookup_cursor = lookup_db.cursor()
        password_check = lookup_cursor.execute("SELECT password FROM staff WHERE user_name = ?", (username,))
        if ph.verify(password, password_check):
            return True, lookup_cursor.execute("SELECT role FROM staff WHERE user_name = ?", (username,))
        else:
            return False
    else:
        return False

    ph = PasswordHasher()

    with open("login.json", "r") as file:
        users = json.load(file)
    
    for user in users["logins"]:
        try:
            if user["username"].lower() == username and ph.verify(user["password"], password):
                return True, user["role"]
            else:
                continue
        except Exception:
            return False

# Returns all patients in the database.
def return_all_patients():
    # Makes the connection and ensures that the tables are created prior to searching them
    lookup_db = sqlite3.connect("Lookup.db")
    lookup_cursor = lookup_db.cursor()
    create_db_tables(lookup_db)

    lookup_cursor.execute("SELECT * FROM patients")

    search_results = lookup_cursor.fetchall()

    lookup_db.close()

    return search_results   

def search_patients(f_name, l_name, search_role):
    # FIXME Still needs some work on how to appropriately link specialists with patient records.
    # Will likely need a join of some form between the staff, visits and patients tables. 
    # Makes the connection and ensures that the tables are created prior to searching them
    lookup_db = sqlite3.connect("Lookup.db")
    lookup_cursor = lookup_db.cursor()
    create_db_tables(lookup_db)

    if search_role == "Dr" or search_role == "Admin":
        lookup_cursor.execute("SELECT * FROM patients WHERE first_name = ? AND last_name = ?", (f_name.upper(), l_name.upper()))

    elif search_role == "Specialist":
        lookup_cursor.execute("SELECT * FROM patients WHERE first_name = ? AND last_name = ?", (f_name.upper(), l_name.upper()))
    search_results = lookup_cursor.fetchall()

    lookup_db.close()

    return search_results

# Returns all patient visits in the database in the database
def return_all_records():
    # Makes the connection and ensures that the tables are created prior to searching them
    lookup_db = sqlite3.connect("Lookup.db")
    lookup_cursor = lookup_db.cursor()
    create_db_tables(lookup_db)

    lookup_cursor.execute("SELECT * FROM records")

    search_results = lookup_cursor.fetchall()

    lookup_db.close()

    return search_results

#TODO This will return all records that the specialist is associated with. 
# Maybe I need to consider searching by patient_id to return all records for a particular patient that they have been referred to the particular specialist for.
def return_specialist_records(specialist_name: str):
    # Makes the connection and ensures that the tables are created prior to searching them
    lookup_db = sqlite3.connect("Lookup.db")
    lookup_cursor = lookup_db.cursor()
    create_db_tables(lookup_db)

    search_sql = "SELECT * FROM records WHERE specialist_appointed = ?"
    lookup_cursor.execute("SELECT * FROM records WHERE specialist_appointed = ?", (specialist_name,))
    
    search_results = lookup_cursor.fetchall()

    lookup_db.close()

    return search_results

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
        ); """
    )
    
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
    
    lookup_cursor.execute(
        """CREATE TABLE IF NOT EXISTS staff (
        user_name PRIMARY KEY, 
        first_name,
        last_name,
        password,
        role
        );
        """
    )
    return

def add_patient_record(first_name: str, last_name, date_of_birth, address, allergies):
    lookup_db = sqlite3.connect("lookup.db")
    lookup_cursor = lookup_db.cursor()

    create_db_tables(lookup_db)

    lookup_cursor.execute("SELECT count(*) FROM patients WHERE first_name = ? AND last_name = ? AND address = ?", (first_name, last_name, address))
    data=lookup_cursor.fetchall()
    
    if len(data)==0:
        insert = """INSERT INTO patients(first_name, last_name, date_of_birth, address, allergies)
        VALUES(?,?,?,?,?)"""

        lookup_cursor.execute(insert, (first_name, last_name, date_of_birth, address, allergies))
        lookup_db.commit()
    else:
        print("User already exists in database.")

    lookup_db.close()
    return

def delete_visit_record():
    raise NotImplementedError

def delete_patient_record():
    # This will need to check through all patient visit records first and then oce all of them are deleted, it can delete the patient.
    raise NotImplementedError

def modify_patient_record():
    raise NotImplementedError

#TODO Need to set a default value of "" or whatever works for a NULL value when inputting the specialist.
#TODO Need to include encryption for values in here.  
#TODO Need to ensure that only patients who exist in the database can have a visit attached. 
#TODO Need to check for an existing entry that matches the entry attempting to be inserted. Do this in a similar way as was done for patients.
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

    search_patients('Z', 'J')
    #print("Enter Login Details")
    #add_patient_record("Z", "J", "1", "2", "None")

    #add_visit_record(1, "1", "1", "ZJ")
    #add_visit_record(2, "1", "1", "")

    #return_specialist_records("ZJ")



if __name__ == "__main__":
    main()