from package import login_manager
import shelve

@login_manager.user_loader
def load_user(user_id):
    userDict={}
    db = shelve.open('storage.db','c')
    try:
        userDict = db['Users']
    except:
        userDict = {}
        print("Error in retrieving Users from storage.db.")
    return userDict[int(user_id)]

def return_usernames(user_dict):
    usernames = []
    for value in list(user_dict.values()):
        usernames.append(value.get_username())
    return usernames

def is_correct_password(username, password, user_dict):    
    for value in list(user_dict.values()):
        if value.get_username() == username:
            if value.get_password() == password:
                return True
    return False

def return_user_id(username, user_dict):
    for value in list(user_dict.values()):
        if value.get_username() == username:
            return value.get_id()