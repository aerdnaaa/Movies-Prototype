class Rental:
    id = "R-1"
    def __init__(self, movie_class, rent_period, price):
        Rental.id = Rental.id[0] + str(int(Rental.id[1:]) + 1)
        self.__id = Rental.id
        self.__movie_class = movie_class
        self.__rent_period = rent_period
        self.__price = price
        self.__users = {}

    def get_id(self):
        return self.__id

    def get_movie_class(self):
        return self.__movie_class

    def get_rent_period(self):
        return self.__rent_period

    def get_price(self):
        return self.__price

    def get_users(self):
        return self.__users

    def set_movie_class(self, movie_class):
        self.__movie_class = movie_class
    
    def set_rent_period(self, rent_period):
        self.__rent_period = rent_period

    def set_price(self, price):
        self.__price = price
    
    def set_users(self, users):
        self.__users = users

    def set_all_attributes(self, movie_class, rent_period, price):
        self.__movie_class = movie_class
        self.__rent_period = rent_period
        self.__price = price