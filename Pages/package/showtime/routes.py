from flask import Blueprint
from flask import render_template, request, redirect, url_for
from package.showtime.classes import Showtime
from package.showtime.forms import CreateShowtime, ModifyShowtime
import shelve, datetime

showtime_blueprint = Blueprint("showtime", __name__)

#* User Showtime
@showtime_blueprint.route("/bookmovie")
def bookmovie():
    # Date
    base = datetime.date.today()
    date_list = [base + datetime.timedelta(days=x) for x in range(7)]
    date_dict = {}
    day_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for date in date_list:
        year, month, day = str(date).split('-')
        value = day_list[date.weekday()] + ', ' + day + ' ' + month_list[int(month)-1] + ' ' + year
        date_dict[str(date)] = value

    # Movie
    db = shelve.open("shelve.db", "c")
    try:
        movie_dict = db["movies"]
    except:
        movie_dict = {}
        db["movies"] = movie_dict
    
    # Theatres
    try:
        theatre_dict = db["movie_theatre"]
    except:
        theatre_dict = {}
        db["movie_theatre"] = theatre_dict
    db.close()
    
    return render_template("User/showtime/showtime.html", title="Book Movie", date_dict=date_dict, movie_dict=movie_dict, theatre_dict=theatre_dict)

@showtime_blueprint.route("/bookmovieseats")
def bookmovieseats():
    return render_template("User/showtime/bookmovieseats.html", title="Buying Seats")


@showtime_blueprint.route("/admin/showtime")
def admin_showtime():
    db = shelve.open('shelve.db', 'c')
    try:
        Showtime_dict = db["showtime"]        
    except:
        Showtime_dict = {}
        db["showtime"] = Showtime_dict
    db.close()
    return render_template("Admin/showtime/showtime.html", title="Showtimes", Showtime_dict=Showtime_dict)

@showtime_blueprint.route("/admin/showtime/add_showtime", methods=["GET","POST"])
def add_showtime():
    form = CreateShowtime()
    db = shelve.open('shelve.db', 'c')
    try:
        Showtime_dict = db["showtime"]
        Movie_theatre_dict = db["movie_theatre"]
        Movies_dict = db["movies"]
        Showtime.id = list(Showtime_dict.values())[-1].get_id()
    except:
        Showtime_dict = {}
        db["showtime"] = Showtime_dict
        # Movie_theatre_dict = {}
        # db["movie_theatre"] = Movie_theatre_dict    
        # Movies_dict = {}
        # db["movies"] = Movies_dict
    theatres = [("","")]        
    for value in list(Movie_theatre_dict.values()):
        theatres.append((value.get_id(), value.get_theatre_name()))
    form.theatre_name.choices = theatres    
    movies = [("","")]
    for value in list(Movies_dict.values()):
        movies.append((value.get_id(), value.get_movie_name()))
    form.movie_title.choices = movies
    timeslots = [("1","9am to 12pm"), ("2", "12pm to 3pm"), ("3", "3pm to 6pm"), ("4", "6pm to 9pm"), ("5", "9pm to 12am")]
    form.timeslot.choices = timeslots
    halls = [("","")]
    for i in range(1,6):
        halls.append((str(i),str(i)))
    form.hall_number.choices = halls
    timeslot_dict = {"1":"9am to 12pm", "2":"12pm to 3pm", "3":"3pm to 6pm", "4":"6pm to 9pm", "5":"9pm to 12am"}
    if request.method == "POST":
        theatre_name = int(form.theatre_name.data)
        theatre_class = Movie_theatre_dict[theatre_name]
        movie_title = int(form.movie_title.data)
        movie_class = Movies_dict[movie_title]
        timeslot_list = form.timeslot.data
        timeslot_data = []
        for timeslot in timeslot_list:
            timeslot_data.append(timeslot_dict[timeslot])
        show_period = form.showtime_start_date.data + " - " + form.showtime_end_date.data
        hall_number = int(form.hall_number.data)
        showtime_class = Showtime(theatre_class, movie_class, show_period, timeslot_data, hall_number)
        showtime_id = showtime_class.get_id()
        Showtime_dict[showtime_id] = showtime_class
        db["showtime"] = Showtime_dict
        db.close()
        return redirect(url_for("showtime.admin_showtime"))
    elif request.method == "GET":
        form.theatre_name.data = ""
        form.movie_title.data = ""
        form.timeslot.data = ""
        form.showtime_start_date.data = ""
        form.showtime_end_date.data = ""
        form.hall_number.data = ""
        db.close()
    return render_template("Admin/showtime/add_showtime.html", title="Add Showtime", form=form)

