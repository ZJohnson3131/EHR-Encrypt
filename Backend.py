import json
from argon2 import PasswordHasher

# Hashing passwords: https://www.geeksforgeeks.org/python/how-to-hash-passwords-in-python/

#TODO
# Might need to build a find user function
# Start understanding what data to put into the database and how to build a SQLite database for housing data. 
# Hash passwords for user logins
# Store all data in PT for now before creating CT storage


#TODO Check if user already exists
def new_user(username: str, role: str):
    user = {
        "username": username, 
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

def main():
    #option = input("Press 1 to login: ")
    #while int(option) != 1:
    #    print("Invalid input!")
    #    option = input("Press 1 to login: ")

    #print("Enter Login Details")
    reset_password("ZJOH")
    change_password()
    pass

if __name__ == "__main__":
    main()