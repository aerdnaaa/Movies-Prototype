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


