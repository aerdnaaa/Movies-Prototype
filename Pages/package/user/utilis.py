from package import login_manager
import shelve

@login_manager.user_loader
def load_user(user_id):
    userDict = {}
    db = shelve.open('shelve.db','c')
    try:
        userDict = db['Users']
    except:
        userDict = {}
    
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
            if value.get_password() == password:
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
    