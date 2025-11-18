from Crypto.Cipher import AES
from secrets import token_bytes
import sqlite3
from argon2 import PasswordHasher
import os

# Hashing passwords: https://www.geeksforgeeks.org/python/how-to-hash-passwords-in-python/
# SQLite3 Table Creation: https://www.sqlitetutorial.net/sqlite-python/creating-tables/
# SQLite3 Table Creation: https://sqlite.org/lang_createtable.html
# SQLite3 Table Creation: https://sqlite.org/withoutrowid.html


#TODO 
# Create unique usernames for staff. 
# Be sure to check for whitespace at the end of name strings and remove as part of checking.

global lookup_db

ENCRYPTION_KEY = "aes.key"

def load_aes_key():
    if os.path.exists(ENCRYPTION_KEY):
        with open(ENCRYPTION_KEY, "rb") as k:
            return k.read()
    else:
        aes_key = token_bytes(32)
        with open(ENCRYPTION_KEY, "wb") as k:
            return k.write(aes_key)
        return aes_key

AES_KEY = load_aes_key()

# TODO Build Test
def new_user(username: str, f_name: str, l_name: str, role: str):
    """_summary_

    Args:
        username (str): _description_
        f_name (str): _description_
        l_name (str): _description_
        role (str): _description_
    """
    if not lookup_user(username):
        lookup_db = sqlite3.connect("lookup.db")
        lookup_cursor = lookup_db.cursor()
        # FIXME Need to create a unique username or find a way of generating this within the SQL Database.
        lookup_cursor.execute("INSERT INTO staff VALUES (?,?,?,?,?)", (username, f_name, l_name, hash_password("1234"), role))
        lookup_db.commit()
        lookup_db.close()
        return True
    else:
        return False
    
def delete_user(username: str):
    if lookup_user(username):
        lookup_db = sqlite3.connect("lookup.db")
        lookup_cursor = lookup_db.cursor()
        lookup_cursor.execute("DELETE FROM staff WHERE user_name = ?", (username,))
        lookup_db.commit()
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
        lookup_db.commit()
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
            lookup_db.commit()
            lookup_db.close()
            return True
        else:
            return False
    else:
        return False        
    
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
        lookup_db.commit()
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
    lookup_db = sqlite3.connect("lookup.db")
    lookup_cursor = lookup_db.cursor()
    create_db_tables(lookup_db)
    
    user_lookup = lookup_cursor.execute("SELECT * FROM staff WHERE user_name = ?", (username,))
    if len(user_lookup.fetchall()) == 0:
        lookup_db.close()
        return False
    else:
        return True

#FIXME This is a duplicate of the lookup_user function. Possibly can delete
# TODO Build Test
def check_staff_exists(username):
    """_summary_

    Args:
        username (_type_): _description_

    Returns:
        _type_: _description_
    """
    lookup_db = sqlite3.connect("lookup.db")
    lookup_cursor = lookup_db.cursor()
    create_db_tables(lookup_db)
    
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
        lookup_db = sqlite3.connect("lookup.db")
        lookup_cursor = lookup_db.cursor()
        lookup_cursor.execute("SELECT password FROM staff WHERE user_name = ?", (username,))
        password_check = lookup_cursor.fetchone()
        if ph.verify(password_check[0], password):
            role = lookup_cursor.execute("SELECT role FROM staff WHERE user_name = ?", (username,)).fetchone()
            print(role[0])
            return True, role[0]
        else:
            return False, None
    else:
        return False, None

def get_specialist_name(username):
    #FIXME Work out why this isn't returning properly
    lookup_db = sqlite3.connect("lookup.db")
    lookup_cursor = lookup_db.cursor()
    create_db_tables(lookup_db)
    print(username)
    if lookup_user(username):
        specialist = lookup_cursor.execute("SELECT first_name, last_name FROM staff WHERE role = Specialist AND UPPER(user_name) = ?", (username.upper(),)).fetchone()
        print(specialist)
        return f"{specialist[0]} {specialist[1]}"
    else:
        return "No Specialist"

