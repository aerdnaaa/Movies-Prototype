class Showtime:
    id = "S-1"
    def __init__(self, theatre_class, movie_class, show_period, timeslot, hall_number):
        Showtime.id = Showtime.id[0] + str(int(Showtime.id[1:]) + 1)
        self.__id = Showtime.id
        self.__theatre_class = theatre_class
        self.__movie_class = movie_class
        self.__show_period = show_period
        self.__timeslot = timeslot
        self.__hall_number = hall_number
        self.__seats_dict = {}

    def get_id(self):
        return self.__id

    def get_theatre_class(self):
        return self.__theatre_class

    def get_movie_class(self):
        return self.__movie_class

    def get_show_period(self):
        return self.__show_period

    def get_timeslot(self):
        return self.__timeslot

    def get_hall_number(self):
        return self.__hall_number

    def get_seats_dict(self):
        return self.__seats_dict

    def set_theatre_class(self, theatre_class):
        self.__theatre_class = theatre_class

    def set_movie_class(self, movie_class):
        self.__movie_class  = movie_class

    def set_show_period(self, show_period):
        self.__show_period = show_period

    def set_timeslot(self, timeslot):
        self.__timeslot = timeslot

    def set_hall_number(self, hall_number):
        self.__hall_number = hall_number

    def set_seats_dict(self, seats_dict):
        self.__seats_dict = seats_dict

    def set_all_attributes(self, theatre_class, movie_class, show_period, timeslot, hall_number):
        self.set_theatre_class(theatre_class)
        self.set_movie_class(movie_class)
        self.set_show_period(show_period)
        self.set_timeslot(timeslot)
        self.set_hall_number(hall_number)
