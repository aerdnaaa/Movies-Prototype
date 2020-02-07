from flask import Blueprint
from flask import render_template, request, redirect, url_for, jsonify
from flask_login import current_user, login_required
from package.showtime.classes import Showtime, SeatClass
from package.showtime.forms import CreateShowtime, ModifyShowtime, PaymentForm
from package.utilis import check_admin
from package.user.classes import AnonymousUser
from package import stripe_keys
import shelve, datetime, stripe

showtime_blueprint = Blueprint("showtime", __name__)

#* User Showtime
@showtime_blueprint.route("/bookmovie", methods=["GET", "POST"])
def bookmovie():
    # Date
    base = datetime.date.today()
    date_list = [base + datetime.timedelta(days=x) for x in range(7)]
    date_dict = {}    
    for date in date_list:        
        value = date.strftime("%a, %d %b %Y")
        date_dict[date] = value

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

    # Showtime
    try:
        Showtime_dict = db["showtime"]
    except:
        Showtime_dict = {}
        db["showtime"] = Showtime_dict
    
    # Genre List
    genre_list = db["genre_list"]
    db.close()
    theatre_movie_showtime_dict = {}

    for key in Showtime_dict:
        showtime_class = Showtime_dict[key]
        theatre_class = showtime_class.get_theatre_class()
        theatre_name = theatre_class.get_theatre_name()
        theatre_movie_showtime_list = theatre_movie_showtime_dict.get(theatre_name, [])            
        theatre_movie_showtime_list.append(showtime_class)
        theatre_movie_showtime_dict[theatre_name] = theatre_movie_showtime_list        
    return render_template("User 2/showtime.html", title="Book Movie", date_dict=date_dict, Movies_dict=movie_dict, genre_list=genre_list, theatre_dict=theatre_dict, theatre_movie_showtime_dict=theatre_movie_showtime_dict) 

@showtime_blueprint.route("/bookmovieseats/<showtime_id>/<timeslot>/<date>")
def bookmovieseats(showtime_id, timeslot, date):    
    db = shelve.open('shelve.db', 'c')
    # Showtime
    try:
        Showtime_dict = db["showtime"]
    except:
        Showtime_dict = {}
        db["showtime"] = Showtime_dict    

    showtime_class = Showtime_dict[showtime_id]
    timeslot_dict = {"1":"9am to 12pm", "2":"12pm to 3pm", "3":"3pm to 6pm", "4":"6pm to 9pm", "5":"9pm to 12am"}
    seat_class_list = showtime_class.get_seats_class()
    for seat_class in seat_class_list:                        
        if seat_class.date_of_showtime.strftime("%Y-%m-%d") == date and seat_class.timeslot_of_showtime in list(timeslot_dict.keys()):
            original_seat_class = seat_class
            seat_class.timeslot_of_showtime = timeslot_dict[seat_class.timeslot_of_showtime]
            seat_class_list.remove(original_seat_class)
            seat_class_list.append(seat_class)
            showtime_class.set_seats_class(seat_class_list)
            Showtime_dict[showtime_id] = showtime_class
            db["showtime"] = Showtime_dict
            
            break
    db.close()
    return render_template("User 2/bookingseats.html", title="Buying Seats", showtime_class=showtime_class, seat_class=seat_class)


@showtime_blueprint.route("/admin/showtime")
@login_required
def admin_showtime():
    check_admin()
    db = shelve.open('shelve.db', 'c')
    try:
        Showtime_dict = db["showtime"]        
    except:
        Showtime_dict = {}
        db["showtime"] = Showtime_dict
    db.close()
    for value in Showtime_dict.values():
        print(value.get_seats_class())
    return render_template("Admin/showtime/showtime.html", title="Showtimes", Showtime_dict=Showtime_dict)