#################################################################
def encrypt(data):
    cipher = AES.new(AES_KEY, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    
    return nonce, ciphertext, tag

def decrypt(nonce, ciphertext, tag):
    cipher = AES.new(AES_KEY, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    cipher.verify(tag)
    return plaintext.decode()

# Returns all patients in the database.
def return_all_patients():
    lookup_db = sqlite3.connect("lookup.db")
    lookup_cursor = lookup_db.cursor()
    create_db_tables(lookup_db)

    lookup_cursor.execute("SELECT * FROM patients")

    search_results = lookup_cursor.fetchall()

    lookup_db.close()

    return search_results   

def lookup_patient(patient_id):
    lookup_db = sqlite3.connect("lookup.db")
    lookup_cursor = lookup_db.cursor()

    patient_lookup = lookup_cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
    if len(patient_lookup.fetchall()) == 0:
        return False
    else:    
        return True   

def search_all_patients(f_name, l_name):
    # FIXME Still needs some work on how to appropriately link specialists with patient records.
    # Will likely need a join of some form between the staff, visits and patients tables. 
    lookup_db = sqlite3.connect("lookup.db")
    lookup_cursor = lookup_db.cursor()
    create_db_tables(lookup_db)

    lookup_cursor.execute("SELECT * FROM patients WHERE UPPER(first_name) = ? AND UPPER(last_name) = ?", (f_name.upper(), l_name.upper()))

    search_results = lookup_cursor.fetchall()

    lookup_db.close()

    return search_results

def search__specialist_patients(f_name, l_name):
    # FIXME Still needs some work on how to appropriately link specialists with patient records.
    # Will likely need a join of some form between the staff, visits and patients tables. 
    lookup_db = sqlite3.connect("lookup.db")
    lookup_cursor = lookup_db.cursor()
    create_db_tables(lookup_db)

    lookup_cursor.execute("SELECT * FROM patients WHERE first_name = ? AND last_name = ?", (f_name.upper(), l_name.upper()))

    search_results = lookup_cursor.fetchall()

    lookup_db.close()

    return search_results

# Returns all patient visits in the database in the database
def return_all_records():
    lookup_db = sqlite3.connect("lookup.db")
    lookup_cursor = lookup_db.cursor()
    create_db_tables(lookup_db)

    lookup_cursor.execute("SELECT * FROM records")

    search_results = lookup_cursor.fetchall()

    lookup_db.close()

    return search_results

def return_specialist_records(specialist_name: str):
    lookup_db = sqlite3.connect("lookup.db")
    lookup_cursor = lookup_db.cursor()
    create_db_tables(lookup_db)

    lookup_cursor.execute(
        "SELECT patients.first_name, patients.last_name, date_of_visit, visit_description FROM records INNER JOIN patients ON records.patient_id = patients.patient_id WHERE specialist_appointed = ?", (specialist_name,))
    
    search_results = lookup_cursor.fetchall()

    lookup_db.close()

    return search_results

def create_db_tables(database):
    lookup_cursor = database.cursor()

    #TODO Add data types and confirm dateTime data type
    lookup_cursor.execute(
        """CREATE TABLE IF NOT EXISTS patients (
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name,
        last_name,
        date_of_birth_nonce,
        date_of_birth_encrypt,
        date_of_birth_tag,
        address_nonce,
        address_encrypt,
        address_tag 
        ); """
    )
    
    lookup_cursor.execute(
        """CREATE TABLE IF NOT EXISTS records (
        visit_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER, 
        date_of_visit_nonce,
        date_of_visit_encrypt,
        date_of_visit_tag,
        visit_description_nonce,
        visit_description_encrypt,
        visit_description_tag,
        actions_taken_nonce, 
        actions_taken_encrypt, 
        actions_taken_tag, 
        specialist_appointed_nonce 
        specialist_appointed_encrypt 
        specialist_appointed_tag 
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

def return_patient_data(patient_id):
    """_summary_

    Args:
        patient_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    lookup_db = sqlite3.connect("lookup.db")
    lookup_cursor = lookup_db.cursor()

    patient_lookup = lookup_cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,)).fetchall()
    decrypted_data = [patient_lookup[0][0], patient_lookup[0][1]]
    for i in range(3,len(patient_lookup[0]),3):
        decrypted_data.append(decrypt(patient_lookup[0][i], patient_lookup[0][i+1], patient_lookup[0][i+2]))
    return decrypted_data 

def search_for_patient(first_name, last_name):
    """_summary_

    Args:
        first_name (_type_): _description_
        last_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    lookup_db = sqlite3.connect("lookup.db")
    lookup_cursor = lookup_db.cursor()

    patient_lookup = lookup_cursor.execute("SELECT * FROM patients WHERE UPPER(first_name) = ? AND UPPER(last_name) = ?", (first_name.upper(), last_name.upper())).fetchall()

    decrypted_data = []
    if len(patient_lookup) > 0:
        for i in range(len(patient_lookup)):
            patient_data = [patient_lookup[i][0], patient_lookup[i][1], patient_lookup[i][2]]
            for j in range(3,len(patient_lookup[i]),3):
                patient_data.append(decrypt(patient_lookup[i][j], patient_lookup[i][j+1], patient_lookup[i][j+2]))
            decrypted_data.append(patient_data)
    return decrypted_data

def add_patient_record(first_name: str, last_name, date_of_birth, address):
    """_summary_

    Args:
        first_name (_type_): _description_
        last_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    matching_patients = search_for_patient(first_name, last_name)
    if len(matching_patients) > 0:
        for i in range(len(matching_patients)):
            if address.upper() == matching_patients[i][3].upper():
                print("Matching Address")
                return None #FIXME Need to work out a good way of pushing to the front end that there was someone with a matching address
            else:
                continue
    print("Can add patient")

    lookup_db = sqlite3.connect("lookup.db")
    lookup_cursor = lookup_db.cursor()

    create_db_tables(lookup_db)

    dob_nonce, dob_cipher, dob_tag = encrypt(date_of_birth)
    address_nonce, address_cipher, address_tag = encrypt(address)

    insert = """INSERT INTO patients(first_name, last_name, date_of_birth_nonce, date_of_birth_encrypt, date_of_birth_tag, address_nonce, address_encrypt, address_tag)
    VALUES(?,?,?,?,?,?,?,?)"""

    lookup_cursor.execute(insert, (first_name, last_name, dob_nonce, dob_cipher, dob_tag, address_nonce, address_cipher, address_tag))
    lookup_db.commit()

    lookup_db.close()
    return True

#FIXME Needs some work
def delete_patient_record(patient_id):
    if delete_visit_record(patient_id):
        lookup_db = sqlite3.connect("lookup.db")
        lookup_cursor = lookup_db.cursor()
        lookup_cursor.execute("DELETE FROM patients WHERE patient_id = ?", (patient_id,))
        lookup_db.commit()
        lookup_db.close()
        return True        
    else:
        return False

#FIXME Needs some work
def modify_patient_record(patient_id, first_name, last_name, dob, address):
    if lookup_patient(patient_id):
        lookup_db = sqlite3.connect("lookup.db")
        lookup_cursor = lookup_db.cursor()
        lookup_cursor.execute(
            "UPDATE FROM patients SET first_name = ?, last_name = ?, date_of_birth = ?, address = ? WHERE patient_id = ?", 
            (first_name, last_name, dob, address, patient_id))
        lookup_db.commit()
        lookup_db.close()
        return True  
    else:
        return False

def return_patient_visits(patient_id):
    if lookup_patient(patient_id):
        lookup_db = sqlite3.connect("lookup.db")
        lookup_cursor = lookup_db.cursor()

        create_db_tables(lookup_db)

        results = lookup_cursor.execute("SELECT records.patient_id, first_name, last_name, date_of_visit, visit_description, actions_taken, specialist_appointed FROM records INNER JOIN patients ON records.patient_id = patients.patient_id WHERE records.patient_id = ?", (patient_id,)).fetchall()

        lookup_db.close()
        return results
    else:
        return None

#TODO Need to include encryption for values in here.  
#TODO Need to check for an existing entry that matches the entry attempting to be inserted. Do this in a similar way as was done for patients.
def add_visit_record(patient_id: int, date_of_visit: str, description: str, actions_taken: str, specialist: str):
    if lookup_patient(patient_id):
        lookup_db = sqlite3.connect("lookup.db")
        lookup_cursor = lookup_db.cursor()

        create_db_tables(lookup_db)
        
        insert = """INSERT INTO records(patient_id, date_of_visit, visit_description, actions_taken, specialist_appointed)
        VALUES(?,?,?,?,?)"""

        lookup_cursor.execute(insert, (patient_id, date_of_visit, description, actions_taken, specialist))
        lookup_db.commit()

        lookup_db.close()
        return True
    else:
        return False

def delete_visit_record(patient_id):
    if lookup_patient(patient_id):
        lookup_db = sqlite3.connect("lookup.db")
        lookup_cursor = lookup_db.cursor()
        lookup_cursor.execute("DELETE FROM records WHERE patient_id = ?", (patient_id,))
        lookup_db.commit()
        lookup_db.close()
        return True        
    else:
        return False

def main():
    #option = input("Press 1 to login: ")
    #while int(option) != 1:
    #    print("Invalid input!")
    #    option = input("Press 1 to login: ")

    #new_user("ZJ", "Zac", "Johnson", "Admin")
    #reset_password("ZJ")
    #print("Enter Login Details")
    #add_patient_record("Joe", "Bloggs", "05/03/05", "123 Fake St, Bloomington, SA")

    #add_visit_record(1, "1", "1", "ZJ")
    #add_visit_record(2, "1", "1", "")

    print(return_specialist_records("OSpec1"))



if __name__ == "__main__":
    #main()

    lookup_db = sqlite3.connect("lookup.db")
    lookup_cursor = lookup_db.cursor()
    
    lookup_cursor.execute("DROP TABLE patients")
    lookup_cursor.execute("DROP TABLE records")
    lookup_cursor.execute("DROP TABLE staff")
    
    create_db_tables(lookup_db)

    lookup_cursor.execute("INSERT INTO staff VALUES (?,?,?,?,?)", ('ZJohn1', 'Zachary', 'Johnson', hash_password("1234"), 'Administrator'))
    lookup_cursor.execute("INSERT INTO staff VALUES (?,?,?,?,?)", ('ZJohn2', 'Zachary', 'Johnson', hash_password("1234"), 'Doctor'))
    lookup_cursor.execute("INSERT INTO staff VALUES (?,?,?,?,?)", ('MSpec1', 'Mister', 'Specialist', hash_password("1234"), 'Specialist'))
    lookup_cursor.execute("INSERT INTO staff VALUES (?,?,?,?,?)", ('OSpec1', 'Other', 'Specialist', hash_password("1234"), 'Specialist'))
    
    
    
    insert = """INSERT INTO patients(first_name, 
    last_name,
    date_of_birth_nonce, date_of_birth_encrypt, date_of_birth_tag,
    address_nonce, address_encrypt, address_tag)
    VALUES(?,?,?,?,?,?,?,?)"""

    patients = [('Martha', 'Stewart', '01/01/99', '27 Crookswold Terrace, Richmond, NSW'),
                ('Joe', 'Bloggs', '05/03/05', '123 Fake St, Bloomington, SA'),
                ('Peter', 'White', '12/12/75', '44 Sunny Ave, Fantasia, QLD'),
                ('Joe', 'Bloggs', '10/07/92', '1 Coal Miners Rd, Winchester, WA')]

    for i in patients:
        f_name = i[0]
        l_name = i[1]
        dob_nonce, dob_cipher, dob_tag = encrypt(i[2])
        address_nonce, address_cipher, address_tag = encrypt(i[3])
        
        lookup_cursor.execute(insert, (f_name, l_name, dob_nonce, dob_cipher, dob_tag, address_nonce, address_cipher, address_tag))
    #lookup_cursor.execute(insert, ('Joe', 'Bloggs', '05/03/05', '123 Fake St, Bloomington, SA'))
    #lookup_cursor.execute(insert, ('Peter', 'White', '12/12/75', '44 Sunny Ave, Fantasia, QLD'))
    #lookup_cursor.execute(insert, ('Joe', 'Bloggs', '10/07/92', '1 Coal Miners Rd, Winchester, WA'))    
    
    
    #insert = """INSERT INTO records(patient_id, date_of_visit, visit_description, actions_taken, specialist_appointed) VALUES(?,?,?,?,?)"""
    #
    #lookup_cursor.execute(insert, ('2', '1', 'This is a specialist appointment and should be viewable by MSpec1', None, 'MSPec1'))
    #lookup_cursor.execute(insert, ('2', '1', 'This does not have a specialist and should not be viewable', None, None))
    #lookup_cursor.execute(insert, ('4', '1', 'Only this for Joe Bloggs 2 should be viewable by OSpec1', None, 'OSpec1'))
    #lookup_cursor.execute(insert, ('2', '1', 'This should only be viewable by OSpec1', None, 'OSpec1'))
    
    
    lookup_db.commit()
    lookup_db.close()
