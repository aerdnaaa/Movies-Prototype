from flask_login import UserMixin

class Person:
    def __init__(self, id, name, profile_picture, email, password):
        self.__id = id
        self.__name = name
        self.__profile_picture = profile_picture
        self.__email = email        
        self.__password = password
    def get_id(self):
        return self.__id
    def get_name(self):
        return self.__name
    def get_email(self):
        return self.__email
    def get_password(self):
        return self.__password
    def get_profile_picture(self):
        return self.__profile_picture
    def set_name(self, name):
        self.__name = name
    def set_profile_picture(self, profile_picture):
        self.__profile_picture = profile_picture
    def set_email(self,email):
        self.__email = email
    def set_password(self,password):
        self.__password = password


class Admin(Person, UserMixin):
    id = "A-1"
    def __init__(self, username, email, administrative_rights, password):
        Admin.id = Admin.id[0] + str(int(Admin.id[1:]) + 1)
        Person.__init__(self, Admin.id, username, "default.png", email, password)
        self.__username = username
        self.__email = email
        self.__administrative_rights = administrative_rights
        self.__password = password         

    def set_username(self, username):
        self.__username = username
    def set_administrative_rights(self, administrative_rights):
        self.__administrative_rights = administrative_rights

    def get_username(self):
        return self.__username
    def get_administrative_rights(self):
        return self.__administrative_rights

class User(Person, UserMixin):
    id = "U-1"
    def __init__(self, fullname, email, password, username, gender, DateofBirth):
        User.id = User.id[0] + str(int(User.id[1:]) + 1)
        Person.__init__(self,User.id,email,"default.png",email,password)        
        self.__fullname= fullname
        self.__password = password
        self.__username = username
        self.__gender = gender
        self.__DateofBirth = DateofBirth        
    def get_fullname(self):
        return self.__fullname
    def get_username(self):
        return self.__username
    def get_gender(self):
        return self.__gender
    def get_DateofBirth(self):
        return self.__DateofBirth
    def set_fullname(self,fullname):
        self.__fullname=fullname
    def set_username(self,username):
        self.__username = username
    def set_gender(self,gender):
        self.__gender = gender
    def set_DateofBirth(self,DateofBirth):
        self.__DateofBirth=DateofBirth


class AnonymousUser():
    id = "a0"
    def __init__(self):
        self.id = AnonymousUser.id
        self.fullname = ""
        self.email = ""
        self.DateofBirth = ""
        self.gender = ""
        self.card_number = ""
        self.card_name = ""
        self.expiry_date = ""
        self.cvc = ""
        self.seats = []
        AnonymousUser.id += 1




