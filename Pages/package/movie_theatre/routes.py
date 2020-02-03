from flask import Blueprint
from flask import render_template, request, redirect, url_for, Markup
from flask_login import current_user, login_required
from package.movie_theatre.forms import CreateMovieTheatre, ModifyMovieTheatre
from package.movie_theatre.classes import Theatre
from package.movie_theatre.utilis import save_picture
from package.utilis import check_admin
import shelve, datetime

theatre_blueprint = Blueprint("movie_theatre", __name__)


#* Admin Movie Theatre
@theatre_blueprint.route("/admin/movie_theatre", methods=["GET","POST"])
@login_required
def admin_movie_theatre():
    check_admin()
    db = shelve.open('shelve.db', 'c')
    try:
        Movie_theatre_dict = db["movie_theatre"]
    except:        
        Movie_theatre_dict = {}
        db["movie_theatre"] = Movie_theatre_dict
    db.close()    
    return render_template("Admin/movie_theatre/movie_theatre.html", title="Movie Theatre", Movie_theatre_dict=Movie_theatre_dict)

@theatre_blueprint.route("/admin/movie_theatre/add_movie_theatre", methods=["GET","POST"])
@login_required
def add_movie_theatre():
    check_admin()
    form = CreateMovieTheatre()
    db = shelve.open('shelve.db', 'c')    
    try:
        Movie_theatre_dict = db["movie_theatre"]
        Theatre.id = list(Movie_theatre_dict.values())[-1].get_id()
    except:        
        Movie_theatre_dict = {}
        db["movie_theatre"] = Movie_theatre_dict      
    if form.validate_on_submit():
        theatre_name = form.theatre_name.data
        theatre_image = save_picture(form.theatre_image.data, "theatre")        
        theatre_halls = int(form.theatre_halls.data)
        movie_theatre_class = Theatre(theatre_name,theatre_image,theatre_halls)
        theatre_id = movie_theatre_class.get_id()
        Movie_theatre_dict[theatre_id] = movie_theatre_class
        db["movie_theatre"] = Movie_theatre_dict
        db.close()
        return redirect(url_for('movie_theatre.admin_movie_theatre'))
    elif request.method == "GET":
        form.theatre_name.data = ""
        form.theatre_halls.data = 1
        db.close()
    return render_template("Admin/movie_theatre/add_movie_theatre.html", title="Add Movie Theatre", form=form)

@theatre_blueprint.route("/admin/movie_theatre/modify_movie_theatre/<movie_theatre_id>", methods=["GET","POST"])
@login_required
def modify_movie_theatre(movie_theatre_id):
    check_admin()
    movie_theatre_id = movie_theatre_id
    form = ModifyMovieTheatre()
    db = shelve.open('shelve.db', 'c')    
    try:
        Movie_theatre_dict = db["movie_theatre"]
    except:        
        Movie_theatre_dict = {}
        db["movie_theatre"] = Movie_theatre_dict 
    if form.validate_on_submit():  
        theatre_name = form.theatre_name.data
        theatre_image = save_picture(form.theatre_image.data, "theatre")        
        theatre_halls = int(form.theatre_halls.data)
        movie_theatre_class = Movie_theatre_dict[movie_theatre_id]
        movie_theatre_class.set_all_attributes(theatre_name, theatre_image, theatre_halls)
        Movie_theatre_dict[movie_theatre_id] = movie_theatre_class
        db["movie_theatre"] = Movie_theatre_dict
        db.close()
        return redirect(url_for('movie_theatre.admin_movie_theatre'))
    elif request.method == "GET":
        movie_theatre = Movie_theatre_dict[movie_theatre_id]
        form.theatre_name.data = movie_theatre.get_theatre_name()
        form.theatre_halls.data = movie_theatre.get_number_of_halls()
        image_source = movie_theatre.get_theatre_image()
        db.close()
    return render_template("Admin/movie_theatre/modify_movie_theatre.html", title="Modify Movie Theatre", form=form, image_source=image_source)

@theatre_blueprint.route("/admin/movie_theatre/delete", methods=["GET","POST"])
@login_required
def delete_movie_theatre():
    check_admin()
    db = shelve.open('shelve.db', 'c')    
    try:
        Movie_theatre_dict = db["movie_theatre"]
        Deleted_list = db["deleted_movie_theatre"]
    except:        
        Movie_theatre_dict = {}
        Deleted_list = []
        db["movie_theatre"] = Movie_theatre_dict
        db["deleted_movie_theatre"] = Deleted_list

    list_of_to_be_deleted_theatres = request.json       
    for theatre_id in list_of_to_be_deleted_theatres: 
        delete_theatre = Movie_theatre_dict[theatre_id]                    
        Deleted_list.append([delete_theatre, datetime.date.today()])
        del Movie_theatre_dict[theatre_id]
    db["movie_theatre"] = Movie_theatre_dict
    db["deleted_movie_theatre"] = Deleted_list
    db.close()    
    return redirect(url_for('movie_theatre.admin_movie_theatre'))
