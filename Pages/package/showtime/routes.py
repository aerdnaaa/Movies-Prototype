from flask import Blueprint
from flask import render_template, request, redirect, url_for, jsonify, flash, send_file
from flask_login import current_user, login_required
from package.showtime.classes import Showtime, SeatClass
from package.showtime.forms import CreateShowtime, ModifyShowtime, PromotionForm
from package.showtime.utilis import return_available_theatres_and_hall, return_available_movie_title, return_timeslots, make_showtime, make_seats_sold
from package.utilis import check_admin, check_rights, generate_pdf
from package.user.classes import AnonymousUser
from package import stripe_keys, mail, app
from flask_mail import Message
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
    try:
        Promo_dict = db["promotion"]
    except:
        Promo_dict = {}
        db["promotion"] = Promo_dict
    form = PromotionForm()
    choices = [('none', 'None')]
    for promoid, value in Promo_dict.items():
        choices.append((promoid, value.get_title()))
    form.promo_id.choices = choices
    showtime_class = Showtime_dict[showtime_id]    
    seat_class_dict = showtime_class.get_seats_class()
    seat_class = seat_class_dict[seat_class_id]    
    db.close()
    return render_template("User 2/bookingseats.html", title="Buying Seats", showtime_class=showtime_class, seat_class=seat_class, form=form)

@showtime_blueprint.route("/showtime_theatre/checkout/<showtime_id>/<seat_class_id>/<list_seats>/<promo_id>", methods=["GET","POST"])
def checkout(showtime_id, seat_class_id, list_seats,promo_id):
    pub_key = stripe_keys['publishable_key']
    db = shelve.open("shelve.db", "c")
    # Showtime
    try:
        Showtime_dict = db["showtime"]
    except:
        Showtime_dict = {}
        db["showtime"] = Showtime_dict    
    try:
        Promo_dict = db["promotion"]
    except:
        Promo_dict = {}
        db["promotion"] = Promo_dict
    if promo_id != "none":
        promo_class = Promo_dict[promo_id]
        promo_price = int(promo_class.get_promoPrice())
        promo_title = promo_class.get_title()
    else:
        promo_price = 0
        promo_title = "None"
    list_current_seats = list_seats.split(',')
    showtime_class = Showtime_dict[showtime_id]
    seat_class_dict = showtime_class.get_seats_class()    
    seat_class = seat_class_dict[seat_class_id]    
    price = (8.5-promo_price) * len(list_current_seats)
    return render_template("User 2/payment.html", title="Payment", showtime_class=showtime_class, seat_class=seat_class, list_current_seats=list_current_seats, price=price, pub_key=pub_key, promo_title=promo_title)

@showtime_blueprint.route("/checkseats/<showtime_id>/<seat_class_id>/<old_list>/<new_list>")
def check_seats(showtime_id, seat_class_id, old_list, new_list):
    db = shelve.open("shelve.db", "c")
     # Showtime
    try:
        Showtime_dict = db["showtime"]
    except:
        Showtime_dict = {}
        db["showtime"] = Showtime_dict    
    #? initialize old list and new list
    if old_list != "none":
        old_list = old_list.split(",")
    else:
        old_list = []
    new_list = new_list.split(",")
    showtime_class = Showtime_dict[showtime_id]
    seat_class_dict = showtime_class.get_seats_class()    
    seat_class = seat_class_dict[seat_class_id]    
    seat_dict = seat_class.get_seat_dict()
    list_of_taken_seats = []
    #! check if seat is taken
    for seat in new_list: 
        if seat_dict[seat] == "on_hold":
            list_of_taken_seats.append(seat)
    #! on hold their seats
    for seat in old_list:
        seat_dict[seat] = "standard_available"
    for seat in new_list:
        seat_dict[seat] = "on_hold"
    seat_class.set_seat_dict(seat_dict)
    seat_class_dict[seat_class_id] = seat_class
    showtime_class.set_seats_class(seat_class_dict)
    Showtime_dict[showtime_id] = showtime_class    
    db["showtime"] = Showtime_dict    
    db.close()    
    if list_of_taken_seats == []:
        list_of_taken_seats = "none"

    return jsonify(list_of_taken_seats)

@showtime_blueprint.route("/get_annonymous_id")
def get_annonymous_id():
    db = shelve.open("shelve.db", "c")
    try:
        annonymous_id = db["annonymous"]        
        annonymous_id += 1        
    except:
        annonymous_id = 0
    db["annonymous"] = annonymous_id
    db.close()
    return jsonify(annonymous_id)

@showtime_blueprint.route("/showtime_theatre/cancel_seats/<showtime_id>/<seat_class_id>/<current_seats>")
def remove_seats(showtime_id,seat_class_id,current_seats):
    db = shelve.open("shelve.db", "c")
    # Showtime
    try:
        Showtime_dict = db["showtime"]
    except:
        Showtime_dict = {}
        db["showtime"] = Showtime_dict    
    list_current_seats = current_seats.split(',')
    showtime_class = Showtime_dict[showtime_id]
    seat_class_dict = showtime_class.get_seats_class()    
    seat_class = seat_class_dict[seat_class_id]    
    seat_dict = seat_class.get_seat_dict()
    for seat in list_current_seats:
        seat_dict[seat] = "standard_available"
    seat_class.set_seat_dict(seat_dict)
    seat_class_dict[seat_class_id] = seat_class
    showtime_class.set_seats_class(seat_class_dict)
    Showtime_dict[showtime_id] = showtime_class    
    db["showtime"] = Showtime_dict    
    db.close()    
    return redirect(url_for('showtime.bookmovie'))

