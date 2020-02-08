import shelve, datetime
from package.showtime.classes import Showtime, SeatClass

def return_available_theatres_and_hall():
    db = shelve.open('shelve.db', 'c')
    try:
        Movie_theatre_dict = db["movie_theatre"]
    except:
        Movie_theatre_dict = {}
        db["movie_theatre"] = Movie_theatre_dict
    theatres = []        
    for value in list(Movie_theatre_dict.values()):
        theatres.append((value.get_id(), value.get_theatre_name()))
    halls = []
    try:
        for i in range(1,list(Movie_theatre_dict.values())[0].get_number_of_halls()+1):
            halls.append((str(i),str(i)))
    except:
        halls = []
    return theatres, halls


def return_available_movie_title():
    db = shelve.open('shelve.db', 'c')
    try:
        Movies_dict = db["movies"]
    except:
        Movies_dict = {}
        db["movies"] = Movies_dict
    movies = []
    for value in list(Movies_dict.values()):
        movies.append((value.get_id(), value.get_movie_name()))
    return movies

def return_timeslots():
    return [("9am to 12pm","9am to 12pm"), ("12pm to 3pm", "12pm to 3pm"), ("3pm to 6pm", "3pm to 6pm"), ("6pm to 9pm", "6pm to 9pm"), ("9pm to 12am", "9pm to 12am")]

def return_date_period(start_date_data, end_date_data):
    start_date = datetime.datetime.strptime(start_date_data, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date_data, "%Y-%m-%d").date()
    day = datetime.timedelta(days=1)
    list_of_dates = []
    while start_date <= end_date:
        list_of_dates.append(start_date)
        start_date += day  
    return list_of_dates

def return_movie_theatre_class(theatre_id_data):
    db = shelve.open('shelve.db', 'c')
    Movie_theatre_dict = db["movie_theatre"]
    return Movie_theatre_dict[theatre_id_data]

def return_movie_class(movie_id):
    db = shelve.open('shelve.db', 'c')
    Movies_dict = db["movies"]
    return Movies_dict[movie_id]

def set_seat_class_dict(showtime_class):
    db = shelve.open('shelve.db', 'c')
    seat_dict = db["Seats"]
    seat_class_dict = {}
    for date in showtime_class.get_show_period():
        for timeslot in showtime_class.get_timeslot():            
            seat_class = SeatClass(date, timeslot, showtime_class.get_hall_number(), seat_dict)    
            seat_class_dict[seat_class.id] = seat_class        
    showtime_class.set_seats_class(seat_class_dict) 
    return showtime_class

def make_showtime(form, id):
    if id == "new":
        showtime_class = Showtime(return_movie_theatre_class(form.theatre_name.data), return_movie_class(form.movie_title.data), return_date_period(form.showtime_start_date.data, form.showtime_end_date.data), form.timeslot.data, form.hall_number.data)
        return set_seat_class_dict(showtime_class)
    else:
        db = shelve.open('shelve.db', 'c')
        Showtime_dict = db["showtime"]
        showtime_class = Showtime_dict[id]
        showtime_class.set_all_attributes(return_movie_theatre_class(form.theatre_name.data), return_movie_class(form.movie_title.data), return_date_period(form.showtime_start_date.data, form.showtime_end_date.data), form.timeslot.data, form.hall_number.data)
        return set_seat_class_dict(showtime_class)