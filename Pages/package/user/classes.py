class Person:
    def __init__(self, id, name, profile_picture, email, password):
        self.id = id
        self.name = name
        self.profile_picture = profile_picture
        self.email = email        
        self.password = password

class Admin(Person):
    id = 0
    def __init__(self, username, email, administrative_rights, password):
        Admin.id += 1
        Person.__init__(self, Admin.id, username, "default.png", email, password)
        self.administrative_rights = administrative_rights        

class User(Person):
    id = 0
    def __init__(self,firstname,lastname,email,password,username,gender,DateofBirth):
        User.id += 1
        Person.__init__(self,User.id,0,0,0,0)
        self.__email = email
        self.__firstname = firstname
        self.__lastname = lastname
        self.__password = password
        self.__username = username
        self.__gender = gender
        self.___DateofBirth = DateofBirth
        self.__userID = User.id

    
    def get_userID(self):
        return self.__userID
    # def get_profilepicture(self):
    #     return self.profile_picture
    def get_firstname(self):
        return self.__firstname
    def get_lastname(self):
        return self.__lastname
    def get_email(self):
        return self.__email
    def get_password(self):
        return self.__password
    def get_username(self):
        return self.__username
    def get_gender(self):
        return self.__gender
    def get_DateofBirth(self):
        return self.__DateofBirth

    def set_userID(self,userID):
        self.__userID = userID
    # def set_profilepicture(self,profile_picture):
    #     self.__profile_picture = profile_picture
    def set_firstname(self,firstname):
        self.__firstname=firstname
    def set_lastname(self,lastname):
        self.__lastname=lastname
    def set_email(self,email):
        self.__email = email
    def set_password(self,password):
        self.__password=password
    def set_username(self,username):
        self.__username = username
    def set_gender(self,gender):
        self.__gender = gender
    def set_DateofBirth(self,DateofBirth):
        self.__DateofBirth=DateofBirth




    




