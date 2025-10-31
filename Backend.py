import json

#TODO
# Might need to build a find user function
# Start understanding what data to put into the database and how to build a SQLite database for housing data. 
# Hash passwords for user logins
# Store all data in PT for now before creating CT storage


#TODO Check if user already exists
def new_user(username: str, role: str):
    user = {
        "username": username, 
        "password": reset_password(username),
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
            return
        else:
            continue
    
    print("User not found in database. No changes made.")
    return

def change_password():
    username = input("Please enter your username: ")
    current_password = input("Please enter your current password: ")
    new_password = input("Please enter your new password: ")

    with open("login.json", "r") as file:
        users = json.load(file)

    for user in users["logins"]:
        if user["username"] == username and user["password"] == current_password:
            user["password"] = new_password
            
            with open("login.json", "w") as file:
                json.dump(users, file, indent=4)
                print("Password successfully changed.")
            return
        else:
            continue
    
    print("User or password were incorrect. No changes made.")
    return

def reset_password(username):
    with open("login.json", "r") as file:
        users = json.load(file)

    for user in users["logins"]:
        if user["username"] == username:
            user["password"] = "1234"
            
            with open("login.json", "w") as file:
                json.dump(users, file, indent=4)
            print("Password successfully reset.")
            return
        else:
            continue
    
    print("User not found in database. No changes made.")
    return
    

#TODO Needs some work I believe
def login():    
    with open("login.json", "r") as file:
        login_details = json.load(file)
    print(login_details)
    """
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    """
    
    pass



def main():
    #option = input("Press 1 to login: ")
    #while int(option) != 1:
    #    print("Invalid input!")
    #    option = input("Press 1 to login: ")

    #print("Enter Login Details")
    change_password()
    pass

if __name__ == "__main__":
    main()