@showtime_blueprint.route("/charge/<showtime_id>/<seat_class_id>/<seats>/<net_price>", methods=["POST"])
def pay(showtime_id,seat_class_id,seats,net_price):
    seats = seats.split(',')
    amount = float(net_price)
    description = f'Showtime_id: {showtime_id} Seat_class_id: {seat_class_id} Movie Tickets for seat(s): {seats}'    
    customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])
    
    charge = stripe.Charge.create(
        customer = customer.id,
        amount=int(amount*100),
        currency='sgd',
        description=description
    )
    db = shelve.open('shelve.db', 'c')
    user_dict = db["Users"]
    showtime_dict = db["showtime"]
    Showtime_seat_class_seats_id = showtime_id + seat_class_id + ".".join(seats)
    if current_user.is_authenticated:
        #? this will add the transaction to their class
        current_user_class = user_dict[current_user.get_id()]
        bought_seats = current_user_class.get_bought_seats()
        bought_seats[Showtime_seat_class_seats_id] = {'showtime_id':showtime_id, 'seat_class_id':seat_class_id, 'seats':seats, 'showtime_class':showtime_dict[showtime_id], 'date':datetime.date.today().strftime("%d %B %Y"), 'price':amount}        
        current_user_class.set_bought_seats(bought_seats)        
        user_dict[current_user_class.get_id()] = current_user_class
    else:
        #? annonymous users come here
        annonymous_class = AnonymousUser()        
        #? need email, showtime_id, seat_class_id, seats 
        annonymous_class.email = request.form['stripeEmail']
        seat_dict = annonymous_class.seats
        seat_dict[Showtime_seat_class_seats_id] = {'showtime_id':showtime_id, 'seat_class_id':seat_class_id, 'seats':seats, 'showtime_class':showtime_dict[showtime_id], 'date':datetime.date.today().strftime("%d %B %Y"), 'price':amount}        
        annonymous_class.seats = seat_dict
        user_dict[annonymous_class.id] = annonymous_class        
    db["Users"] = user_dict
    db.close()        
    #? generate_pdf here
    generate_pdf(request.form['stripeEmail'], Showtime_seat_class_seats_id, {'showtime_id':showtime_id, 'seat_class_id':seat_class_id, 'seats':seats, 'showtime_class':showtime_dict[showtime_id], 'date':datetime.date.today().strftime("%d %B %Y")}, amount)
    make_seats_sold(showtime_id, seat_class_id, seats)    
    #? send email
    recipient = request.form['stripeEmail']
    filename = Showtime_seat_class_seats_id+'.pdf'
    msg = Message("Saw Cinematics e-receipt", sender=app.config.get("MAIL_USERNAME"), recipients=[recipient])
    file_path = "static/pdf/" + filename
    with app.open_resource(file_path) as pdf:
        msg.attach(filename, 'application/pdf', pdf.read())
    msg.body = f"Dear Sir/Madam \nThis is your receipt. Thank you. \nBest Regards \nSaw Cinematics"
    # mail.send(msg)
    return redirect(url_for('showtime.thankyoupage', showtime_id=showtime_id, seat_class_id=seat_class_id, bought_seats=seats, Showtime_seat_class_seats_id=Showtime_seat_class_seats_id))

@showtime_blueprint.route("/thankyou/<showtime_id>/<seat_class_id>/<bought_seats>/<Showtime_seat_class_seats_id>")
def thankyoupage(showtime_id,seat_class_id,bought_seats, Showtime_seat_class_seats_id):
    return render_template("User 2/thankyou.html", title="Thank you", showtime_id=showtime_id, seat_class_id=seat_class_id, Showtime_seat_class_seats_id=Showtime_seat_class_seats_id)

@showtime_blueprint.route("/send_pdf/<Showtime_seat_class_seats_id>")
def send_pdf(Showtime_seat_class_seats_id):
    return send_file(app.root_path + '/static/pdf/' + Showtime_seat_class_seats_id + '.pdf', attachment_filename=Showtime_seat_class_seats_id + '.pdf')

@showtime_blueprint.route("/admin/showtime")
@login_required
def admin_showtime():
    check_admin()
    check_rights()
    db = shelve.open('shelve.db', 'c')
    try:
        Showtime_dict = db["showtime"]        
    except:
        Showtime_dict = {}
        db["showtime"] = Showtime_dict
    print(Showtime_dict)
    db.close()
    return render_template("Admin/showtime/showtime.html", title="Showtimes", Showtime_dict=Showtime_dict)

@showtime_blueprint.route("/admin/showtime/add_showtime", methods=["GET","POST"])
@login_required
def add_showtime():
    check_admin()
    check_rights()
    form = CreateShowtime()
    db = shelve.open('shelve.db', 'c')
    try:
        Showtime_dict = db["showtime"]        
        Showtime.id = list(Showtime_dict.keys())[-1]
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
    check_rights()
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
    check_rights()
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

# @showtime_blueprint.route("/admin/delete_showtime")
# def delete():
#     db = shelve.open('shelve.db', 'c')
#     db["showtime"] = {}
#     db.close()
#     return ""