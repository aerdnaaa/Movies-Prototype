class Person:
    def __init__(self, id, name, profile_picture):
        self.id = id
        self.name = name
        self.profile_picture = profile_picture

class Admin(Person):
    id = 0
    def __init__(self, name, profile_picture, admininstrative_rights):
        Admin.id += 1
        Person.__init__(Admin.id, name, profile_picture)
        self.admininstrative_rights = admininstrative_rights

class User(Person):
    id = 0
    def __init__(self,profile_picture,firstname,lastname,email,password):
        User.id += 1
        Person.__init__(User.id,profile_picture)
        self.__email = email
        self.__firstname = firstname
        self.__lastname = lastname
        self.__password = password
        
    def get_userID(self):
        return User.id
    def get_profilepicture(self):
        return self.profile_picture
    def get_firstname(self):
        return self.firstname
    def get_lastname(self):
        return self.lastname
    def get_email(self):
        return self.email
    def get_password(self):
        return self.password

    def set_userID(self,userID):
        User.id = userID
    def set_profilepicture(self,profile_picture):
        self.__profile_picture = profile_picture
    def set_firstname(self,firstname):
        self.__firstname=firstname
    def set_lastname(self,lastname):
        self.__lastname=lastname
    def set_email(self,email):
        self.__email = email
    def set_password(self,password):
        self.__password=password




    