@showtime_blueprint.route("/admin/showtime/modify_showtime/<showtime_id>", methods=["GET","POST"])
def modify_showtime(showtime_id):
    showtime_id = int(showtime_id)
    form = ModifyShowtime()
    db = shelve.open('shelve.db', 'c')
    try:
        Showtime_dict = db["showtime"]
        Movie_theatre_dict = db["movie_theatre"]
        Movies_dict = db["movies"]
    except:
        Showtime_dict = {}
        db["showtime"] = Showtime_dict
        Movie_theatre_dict = {}
        db["movie_theatre"] = Movie_theatre_dict    
        Movies_dict = {}
        db["movies"] = Movies_dict
    showtime_class = Showtime_dict[showtime_id]
    theatres = [("","")]        
    for value in list(Movie_theatre_dict.values()):
        theatres.append((value.get_id(), value.get_theatre_name()))
    form.theatre_name.choices = theatres    
    movies = [("","")]
    for value in list(Movies_dict.values()):
        movies.append((value.get_id(), value.get_movie_name()))
    form.movie_title.choices = movies
    timeslots = [("1","9am to 12pm"), ("2", "12pm to 3pm"), ("3", "3pm to 6pm"), ("4", "6pm to 9pm"), ("5", "9pm to 12am")]
    form.timeslot.choices = timeslots
    halls = [("","")]
    for i in range(1,6):
        halls.append((str(i),str(i)))
    form.hall_number.choices = halls
    timeslot_dict = {"1":"9am to 12pm", "2":"12pm to 3pm", "3":"3pm to 6pm", "4":"6pm to 9pm", "5":"9pm to 12am"}
    if request.method == "GET":
        form.theatre_name.data = str(showtime_class.get_theatre_class().get_id())
        form.movie_title.data = str(showtime_class.get_movie_class().get_id())
        form.timeslot.data = ""
        form.showtime_start_date.data, form.showtime_end_date.data = showtime_class.get_show_period().split(" - ")
        form.hall_number.data = str(showtime_class.get_hall_number())
    elif request.method == "POST":
        theatre_class = Movie_theatre_dict[int(form.theatre_name.data)]
        movie_class = Movies_dict[int(form.movie_title.data)]
        timeslot_list = form.timeslot.data
        timeslot_data = []
        for timeslot in timeslot_list:
            timeslot_data.append(timeslot_dict[timeslot])
        show_period = form.showtime_start_date.data + " - " + form.showtime_end_date.data
        hall_number = form.hall_number.data
        showtime_class.set_all_attributes(theatre_class, movie_class, timeslot_data, show_period, hall_number)
        return redirect(url_for("showtime.admin_showtime"))
    return render_template("/Admin/showtime/modify_showtime.html", title="Modify Showtime", form=form)

@showtime_blueprint.route("/admin/showtime/delete_showtime", methods=["GET","POST"])
def delete_showtime():
    db = shelve.open('shelve.db', 'c')
    try:
        Showtime_dict = db["showtime"]
        Deleted_list = db["deleted_showtime"]
    except:
        Showtime_dict = {}
        Deleted_list = []
        db["showtime"] = Showtime_dict
        db["deleted_showtime"] = Deleted_list
    list_of_to_be_deleted_showtimes = request.json
    for showtime_id in list_of_to_be_deleted_showtimes:
        showtime_class = Showtime_dict[int(showtime_id)]
        Deleted_list.append([showtime_class, datetime.date.today()])
        del Showtime_dict[int(showtime_id)]
    db["showtime"] = Showtime_dict
    db["deleted_showtime"] = Deleted_list
    db.close()
    return redirect(url_for("showtime.admin_showtime"))