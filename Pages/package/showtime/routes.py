from flask import Blueprint
from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_login import current_user, login_required
from package.showtime.classes import Showtime, SeatClass
from package.showtime.forms import CreateShowtime, ModifyShowtime, PaymentForm
from package.showtime.utilis import return_available_theatres_and_hall, return_available_movie_title, return_timeslots, make_showtime
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

@showtime_blueprint.route("/bookmovieseats/<showtime_id>/<seat_class_id>")
def bookmovieseats(showtime_id, seat_class_id):    
    db = shelve.open('shelve.db', 'c')
    # Showtime
    try:
        Showtime_dict = db["showtime"]
    except:
        Showtime_dict = {}
        db["showtime"] = Showtime_dict    

    showtime_class = Showtime_dict[showtime_id]    
    seat_class_dict = showtime_class.get_seats_class()
    seat_class = seat_class_dict[seat_class_id]
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
    return render_template("Admin/showtime/showtime.html", title="Showtimes", Showtime_dict=Showtime_dict)

@showtime_blueprint.route("/admin/showtime/add_showtime", methods=["GET","POST"])
@login_required
def add_showtime():
    check_admin()
    form = CreateShowtime()
    db = shelve.open('shelve.db', 'c')
    try:
        Showtime_dict = db["showtime"]        
        Showtime.id = list(Showtime_dict.values())[-1].get_id()
    except:
        Showtime_dict = {}
        db["showtime"] = Showtime_dict
    #? initialize form choices
    form.theatre_name.choices, form.hall_number.choices  = return_available_theatres_and_hall()
    form.movie_title.choices = return_available_movie_title()
    form.timeslot.choices = return_timeslots() 
    #? will redirect back if there is no theatre and movies        
    if return_available_movie_title() == [] or return_available_theatres_and_hall()[0] == []:
        flash("You cannot add showtime if there is no movie added and/or no theatre available.", "danger")
        return redirect(url_for("showtime.admin_showtime"))
    else:
        if request.method == "POST" and form.validate_on_submit():
            showtime_class = make_showtime(form, "new")
            showtime_id = showtime_class.get_id()
            Showtime_dict[showtime_id] = showtime_class
            db["showtime"] = Showtime_dict
            db.close()
            flash("Showtime has been added !", "success")        
            return redirect(url_for("showtime.admin_showtime"))
        elif request.method == "POST" and not form.validate_on_submit():
            flash("Some field(s) are incorrect. Please try again", "danger")
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
@login_required
def modify_showtime(showtime_id):
    check_admin()
    form = ModifyShowtime()
    db = shelve.open('shelve.db', 'c')
    try:
        Showtime_dict = db["showtime"]        
    except:
        Showtime_dict = {}
        db["showtime"] = Showtime_dict
    showtime_class = Showtime_dict[showtime_id]

    #? initialize form choices
    form.theatre_name.choices, form.hall_number.choices  = return_available_theatres_and_hall()
    form.movie_title.choices = return_available_movie_title()
    form.timeslot.choices = return_timeslots()  

    if request.method == "GET":
        form.theatre_name.data = str(showtime_class.get_theatre_class().get_id())
        form.movie_title.data = str(showtime_class.get_movie_class().get_id())
        form.timeslot.data = showtime_class.get_timeslot()
        form.showtime_start_date.data, form.showtime_end_date.data = showtime_class.get_show_period()[0], showtime_class.get_show_period()[-1]
        form.hall_number.data = str(showtime_class.get_hall_number())
    elif request.method == "POST" and form.validate_on_submit():
        Showtime_dict[showtime_id] = make_showtime(form, showtime_id)        
        db["showtime"] = Showtime_dict
        db.close()
        flash("Showtime has been modified !", "success")    
        return redirect(url_for("showtime.admin_showtime"))
    elif request.method == "POST" and not form.validate_on_submit():
        flash("Some field(s) are incorrect. Please try again", "danger")
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

@showtime_blueprint.route("/admin/add_showtime_theatre/<theatre>/<start_date>/<end_date>/<timeslot>", methods=["GET","POST"])
@login_required
def add_hall_number(theatre, start_date, end_date, timeslot):
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

@showtime_blueprint.route("/admin/modify_showtime_theatre/<theatre>/<start_date>/<end_date>/<timeslot>", methods=["GET","POST"])
@login_required
def modify_hall_number(theatre, start_date, end_date, timeslot):
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
                    if not (smaller_list == larger_list and (datetime.datetime.strptime(end_date, "%Y-%m-%d").date() == value.get_show_period()[0] and datetime.datetime.strptime(start_date, "%Y-%m-%d").date() == value.get_show_period()[-1])):
                        list_of_available_halls.remove(str(value.get_hall_number()))
                    if ValueError:
                        break
    print(list_of_available_halls)
    return jsonify({"hall_list":list_of_available_halls})    

@showtime_blueprint.route("/admin/showtime_theatre/payment/<showtime_id>/<seat_class_id>/<list_seats>", methods=["GET","POST"])
def payment(showtime_id, seat_class_id, list_seats):
    form = PaymentForm()
    db =shelve.open("shelve.db", "c")
    showtime_dict = db["showtime"]
    showtime_class = showtime_dict[showtime_id]
    list_seats = list_seats.split(",")
    price = len(list_seats) *8.50    
    if request.method == "POST":        
        pass
    else:
        seat_class = showtime_class.get_seats_class()[seat_class_id]
        timeslot = seat_class.timeslot_of_showtime
        date = seat_class.date_of_showtime  
        seat_dict = seat_class.seat_dict
        #? make seat on hold
        for seat in list_seats:
            seat_dict["seats"][seat] = "on_hold"
        seat_class.seat_dict = seat_dict
                        
        showtime_dict[showtime_id] = showtime_class
        db["showtime"] = showtime_dict
                
                
        db.close()        
    return render_template("User 2/payment.html", showtime_class=showtime_class, list_seats=list_seats, price=price, form=form)

@showtime_blueprint.route("/checkseats/<showtime_id>/<seat_class_id>/<list_seats>")
def check_seats(showtime_id, seat_class_id, list_seats):
    db =shelve.open("shelve.db", "c")
    showtime_dict = db["showtime"]
    showtime_class = showtime_dict[showtime_id]
    list_seats = list_seats.split(",")

    list_of_seats_that_are_on_hold = []
    seat_class_dict = showtime_class.get_seats_class()
    seat_class = seat_class_dict[seat_class_id]
    seat_dict = seat_class.seat_dict["seats"]
    for seat in list_seats:
        if seat_dict[seat] == "on_hold":
            list_of_seats_that_are_on_hold.append(seat)
    if list_of_seats_that_are_on_hold == []:
        return jsonify("none")
    else:
        return jsonify(",".join(list_of_seats_that_are_on_hold))