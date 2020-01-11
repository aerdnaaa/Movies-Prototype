class Theatre:
    id = 0
    def __init__(self, theatre_name, theatre_image, number_of_halls):
        Theatre.id += 1
        self.__id = Theatre.id
        self.__theatre_name = theatre_name
        self.__theatre_image = theatre_image
        self.__number_of_halls = number_of_halls

    def get_id(self):
        return self.__id
    
    def get_theatre_name(self):
        return self.__theatre_name

    def get_theatre_image(self):
        return self.__theatre_image

    def get_number_of_halls(self):
        return self.__number_of_halls
    
    def set_theatre_name(self, theatre_name):
        self.__theatre_name = theatre_name

    def set_theatre_image(self, theatre_image):
        self.__theatre_name = theatre_image

    def set_number_of_halls(self, number_of_halls):
        self.__number_of_halls = number_of_halls

    def set_all_attributes(self, theatre_name, theatre_image, number_of_halls):
        self.__theatre_name = theatre_name
        self.__theatre_image = theatre_image
        self.__number_of_halls = number_of_halls
