import json
import os

def requestUserCredentials():
    username = input("Enter username: ")
    password = input("Enter password: ")
    return username, password

def verifyUserCredentials(userName: str, password: str, oldData: list[dict]):
    # check if user exists
    for user in oldData:
        if user["userName"] == userName and user["password"] == password:
            return True
    return False

def load_users():
    filename = "users.json"
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump([], f)
    with open(filename, "r") as f:
        return json.load(f)

def save_users(users):
    filename = "users.json"
    with open(filename, "w") as f:
        json.dump(users, f, indent=2)

def login_menu():
    print("welcome to personal expense tracker")

    while True:
        print("1) Login")
        print("2) Register")
        print("3) quit")

        choose = input("Enter your choice: ")

        if choose == "1":
            users = load_users()
            user_name, password = requestUserCredentials()
            
            # verify data entered
            if verifyUserCredentials(user_name, password, users):
                print("Access granted")
                print("welcome to main menu")
 
                return user_name  
                
            else:
                print("Invalid username or password.")

        elif choose == "2":
            users = load_users()
            user_name, password = requestUserCredentials()
            
            # check if user exists already
            if any(user["userName"] == user_name for user in users):
                print("Username already exists. Choose a different one.")
            else:
                users.append({"userName": user_name, "password": password})
                save_users(users)
                print("Registration successful")

        elif choose == "3":
            print("thanks for using your personal expense tracker")
            return None 
        else:
            print("Invalid choice please choose the correct option")



