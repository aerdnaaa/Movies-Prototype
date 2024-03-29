from package import login_manager, bcrypt, app
import shelve, os, secrets

@login_manager.user_loader
def load_user(user_id):    
    db = shelve.open('shelve.db','c')
    userDict = db['Users']    
    db.close()
    try:
        return userDict[user_id]
    except:
        return userDict    
 
def return_emails(user_dict):
    emails = []
    for value in list(user_dict.values()):
        emails.append(value.get_email())    
    return emails

def is_correct_password(email, password, user_dict):    
    for value in list(user_dict.values()):
        if value.get_email() == email:
            print(value.get_password())
            if bcrypt.check_password_hash(value.get_password(), password):
                return True
    return False

def return_user_id(email, user_dict):
    for value in list(user_dict.values()):
        if value.get_email() == email:
            return value.get_id()

def save_picture(form_picture, path):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images/' + path, picture_fn)
    form_picture.save(picture_path)
    return picture_fn
    