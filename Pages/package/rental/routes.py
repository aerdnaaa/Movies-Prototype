from flask import Blueprint
from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required
from package.rental.forms import CreateRental, ModifyRental
from package.rental.classes import Rental
from package.rental.utilis import save_picture
from package.utilis import check_admin
import shelve, datetime

rental_blueprint = Blueprint("rental", __name__)

#* Home Page contains rental
@rental_blueprint.route("/rentmovie")
def rentmovie():
    db = shelve.open('shelve.db', 'c')
    try:
        Rental_dict = db["rental"]
    except:        
        Rental_dict = {}
        db["rental"] = Rental_dict
    genre_list = db["genre_list"]
    return render_template("User 2/rentmovie.html", title="Rent Movie",  Rental_dict=Rental_dict, genre_list=genre_list)


#* Admin Rental
@rental_blueprint.route("/admin/rental")
@login_required
def admin_rental():
    check_admin()
    db = shelve.open('shelve.db', 'c')
    try:
        Rental_dict = db["rental"]
    except:        
        Rental_dict = {}
        db["rental"] = Rental_dict
    db.close()
    return render_template("Admin/rental/rental.html", title="Rental", Rental_dict=Rental_dict)

@rental_blueprint.route("/admin/rental/add_rental", methods=["GET","POST"])
@login_required
def add_rental():
    check_admin()
    form = CreateRental()
    db = shelve.open('shelve.db', 'c')
    try:
        Rental_dict = db["rental"]
        Movies_dict = db["movies"]
        Rental.id = list(Rental_dict.values())[-1].get_id()
    except:        
        Rental_dict = {}
        db["rental"] = Rental_dict        
    movie_available = [("","")]    
    for key in Movies_dict:
        movie_class = Movies_dict[key]        
        movie_available.append((movie_class.get_id(), movie_class.get_movie_name()))        
    form.movie_title.choices = movie_available
    if request.method == "POST":        
        rent_period = form.rent_start_date.data + " - " + form.rent_end_date.data
        rent_price = int(form.rent_price.data)
        movie_class = Movies_dict[form.movie_title.data]
        rental_class = Rental(movie_class, rent_period, rent_price)
        rental_id = rental_class.get_id()
        Rental_dict[rental_id] = rental_class
        db["rental"] = Rental_dict
        db.close()        
        return redirect(url_for("rental.admin_rental"))
    elif request.method == "GET":
        form.movie_title.data = ""
        form.rent_start_date.data = ""
        form.rent_end_date.data = ""
        form.rent_price.data = 0
    return render_template("Admin/rental/add_rental.html", title="Add Rental", form=form)    
    
@rental_blueprint.route("/admin/rental/modify_rental/<rental_id>", methods=["GET","POST"])
@login_required
def modify_rental(rental_id):
    check_admin()
    form = ModifyRental()
    db = shelve.open('shelve.db', 'c')
    try:
        Rental_dict = db["rental"]        
        Movies_dict = db["movies"]
        Rental.id = list(Rental_dict.values())[-1].get_id()
    except:        
        Rental_dict = {}
        db["rental"] = Rental_dict        
    movie_available = [("","")]    
    for key in Movies_dict:
        movie_class = Movies_dict[key]        
        movie_available.append((movie_class.get_id(), movie_class.get_movie_name()))        
    form.movie_title.choices = movie_available
    if request.method == "POST":
        rent_period = form.rent_start_date.data + " - " + form.rent_end_date.data
        rent_price = int(form.rent_price.data)
        movie_class = Movies_dict[form.movie_title.data]
        rental_class = Rental_dict[rental_id]
        rental_class.set_all_attributes(movie_class, rent_period, rent_price)
        Rental_dict[rental_id] = rental_class
        db["rental"] = Rental_dict
        db.close()
        return redirect(url_for("rental.admin_rental"))
    elif request.method == "GET":
        rental_class = Rental_dict[rental_id]
        form.movie_title.data = str(rental_class.get_movie_class().get_id())        
        form.rent_start_date.data, form.rent_end_date.data = rental_class.get_rent_period().split(" - ")
        form.rent_price.data = rental_class.get_price()
    return render_template("Admin/rental/modify_rental.html", title="Modify Rental", form=form)    

@rental_blueprint.route("/admin/rental/delete", methods=["GET","POST"])
@login_required
def delete_rental():
    check_admin()
    db = shelve.open('shelve.db', 'c')
    try:
        Rental_dict = db["rental"]
        Deleted_list = db["deleted_rental"]
        Movies_dict = db["movies"]        
    except:        
        Rental_dict = {}
        Deleted_list = []
        db["rental"] = Rental_dict
        db["deleted_rental"] = Deleted_list
    list_of_to_be_deleted_rentals = request.json
    for rental_id in list_of_to_be_deleted_rentals:
        rental_class = Rental_dict[rental_id]
        Deleted_list.append([rental_class, datetime.date.today()])
        del Rental_dict[rental_id]
    db["rental"] = Rental_dict
    db["deleted_rental"] = Deleted_list
    db.close()
    return redirect(url_for("rental.admin_rental"))
@rental_blueprint.route("/admin/rental/rental_users")
def rental_users():
    pass