@showtime_blueprint.route("/admin/showtime/add_showtime", methods=["GET","POST"])
@login_required
def add_showtime():
    check_admin()
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
    seat_dict = db["Seats"]
    theatres = []        
    for value in list(Movie_theatre_dict.values()):
        theatres.append((value.get_id(), value.get_theatre_name()))
    form.theatre_name.choices = theatres    
    movies = [("","")]
    for value in list(Movies_dict.values()):
        movies.append((value.get_id(), value.get_movie_name()))
    form.movie_title.choices = movies
    timeslots = [("1","9am to 12pm"), ("2", "12pm to 3pm"), ("3", "3pm to 6pm"), ("4", "6pm to 9pm"), ("5", "9pm to 12am")]
    form.timeslot.choices = timeslots
    halls = []
    for i in range(1,list(Movie_theatre_dict.values())[0].get_number_of_halls()+1):
        halls.append((str(i),str(i)))
    form.hall_number.choices = halls
    timeslot_dict = {"1":"9am to 12pm", "2":"12pm to 3pm", "3":"3pm to 6pm", "4":"6pm to 9pm", "5":"9pm to 12am"}
    if request.method == "POST" and form.validate_on_submit():
        print(form.validate_on_submit())
        timeslot_list = form.timeslot.data
        timeslot_data = []
        for timeslot in timeslot_list:
            timeslot_data.append(timeslot_dict[timeslot])
        #? Setting dates
        start_date = datetime.datetime.strptime(form.showtime_start_date.data, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(form.showtime_end_date.data, "%Y-%m-%d").date()
        day = datetime.timedelta(days=1)
        list_of_dates = []
        while start_date <= end_date:
            list_of_dates.append(start_date)
            start_date += day        
        print(list_of_dates)
        showtime_class = Showtime(Movie_theatre_dict[form.theatre_name.data], Movies_dict[form.movie_title.data], list_of_dates, timeslot_data, form.hall_number.data)
        #? Setting seats        
        seat_list_class = []
        for date in list_of_dates:
            for timeslot in timeslot_list:                
                seat_class = SeatClass(date, timeslot_dict[timeslot], hall_number, seat_dict)
                seat_list_class.append(seat_class)
        showtime_class.set_seats_class(seat_list_class)                    
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
    elif request.method == "POST" and request.json:
        print(request.json)
    print(form.timeslot.data)
    return render_template("Admin/showtime/add_showtime.html", title="Add Showtime", form=form)

@showtime_blueprint.route("/admin/showtime/modify_showtime/<showtime_id>", methods=["GET","POST"])
@login_required
def modify_showtime(showtime_id):
    check_admin()
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
        theatre_class = Movie_theatre_dict[form.theatre_name.data]
        movie_class = Movies_dict[form.movie_title.data]
        timeslot_list = form.timeslot.data
        timeslot_data = []
        for timeslot in timeslot_list:
            timeslot_data.append(timeslot_dict[timeslot])
        show_period = form.showtime_start_date.data + " - " + form.showtime_end_date.data
        hall_number = form.hall_number.data
        showtime_class.set_all_attributes(theatre_class, movie_class, show_period, timeslot_data, hall_number)
        db["showtime"] = Showtime_dict
        db.close()
        return redirect(url_for("showtime.admin_showtime"))
    return render_template("/Admin/showtime/modify_showtime.html", title="Modify Showtime", form=form)

@showtime_blueprint.route("/admin/showtime/delete_showtime", methods=["GET","POST"])
@login_required
def delete_showtime():
    check_admin()
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
        showtime_class = Showtime_dict[showtime_id]
        Deleted_list.append([showtime_class, datetime.date.today()])
        del Showtime_dict[showtime_id]
    db["showtime"] = Showtime_dict
    db["deleted_showtime"] = Deleted_list
    db.close()
    return redirect(url_for("showtime.admin_showtime"))

@showtime_blueprint.route("/admin/showtime_theatre/<theatre>/<start_date>/<end_date>/<timeslot>", methods=["GET","POST"])
@login_required
def hall_number(theatre, start_date, end_date, timeslot):
    check_admin()        
    timeslot = timeslot.split(",")    
    db = shelve.open('shelve.db', 'c')
    showtime_dict = db["showtime"]
    theatre_dict = db["movie_theatre"]
    value = theatre_dict[theatre]
    list_of_available_halls = [str(hall_number) for hall_number in range(1, value.get_number_of_halls()+1)]
    for value in showtime_dict.values():        
        if value.get_theatre_class().get_id() == theatre:
            print("theatre is in this show time")
            #? see which list is bigger
            if len(timeslot) > len(value.get_timeslot()):
                larger_list = timeslot
                smaller_list = value.get_timeslot()
            else:
                larger_list = value.get_timeslot()
                smaller_list = timeslot            
            if (all(ts in larger_list for ts in smaller_list)):
                print("timeslot is part of this showtime")
                if not (datetime.datetime.strptime(end_date, "%Y-%m-%d").date() <= value.get_show_period()[0] or datetime.datetime.strptime(start_date, "%Y-%m-%d").date() >= value.get_show_period()[-1]):
                    print("they do overlap")
                    print(str(value.get_hall_number()))
                    list_of_available_halls.remove(str(value.get_hall_number()))
                    if ValueError:
                        break
    print(list_of_available_halls)
    return jsonify({"hall_list":list_of_available_halls})    

@showtime_blueprint.route("/admin/showtime_theatre/payment/<showtime_id>/<date>/<timeslot>/<list_seats>", methods=["GET","POST"])
def payment(showtime_id, date, timeslot, list_seats):
    form = PaymentForm()
    db =shelve.open("shelve.db", "c")
    showtime_dict = db["showtime"]
    showtime_class = showtime_dict[showtime_id]
    price = len(list_seats) *8.50
    list_seats = list_seats.split(",")
    date = datetime.datetime.strptime(str(date), "%Y-%m-%d").date()
    if request.method == "POST":        
        # AnonymousUser(form.fullname.data, form.email.data, form.dateOfBirth.data, form.gender.data, form.card_number.data, form.card_name.data,  form.dateOfExpiry.data.strftime("$m-%Y"), form.cvc.data)
        for seat_class in showtime_class.get_seats_class():
            if seat_class.date_of_showtime == date and timeslot in seat_class.timeslot_of_showtime:                
                original_seat_class = seat_class
                seat_dict = seat_class.seat_dict
                for seat in list_seats:
                    seat_dict["seats"][seat] = "sold"
                print(seat_dict)
                seat_class.seat_dict = seat_dict
                showtime_class.get_seats_class().remove(original_seat_class)
                showtime_class.get_seats_class().append(seat_class)                
                showtime_dict[showtime_id] = showtime_class
                db["showtime"] = showtime_dict
                
    else:
        for seat_class in showtime_class.get_seats_class():
            if seat_class.date_of_showtime == date and timeslot in seat_class.timeslot_of_showtime:
                timeslot = seat_class.timeslot_of_showtime
                date = seat_class.date_of_showtime                
                seat_class = seat_class
                
        db.close()        
    return render_template("User 2/payment.html", showtime_class=showtime_class, timeslot=timeslot, date=date, list_seats=list_seats, price=price, form=form)